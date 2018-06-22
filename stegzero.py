#!/usr/bin/env python

import zlib
import os
import struct
import logging
import shutil
import argparse
import random


def display_logo():
    print('\n')
    print(' _____ _              ______')
    print('/  ___| |            |___  /')
    print('\ `--.| |_ ___  __ _    / /  ___ _ __ ___')
    print(" `--. \ __/ _ \/ _` |  / /  / _ \ '__/ _ \\")
    print('/\__/ / ||  __/ (_| |./ /__|  __/ | | (_) |')
    print('\____/ \__\___|\__, |\_____/\___|_|  \___/')
    print('                __/ | Steganography CTF Assistant')
    print('               |___/  https://www.github.com/infoseczero')
    print('\n')


def log_event(event, log_level):
    try:
        log_file = os.path.expanduser('~/stegzero.log')
        setlevel = getattr(logging, log_level.upper(), None)
        logging.basicConfig(filename=log_file, level=setlevel)
        logging.log(setlevel, event)
        print(event)
    except (ValueError, IOError, OSError) as error:
        print(error)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-sp', '--swap-palette',
                        metavar='image_path', nargs=1,
                        required=False,
                        help='Swap PNG palette entries to show hidden text')
    parser.add_argument('-cr', '--color-range',
                        metavar=('image_path', 'color_range'), nargs=2,
                        required=False,
                        help='Create a color range to make text readable')
    args = vars(parser.parse_args())
    return args


def make_workspace():
    try:
        path_name = 'stegzero_workspace_{}'.format(random.randint(1,10000))
        os.makedirs(os.path.join(os.getcwd(), path_name))
    except(ValueError, IOError, OSError) as error:
        log_event(error, 'critical')
    return os.path.join(os.getcwd(), path_name)


def make_image_copy(image, workspace):
    try:
        new_image = '{}/stegzero_copy.png'.format(workspace)
        shutil.copyfile(image, new_image)
    except(ValueError, IOError, OSError) as error:
        log_event(error, 'critical')
    return new_image


def verify_png(image):
    try:
        with open(image, 'r+b') as image_file:
            image_file.seek(0)
            signature = '\x89PNG\r\n\x1a\n'
            if image_file.read(len(signature)) != signature:
                log_event('Aborting operation. Invalid PNG!', 'critical')
                raise SystemExit
    except(ValueError, IOError, OSError) as error:
        log_event(error, 'critical')


# The swap_palette function is a fork of the following code:
# https://pequalsnp-team.github.io/assets/change_palette.py
def swap_palette(image, color_range, workspace):
    for iteration in range(color_range):
        with open(image, 'r+b') as image_file:
            image_file.seek(8)    
            while True:
                chunk = image_file.read(8)
                if len(chunk) != 8:
                    break                
                # Decode chunk header
                length, chtype = struct.unpack('>L4s', chunk)
                # Extract PLTE chunk
                if chtype == 'PLTE':
                    curpos = image_file.tell()
                    palette_data = image_file.read(length)
                    black = '\x00\x00\x00'
                    white = '\xff\xff\xff'
                    # Swap palette entries with white/black
                    # to expose hidden text
                    if color_range == 255:
                        palette_data = ((black * iteration) + white + 
                                        (black * (256 - iteration - 1)))
                    # Swap a user-defined range of palette entries with
                    # white/black to expose text hidden across several
                    # different palette entries
                    if not color_range == 255:
                        palette_data = ((black * color_range) + white *
                                        iteration + (black * 
                                        (256 - (color_range + iteration))))
                    # Do an in-place modification of the image
                    image_file.seek(curpos)
                    image_file.write(palette_data)
                    image_crc32 = zlib.crc32(chtype+palette_data)&0xffffffff
                    image_file.write(struct.pack('>L', image_crc32))
                else:
                    image_file.seek(length+4, os.SEEK_CUR)

            # Save a copy of the image to disk after it has been modified
            if color_range == 255:
                shutil.copyfile(image, '{}/stegzero_default_range_{}.png'.
                                format(workspace, iteration))

            if not color_range == 255:
                shutil.copyfile(image, '{}/stegzero_custom_range_{}_{}.png'.
                                format(workspace, color_range, iteration))


def main():
    display_logo()
    if parse_arguments()['swap_palette']:
        try:
            log_event('Default PNG palette swap requested', 'info')
            # Image file from user-input
            original_image = parse_arguments()['swap_palette'][0]
            # Ensure user-supplied image is a valid PNG file
            verify_png(original_image)
            # Create a new directory and copy a temporary image file there
            workspace = make_workspace()
            new_image = make_image_copy(original_image, workspace)
            # Perform a default palette swap
            log_event('Generating images...', 'info')
            swap_palette(new_image, 255, workspace)
            log_event('Images have been placed in a new directory', 'info')
        except (ValueError, IOError, OSError) as error:
            log_event(error, 'critical')

    if parse_arguments()['color_range']:
        try:
            log_event('User-defined PNG palette swap requested', 'info')
            # Image file from user-input
            original_image = parse_arguments()['color_range'][0]
            # Ensure user-supplied image is a valid PNG file
            verify_png(original_image)
            # Color range from user-input
            color_range = int(parse_arguments()['color_range'][1])
            # Create a new directory and copy a temporary image file there
            workspace = make_workspace()
            new_image = make_image_copy(original_image, workspace)
            # Do a palette swap with a user-defined palette range
            log_event('Generating images...', 'info')
            swap_palette(new_image, color_range, workspace)
            log_event('Images have been placed in a new directory', 'info')
        except (ValueError, IOError, OSError) as error:
            log_event(error, 'critical')


if __name__=='__main__':
    main()


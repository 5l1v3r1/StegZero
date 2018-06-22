# Introduction
StegZero is a steganographic utility which focuses on discovering messages hidden within the 8-bit colormap of a Portable Network Graphic file. Specifically, the utility will create a copy of the original image and manipulate the PLTE chunk so that a single palette entry is rendered in white while the remaining palette entries are rendered in black. StegZero will modify all 256 palette entries, one at a time, and save the modified image(s) in a new directory. Therefore, a successful run will output 256 different images that will render the background as black while exposing any hidden content as white.

# Demonstration
StegZero is forked from a script created by the HacknamStyle CTF team, so it seems fitting to use the image from their original challenge write-up in this demonstration. The original challenge write-up can be found at: <https://github.com/ctfs/write-ups-2014/tree/master/plaid-ctf-2014/doge-stege>.

* The first step is to manipulate the PLTE chunk so that a single palette entry is rendered in white and the remaining palette entries are rendered in black. Figure 1 demonstrates how to perform this operation.

<p align="center">
  <img src="https://raw.githubusercontent.com/infoseczero/StegZero/master/assets/figure1.png" alt="Figure 1"/>
</p>

* The second step is to examine all 256 generated images for any content that might have been hidden inside of the 8-bit colormap. StegZero will automatically place the modified images in a new directory created in the same location the script was ran from. In this specific example, a small amount of hidden text is exposed after modifying the 127th palette entry (stegzero_default_range_127.png). However, since this particular challenge has text hidden across multiple palette entries, an additional step is required to expose all of the hidden content.

* The third step is to expose all of the hidden text found in stegzero_default_range_127.png by rendering a range of palettes, beginning with the 127th palette entry, as white. Figure 2 demonstrates how to perform this operation.

<p align="center">
  <img src="https://raw.githubusercontent.com/infoseczero/StegZero/master/assets/figure2.png" alt="Figure 2"/>
</p>

* The final step is to look through a new set of generated image files for an image that has the entire hidden message exposed. StegZero will automatically place the modified images in a new directory created in the same location the script was ran from. In this specific example, all of the hidden text is exposed after modifying the 60th palette entry (stegzero_custom_range_127_60.png). The secret message is now fully exposed and you can pat yourself on the back for completing this challenge the easy way.

# Before & After
dog_stege.png          |  stegzero_custom_range_127_60.png
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/infoseczero/StegZero/master/assets/dog_stege.png)  |  ![](https://raw.githubusercontent.com/infoseczero/StegZero/master/assets/stegzero_custom_range_127_60.png)

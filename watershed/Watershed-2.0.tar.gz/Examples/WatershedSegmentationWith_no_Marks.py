#!/usr/bin/env python

## WatershedWithNoMarkings.py

'''
To see wathershed segmentation of an image that does not require any user
interaction, execute this script.

As you will notice that, when no user interaction is involved, the
Wathershed algorithm over-segments the image.  For an example of the
segmentation produced by this script, for the following image

    orchid0001.jpg

of an orchid, the script produced the segmentation shown in

    _output_segmentation_for_orchid_with_no_marks.jpg
'''



from Watershed import *

shed = Watershed(
               data_image = "orchid0001.jpg",
               binary_or_gray_or_color = "color",
               size_for_calculations = 128,
               sigma = 1,
               gradient_threshold_as_fraction = 0.1,
               level_decimation_factor = 16,
       )

shed.extract_data_pixels() 
print("Displaying the original image:")
shed.display_data_image()
print("Calculating the gradient image")
shed.compute_gradient_image()
print("Computing Z level sets for the gradient image")
shed.compute_Z_level_sets_for_gradient_image()
print("Propagating influences:")
shed.propagate_influence_zones_from_bottom_to_top_of_Z_levels()
shed.display_watershed()
shed.display_watershed_in_color()
shed.extract_watershed_contours()
shed.display_watershed_contours_in_color()






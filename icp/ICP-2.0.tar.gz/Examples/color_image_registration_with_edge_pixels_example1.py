#!/usr/bin/env python 


##     color_image_registration_with_edge_pixels_example1.py

##  This example is for the color images SydneyOpera.jpg and
##  SydneyOpera2.jpg in the Examples directory.  We must set the
##  binary_or_color parameter to 'color' in this case since we are dealing
##  with color images.  We want the ICP registration to be carried out in
##  'edges' mode.



import ICP


icp = ICP.ICP( 
               binary_or_color = "color",
               corners_or_edges = "edges",
               auto_select_model_and_data = 1,
               calculation_image_size = 200,
               max_num_of_pixels_used_for_icp = 300,
               pixel_correspondence_dist_threshold = 20,
               iterations = 24,
               model_image =  "SydneyOpera.jpg",
               data_image = "SydneyOpera2.jpg",
            )

icp.extract_pixels_from_color_image("model")
icp.extract_pixels_from_color_image("data")
icp.icp()
icp.display_images_used_for_edge_based_icp()
icp.display_results_as_movie()
icp.cleanup_directory()


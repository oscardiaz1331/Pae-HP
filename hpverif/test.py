import pyrealsense2 as rs
import numpy as np
import open3d as o3d


## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2017 Intel Corporation. All Rights Reserved.

#####################################################
##                  Export to PLY                  ##
#####################################################

# First import the library
import pyrealsense2 as rs

# Declare pointcloud object, for calculating pointclouds and texture mappings
#pc = o3d.geometry.PointCloud
# We want the points object to be persistent so we can display the last cloud when a frame drops
points = rs.points()

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()
config = rs.config()
# Enable depth stream
config.enable_stream(rs.stream.depth)
spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 2)
spatial.set_option(rs.option.filter_smooth_alpha, 0.5)
spatial.set_option(rs.option.filter_smooth_delta, 20)

temporal = rs.temporal_filter()

hole_filling = rs.hole_filling_filter()

# Start streaming with chosen configuration
pipe.start(config)

# We'll use the colorizer to generate texture for our PLY
# (alternatively, texture can be obtained from color or infrared stream)
colorizer = rs.colorizer()

try:
    # Wait for the next set of frames from the camera
    frames = pipe.wait_for_frames()
    colorized = colorizer.process(frames)
    depth = frames.get_depth_frame()
    depth = temporal.process(depth)
    depth = spatial.process(depth)
    color = frames.get_color_frame()
    # Create save_to_ply object
    ply = rs.save_to_ply("6.ply")
    print(ply)
    # Set options to the desired values
    # In this example we'll generate a textual PLY with normals (mesh is already created by default)
    ply.set_option(rs.save_to_ply.option_ply_binary, False)
    ply.set_option(rs.save_to_ply.option_ply_normals, True)

    print("Saving to 1.ply...")
    # Apply the processing block to the frameset which contains the depth frame and the texture
    ply.process(colorized)
    print("Done")
finally:
    pipe.stop()


pc = o3d.io.read_point_cloud("C:/Users/llore/Desktop/UNI/PAESAV/Pae-HP/6.ply")
o3d.visualization.draw_geometries([pc])

# Calcula los vectores de normales
pc.estimate_normals()

# Crea la malla de triángulos utilizando el método de Poisson
mesh = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(pc)

# Visualiza la malla de triángulos
o3d.visualization.draw_geometries([mesh])
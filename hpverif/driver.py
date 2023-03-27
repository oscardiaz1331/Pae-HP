
import verification as v
import pyrealsense2 as rs
import CenterAverage as ca
import open3d as o3d
import cv2
import numpy as np



verif = v.Verification()
dp,dc,pc = verif.show_files(50, "./prueba_estatica3.bag")

fm = verif.matrixDiagn(dp)


# Load the depth frame as a 16-bit grayscale image
depth_image = np.array(fm)
# Normalize the depth values between 0 and 255
depth_frame_norm = cv2.normalize(depth_image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

# Convert the depth frame to a color map
depth_colormap = cv2.applyColorMap(depth_frame_norm, cv2.COLORMAP_JET)

# Save the depth map as a PNG image
cv2.imwrite('depth_map.png', depth_colormap)


depth_image = cv2.imread("./depth_map.png",cv2.IMREAD_ANYDEPTH)
depth_image = depth_image.astype(np.uint16)
depth_o3d = o3d.geometry.Image(depth_image)

print(depth_o3d)
# Create a depth image from the numpy array
intrinsic = o3d.camera.PinholeCameraIntrinsic(640, 480, 525, 525, 320, 240)
im = o3d.geometry.PointCloud.create_from_depth_image(depth_o3d,intrinsic)

o3d.visualization.draw_geometries([im])
#s = verif.matrixDiagn(dp)




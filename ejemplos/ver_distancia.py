import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API

print("reset start")
ctx = rs.context()
devices = ctx.query_devices()
for dev in devices:
    dev.hardware_reset()
print("reset done")

print("Environment Ready")

# Setup:
pipe = rs.pipeline()
cfg = rs.config()
#cfg.enable_device_from_file("stairs.bag")
profile = pipe.start(cfg)

# Skip 5 first frames to give the Auto-Exposure time to adjust
for x in range(5):
  pipe.wait_for_frames()
  
# Store next frameset for later processing:
frameset = pipe.wait_for_frames()
depth_frame = frameset.get_depth_frame()

# Cleanup:
pipe.stop()
print("Frames Captured")

colorizer = rs.colorizer()
colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())

plt.rcParams["axes.grid"] = False
plt.rcParams['figure.figsize'] = [8, 4]
plt.imshow(colorized_depth)

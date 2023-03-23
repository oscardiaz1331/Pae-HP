import pyrealsense2 as rs
import open3d as o3d
import numpy as np

# Inicializar la cámara RealSense
pipe = rs.pipeline()
cfg = rs.config()
cfg.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
cfg.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Iniciar la captura de imágenes
pipe.start(cfg)
# Configurar el objeto pointcloud
pc = rs.pointcloud()

# Definir los filtros que deseas aplicar
spatial = rs.spatial_filter()
spatial.set_option(rs.option.filter_magnitude, 2)
spatial.set_option(rs.option.filter_smooth_alpha, 0.5)
spatial.set_option(rs.option.filter_smooth_delta, 20)

temporal = rs.temporal_filter()

hole_filling = rs.hole_filling_filter()
# Capturar las imágenes de la cámara RealSense y convertirlas a formato de nube de puntos 3D
for i in range(10):
    frames = pipe.wait_for_frames()
    depth = frames.get_depth_frame()
    depth = spatial.process(depth)
    depth = temporal.process(depth)
    depth = hole_filling.process(depth)
    color = frames.get_color_frame()

    pc.map_to(color)
    points = pc.calculate(depth)
    verts = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, 3)
# Crear un objeto open3d.geometry.PointCloud y pasar los vértices a su propiedad points
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(verts)

# Visualizar la nube de puntos
o3d.visualization.draw_geometries([pcd])
# Cerrar la conexión con la cámara RealSense
pipe.stop()

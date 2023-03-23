import verification as v
import pyrealsense2 as rs
import CenterAverage as ca
import open3d as o3d


verif = v.Verification()
verif.capture_frame_ply("prueba1",4)

pc = o3d.io.read_point_cloud("prueba1.ply")
o3d.visualization.draw_geometries([pc])

#s = verif.matrixDiagn(dp)





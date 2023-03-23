import verification as v
from pyntcloud import PyntCloud
import open3d as o3d
import numpy as np


verif = v.Verification()
dp,cp = verif.capture_frame(100, "tt.bag")



import verification as v
import Kmeans as k


verif = v.Verification()
dp,cp = verif.show_files(15, "recording4.bag")

ms = verif.MatrixDiagn(dp)
k.Kmeans(ms, 2)
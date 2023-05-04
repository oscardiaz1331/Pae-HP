import Verification  as v
import os
import glob

bag_files = glob.glob("./*.bag")
verif = v.Verification()
#dp,dc = verif.capture_frame(100, "prueba3m.bag", 0)

for file in bag_files:
        print(file)
        dp,dc,p = verif.show_files(26,file)
        file_name, file_ext = os.path.splitext(file)
        min,max= verif.PointCloud(dp,file_name)
#verif.Segmentation("./gg_final/gg_final.ply",min,max)


'''
Precision aceptables de 60cm-1.5 metros

Con diferentes luces: con luz directa exterior depth frames no optimos, igual con ventanas. Con luz no directa bien.



Pruebas de precisión:

distancia pared a camara:
        real        sensor
10cm:   
20:
30:
40:
50:
60:
70:
80:
90:
1m:
1,25
1,5:
1,75:
2m:

'''
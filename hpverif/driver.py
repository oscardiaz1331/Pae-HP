import verification  as v



verif = v.Verification()
dp,dc = verif.capture_frame(100, "prueba_1m.bag", 0)
dp,dc,p = verif.show_files(26,"prueba_1m.bag")

min,max= verif.PointCloud(dp,"prueba_1m")
#verif.Segmentation("./gg_final/gg_final.ply",min,max)



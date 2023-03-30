import verification  as v



verif = v.Verification()
dp,dc,p = verif.show_files(26,"prueba_estatica2.bag")
verif.PointCloud(dp,"imagen_columna")
verif.Segmentation("./imagen_columna/imagen_columna.ply")

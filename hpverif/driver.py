import verification  as v



verif = v.Verification()


dp,dc,p = verif.show_files(26,"./hpverif/recording3.bag")

verif.PointCloud(dp,"imagen_columna")

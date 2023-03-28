import verification  as v



verif = v.Verification()


dp,dc,p = verif.show_files(20,"./recording3.bag")

verif.PointCloud(dp,"alex")

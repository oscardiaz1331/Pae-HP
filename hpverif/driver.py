import verification  as v



verif = v.Verification()
dp,dc = verif.capture_frame(100, "gg.bag", 0)
dp,dc,p = verif.show_files(26,"gg.bag")
verif.PointCloud(dp,"gg_pared")
#verif.Segmentation("./gg/gg.ply")

import verification  as v



verif = v.Verification()
dp,dc = verif.capture_frame(100, "gg_final2.bag", 0)
dp,dc,p = verif.show_files(26,"gg_final2.bag")
verif.PointCloud(dp,"gg_final2")
#verif.Segmentation("./gg/gg.ply")

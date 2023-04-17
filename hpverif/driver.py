import verification  as v



verif = v.Verification()
#dp,dc = verif.capture_frame(100, "gg.bag", 0)
dp,dc,p = verif.show_files(26,"gg_final.bag")

min,max= verif.PointCloud(dp,"gg_final")
verif.Segmentation("./gg_final/gg_final.ply",min,max)



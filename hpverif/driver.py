import verification  as v



verif = v.Verification()
#dp,dc = verif.capture_frame(100, "gg.bag", 0)
dp,dc,p = verif.show_files(26,"recording5.bag")

verif.PointCloud(dp,"recording5")
#a,c = verif.Segmentation("./gg_final2/gg_final2.ply")



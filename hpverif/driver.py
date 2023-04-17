import verification  as v



verif = v.Verification()
#dp,dc = verif.capture_frame(100, "gg.bag", 0)
dp,dc,p = verif.show_files(26,"gg_final.bag")

verif.PointCloud(dp,"gg_final_v2")
#a,c = verif.Segmentation("./gg_final2/gg_final2.ply")



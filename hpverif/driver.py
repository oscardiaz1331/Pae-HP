import verification  as v



verif = v.Verification()
dp,dc = verif.capture_frame(100, "gg.bag", 0)
dp,dc,p = verif.show_files(26,"gg.bag")

verif.PointCloud(dp,"gg")
a,c = verif.Segmentation("./gg/gg.ply")

min_bound = c.get_min_bound()
max_bound = c.get_max_bound()

# Calculate the depth of each point
depth_values = c.points[:, 2] - min_bound[2]

print(depth_values)

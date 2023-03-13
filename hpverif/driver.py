import verification as v



verif = v.Verification()
dp,cp = verif.show_files(15, "../recordings/recordings/recording4.bag")

ms = verif.matrixDiagn(dp)
verif.kmeans(ms, 2)

set -e
for year in 2017
do
  for tau in 000100 000300 001000 003000 010000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    for mass in 15 55
    do
      #cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverJetByJetHistsOnnormdzulv30lepmumv6_20_tau${tau}um_M${mass}_2Djetdrjet1sump1Dmovedist3Correction"
      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverJetByJetHistsOnnormdzulv30lepmumv6_20_tau${tau}um_noCorrection"
      mhadd . --ignore-done &
    done
  done
done

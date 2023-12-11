set -e
sigpth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruthVetoPUPVetoTrkJetByMiniJetHistsUlv30lepmumv4"
pth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverJetByJetHistsUlv30lepmumv4_20_tau001000um_2Djetdrjet1sumpCorrection"
for year in 2017
do
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python draw.py TM_config20_M55_tau000${tau}um ${pth}/SingleMuon${year}.root ${pth}/background_leptonpresel_${year}.root ${sigpth}/WplusHToSSTodddd_tau1mm_M55_2017.root  
  done
done

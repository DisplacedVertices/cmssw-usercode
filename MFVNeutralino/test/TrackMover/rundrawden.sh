set -e
sigpth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruthVetoPUPVetoTrkJetByMiniJetHistsUlv30lepmumv4"
pth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverJetByJetHistsUlv30lepmumv4_20_tau001000um_2Djetdrjet1sumpCorrection"
for year in 2017
do
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python drawden.py TM_config20_M55_tau000${tau}um_den_2Dreweight ${pth}/SingleMuon${year}.root ${pth}/others_leptonpresel_2017.root ${pth}/qcd_leptonpresel_${year}.root ${pth}/dyjets_leptonpresel_2017.root ${pth}/wjetstolnu_leptonpresel_2017.root ${pth}/qcdmupt5_leptonpresel_2017.root ${sigpth}/WplusHToSSTodddd_tau1mm_M55_2017.root  long Muon

  done
done

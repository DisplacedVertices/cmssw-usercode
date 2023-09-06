set -e
sigpth="/uscms/home/pkotamni/nobackup/crabdirs/"
pth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverHistsTightIPMETcutUlv30lepmumv7_20_tau"
for year in 2017
do
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python drawden.py TM_drawtau${tau}_Mu${year}_bkg${year}_v7TightIPMET_den_stack ${pth}${tau}um/SingleMuon${year}.root ${pth}${tau}um/others_leptonpresel_2017.root ${pth}${tau}um/qcd_leptonpresel_${year}.root ${pth}${tau}um/dyjets_leptonpresel_2017.root ${pth}${tau}um/wjetstolnu_amcatnlo_2017.root ${pth}${tau}um/qcdmupt5_leptonpresel_2017.root ${sigpth}TrackMoverMCTruthHistUlv30mv7/WplusHToSSTodddd_tau1mm_M55_2017.root ${sigpth}TrackMoverMCTruthHistUlv30mv7/WplusHToSSTodddd_tau1mm_M55_2017.root  long Muon

  done
done

set -e
pth="/uscms/home/pkotamni/nobackup/crabdirs/"
for year in 2017
do
  for tau in 000300 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python drawden.py TM_drawtau${tau}_Mu${year}_bkg${year}_wplus55GeV_den ${pth}TrackMoverHistsUlv30lepmumv4_20_tau${tau}um/SingleMuon${year}.root ${pth}TrackMoverHistsUlv30lepmumv4_20_tau${tau}um/ttbar_2017.root ${pth}TrackMoverHistsUlv30lepmumv4_20_tau${tau}um/qcd_leptonpresel_${year}.root ${pth}TrackMoverHistsUlv30lepmumv4_20_tau${tau}um/wjetstolnu_2017.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruthHistsUlv30lepMumv4/WplusHToSSTodddd_tau300um_M55_${year}.root
    
    python drawden.py TM_drawtau${tau}_Ele${year}_bkg${year}_wplus55GeV_den ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/SingleElectron${year}.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/ttbar_2017.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/qcd_leptonpresel_${year}.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/wjetstolnu_2017.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruthHistsUlv30lepMumv4/WplusHToSSTodddd_tau300um_M55_${year}.root

  done
done

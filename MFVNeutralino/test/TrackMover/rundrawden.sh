set -e
pth="/uscms/home/pkotamni/nobackup/crabdirs/"
for year in 2017
do
  for tau in 010000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    python drawden.py TM_drawtau${tau}_Mu${year}_bkg${year}_den_stack ${pth}TrackMoverHistsUlv30lepmumv6_20_tau${tau}um/SingleMuon${year}.root ${pth}TrackMoverHistsUlv30lepmumv6_20_tau${tau}um/bkg_leptonpresel_2017.root ${pth}TrackMoverHistsUlv30lepmumv6_20_tau${tau}um/qcd_leptonpresel_${year}.root ${pth}TrackMoverHistsUlv30lepmumv6_20_tau${tau}um/dyjets_leptonpresel_2017.root ${pth}TrackMoverHistsUlv30lepmumv6_20_tau${tau}um/wjetstolnu_amcatnlo_2017.root long Muon

    #python drawden.py TM_drawtau${tau}_Ele${year}_bkg${year}_wplus55GeV_den_stack ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/SingleElectron${year}.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/bkg_leptonpresel_2017.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/qcd_leptonpresel_${year}.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/dyjetstollM10_2017.root ${pth}TrackMoverHistsUlv30lepelemv4_20_tau${tau}um/wjetstolnu_amcatnlo_2017.root /uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruthHistsUlv30lepMumv4/WplusHToSSTodddd_tau1mm_M55_${year}.root long Ele

  done
done

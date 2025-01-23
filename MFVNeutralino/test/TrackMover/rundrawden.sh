set -e

data="SingleMuon2017p8.root"
bkg="background_leptonpresel_2017p8.root"
for year in "2017p8"
do
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    for mass in 15 
    do
     tau_mm=$(echo "$tau/1000" | bc)
     pth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection"
     pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection"
     pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection"
     sigpth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau${tau_mm}mm_M${mass}_20161p2.root"
     sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau${tau_mm}mm_M${mass}_2017p8.root"
     sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6/VHToSSTodddd_tau${tau_mm}mm_M${mass}_${year}.root"
      python drawden.py TM_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_loweta_VHSS4d_compare_years ${pth1}/${bkg} ${pth1}/${data} ${sigpth1} ${sigpth2} ${pth1}/${bkg} ${pth1}/${data} long Low
      #python drawden.py TM_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_mixeta_VHSS4d ${pth2}/${bkg} ${pth2}/${data} ${sigpth2} ${sigpth2} ${pth2}/${bkg} ${pth2}/${data} long Mix
      #python drawden.py TM_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_higheta_VHSS4d ${pth3}/${bkg} ${pth3}/${data} ${sigpth3} ${sigpth3} ${pth3}/${bkg} ${pth3}/${data} long High
    done

  done

done

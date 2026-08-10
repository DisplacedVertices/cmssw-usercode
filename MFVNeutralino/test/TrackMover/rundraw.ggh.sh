set -e
for year in "2017p8"
do
  data="BTagDispl${year}.root"
  bkg="background_btagpresel_${year}.root"
  for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    for mass in 55
    do
     mass_int=$(echo "$mass" | bc)
     tau_mm=$(echo "$tau/1000" | bc)
     pth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_ggH_20_tau${tau}um_M${mass_int}_2DCorrection"
     pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_ggH_20_tau${tau}um_M${mass_int}_2DCorrection"
     pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_ggH_20_tau${tau}um_M${mass_int}_2DCorrection"
     sigpth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau${tau_mm}mm_M${mass}_${year}.root" 
     sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau${tau_mm}mm_M${mass}_${year}.root"
     sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6/ggHToSSTodddd_tau${tau_mm}mm_M${mass}_${year}.root"
     python draw.py TM_TOC_B_year${year}_ctau${tau}um_mass${mass}_loweta_ggH_ACTUAL ${pth1}/${bkg} ${pth1}/${data}  ${sigpth1} ${sigpth1} ${pth1}/${data} Low
     #python draw.py TM_TOC_B_year${year}_ctau${tau}um_mass${mass}_mixeta_ggH ${pth2}/${bkg} ${pth2}/${data}  ${sigpth2} ${sigpth2} ${pth2}/${data} Mix
     #python draw.py TM_TOC_B_year${year}_ctau${tau}um_mass${mass}_higheta_ggH ${pth3}/${bkg} ${pth3}/${data}  ${sigpth3} ${sigpth3} ${pth3}/${data} High
    done

  done

done

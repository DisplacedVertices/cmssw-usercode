set -e
for year in "2017p8"
do
  data="BTagDispl${year}.root"
  bkg="background_btagpresel_${year}.root"
  for tau in 000300 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
  do
    for mass in 0400 
    do
     mass_int=$(echo "$mass" | bc)
     pth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselhighptv8_20_tau${tau}um_M${mass_int}_2DCorrection"
     pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselhighptv8_20_tau${tau}um_M${mass_int}_2DCorrection"
     pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselhighptv8_20_tau${tau}um_M${mass_int}_2DCorrection"
     sigpth1="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau${tau}um_M${mass}_${year}.root" 
     sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau${tau}um_M${mass}_${year}.root"
     sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselhighptv6/mfv_stopdbardbar_tau${tau}um_M${mass}_${year}.root"
     
     python draw.py TM_TOC_B_year${year}_ctau${tau}um_mass${mass}_loweta_Stopdbardbar ${pth1}/${bkg} ${pth1}/${data}  ${sigpth1} ${sigpth1} ${pth1}/${data} Low
     #python draw.py TM_TOC_B_year${year}_ctau${tau}um_mass${mass}_mixeta_Stopdbardbar ${pth2}/${bkg} ${pth2}/${data}  ${sigpth2} ${sigpth2} ${pth2}/${data} Mix
     #python draw.py TM_TOC_B_year${year}_ctau${tau}um_mass${mass}_higheta_Stopdbardbar ${pth3}/${bkg} ${pth3}/${data}  ${sigpth3} ${sigpth3} ${pth3}/${data} High
    done

  done

done

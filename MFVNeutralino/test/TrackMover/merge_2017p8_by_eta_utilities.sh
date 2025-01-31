set -e
for eta in 'Low' 'Mix' 'High'
do
  for tau in 1 10 #000100 000300 001000 010000 030000 #1 3 10 30  
  do
    for mass in 40
    do
      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_${eta}Eta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
      #hadd mfv_stopbbarbbar_tau${tau}um_M${mass}_2017p8.root mfv_stopbbarbbar_tau${tau}um_M${mass}_2017.root mfv_stopbbarbbar_tau${tau}um_M${mass}_2018.root 
      #cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_${eta}Eta_LowdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
      hadd ggHToSSTodddd_tau${tau}mm_M${mass}_2017p8.root ggHToSSTodddd_tau${tau}mm_M${mass}_2017.root ggHToSSTodddd_tau${tau}mm_M${mass}_2018.root 
    done
  done
done


#for eta in 'Low' 'Mix' 'High'
#do
#  for tau in 100 300
#  do
#    for mass in 15 40 55
#    do
#      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_${eta}Eta_LowdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
#      hadd VHToSSTodddd_tau${tau}um_M${mass}_2017p8.root *HToSSTodddd_tau${tau}um_M${mass}_2017.root *HToSSTodddd_tau${tau}um_M${mass}_2018.root 
#    done
#  done
#done


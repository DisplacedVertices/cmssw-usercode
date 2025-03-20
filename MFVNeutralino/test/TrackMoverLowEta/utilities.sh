set -e

#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_20_noCorrection"
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_noCorrection"
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py leptonpresel histos 20161 &
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py leptonpresel histos 20162 &
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_2018.py leptonpresel histos 2018 &
#rm -rf *2017p8*
#rm -rf *btagpresel*2017*
#rm -rf *btagpresel*2018*
#rm -rf *20161.root*
#rm -rf *20162.root*
#rm -rf *2017.root*
#rm -rf *2018.root*
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py btagpresel histos 20161 &
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py btagpresel histos 20162 &
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities.py btagpresel histos 2017 &
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_2018.py btagpresel histos 2018 &
#mhadd ./*2016* --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_LowdVV_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#hadd.py background_btagpresel_2017p8.root background_btagpresel_2017.root background_btagpresel_2018.root
#hadd.py BTagDispl2017p8.root DisplacedJet2017.root DisplacedJet2018.root BTagCSV2017.root JetHT2018.root
#hadd.py background_btagpresel_20161p2.root background_btagpresel_20161.root background_btagpresel_20162.root
#hadd.py BTagDispl20161p2.root DisplacedJet20161.root DisplacedJet20162.root BTagCSV20161.root BTagCSV20162.root


#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau000300um_M40_2DCorrection"
#rm -rf *leptonpresel*2016*
#rm -rf SingleMuon20161.root*
#rm -rf SingleMuon20162.root*
#rm -rf SingleMuon20161p2.root*
#mhadd ./*2016* --ignore-done & 
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py leptonpresel histos 20161 &
#~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py leptonpresel histos 20162 &
#hadd.py background_leptonpresel_20161p2.root background_leptonpresel_20161.root background_leptonpresel_20162.root
#hadd.py SingleMuon20161p2.root SingleMuon20161.root SingleMuon20162.root

#for tau in 001000 010000 
#do
#    for mass in 40
#    do
#      cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_ggH_20_tau${tau}um_M${mass}_2DCorrection"
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py leptonpresel histos 20161 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py leptonpresel histos 20162 &
      #rm -rf DisplacedJet20161.root*
      #rm -rf DisplacedJet20162.root*
      #rm -rf BTagCSV20161.root*
      #rm -rf BTagCSV20162.root*
      #rm -rf *btagpresel*2016*
      #rm -rf BTagDispl20161p2.root
      #rm -rf *leptonpresel*2016*
      #rm -rf SingleMuon20161.root*
      #rm -rf SingleMuon20162.root*
#     rm -rf SingleMuon20161p2.root*
      #mhadd ./*2017* --ignore-done & 
      #mhadd ./*2018* --ignore-done & 
      #mhadd ./*2016* --ignore-done & 
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities.py btagpresel histos 2017 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_2018.py btagpresel histos 2018 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py btagpresel histos 20161 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py btagpresel histos 20162 &
      #hadd.py background_btagpresel_2017p8.root background_btagpresel_2017.root background_btagpresel_2018.root
      #hadd.py BTagDispl2017p8.root DisplacedJet2017.root DisplacedJet2018.root BTagCSV2017.root JetHT2018.root
#      hadd.py background_btagpresel_20161p2.root background_btagpresel_20161.root background_btagpresel_20162.root
#      hadd.py BTagDispl20161p2.root DisplacedJet20161.root DisplacedJet20162.root BTagCSV20161.root BTagCSV20162.root
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py leptonpresel histos 20161 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py leptonpresel histos 20162 &
      #hadd.py background_leptonpresel_20161p2.root background_leptonpresel_20161.root background_leptonpresel_20162.root
      #hadd.py SingleMuon20161p2.root SingleMuon20161.root SingleMuon20162.root
#    done
#done

#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#mhadd . --ignore-done & 

#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_LowdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
#mhadd . --ignore-done & 
#cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
#mhadd . --ignore-done & 



for tau in 000100 000300 001000 003000 010000 030000
do
    for mass in 15 #40 55 #15 
    do
      #cd "/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection"
      cd "/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau${tau}um_M${mass}_2DCorrection/" 
      #rm *leptonpresel* 
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py leptonpresel histos 20161 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py leptonpresel histos 20162 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities.py leptonpresel histos 2017 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_2018.py leptonpresel histos 2018 &
      hadd.py background_leptonpresel_2017p8.root background_leptonpresel_2017.root background_leptonpresel_2018.root
#      hadd.py SingleMuon2017p8.root SingleMuon2017.root SingleMuon2018.root
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20161.py leptonpresel histos 20161 &
      #~/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/utilities_20162.py leptonpresel histos 20162 &
      hadd.py background_leptonpresel_20161p2.root background_leptonpresel_20161.root background_leptonpresel_20162.root
#      hadd.py SingleMuon20161p2.root SingleMuon20161.root SingleMuon20162.root
    done
done

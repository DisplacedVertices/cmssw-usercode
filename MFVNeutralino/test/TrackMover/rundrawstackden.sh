set -e
sigpth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_MixEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30lepmumv6"
pth="/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"
pth2="/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"
pth3="/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"

#pthx="/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"
#pthx2="/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"
#pthx3="/eos/uscms/store/user/pkotamni/TrackMover_LEPTONMU/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"


mass=55
year="2017p8"

for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
do
    python drawstackden.py TM_STACK_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_loweta_VHSS4d_ADDTTbar ${pth}/SingleMuon${year}.root ${pth}/ttbar_leptonpresel_${year}.root ${pth}/background_leptonpresel_${year}.root ${pth}/dyjets_leptonpresel_${year}.root ${pth}/wjetstolnu_leptonpresel_${year}.root ${pth}/diboson_leptonpresel_${year}.root ${sigpth}/VHToSSTodddd_tau1mm_M${mass}_${year}.root  long Muon

    python drawstackden.py TM_STACK_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_mixeta_VHSS4d_ADDTTbar ${pth2}/SingleMuon${year}.root ${pth2}/ttbar_leptonpresel_${year}.root ${pth2}/background_leptonpresel_${year}.root ${pth2}/dyjets_leptonpresel_${year}.root ${pth2}/wjetstolnu_leptonpresel_${year}.root ${pth2}/diboson_leptonpresel_${year}.root ${sigpth2}/VHToSSTodddd_tau1mm_M${mass}_${year}.root  long Muon

    python drawstackden.py TM_STACK_DENOM_Mu_year${year}_ctau${tau}um_mass${mass}_higheta_VHSS4d_ADDTTbar ${pth3}/SingleMuon${year}.root ${pth3}/ttbar_leptonpresel_${year}.root ${pth3}/background_leptonpresel_${year}.root ${pth3}/dyjets_leptonpresel_${year}.root ${pth3}/wjetstolnu_leptonpresel_${year}.root ${pth3}/diboson_leptonpresel_${year}.root ${sigpth3}/VHToSSTodddd_tau1mm_M${mass}_${year}.root  long Muon
done

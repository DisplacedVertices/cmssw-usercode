set -e
sigpth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
sigpth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_LowEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30mpreselv6"
sigpth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMoverMCTruth_HighEta_HighdVV0p36_NoPreSelRelaxBSPVetodR0p4VetoMissLLPVetoTrkJetByMiniJetHistsOnnormdzUlv30bmpreselv6"
#pth="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_LowEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30bmofftosspreselv8_20_noCorrection"
#pth2="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_MixEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"
#pth3="/uscms/home/pkotamni/nobackup/crabdirs/TrackMover_HighEta_NoPreSelRelaxBSPNotwVetodR0p4JetByJetHistsOnnormdzulv30lepmumv8_20_tau001000um_M55_2DCorrection"


year="2017p8"

for tau in 001000 #001000 030000 #000000100 000000300 000001000 000003000 000010000 000030000 000100000
do
    #python drawden.py TM_DENOM_B_year${year}_neu_1mm_M400_loweta_by_trigs ${sigpth}/mfv_stopdbardbar_tau000300um_M3000_${year}.root ${sigpth}/mfv_neu_tau001000um_M0400_${year}.root ${sigpth}/mfv_stopdbardbar_tau000300um_M0400_${year}.root  ${sigpth2}/mfv_neu_tau001000um_M0400_${year}.root  ${sigpth}/mfv_neu_tau001000um_M0400_${year}.root  ${sigpth}/mfv_neu_tau001000um_M0400_${year}.root long Barrel
    python draw.py TM_TOC_B_year${year}_neu_1mm_M400_loweta_by_trigs ${sigpth}/mfv_stopdbardbar_tau000300um_M3000_${year}.root ${sigpth}/mfv_neu_tau001000um_M0400_${year}.root ${sigpth}/mfv_stopdbardbar_tau000300um_M0400_${year}.root  ${sigpth2}/mfv_neu_tau001000um_M0400_${year}.root ${sigpth}/mfv_neu_tau001000um_M0400_${year}.root Barrel

done

#!/usr/bin/env python

import sys, optparse

################################################################################

parser = optparse.OptionParser(usage='%prog [options] input.root [plot path]')
parser.add_option('--dir', default='SimpleTriggerEfficiency',
                  help='The directory name (i.e. the module label used for SimpleTriggerEfficiency).')
parser.add_option('--dir2',
                  help='The second directory name (if applicable, e.g. in --compare).')
parser.add_option('--table', action='store_true', default=False,
                  help='Print a table of the paths and efficiencies.')
parser.add_option('--table-nevents', action='store_true', default=False,
                  help='In the table, also print number of events instead of just the efficiencies.')
parser.add_option('--table-conf-level', type=float, default=0.6827,
                  help='Confidence level for the intervals displayed (default is %default).')
parser.add_option('--table-apply-prescales', action='store_true', default=False,
                  help='Use prescales from prescales.py in current directory.')
parser.add_option('--table-apply-prescales-in-sort', action='store_true', default=False,
                  help='Use prescaled values when sorting the table (implies --table-apply-prescales).')
parser.add_option('--table-sort-by-bit', action='store_true', default=False,
                  help='Sort by trigger bit instead of decreasing efficiency.')
parser.add_option('--compare', action='store_true', default=False,
                  help='Compare two sets of efficiencies (requires --dir2 to be specified).')
parser.add_option('--twod', action='store_true', default=False,
                  help='Not implemented.')

options, args = parser.parse_args()
#print options ; print args ; import sys ; print sys.argv ; raise 1

if not options.dir:
    raise ValueError('must supply a directory name')

if options.twod:
    raise NotImplementedError('twod')

if not any((options.table, options.compare, options.twod)):
    print 'none of --table, --compare, --twod specified, defaulting to --table'
    options.table = True

options.input_fn = args[0]
options.will_plot = options.compare or options.twod

if options.will_plot:
    if len(args) < 2:
        raise ValueError('must supply plot path when plotting')
    options.plot_path = args[1]

if options.table_apply_prescales_in_sort:
    options.table_apply_prescales = True

unprescaled = [
'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_TightID_CrossL1_v'
,'HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTauHPS30_eta2p1_CrossL1_v'
,'HLT_Ele24_eta2p1_WPTight_Gsf_MediumChargedIsoPFTauHPS30_eta2p1_TightID_CrossL1_v'
,'HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTauHPS30_eta2p1_CrossL1_v'
,'HLT_Ele24_eta2p1_WPTight_Gsf_TightChargedIsoPFTauHPS30_eta2p1_TightID_CrossL1_v'
,'HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v'
,'HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v'
,'HLT_DoubleMediumChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v'
,'HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_TightID_eta2p1_Reg_v'
,'HLT_DoubleTightChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v'
,'HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_TightID_eta2p1_Reg_v'
,'HLT_DoubleTightChargedIsoPFTauHPS40_Trk1_eta2p1_Reg_v'
,'AlCa_EcalEtaEBonly_v'
,'AlCa_EcalEtaEEonly_v'
,'AlCa_EcalPi0EBonly_v'
,'AlCa_EcalPi0EEonly_v'
,'HLT_L2Mu40_NoVertex_3Sta_NoBPTX3BX_v'
,'HLT_L2Mu45_NoVertex_3Sta_NoBPTX3BX_v'
,'HLT_UncorrectedJetE30_NoBPTX3BX_v'
,'HLT_UncorrectedJetE30_NoBPTX_v'
,'HLT_UncorrectedJetE60_NoBPTX3BX_v'
,'HLT_Diphoton30PV_18PV_R9Id_AND_IsoCaloId_AND_HE_R9Id_PixelVeto_Mass55_v'
,'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_NoPixelVeto_v'
,'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass90_v'
,'HLT_Diphoton30_22_R9Id_OR_IsoCaloId_AND_HE_R9Id_Mass95_v'
,'HLT_DoubleEle25_CaloIdL_MW_v'
,'HLT_DoubleEle33_CaloIdL_MW_v'
,'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_DZ_PFHT350_v'
,'HLT_DoubleEle8_CaloIdM_TrackIdM_Mass8_PFHT350_v'
,'HLT_DoublePhoton70_v'
,'HLT_DoublePhoton85_v'
,'HLT_Ele115_CaloIdVT_GsfTrkIdT_v'
,'HLT_Ele15_IsoVVVL_PFHT450_PFMET50_v'
,'HLT_Ele15_IsoVVVL_PFHT450_v'
,'HLT_Ele15_IsoVVVL_PFHT600_v'
,'HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL_v'
,'HLT_Ele20_WPLoose_Gsf_v'
,'HLT_Ele20_WPTight_Gsf_v'
,'HLT_Ele20_eta2p1_WPLoose_Gsf_v'
,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v'
,'HLT_Ele24_eta2p1_WPTight_Gsf_LooseChargedIsoPFTauHPS30_eta2p1_CrossL1_v'
,'HLT_Ele27_Ele37_CaloIdL_MW_v'
,'HLT_Ele28_WPTight_Gsf_v'
,'HLT_Ele28_eta2p1_WPTight_Gsf_HT150_v'
,'HLT_Ele30_eta2p1_WPTight_Gsf_CentralPFJet35_EleCleaned_v'
,'HLT_Ele32_WPTight_Gsf_v'
,'HLT_Ele35_WPTight_Gsf_L1EGMT_v'
,'HLT_Ele35_WPTight_Gsf_v'
,'HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v'
,'HLT_Ele50_IsoVVVL_PFHT450_v'
,'HLT_Photon100EE_TightID_TightIso_v'
,'HLT_Photon165_R9Id90_HE10_IsoM_v'
,'HLT_Photon200_v'
,'HLT_Photon50_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_PFMET50_v'
,'HLT_Photon60_R9Id90_CaloIdL_IsoL_DisplacedIdL_PFHT350MinPFJet15_v'
,'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ300_PFJetsMJJ400DEta3_v'
,'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ300DEta3_v'
,'HLT_TriplePhoton_20_20_20_CaloIdLV2_R9IdVL_v'
,'HLT_TriplePhoton_20_20_20_CaloIdLV2_v'
,'HLT_TriplePhoton_30_30_10_CaloIdLV2_R9IdVL_v'
,'HLT_TriplePhoton_30_30_10_CaloIdLV2_v'
,'HLT_TriplePhoton_35_35_5_CaloIdLV2_R9IdVL_v'
,'HLT_BTagMu_AK8Jet170_DoubleMu5_noalgo_v'
,'HLT_HT430_DisplacedDijet40_DisplacedTrack_v'
,'HLT_AK8PFHT800_TrimMass50_v'
,'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p17_v'
,'HLT_AK8PFJet330_TrimMass30_PFAK8BTagDeepCSV_p1_v'
,'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np2_v'
,'HLT_AK8PFJet360_TrimMass30_v'
,'HLT_AK8PFJet380_TrimMass30_v'
,'HLT_AK8PFJet500_v'
,'HLT_AK8PFJet550_v'
,'HLT_CaloJet500_NoJetID_v'
,'HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v'
,'HLT_Mu12_DoublePFJets40MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v'
,'HLT_PFHT1050_v'
,'HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v'
,'HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v'
,'HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v'
,'HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v'
,'HLT_PFHT500_PFMET100_PFMHT100_IDTight_v'
,'HLT_PFHT700_PFMET85_PFMHT85_IDTight_v'
,'HLT_PFHT800_PFMET75_PFMHT75_IDTight_v'
,'HLT_PFJet500_v'
,'HLT_PFJet550_v'
,'HLT_QuadPFJet98_83_71_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v'
,'HLT_QuadPFJet98_83_71_15_PFBTagDeepCSV_1p3_VBF2_v'
,'HLT_Rsq0p35_v'
,'HLT_RsqMR300_Rsq0p09_MR200_4jet_v'
,'HLT_RsqMR300_Rsq0p09_MR200_v'
,'HLT_DiJet110_35_Mjj650_PFMET110_v'
,'HLT_MET105_IsoTrk50_v'
,'HLT_MonoCentralPFJet80_PFMETNoMu120_PFMHTNoMu120_IDTight_v'
,'HLT_PFMET110_PFMHT110_IDTight_CaloBTagDeepCSV_3p1_v'
,'HLT_PFMET120_PFMHT120_IDTight_v'
,'HLT_PFMET200_HBHE_BeamHaloCleaned_v'
,'HLT_PFMET250_HBHECleaned_v'
,'HLT_PFMET300_HBHECleaned_v'
,'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v'
,'HLT_PFMETTypeOne140_PFMHT140_IDTight_v'
,'HLT_PFMETTypeOne200_HBHE_BeamHaloCleaned_v'
,'HLT_TripleJet110_35_35_Mjj650_PFMET110_v'
,'HLT_DoubleMediumChargedIsoPFTauHPS30_L1MaxMass_Trk1_eta2p1_Reg_v'
,'HLT_DoubleMediumChargedIsoPFTauHPS35_Trk1_eta2p1_Reg_v'
,'HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_v'
,'HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET100_v'
,'HLT_Photon35_TwoProngs35_v'
,'HLT_VBF_DoubleLooseChargedIsoPFTauHPS20_Trk1_eta2p1_v'
,'HLT_VBF_DoubleMediumChargedIsoPFTauHPS20_Trk1_eta2p1_v'
,'HLT_VBF_DoubleTightChargedIsoPFTauHPS20_Trk1_eta2p1_v'
,'HLT_Dimuon0_Jpsi3p5_Muon2_v'
,'HLT_Dimuon18_PsiPrime_noCorrL1_v'
,'HLT_Dimuon18_PsiPrime_v'
,'HLT_Dimuon25_Jpsi_noCorrL1_v'
,'HLT_Dimuon25_Jpsi_v'
,'HLT_DoubleMu2_Jpsi_DoubleTkMu0_Phi_v'
,'HLT_DoubleMu2_Jpsi_DoubleTrk1_Phi1p05_v'
,'HLT_DoubleMu4_3_Bs_v'
,'HLT_DoubleMu4_JpsiTrkTrk_Displaced_v'
,'HLT_DoubleMu4_JpsiTrk_Displaced_v'
,'HLT_DoubleMu4_PsiPrimeTrk_Displaced_v'
,'HLT_Mu30_TkMu0_Psi_v'
,'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_NoL2Matched_v'
,'HLT_DoubleL2Mu23NoVtx_2Cha_CosmicSeed_v'
,'HLT_DoubleL2Mu23NoVtx_2Cha_NoL2Matched_v'
,'HLT_DoubleL2Mu23NoVtx_2Cha_v'
,'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_Eta2p4_v'
,'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_v'
,'HLT_DoubleL2Mu25NoVtx_2Cha_Eta2p4_v'
,'HLT_DoubleL2Mu25NoVtx_2Cha_v'
,'HLT_DoubleL2Mu30NoVtx_2Cha_CosmicSeed_Eta2p4_v'
,'HLT_DoubleL2Mu30NoVtx_2Cha_Eta2p4_v'
,'HLT_DoubleMu33NoFiltersNoVtxDisplaced_v'
,'HLT_DoubleMu3_DCA_PFMET50_PFMHT60_v'
,'HLT_DoubleMu3_DZ_PFMET50_PFMHT60_v'
,'HLT_DoubleMu3_DZ_PFMET70_PFMHT70_v'
,'HLT_DoubleMu3_DZ_PFMET90_PFMHT90_v'
,'HLT_DoubleMu43NoFiltersNoVtx_v'
,'HLT_DoubleMu4_Mass3p8_DZ_PFHT350_v'
,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8_v'
,'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8_v'
,'HLT_Mu18_Mu9_SameSign_DZ_v'
,'HLT_Mu18_Mu9_SameSign_v'
,'HLT_Mu23_Mu12_SameSign_DZ_v'
,'HLT_Mu23_Mu12_SameSign_v'
,'HLT_Mu37_TkMu27_v'
,'HLT_TripleMu_10_5_5_DZ_v'
,'HLT_TripleMu_12_10_5_v'
,'HLT_TripleMu_5_3_3_Mass3p8_DCA_v'
,'HLT_TripleMu_5_3_3_Mass3p8_DZ_v'
,'HLT_TrkMu16_DoubleTrkMu6NoFiltersNoVtx_v'
,'HLT_DoubleMu3_TkMu_DsTau3Mu_v'
,'HLT_DoubleMu4_LowMassNonResonantTrk_Displaced_v'
,'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_v'
,'HLT_Dimuon12_Upsilon_y1p4_v'
,'HLT_Dimuon14_Phi_Barrel_Seagulls_v'
,'HLT_Dimuon24_Phi_noCorrL1_v'
,'HLT_Dimuon24_Upsilon_noCorrL1_v'
,'HLT_DoubleMu3_DoubleEle7p5_CaloIdL_TrackIdL_Upsilon_v'
,'HLT_DoubleMu5_Upsilon_DoubleEle3_CaloIdL_TrackIdL_v'
,'HLT_Mu25_TkMu0_Phi_v'
,'HLT_Mu30_TkMu0_Upsilon_v'
,'HLT_Trimuon5_3p5_2_Upsilon_Muon_v'
,'HLT_DiMu4_Ele9_CaloIdL_TrackIdL_DZ_Mass3p8_v'
,'HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ_v'
,'HLT_DoubleMu20_7_Mass0to30_Photon23_v'
,'HLT_Mu12_DoublePhoton20_v'
,'HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v'
,'HLT_Mu17_Photon30_IsoCaloId_v'
,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v'
,'HLT_Mu27_Ele37_CaloIdL_MW_v'
,'HLT_Mu37_Ele27_CaloIdL_MW_v'
,'HLT_Mu38NoFiltersNoVtxDisplaced_Photon38_CaloIdL_v'
,'HLT_Mu43NoFiltersNoVtx_Photon43_CaloIdL_v'
,'HLT_Mu48NoFiltersNoVtx_Photon48_CaloIdL_v'
,'HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ_v'
,'HLT_Mu8_Ele8_CaloIdM_TrackIdM_Mass8_PFHT350_DZ_v'
,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_CaloDiJet30_CaloBtagDeepCSV_1p5_v'
,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_CaloDiJet30_v'
,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_PFBtagDeepCSV_1p5_v'
,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_PFDiJet30_v'
,'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v'
,'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_CrossL1_v'
,'HLT_IsoMu20_eta2p1_LooseChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1_v'
,'HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_CrossL1_v'
,'HLT_IsoMu20_eta2p1_MediumChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1_v'
,'HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_CrossL1_v'
,'HLT_IsoMu20_eta2p1_TightChargedIsoPFTauHPS27_eta2p1_TightID_CrossL1_v'
,'HLT_IsoMu24_v'
,'HLT_IsoMu27_v'
,'HLT_Mu10_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT350_PFMETNoMu60_v'
,'HLT_Mu15_IsoVVVL_PFHT450_v'
,'HLT_Mu15_IsoVVVL_PFHT600_v'
,'HLT_Mu3er1p5_PFJet100er2p5_PFMET80_PFMHT80_IDTight_v'
,'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu80_PFMHTNoMu80_IDTight_v'
,'HLT_Mu4_TrkIsoVVL_DiPFJet90_40_DEta3p5_MJJ750_HTT300_PFMETNoMu60_v'
,'HLT_Mu50_IsoVVVL_PFHT450_v'
,'HLT_Mu50_v'
,'HLT_Mu8_TrkIsoVVL_DiPFJet40_DEta3p5_MJJ750_HTT300_PFMETNoMu60_v'
,'HLT_OldMu100_v'
,'HLT_TkMu100_v'
,'DST_HT250_CaloBTagScouting_v'
,'DST_HT250_CaloScouting_v'
,'DST_DoubleMu1_noVtx_CaloScouting_v'
,'DST_DoubleMu3_noVtx_CaloScouting_v'
,'DST_HT410_BTagScouting_v'
,'DST_HT410_PFScouting_v'
,'DST_DoubleMu3_noVtx_Mass10_PFScouting_v'
,'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_v'
,'HLT_Ele28_HighEta_SC20_Mass55_v'
,'HLT_Ele32_WPTight_Gsf_L1DoubleEG_v'
,'HLT_BTagMu_AK4Jet300_Mu5_noalgo_v'
,'HLT_BTagMu_AK8Jet300_Mu5_noalgo_v'
,'HLT_DoubleL2Mu50_v'
,'HLT_TrkMu12_DoubleTrkMu5NoFiltersNoVtx_v'
,'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v'
,'HLT_IsoMu24_TwoProngs35_v'
,'DST_DoubleMu3_noVtx_CaloScouting_Monitoring_v'
,'HLT_CDC_L2cosmic_5p5_er1p0_v'
,'HLT_UncorrectedJetE70_NoBPTX3BX_v'
,'HLT_Diphoton30_18_R9IdL_AND_HE_AND_IsoCaloId_NoPixelVeto_Mass55_v'
,'HLT_DoubleEle27_CaloIdL_MW_v'
,'HLT_ECALHT800_v'
,'HLT_Ele135_CaloIdVT_GsfTrkIdT_v'
,'HLT_Ele145_CaloIdVT_GsfTrkIdT_v'
,'HLT_Ele15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v'
,'HLT_Ele200_CaloIdVT_GsfTrkIdT_v'
,'HLT_Ele250_CaloIdVT_GsfTrkIdT_v'
,'HLT_Ele300_CaloIdVT_GsfTrkIdT_v'
,'HLT_Ele30_WPTight_Gsf_v'
,'HLT_Ele38_WPTight_Gsf_v'
,'HLT_Ele40_WPTight_Gsf_v'
,'HLT_Photon110EB_TightID_TightIso_v'
,'HLT_Photon120EB_TightID_TightIso_v'
,'HLT_Photon300_NoHE_v'
,'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_CaloMJJ400_PFJetsMJJ600DEta3_v'
,'HLT_Photon75_R9Id90_HE10_IsoM_EBOnly_PFJetsMJJ600DEta3_v'
,'HLT_HT430_DisplacedDijet60_DisplacedTrack_v'
,'HLT_HT500_DisplacedDijet40_DisplacedTrack_v'
,'HLT_HT650_DisplacedDijet60_Inclusive_v'
,'HLT_AK8PFHT850_TrimMass50_v'
,'HLT_AK8PFHT900_TrimMass50_v'
,'HLT_AK8PFJet330_TrimMass30_PFAK8BoostedDoubleB_np4_v'
,'HLT_AK8PFJet400_TrimMass30_v'
,'HLT_AK8PFJet420_TrimMass30_v'
,'HLT_AK8PFJetFwd500_v'
,'HLT_CaloJet550_NoJetID_v'
,'HLT_DoublePFJets128MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v'
,'HLT_Mu12_DoublePFJets54MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v'
,'HLT_Mu12_DoublePFJets62MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v'
,'HLT_PFHT400_FivePFJet_120_120_60_30_30_DoublePFBTagDeepCSV_4p5_v'
,'HLT_PFHT500_PFMET110_PFMHT110_IDTight_v'
,'HLT_PFHT700_PFMET95_PFMHT95_IDTight_v'
,'HLT_PFHT800_PFMET85_PFMHT85_IDTight_v'
,'HLT_PFJetFwd450_v'
,'HLT_PFJetFwd500_v'
,'HLT_QuadPFJet103_88_75_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v'
,'HLT_QuadPFJet103_88_75_15_PFBTagDeepCSV_1p3_VBF2_v'
,'HLT_QuadPFJet105_88_76_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v'
,'HLT_QuadPFJet105_88_76_15_PFBTagDeepCSV_1p3_VBF2_v'
,'HLT_QuadPFJet111_90_80_15_DoublePFBTagDeepCSV_1p3_7p7_VBF1_v'
,'HLT_QuadPFJet111_90_80_15_PFBTagDeepCSV_1p3_VBF2_v'
,'HLT_Rsq0p40_v'
,'HLT_RsqMR320_Rsq0p09_MR200_4jet_v'
,'HLT_RsqMR320_Rsq0p09_MR200_v'
,'HLT_CaloMET350_HBHECleaned_v'
,'HLT_DiJet110_35_Mjj650_PFMET120_v'
,'HLT_DiJet110_35_Mjj650_PFMET130_v'
,'HLT_MET120_IsoTrk50_v'
,'HLT_MonoCentralPFJet80_PFMETNoMu130_PFMHTNoMu130_IDTight_v'
,'HLT_MonoCentralPFJet80_PFMETNoMu140_PFMHTNoMu140_IDTight_v'
,'HLT_PFMET120_PFMHT120_IDTight_CaloBTagDeepCSV_3p1_v'
,'HLT_PFMET120_PFMHT120_IDTight_PFHT60_v'
,'HLT_PFMET130_PFMHT130_IDTight_CaloBTagDeepCSV_3p1_v'
,'HLT_PFMET130_PFMHT130_IDTight_v'
,'HLT_PFMET140_PFMHT140_IDTight_CaloBTagDeepCSV_3p1_v'
,'HLT_PFMET140_PFMHT140_IDTight_v'
,'HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_PFHT60_v'
,'HLT_PFMETNoMu130_PFMHTNoMu130_IDTight_v'
,'HLT_PFMETNoMu140_PFMHTNoMu140_IDTight_v'
,'HLT_TripleJet110_35_35_Mjj650_PFMET120_v'
,'HLT_TripleJet110_35_35_Mjj650_PFMET130_v'
,'HLT_MediumChargedIsoPFTau180HighPtRelaxedIso_Trk50_eta2p1_1pr_v'
,'HLT_MediumChargedIsoPFTau200HighPtRelaxedIso_Trk50_eta2p1_v'
,'HLT_MediumChargedIsoPFTau220HighPtRelaxedIso_Trk50_eta2p1_v'
,'HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET110_v'
,'HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET120_v'
,'HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET130_v'
,'HLT_MediumChargedIsoPFTau50_Trk30_eta2p1_1pr_MET140_v'
,'HLT_DoubleL2Mu25NoVtx_2Cha_CosmicSeed_NoL2Matched_v'
,'HLT_DoubleL2Mu25NoVtx_2Cha_NoL2Matched_v'
,'HLT_DoubleMu40NoFiltersNoVtxDisplaced_v'
,'HLT_DoubleMu48NoFiltersNoVtx_v'
,'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass3p8_v'
,'HLT_Mu19_TrkIsoVVL_Mu9_TrkIsoVVL_DZ_Mass8_v'
,'HLT_Mu20_Mu10_SameSign_DZ_v'
,'HLT_Mu20_Mu10_SameSign_v'
,'HLT_TrkMu17_DoubleTrkMu8NoFiltersNoVtx_v'
,'HLT_Tau3Mu_Mu7_Mu1_TkMu1_IsoTau15_Charge1_v'
,'HLT_Mu43NoFiltersNoVtxDisplaced_Photon43_CaloIdL_v'
,'HLT_IsoMu30_v'
,'HLT_Mu15_IsoVVVL_PFHT450_CaloBTagDeepCSV_4p5_v'
,'HLT_Mu15_IsoVVVL_PFHT450_PFMET50_v'
,'HLT_Mu3er1p5_PFJet100er2p5_PFMET100_PFMHT100_IDTight_v'
,'HLT_Mu3er1p5_PFJet100er2p5_PFMET90_PFMHT90_IDTight_v'
,'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu100_PFMHTNoMu100_IDTight_v'
,'HLT_Mu3er1p5_PFJet100er2p5_PFMETNoMu90_PFMHTNoMu90_IDTight_v'
,'HLT_Mu55_v'
]

################################################################################

from math import log10
from JMTucker.Tools.ROOTTools import *

input_f = ROOT.TFile(options.input_fn)

if options.compare or options.twod:
    set_style()
    ps = plot_saver(options.plot_path)
    
def get_hists(dn, twod=False):
    hnum = input_f.Get(dn).Get('triggers%s_pass_num' % ('2d' if twod else ''))
    hden = input_f.Get(dn).Get('triggers%s_pass_den' % ('2d' if twod else ''))
    return hnum, hden

################################################################################

if options.table:
    hnum, hden = get_hists(options.dir)
    print 'number of events:', hden.GetBinContent(1)
    
    width = 0
    content = []
    mx = 0
    for i in xrange(1, hden.GetNbinsX() + 1):
        path = hden.GetXaxis().GetBinLabel(i)
        width = max(width, len(path))

        num = hnum.GetBinContent(i)
        den = hden.GetBinContent(i)
        eff, lo, hi = clopper_pearson(num, den, alpha=1-options.table_conf_level)

        prescaled_eff = 1
        
        if options.table_apply_prescales:
            import prescales
            l1, hlt, overall = prescales.get(path)
            if overall > 0:
                eff /= overall
                lo /= overall
                hi /= overall
            elif overall == 0:
                eff = lo = hi = 0.
        else:
            l1, hlt, overall = -1, -1, -1

        mx = max(mx, num, hi*den)
        if options.table_nevents:
            c = (i-1, path, num, int(round(lo*den)), int(round(hi*den)))
        else:
            c = (i-1, path, eff, (hi-lo)/2, lo, hi)
        if options.table_apply_prescales:
            c += (l1, hlt, overall, prescaled_eff)
        content.append(c)

    if options.table_nevents:
        num_width = '%' + str(int(round(log10(mx))) + 2) + 'i'
        fmt = '(%3i) %' + str(width + 2) + 's ' + num_width + '  68%% CL: [' + num_width + ', ' + num_width + ']'
    else:
        fmt = '(%3i) %' + str(width + 2) + 's %.3e +- %.3e 68%% CL: [%.3e, %.3e]'
    if options.table_apply_prescales:
        fmt += '   after prescales: (%10i * %10i = %10i):  %.4f'

    if options.table_sort_by_bit:
        print 'sorted by trigger bit:'
        for c in content:
            print fmt % c
        print
    else:
        print 'sorted by decreasing eff',
        if options.table_apply_prescales_in_sort:
            print '(after applying prescales):'
            key = lambda x: x[-1]
        else:
            print ':'
            key = lambda x: x[2]
        content.sort(key=key, reverse=True)
        for c in content:
            for c_good in unprescaled :
                #print "1 "+ (fmt % c)
                #print "2 " + c_good
                #print (fmt % c).find(c_good)
                if (fmt % c).find(c_good) != -1 :
                    print fmt % c

################################################################################
            
if options.compare:
    hnum,  hden  = get_hists(options.dir)
    hnum2, hden2 = get_hists(options.dir2)

    eff  = histogram_divide(hnum,    hden)
    eff2 = histogram_divide(hnum_mu, hden_mu)

    eff.SetLineColor(ROOT.kRed)
    eff.Draw('APL')
    eff2.SetLineColor(ROOT.kBlue)
    eff2.Draw('P same')
    ps.save('compare')

################################################################################
            
if False and options.twod:
    hnum, hden = get_hists(options.dir, twod=True)
    hnum.Divide(hden)
    xax, yax = hnum.GetXaxis(), hnum.GetYaxis()
    for x in xrange(1, xax.GetNbins()+1):
        for y in xrange(1, yax.GetNbins()+1):
            xpath = xax.GetBinLabel(x)
            ypath = yax.GetBinLabel(y)
            # ...

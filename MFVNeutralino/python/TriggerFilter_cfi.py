import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.hltHighLevel_cfi

jet_paths = [
    "HLT_PFHT1050_v*",
    ]

bjet_paths = [
    # bjet triggers 2017 - only use the first two, since they contribute most of the efficiency
    "HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v*",
    #"HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v*",
    #"HLT_PFHT380_SixPFJet32_DoublePFBTagDeepCSV_2p2_v*",
    #"HLT_PFHT380_SixPFJet32_DoublePFBTagCSV_2p2_v*",
    #"HLT_PFHT430_SixPFJet40_PFBTagCSV_1p5_v*",
    # bjet triggers 2018  - only use the first two, since they contribute most of the efficiency
    #"HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v*",
    #"HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v*",
    #"HLT_PFHT400_FivePFJet_100_100_60_30_30_DoublePFBTagDeepCSV_4p5_v*",
    #"HLT_PFHT400_SixPFJet32_DoublePFBTagDeepCSV_2p94_v*",
    #"HLT_PFHT450_SixPFJet36_PFBTagDeepCSV_1p59_v*",
    ]

displaced_dijet_paths = [
    #"HLT_HT430_DisplacedDijet40_DisplacedTrack_v*",
    #"HLT_HT650_DisplacedDijet60_Inclusive_v*",
    ]

lepton_paths = [
    #"HLT_Ele35_WPTight_Gsf_v*",
    #"HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
    #"HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
    "HLT_IsoMu27_v*",
    #"HLT_Mu50_v*",
    ]

cross_paths = [
    "HLT_Ele15_IsoVVVL_PFHT450_v*", # JMTBAD these two cross triggers are rendered useless with the offline ht and lepton pt cuts imposed in eventFilter
    "HLT_Mu15_IsoVVVL_PFHT450_v*",
    ]

mfvTriggerFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = jet_paths + lepton_paths + cross_paths,
    andOr = True, # = OR
    throw = False,
    )

mfvTriggerFilterJetsOnly = mfvTriggerFilter.clone(HLTPaths = jet_paths)
mfvTriggerFilterBJetsOnly = mfvTriggerFilter.clone(HLTPaths = bjet_paths)
mfvTriggerFilterDisplacedDijetOnly = mfvTriggerFilter.clone(HLTPaths = displaced_dijet_paths)
mfvTriggerFilterLeptonsOnly = mfvTriggerFilter.clone(HLTPaths = lepton_paths)

mfvTriggerFilterHTORBjetsORDisplacedDijet = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = jet_paths + bjet_paths + displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterBjetsORDisplacedDijet = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = bjet_paths + displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterBjetsORDisplacedDijetVetoHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = bjet_paths + displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.hltHighLevel_cfi

jet_paths = [
    "HLT_PFHT1050_v*",
    ]

MET_paths = [
    "HLT_PFMET120_PFMHT120_IDTight_v*",
    #"HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v*",
    ]

low_HT_paths = [
    "HLT_HT325_v*",  # for 2016 HLT track studies
    "HLT_HT425_v*",  # for 2017+8 HLT track studies
    ]

bjet_paths = [
    # bjet triggers 2016
    "HLT_QuadJet45_TripleBTagCSV_p087_v*", 
    "HLT_DoubleJet90_Double30_TripleBTagCSV_p087_v*",
    "HLT_DoubleJetsC100_DoubleBTagCSV_p014_DoublePFJetsC100MaxDeta1p6_v*",
    # bjet triggers 2017
    "HLT_DoublePFJets100MaxDeta1p6_DoubleCaloBTagCSV_p33_v*",
    "HLT_PFHT300PT30_QuadPFJet_75_60_45_40_TriplePFBTagCSV_3p0_v*",
    # bjet triggers 2018
    "HLT_DoublePFJets116MaxDeta1p6_DoubleCaloBTagDeepCSV_p71_v*",
    "HLT_PFHT330PT30_QuadPFJet_75_60_45_40_TriplePFBTagDeepCSV_4p5_v*",
    ]

displaced_dijet_paths = [
    # displaced dijet triggers 2016
    "HLT_HT350_DisplacedDijet40_DisplacedTrack_v*",
    "HLT_HT650_DisplacedDijet80_Inclusive_v*",
    # displaced dijet triggers 2017/2018
    "HLT_HT430_DisplacedDijet40_DisplacedTrack_v*",
    "HLT_HT650_DisplacedDijet60_Inclusive_v*",
    ]

muon_paths = [
    "HLT_IsoMu27_v*", #2017
    "HLT_IsoMu24_v*", #2016,2018
    "HLT_Mu50_v*"
]

muoniso_paths = [
     "HLT_IsoMu27_v*",
]

electron_paths = [
    "HLT_Ele27_WPTight_Gsf_v*", #2016
    "HLT_Ele35_WPTight_Gsf_v*", #2017
    "HLT_Ele32_WPTight_Gsf_v*", #2018
    "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
    "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
]

dilepton_paths = [
    "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_v*",
    "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_v*",
    "HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ_v*",
    "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ_v*",
]

cross_paths = [
    "HLT_Ele15_IsoVVVL_PFHT450_v*", # JMTBAD these two cross triggers are rendered useless with the offline ht and lepton pt cuts imposed in eventFilter
    "HLT_Mu15_IsoVVVL_PFHT450_v*",
    ]

mfvTriggerFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = jet_paths + electron_paths + muon_paths + cross_paths,
    andOr = True, # = OR
    throw = False,
    )

mfvTriggerFilterJetsOnly = mfvTriggerFilter.clone(HLTPaths = jet_paths)
mfvTriggerFilterMETOnly = mfvTriggerFilter.clone(HLTPaths = MET_paths)
mfvTriggerFilterLowHT    = mfvTriggerFilter.clone(HLTPaths = low_HT_paths)
mfvTriggerFilterBJetsOnly = mfvTriggerFilter.clone(
        HLTPaths = bjet_paths,
        andOr = True,
        throw = False,
        )
mfvTriggerFilterDisplacedDijetOnly = mfvTriggerFilter.clone(HLTPaths = displaced_dijet_paths)
mfvTriggerFilterMuonsOnly = mfvTriggerFilter.clone(HLTPaths = muon_paths)
mfvTriggerFilterElectronsOnly = mfvTriggerFilter.clone(HLTPaths = electron_paths)
mfvTriggerFilterLeptonsOnly = mfvTriggerFilter.clone(
    HLTPaths = electron_paths + muon_paths,
    andOr = True, # OR
    throw = False,
)
mfvTriggerFilterDileptonOnly = mfvTriggerFilter.clone(
        HLTPaths = dilepton_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterMETANDMuons = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = MET_paths + muoniso_paths,
        andOr = False, # AND
        throw = False,
        )

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

mfvTriggerFilterBjetsORDisplacedDijetVetoLeptonHT = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = bjet_paths + displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

mfvTriggerFilterDisplacedDijetVetoBjets = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
        HLTPaths = displaced_dijet_paths,
        andOr = True, # OR
        throw = False,
        )

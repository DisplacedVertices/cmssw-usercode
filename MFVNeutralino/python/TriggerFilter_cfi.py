import FWCore.ParameterSet.Config as cms
import HLTrigger.HLTfilters.hltHighLevel_cfi

mfvTriggerFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone(
    HLTPaths = [
        "HLT_PFHT1050_v*",
        "HLT_Ele35_WPTight_Gsf_v*",
        "HLT_Ele115_CaloIdVT_GsfTrkIdT_v*",
        "HLT_Ele50_CaloIdVT_GsfTrkIdT_PFJet165_v*",
        "HLT_IsoMu27_v*",
        "HLT_Mu50_v*",
        "HLT_Ele15_IsoVVVL_PFHT450_v*", # JMTBAD these two cross triggers are rendered useless with the offline ht and lepton pt cuts imposed in eventFilter
        "HLT_Mu15_IsoVVVL_PFHT450_v*",
        ],
    andOr = True, # = OR
    throw = False,
    )

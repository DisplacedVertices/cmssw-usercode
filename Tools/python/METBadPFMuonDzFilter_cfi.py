import FWCore.ParameterSet.Config as cms
from RecoMET.METFilters.BadPFMuonDzFilter_cfi import BadPFMuonDzFilter

# JPR 2/5/2026: This special recipe is no longer needed in UL MiniAODv2, so I dropped all reference to it throughout our code.

# MET filter:
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#Analysis_Recommendations_for_ana
# https://twiki.cern.ch/twiki/bin/view/CMS/MissingETOptionalFiltersRun2#Recipe_for_BadPFMuonDz_filter_in
BadPFMuonFilterUpdateDz=BadPFMuonDzFilter.clone(
    muons = cms.InputTag("slimmedMuons"),
    vtx   = cms.InputTag("offlineSlimmedPrimaryVertices"),
    PFCandidates = cms.InputTag("packedPFCandidates"),
    minDzBestTrack = cms.double(0.5),
    taggingMode    = cms.bool(True)
)

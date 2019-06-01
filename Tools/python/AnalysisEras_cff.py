import FWCore.ParameterSet.Config as cms

jmtAnalysisEras = cms.PSet(
    which = cms.int32(-1), # -1 means pick randomly weighted by eras' int lumi, otherwise must be one of the era numbers
    )


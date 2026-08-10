import FWCore.ParameterSet.Config as cms

mcStat = cms.EDProducer('MCStatProducer', gen_info_src = cms.InputTag('generator'))
pmcStat = cms.Path(mcStat)

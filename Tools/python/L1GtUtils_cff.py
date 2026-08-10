import FWCore.ParameterSet.Config as cms

l1GtUtilsTags = cms.PSet(
    l1GtReadoutRecordInputTag = cms.InputTag('gtDigis'),
    l1GtRecordInputTag = cms.InputTag('gtDigis'),
    l1GtTriggerMenuLiteInputTag = cms.InputTag('gtDigis'),
    )

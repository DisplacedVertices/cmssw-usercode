import FWCore.ParameterSet.Config as cms

mfvMETTrigFilter = cms.EDFilter('MFVMETTrigFilter',
                                processName = cms.untracked.string("HLT"),
                                sigTriggerName = cms.untracked.string("HLT_PFMET120_PFMHT120_IDTight_v16"),
                                triggerResultsTag = cms.untracked.InputTag("TriggerResults", "", "HLT"),
                                pfMetInputTag_ = cms.untracked.InputTag('slimmedMETs', '', 'Ntuple'),
                                met_thresh = cms.untracked.double(150),
                                verbose = cms.untracked.bool(False),
)

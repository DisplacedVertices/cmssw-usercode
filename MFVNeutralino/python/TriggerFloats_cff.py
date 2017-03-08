import FWCore.ParameterSet.Config as cms

mfvTriggerFloats = cms.EDProducer('MFVTriggerFloats',
                                  l1_results_src = cms.InputTag('gtStage2Digis'),
                                  trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                  trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                                  prints = cms.untracked.bool(False),
                                  tree = cms.untracked.bool(False),
                                  )

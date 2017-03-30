import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.L1GtUtils_cff import l1GtUtilsTags

mfvTriggerFloats = cms.EDProducer('MFVTriggerFloats',
                                  l1GtUtilsTags, # will be ignored with 2016
                                  l1_results_src = cms.InputTag('gtStage2Digis'), # ditto 2015
                                  trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                  trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                                  prints = cms.untracked.bool(False),
                                  )

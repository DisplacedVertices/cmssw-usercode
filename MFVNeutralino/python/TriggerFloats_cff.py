import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.L1GtUtils_cff import l1GtUtilsTags

mfvTriggerFloats = cms.EDFilter('MFVTriggerFloats',
                                l1GtUtilsTags, # will be ignored with 2016
                                l1_results_src = cms.InputTag('gtStage2Digis'), # ditto 2015
                                trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                trigger_objects_src = cms.InputTag('selectedPatTrigger'),
                                ht_cut = cms.double(-1),
                                prints = cms.untracked.bool(False),
                                )

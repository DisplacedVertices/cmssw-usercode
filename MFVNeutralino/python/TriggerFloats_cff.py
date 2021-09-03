import FWCore.ParameterSet.Config as cms

from DVCode.Tools.PATTupleSelection_cfi import jtupleParams

mfvTriggerFloats = cms.EDProducer('MFVTriggerFloats',
                                  l1_results_src = cms.InputTag('gtStage2Digis'),
                                  trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                  trigger_objects_src = cms.InputTag('slimmedPatTrigger'),
                                  jets_src = cms.InputTag('selectedPatJets'), # slimmedJets when running directly on miniaod
                                  jet_cut = jtupleParams.jetCut,
                                  prints = cms.untracked.int32(0),
                                  )

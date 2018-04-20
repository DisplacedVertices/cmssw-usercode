import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.L1GtUtils_cff import l1GtUtilsTags
from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvTriggerFloats = cms.EDProducer('MFVTriggerFloats',
                                  l1GtUtilsTags, # will be ignored with 2016
                                  l1_results_src = cms.InputTag('gtStage2Digis'), # ditto 2015
                                  trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                  trigger_objects_src = cms.InputTag('slimmedPatTrigger'),
                                  jets_src = cms.InputTag('selectedPatJets'), # slimmedJets for miniaod
                                  jet_cut = jtupleParams.jetCut,
                                  prints = cms.untracked.int32(0),
                                  )

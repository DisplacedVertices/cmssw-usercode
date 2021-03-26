import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.PATTupleSelection_cfi import jtupleParams

mfvTriggerFloats = cms.EDProducer('MFVTriggerFloats',
                                  l1_results_src = cms.InputTag('gtStage2Digis'),
                                  trigger_results_src = cms.InputTag('TriggerResults', '', 'HLT'),
                                  trigger_objects_src = cms.InputTag('slimmedPatTrigger'),
                                  met_filters_src = cms.InputTag('TriggerResults', '', 'PAT'),
                                  jets_src = cms.InputTag('selectedPatJets'), # slimmedJets when running directly on miniaod
                                  jet_cut = jtupleParams.jetCut,
                                  met_src = cms.InputTag('slimmedMETs', '', 'BasicAnalyzer'),
                                  #met_src = cms.InputTag('slimmedMETs'),
                                  muons_src = cms.InputTag('slimmedMuons'),
                                  muon_cut = cms.string(jtupleParams.muonCut.value()),
                                  primary_vertex_src = cms.InputTag('offlineSlimmedPrimaryVertices'), #goodOfflinePrimaryVertices
                                  #primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'), #goodOfflinePrimaryVertices
                                  isMC = cms.bool(True),
                                  prints = cms.untracked.int32(0),
                                  )

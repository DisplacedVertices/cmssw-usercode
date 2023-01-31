import FWCore.ParameterSet.Config as cms


mfvVerticesToLeptons = cms.EDProducer('MFVLeptonVertexAssociator',
                                   enable = cms.bool(True),
                                   muons_src = cms.InputTag('selectedPatMuons'),
                                   electrons_src = cms.InputTag('selectedPatElectrons'),
                                   vertex_src = cms.InputTag('mfvSelectedVerticesTmp'),
                                   input_is_refs = cms.bool(True),
                                   min_vertex_track_weight = cms.double(0.5),
                                   histos = cms.untracked.bool(False),
                                   verbose = cms.untracked.bool(False),
                                   )
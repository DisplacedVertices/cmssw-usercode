import FWCore.ParameterSet.Config as cms

mfvVerticesAuxTmp = cms.EDProducer('MFVVertexAuxProducer',
                                   beamspot_src = cms.InputTag('offlineBeamSpot'),
                                   primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                   muons_src = cms.InputTag('selectedPatMuonsPF'),
                                   electrons_src = cms.InputTag('selectedPatElectronsPF'),
                                   gen_vertices_src = cms.InputTag('mfvGenVertices'),
                                   vertex_src = cms.InputTag('mfvVertices'),
                                   sv_to_jets_src = cms.string('dummy'),
                                   sort_by = cms.string('ntracks_then_mass'),
                                   )

mfvVerticesAux = mfvVerticesAuxTmp.clone(sv_to_jets_src = 'mfvVerticesToJets')

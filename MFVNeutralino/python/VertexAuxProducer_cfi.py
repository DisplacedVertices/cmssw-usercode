import FWCore.ParameterSet.Config as cms

mfvVerticesAuxTmp = cms.EDProducer('MFVVertexAuxProducer',
                                   primary_vertex_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                   gen_vertices_src = cms.InputTag('mfvGenVertices'),
                                   vertex_src = cms.InputTag('mfvVertices'),
                                   sv_to_jets_src = cms.string('dummy'),
                                   sort_by = cms.string('ntracks'),
                                   )

mfvVerticesAux = mfvVerticesAuxTmp.clone(sv_to_jets_src = 'mfvVerticesToJets')

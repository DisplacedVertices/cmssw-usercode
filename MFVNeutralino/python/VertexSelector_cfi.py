import FWCore.ParameterSet.Config as cms

mfvSelectedVertices = cms.EDProducer('MFVVertexSelector',
                                     vertex_src = cms.InputTag('mfvVertices'),
                                     gen_vertices_src = cms.InputTag('mfvGenVertices'),
                                     track_vertex_weight_min = cms.double(0.5),
                                     min_ntracks = cms.int32(0),
                                     max_chi2dof = cms.double(1e6),
                                     max_err2d   = cms.double(1e6),
                                     max_err3d   = cms.double(1e6),
                                     min_mass    = cms.double(0),
                                     min_drmax   = cms.double(0),
                                     min_gen3dsig = cms.double(0),
                                     max_gen3dsig = cms.double(1e6),
                                     )

import FWCore.ParameterSet.Config as cms

mfvSelectedVertices = cms.EDProducer('MFVVertexSelector',
                                     vertex_aux_src = cms.InputTag('mfvVerticesAuxTmp'),
                                     produce_refs = cms.bool(True),
                                     min_ntracks = cms.int32(0),
                                     max_chi2dof = cms.double(1e9),
                                     max_err2d   = cms.double(1e9),
                                     max_err3d   = cms.double(1e9),
                                     min_mass    = cms.double(0),
                                     min_drmin   = cms.double(0),
                                     max_drmin   = cms.double(1e9),
                                     min_drmax   = cms.double(0),
                                     max_drmax   = cms.double(1e9),
                                     min_gen3dsig = cms.double(0),
                                     max_gen3dsig = cms.double(1e6),
                                     min_maxtrackpt = cms.double(0),
                                     max_bs2derr = cms.double(1e9),
                                     min_njetssharetks = cms.int32(0),
                                     sort_by = cms.string('ntracks'),
                                     )

mfvSelectedVerticesTight = mfvSelectedVertices.clone(
    min_ntracks = 7,
    min_maxtrackpt = 15,
    max_drmin = 0.4,
    max_drmax = 4,
    max_bs2derr = 0.005,
    sort_by = 'ntracks'
    )

import FWCore.ParameterSet.Config as cms

mfvSelectedVertices = cms.EDProducer('MFVVertexSelector',
                                     vertex_src = cms.InputTag('mfvVertices'),
                                     vertex_aux_src = cms.InputTag('mfvVerticesAux'),
                                     produce_vertices = cms.bool(False),
                                     produce_refs = cms.bool(False),
                                     min_ntracks          = cms.int32(0),
                                     min_ntracksptgt3     = cms.int32(0),
                                     min_ntracksptgt5     = cms.int32(0),
                                     min_ntracksptgt10    = cms.int32(0),
                                     min_njetssharetks    = cms.int32(0),
                                     max_njetssharetks    = cms.int32(1000000),
                                     min_jetsmassntks     = cms.double(0),
                                     max_chi2dof          = cms.double(1e9),
                                     min_p                = cms.double(0),
                                     min_pt               = cms.double(0),
                                     max_abs_eta          = cms.double(1e9),
                                     max_abs_rapidity     = cms.double(1e9),
                                     min_mass             = cms.double(0),
                                     min_costhmombs       = cms.double(-1),
                                     min_sumpt2           = cms.double(0),
                                     min_maxtrackpt       = cms.double(0),
                                     min_maxm1trackpt     = cms.double(0),
                                     min_maxm2trackpt     = cms.double(0),
                                     min_drmin            = cms.double(0),
                                     max_drmin            = cms.double(1e9),
                                     min_drmax            = cms.double(0),
                                     max_drmax            = cms.double(1e9),
                                     max_err2d            = cms.double(1e9),
                                     max_err3d            = cms.double(1e9),
                                     min_gen3dsig         = cms.double(0),
                                     max_gen3dsig         = cms.double(1e6),
                                     min_bs2ddist         = cms.double(0),
                                     max_bs2derr          = cms.double(1e9),
                                     min_bs2dsig          = cms.double(0),
                                     min_bs3ddist         = cms.double(0),
                                     sort_by = cms.string('ntracks_then_mass'),
                                     )

mfvSelectedVerticesLoose = mfvSelectedVertices.clone(
    min_ntracks = 5
    )

mfvSelectedVerticesMedium = mfvSelectedVertices.clone(
    min_ntracks = 5,
    max_drmin = 0.4,
    max_drmax = 4,
    max_bs2derr = 0.005,
)

mfvSelectedVerticesTight = mfvSelectedVertices.clone(
    min_ntracks = 7,
    min_maxtrackpt = 15,
    max_drmin = 0.4,
    max_drmax = 4,
    max_bs2derr = 0.005,
    )

mfvSelectedVerticesSeq = cms.Sequence(mfvSelectedVerticesLoose + mfvSelectedVerticesTight)

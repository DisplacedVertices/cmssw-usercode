import FWCore.ParameterSet.Config as cms

from DVCode.MFVNeutralino.Vertexer_cfi import kvr_params

mfvVertexRefits = cms.EDProducer('MFVVertexRefitter',
                                 kvr_params = kvr_params,
                                 beamspot_src = cms.InputTag('offlineBeamSpot'),
                                 vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                 n_tracks_to_drop = cms.uint32(1),
                                 sort_tracks_by = cms.string('dxyerr'),
                                 histos = cms.untracked.bool(False),
                                 verbose = cms.untracked.bool(False),
                                 )



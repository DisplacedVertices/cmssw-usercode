import FWCore.ParameterSet.Config as cms

TrackerMapper = cms.EDAnalyzer('TrackerMapper',
                               track_src = cms.InputTag('generalTracks'),
                               beamspot_src = cms.InputTag('offlineBeamSpot'),
                               primary_vertex_src = cms.InputTag('offlinePrimaryVertices'),
                               use_duplicateMerge = cms.int32(-1),
                               pileup_weights = cms.vdouble(*([1]*100)),
                               )

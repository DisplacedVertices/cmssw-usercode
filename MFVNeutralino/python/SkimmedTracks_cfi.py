import FWCore.ParameterSet.Config as cms

mfvSkimmedTracks = cms.EDFilter('MFVSkimmedTracks',
                                min_pt = cms.double(1),
                                min_nsigmadxybs = cms.double(4),
                                tracks_src = cms.InputTag('generalTracks'),
                                primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                cut = cms.bool(False),
                                )

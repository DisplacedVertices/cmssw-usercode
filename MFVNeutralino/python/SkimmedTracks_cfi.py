import FWCore.ParameterSet.Config as cms

mfvSkimmedTracks = cms.EDFilter('MFVSkimmedTracks',
                                min_pt = cms.double(1),
                                min_dxybs = cms.double(0),
                                min_nsigmadxybs = cms.double(4),
                                tracks_src = cms.InputTag('generalTracks'),
                                primary_vertices_src = cms.InputTag('goodOfflinePrimaryVertices'),
                                packed_candidates_src = cms.InputTag('packedPFCandidates'),
                                input_is_miniaod = cms.bool(False),
                                cut = cms.bool(False),
                                )

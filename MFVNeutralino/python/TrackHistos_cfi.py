import FWCore.ParameterSet.Config as cms

mfvTrackHistos = cms.EDAnalyzer('MFVTrackHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                track_src = cms.InputTag('jmtRescaledTracks'),
                                max_ntrack = cms.int32(50),
                               )

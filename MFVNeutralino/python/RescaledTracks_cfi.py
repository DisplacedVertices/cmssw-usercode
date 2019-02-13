import FWCore.ParameterSet.Config as cms

mfvRescaledTracks = cms.EDProducer('MFVRescaledTracks',
                                   tracks_src = cms.InputTag('generalTracks'),
                                   enable = cms.bool(False),
                                   )

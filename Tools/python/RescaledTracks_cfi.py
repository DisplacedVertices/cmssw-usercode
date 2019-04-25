import FWCore.ParameterSet.Config as cms

jmtRescaledTracks = cms.EDProducer('JMTRescaledTracks',
                                   tracks_src = cms.InputTag('generalTracks'),
                                   enable = cms.bool(False),
                                   pick = cms.bool(False),
                                   which = cms.int32(0),
                                   )

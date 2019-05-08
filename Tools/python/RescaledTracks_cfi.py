import FWCore.ParameterSet.Config as cms

jmtRescaledTracks = cms.EDProducer('JMTRescaledTracks',
                                   tracks_src = cms.InputTag('generalTracks'),
                                   which = cms.int32(-1), # -1 = disable, 0 = JetHT rescaling
                                   )

import FWCore.ParameterSet.Config as cms

jmtRescaledTracks = cms.EDProducer('JMTRescaledTracks',
                                   tracks_src = cms.InputTag('generalTracks'),
                                   muons_src = cms.InputTag('jmtUnpackedCandidateTracks', 'muons'),
                                   electrons_src = cms.InputTag('jmtUnpackedCandidateTracks', 'electrons'),
                                   add_separated_leptons = cms.bool(True),
                                   which = cms.int32(-1), # -1 = disable, 0 = JetHT rescaling
                                   )

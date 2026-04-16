import FWCore.ParameterSet.Config as cms

jmtRescaledTracks = cms.EDProducer('JMTRescaledTracks',
                                   tracks_src = cms.InputTag('generalTracks'),
                                   #muons_src = cms.InputTag('jmtUnpackedCandidateTracks', 'medmu'),
                                   #electrons_src = cms.InputTag('jmtUnpackedCandidateTracks', 'tightele'),
                                   muons_src = cms.InputTag('jmtUnpackedCandidateTracks', 'muons'),
                                   electrons_src = cms.InputTag('jmtUnpackedCandidateTracks', 'electrons'),
                                   add_separated_leptons = cms.bool(False), # Turning this off in this fork, but Abby uses this extensively
                                   which = cms.int32(-1), # -1 = disable, 0 = BTagDisplJet rescaling, 1 = Lepton rescaling, 2 = JetHT rescaling
                                   )

import FWCore.ParameterSet.Config as cms

mfvUnpackedCandidateTracks = cms.EDProducer('MFVUnpackedCandidateTracks',
                                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                                            add_lost_candidates = cms.bool(False),
                                            lost_candidates_src = cms.InputTag('lostTracks'),
                                            skip_weirdos = cms.bool(False),
                                            debug = cms.untracked.bool(False),
                                            )

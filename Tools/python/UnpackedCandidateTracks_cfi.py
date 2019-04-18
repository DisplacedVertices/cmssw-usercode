import FWCore.ParameterSet.Config as cms

jmtUnpackedCandidateTracks = cms.EDProducer('JMTUnpackedCandidateTracks',
                                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                                            add_lost_candidates = cms.bool(False),
                                            lost_candidates_src = cms.InputTag('lostTracks'),
                                            cut_level = cms.int32(-1),
                                            skip_weirdos = cms.bool(False),
                                            debug = cms.untracked.bool(False),
                                            )

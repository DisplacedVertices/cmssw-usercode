import FWCore.ParameterSet.Config as cms

mfvUnpackedCandidateTracks = cms.EDProducer('MFVUnpackedCandidateTracks',
                                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                                            debug = cms.untracked.bool(False),
                                            )

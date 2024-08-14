import FWCore.ParameterSet.Config as cms

jmtUnpackedCandidateTracks = cms.EDProducer('JMTUnpackedCandidateTracks',
                                            packed_candidates_src = cms.InputTag('packedPFCandidates'),
                                            electrons_src = cms.InputTag('slimmedElectrons'),
                                            muons_src = cms.InputTag('slimmedMuons'),
                                            separate_leptons = cms.bool(True),
                                            add_lost_candidates = cms.bool(False),
                                            lost_candidates_src = cms.InputTag('lostTracks'),
                                            cut_level = cms.int32(-1),
                                            lep_pt_cutoff = cms.double(20), #min pt required to separate soft from hard leptons
                                            skip_weirdos = cms.bool(False),
                                            debug = cms.untracked.bool(False),
                                            )
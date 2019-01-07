import FWCore.ParameterSet.Config as cms

mfvJetTrackRefGetter = cms.PSet(
    input_is_miniaod = cms.bool(False),
    unpacked_tracks_src = cms.InputTag('mfvUnpackedCandidateTracks'),
    unpacking_map_src = cms.InputTag('mfvUnpackedCandidateTracks'),
    jtrg_verbose = cms.untracked.bool(False),
    )

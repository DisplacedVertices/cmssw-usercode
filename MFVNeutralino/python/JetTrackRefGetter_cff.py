import FWCore.ParameterSet.Config as cms

mfvJetTrackRefGetter = cms.PSet(
    input_is_miniaod = cms.bool(False),
    unpacked_candidate_tracks_map_src = cms.InputTag('mfvUnpackedCandidateTracks'),
    tracks_maps_srcs = cms.VInputTag(cms.InputTag('mfvRescaledTracks')),
    verbose = cms.untracked.bool(False),
    )

import FWCore.ParameterSet.Config as cms

jmtTrackRefGetter = cms.PSet(
    input_is_miniaod = cms.bool(False),
    unpacked_candidate_tracks_map_src = cms.InputTag('jmtUnpackedCandidateTracks'),
    tracks_maps_srcs = cms.VInputTag(cms.InputTag('jmtRescaledTracks')),
    verbose = cms.untracked.bool(False),
    )

jmtTrackRefGetterMiniAOD = jmtTrackRefGetter.clone(input_is_miniaod = True)

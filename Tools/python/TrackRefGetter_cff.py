import FWCore.ParameterSet.Config as cms

jmtTrackRefGetter = cms.PSet(
    input_is_miniaod = cms.bool(False),
    unpacked_candidate_tracks_map_src = cms.InputTag('jmtUnpackedCandidateTracks'),
    unpacked_candidate_mutracks_map_src = cms.InputTag('jmtUnpackedCandidateTracks', 'mumap'),
    unpacked_candidate_eletracks_map_src = cms.InputTag('jmtUnpackedCandidateTracks', 'elemap'),
    #here add in the rest of the tracks maps : muons, electrons [TODO]
    tracks_maps_srcs = cms.VInputTag(cms.InputTag('jmtRescaledTracks')),
    mutracks_maps_srcs = cms.VInputTag(cms.InputTag('jmtRescaledTracks', 'muons')),
    eletracks_maps_srcs = cms.VInputTag(cms.InputTag('jmtRescaledTracks', 'electrons')),
    verbose = cms.untracked.bool(False),
    )

jmtTrackRefGetterMiniAOD = jmtTrackRefGetter.clone(input_is_miniaod = True)

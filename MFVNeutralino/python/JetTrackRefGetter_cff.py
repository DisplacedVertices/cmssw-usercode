import FWCore.ParameterSet.Config as cms

# JMTBAD don't append pset but pass pset

mfvJetTrackRefGetter = cms.PSet(
    input_is_miniaod = cms.bool(False),
    unpacked_candidate_tracks_map_src = cms.InputTag('mfvUnpackedCandidateTracks'),
    jtrg_verbose = cms.untracked.bool(False),
    )

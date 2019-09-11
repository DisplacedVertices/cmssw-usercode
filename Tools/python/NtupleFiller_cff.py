import FWCore.ParameterSet.Config as cms

from JMTucker.Tools.TrackRefGetter_cff import *

jmtNtupleFiller = cms.PSet(
    input_is_miniaod = cms.bool(False),
    gen_particles_src = cms.InputTag('genParticles'),
    gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
    mci_src = cms.InputTag('mfvGenParticles'),
    weight_src = cms.InputTag('jmtWeight'),
    pileup_info_src = cms.InputTag('addPileupInfo'),
    rho_src = cms.InputTag('fixedGridRhoFastjetAll'),
    mets_src = cms.InputTag('patMETsNoHF'),
    beamspot_src = cms.InputTag('offlineBeamSpot'),
    primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
    tracks_src = cms.InputTag('generalTracks'),
    jets_src = cms.InputTag('selectedPatJets'),
    packed_candidates_src = cms.InputTag('packedPFCandidates'),
    track_ref_getter = jmtTrackRefGetter,
    )

jmtNtupleFillerMiniAOD = jmtNtupleFiller.clone(
    input_is_miniaod = True,
    gen_particles_src = 'prunedGenParticles',
    weight_src = 'jmtWeightMiniAOD',
    pileup_info_src = 'slimmedAddPileupInfo',
    mets_src = cms.InputTag('slimmedMETs'),
    primary_vertices_src = 'offlineSlimmedPrimaryVertices',
    tracks_src = 'jmtUnpackedCandidateTracks',
    track_ref_getter = jmtTrackRefGetterMiniAOD,
    )

def jmtNtupleFiller_pset(miniaod):
    return jmtNtupleFillerMiniAOD if miniaod else jmtNtupleFiller

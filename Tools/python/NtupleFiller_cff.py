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
    triggerfloats_src = cms.InputTag(''),
    beamspot_src = cms.InputTag('offlineBeamSpot'),
    primary_vertices_src = cms.InputTag('offlinePrimaryVertices'),
    tracks_src = cms.InputTag('generalTracks'),
    jets_src = cms.InputTag('selectedPatJets'),
    muons_src = cms.InputTag('selectedPatMuons'),
    electrons_src = cms.InputTag('selectedPatElectrons'),
    electron_effective_areas = cms.FileInPath('RecoEgamma/ElectronIdentification/data/Fall17/effAreaElectrons_cone03_pfNeuHadronsAndPhotons_92X.txt'),
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
    muon_tracks_src = cms.InputTag('jmtUnpackedCandidateTracks', 'muons'),
    electron_tracks_src = cms.InputTag('jmtUnpackedCandidateTracks', 'electrons'),
    track_ref_getter = jmtTrackRefGetterMiniAOD,
    )

def jmtNtupleFiller_pset(miniaod, using_rescaled_tracks=False, corrected_met=True):
    p = jmtNtupleFillerMiniAOD if miniaod else jmtNtupleFiller
    if using_rescaled_tracks: # not necessarily rescaling them, but that they are in the workflow and track_ref_getter will hit them
        p.tracks_src = 'jmtRescaledTracks'
    if corrected_met:
        p.triggerfloats_src = 'mfvTriggerFloats'
        p.mets_src = cms.InputTag('slimmedMETs', '', 'Ntuple')
    return p

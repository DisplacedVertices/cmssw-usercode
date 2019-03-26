import FWCore.ParameterSet.Config as cms

mfvNtupleFiller = cms.PSet(
    gen_particles_src = cms.InputTag('genParticles'),
    gen_vertex_src = cms.InputTag('mfvGenParticles', 'genVertex'),
    mci_src = cms.InputTag('mfvGenParticles'),
)

mfvNtupleFillerMiniAOD = mfvNtupleFiller.clone(
    gen_particles_src = 'prunedGenParticles',
)

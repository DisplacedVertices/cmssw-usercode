import FWCore.ParameterSet.Config as cms

mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                 gen_particles_src = cms.InputTag('genParticles'),
                                 beamspot_src = cms.InputTag('offlineBeamSpot'),
                                 debug = cms.untracked.bool(False),
                                 )

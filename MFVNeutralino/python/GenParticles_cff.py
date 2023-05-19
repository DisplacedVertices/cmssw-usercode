import FWCore.ParameterSet.Config as cms

mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                 gen_particles_src = cms.InputTag('prunedGenParticles'),
                                 beamspot_src = cms.InputTag('offlineBeamSpot'),
                                 last_flag_check = cms.bool(False), # needs to be false now that we're using MiniAOD
                                 debug = cms.untracked.bool(True),
                                 histos = cms.untracked.bool(True),
                                 lsp_id = cms.untracked.int32(-1)
                                 )

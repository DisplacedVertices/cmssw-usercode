import FWCore.ParameterSet.Config as cms

mfvGenParticleFilter = cms.EDFilter('MFVGenParticleFilter',
                                    gen_src = cms.InputTag('genParticles'),
                                    cut_invalid = cms.bool(True),
                                    min_rho0 = cms.double(-1),
                                    max_rho0 = cms.double(-1),
                                    min_rho1 = cms.double(-1),
                                    max_rho1 = cms.double(-1),
                                    )

                                    

import FWCore.ParameterSet.Config as cms

mfvGenParticleFilter = cms.EDFilter('MFVGenParticleFilter',
                                    gen_src = cms.InputTag('genParticles'),
                                    print_info = cms.bool(False),
                                    cut_invalid = cms.bool(True),
                                    required_num_leptonic = cms.int32(-1),
                                    allowed_decay_types = cms.vint32(),
                                    min_lepton_pt = cms.double(0),
                                    max_lepton_eta = cms.double(1e99),
                                    min_rho0 = cms.double(-1),
                                    max_rho0 = cms.double(-1),
                                    min_rho1 = cms.double(-1),
                                    max_rho1 = cms.double(-1),
                                    )

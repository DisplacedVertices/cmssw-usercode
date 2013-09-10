import FWCore.ParameterSet.Config as cms

mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                 gen_src = cms.InputTag('genParticles'),
                                 print_info = cms.bool(False),
                                 )

mfvGenVertices = cms.EDProducer('MFVGenVertices',
                                gen_src = cms.InputTag('genParticles'),
                                is_mfv = cms.bool(True),
                                is_ttbar = cms.bool(False)
                                )

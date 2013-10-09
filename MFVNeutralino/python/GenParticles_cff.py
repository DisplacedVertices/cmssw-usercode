import FWCore.ParameterSet.Config as cms

mfvGenParticles = cms.EDProducer('MFVGenParticles',
                                 gen_src = cms.InputTag('genParticles'),
                                 print_info = cms.bool(False),
                                 )

mfvGenVertices = cms.EDProducer('MFVGenVertices',
                                gen_src = cms.InputTag('genParticles'),
                                debug = cms.untracked.bool(False),
                                )

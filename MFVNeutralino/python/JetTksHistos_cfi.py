import FWCore.ParameterSet.Config as cms

mfvJetTksHistos = cms.EDAnalyzer('MFVJetTksHistos',
                                gen_src = cms.InputTag('prunedGenParticles'),
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                )

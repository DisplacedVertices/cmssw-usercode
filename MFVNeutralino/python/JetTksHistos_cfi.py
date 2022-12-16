import FWCore.ParameterSet.Config as cms

mfvJetTksHistos = cms.EDAnalyzer('MFVJetTksHistos',
                                gen_src     = cms.InputTag('prunedGenParticles'),
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src  = cms.InputTag('mfvEvent'),
                                weight_src  = cms.InputTag('mfvWeight'),
                                offline_csv = cms.double(0.001) # "No" CSV
                                #offline_csv = cms.double(0.58) # Loose CSV
                                #offline_csv = cms.double(0.88) # Medium CSV
                                #offline_csv = cms.double(0.97) # Tight CSV
                                )
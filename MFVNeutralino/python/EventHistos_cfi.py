import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                gen_src = cms.InputTag('prunedGenParticles'),
                                weight_src = cms.InputTag('mfvWeight'),
                                temp_caloht_cut = cms.double(-0.1),
                                require_two_good_leptons = cms.bool(False),
                                )

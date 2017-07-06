import FWCore.ParameterSet.Config as cms

mfvJetEnergyHistos = cms.EDAnalyzer('MFVJetEnergyHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                force_bs = cms.vdouble(),
                                jes = cms.bool(False),
                                )

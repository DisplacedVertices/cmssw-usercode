import FWCore.ParameterSet.Config as cms

mfvFilterHistos = cms.EDAnalyzer('MFVFilterHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                )

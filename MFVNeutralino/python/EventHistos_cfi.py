import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                weight_src = cms.InputTag('mfvWeight'),
                                )

import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                vertex_src = cms.InputTag('mfvSelectedVerticesLoose'),
                                max_ntrackplots = cms.int32(-1),
                                do_scatterplots = cms.bool(False),
                                )

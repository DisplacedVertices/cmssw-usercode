import FWCore.ParameterSet.Config as cms

mfvVertexHistos = cms.EDAnalyzer('MFVVertexHistos',
                                 mevent_src = cms.InputTag('mfvEvent'),
                                 weight_src = cms.InputTag('mfvWeight'),
                                 vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                 max_ntrackplots = cms.int32(-1),
                                 do_scatterplots = cms.bool(False),
                                 )

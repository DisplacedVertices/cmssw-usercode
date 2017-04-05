import FWCore.ParameterSet.Config as cms

mfvVertexHistos = cms.EDAnalyzer('MFVVertexHistos',
                                 mevent_src = cms.InputTag('mfvEvent'),
                                 weight_src = cms.InputTag('mfvWeight'),
                                 vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                 force_bs = cms.vdouble(),
                                 do_trackplots = cms.bool(True),
                                 do_scatterplots = cms.bool(False),
                                 )

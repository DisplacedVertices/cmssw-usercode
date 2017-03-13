import FWCore.ParameterSet.Config as cms

mfvVertexHistos = cms.EDAnalyzer('MFVVertexHistos',
                                 mevent_src = cms.InputTag('mfvEvent'),
                                 weight_src = cms.InputTag('mfvWeight'),
                                 vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                 force_bs = cms.vdouble(),
                                 reco_vertex_src = cms.InputTag(''),
                                 vertex_to_jets_src = cms.InputTag(''),
                                 do_trackplots = cms.bool(True),
                                 do_scatterplots = cms.bool(False),
                                 do_only_1v = cms.bool(False),
                                 )

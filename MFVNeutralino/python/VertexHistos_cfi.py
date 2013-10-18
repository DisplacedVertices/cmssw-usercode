import FWCore.ParameterSet.Config as cms

mfvVertexHistos = cms.EDAnalyzer('MFVVertexHistos',
                                 mfv_event_src = cms.InputTag('mfvEvent'),
                                 vertex_aux_src = cms.InputTag('mfvSelectedVerticesTight'),
                                 weight_src = cms.InputTag('mfvWeight'),
                                 use_ref = cms.bool(True),
                                 do_scatterplots = cms.bool(False),
                                 )

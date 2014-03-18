import FWCore.ParameterSet.Config as cms

mfvVertexHistos = cms.EDAnalyzer('MFVVertexHistos',
                                 mfv_event_src = cms.InputTag('mfvEvent'),
                                 vertex_aux_src = cms.InputTag('mfvSelectedVerticesTight'),
                                 vertex_src = cms.InputTag(''),
                                 vertex_to_jets_src = cms.InputTag(''),
                                 weight_src = cms.InputTag('mfvWeight'),
                                 do_scatterplots = cms.bool(False),
                                 )

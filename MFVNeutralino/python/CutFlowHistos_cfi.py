import FWCore.ParameterSet.Config as cms

mfvCutFlowHistos = cms.EDAnalyzer('MFVCutFlowHistos',
                                  mevent_src = cms.InputTag('mfvEvent'),
                                  weight_src = cms.InputTag('mfvWeight'),
                                  vertex_aux_src = cms.InputTag('mfvVerticesAux'),
                                  )

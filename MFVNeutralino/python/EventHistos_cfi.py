import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                force_bs = cms.vdouble(),
                                primary_vertex_src = cms.InputTag(''),
                                jets_src = cms.InputTag(''),
                                )

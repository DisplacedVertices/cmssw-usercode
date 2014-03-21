import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                mfv_event_src = cms.InputTag('mfvEvent'),
                                primary_vertex_src = cms.InputTag(''),
                                jets_src = cms.InputTag(''),
                                weight_src = cms.InputTag('mfvWeight'),
                                re_trigger = cms.bool(False),
                                )

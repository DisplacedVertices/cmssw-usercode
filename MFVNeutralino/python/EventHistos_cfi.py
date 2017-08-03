import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
				triggerSel = cms.vint32(), #SH
                                force_bs = cms.vdouble(),
                                )

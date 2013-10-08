import FWCore.ParameterSet.Config as cms

mfvEventHistos = cms.EDAnalyzer('MFVEventHistos',
                                 mfv_event_src = cms.InputTag('mfvEvent'),
                                 )

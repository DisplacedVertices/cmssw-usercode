import FWCore.ParameterSet.Config as cms

mfvFilterHistos = cms.EDAnalyzer('MFVFilterHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                require_L1          = cms.int32(0),
                                min_filtjets        = cms.int32(4),
                                min_filtjetpt       = cms.double(25.),
                                max_filtjeteta      = cms.double(2.4),
                                min_filtjetbscore   = cms.double(0.0),
                                min_pt_for_deta     = cms.double(100.),
                                min_pt_for_bfilter  = cms.double(70.),
                                )

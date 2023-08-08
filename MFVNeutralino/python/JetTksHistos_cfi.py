import FWCore.ParameterSet.Config as cms

mfvJetTksHistos = cms.EDAnalyzer('MFVJetTksHistos',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src  = cms.InputTag('mfvEvent'),
                                weight_src  = cms.InputTag('mfvWeight'),
                                offline_csv = cms.double(1e-7), # "No" CSV
                                calojet_category = cms.int32(0),
                                pt_thresh_shift = cms.double(0.0),
                                tk_match_shift  = cms.double(0.0),
                                soft_tk_thresh  = cms.double(999),
                                plot_soft_tks = cms.bool(False),
                                plot_hard_tks = cms.bool(False),
                                trigger_bit = cms.int32(0),
                                require_triggers = cms.bool(False),
                                veto_bjet_events = cms.bool(False),
                                require_tk_quality = cms.bool(True),
                                require_gen_sumdbv = cms.bool(False),
                                do_tk_filt_refactor = cms.bool(False),
                                )

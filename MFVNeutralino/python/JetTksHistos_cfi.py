import FWCore.ParameterSet.Config as cms

mfvJetTksHistos = cms.EDAnalyzer('MFVJetTksHistos',
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                mevent_src  = cms.InputTag('mfvEvent'),
                                weight_src  = cms.InputTag('mfvWeight'),
                                offline_csv = cms.double(1e-7), # "No" CSV
                                calojet_category = cms.int32(0),
                                pt_thresh_shift = cms.double(0.0),
                                pt_lo_for_tag_probe = cms.double(30.0),
                                pt_hi_for_tag_probe = cms.double(999.0),
                                tk_match_shift  = cms.double(0.0),
                                soft_tk_thresh  = cms.double(999),
                                plot_soft_tks = cms.bool(False),
                                plot_hard_tks = cms.bool(False),
                                trigger_bit = cms.int32(0),
                                require_triggers = cms.bool(False),
                                veto_bjet_events = cms.bool(False),
                                require_tk_quality = cms.bool(False),
                                #require_tk_quality = cms.bool(True), //FIXME
                                require_gen_sumdbv = cms.bool(False),
                                require_two_good_leptons = cms.bool(False),
                                do_tk_filt_refactor = cms.bool(False),
                                get_hlt_btag_factors_pf   = cms.bool(False),
                                get_hlt_btag_factors_calo = cms.bool(False),
                                get_hlt_btag_factors_calo_low = cms.bool(False),
                                force_hlt_btag_study = cms.bool(False), # essentially, sets all of the "get_hlt_btag..." flags to true to avoid bugs when applying the hlt btag SFs
                                require_match_to_hlt = cms.bool(False),
                                require_early_b_filt = cms.bool(False),
                                apply_hlt_btagging = cms.bool(False),
                                apply_offline_dxy_res = cms.bool(False),
                                )

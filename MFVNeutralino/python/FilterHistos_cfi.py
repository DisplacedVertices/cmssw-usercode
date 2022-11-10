import FWCore.ParameterSet.Config as cms

mfvFilterHistos = cms.EDAnalyzer('MFVFilterHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                ul_year    = cms.int32(2018),
                                is_dibjet           = cms.bool(False),


                                # UL doesn't seem to have CSV scores, so we should remove/change these four
                                #offline_csv = cms.double(0.01), # "No"   CSV
                                #offline_csv = cms.double(0.58), # Loose  CSV
                                #offline_csv = cms.double(0.88), # Medium CSV
                                #offline_csv = cms.double(0.97), # Tight  CSV

                                #offline_csv = cms.double(0.0001), # "No"   DeepCSV
                                #offline_csv = cms.double(0.1355), # Loose  DeepCSV
                                #offline_csv = cms.double(0.4506), # Medium DeepCSV
                                offline_csv = cms.double(0.7738), # Tight  DeepCSV


                                #offline_csv = cms.double(0.0001), # "No"   DeepFlav
                                #offline_csv = cms.double(0.0490), # Loose   DeepFlav
                                #offline_csv = cms.double(0.2783), # Medium  DeepFlav
                                #offline_csv = cms.double(0.7100), # Tight   DeepFlav

                                skew_dR_cut = cms.double(1.6),
                                btag_pt_cut = cms.double(0.0),

                                # Parameters used iff is_dibjet = True
                                di_bitL1             = cms.int32(20),
                                di_minfiltjets       = cms.int32(2),
                                di_minfiltjetpt      = cms.double(60.),
                                di_maxfiltjeteta     = cms.double(2.3),
                                di_minfiltjetbdisc   = cms.double(0.0),

                                # Parameters used iff is_dibjet = False
                                tri_bitL1            = cms.int32(18),
                                tri_minfiltjets      = cms.int32(4),
                                tri_minfiltjetpt     = cms.double(25.),
                                tri_maxfiltjeteta    = cms.double(2.4),
                                tri_minfiltjetbdisc  = cms.double(0.0),

                                # Parameters used in either case. Mostly useful for di-bjet, though
                                min_pt_for_deta     = cms.double(100.),
                                min_pt_for_bfilter  = cms.double(70.),
                                )

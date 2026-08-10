import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.Year import year

mfvFilterHistos = cms.EDAnalyzer('MFVFilterHistos',
                                mevent_src = cms.InputTag('mfvEvent'),
                                weight_src = cms.InputTag('mfvWeight'),
                                vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                track_src = cms.InputTag('jmtRescaledTracks'),
                                is_dibjet  = cms.bool(False),
                                skew_dR_cut = cms.double(1.6),
                                btag_pt_cut = cms.double(0.0),
                                require_two_good_leptons = cms.bool(False),
                                require_exact_ncalojets  = cms.bool(False),
                                ncalojet_req             = cms.int32(0), # only used if above bool = True

                                # Parameters used iff is_dibjet = True
                                di_bitL1             = cms.int32(20) if year==2017 else cms.int32(21),
                                di_minfiltjets       = cms.int32(2),
                                di_minfiltjetpt      = cms.double(60.) if year==2017 else cms.double(70.),
                                di_maxfiltjeteta     = cms.double(2.3),
                                di_minfiltjetbdisc   = cms.double(0.0),

                                # Parameters used iff is_dibjet = False
                                tri_bitL1            = cms.int32(18) if year==2017 else cms.int32(19),
                                tri_minfiltjets      = cms.int32(4),
                                tri_minfiltjetpt     = cms.double(25.),
                                tri_maxfiltjeteta    = cms.double(2.4),
                                tri_minfiltjetbdisc  = cms.double(0.0),

                                # Parameters used in either case. Mostly useful for di-bjet, though
                                min_pt_for_deta     = cms.double(100.) if year==2017 else cms.double(112.),
                                min_pt_for_bfilter  = cms.double(70.),

                                # Parameter used to study weird HT behavior
                                nhltcalojet_req = cms.int32(-1),
                                )

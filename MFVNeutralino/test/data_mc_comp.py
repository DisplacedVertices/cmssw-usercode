#!/usr/bin/env python

import os
from functools import partial
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

year = '2018'
version = 'ULV3Lepm_SingleLep'
#root_file_dir = 'afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version
#root_file_dir = '/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackingTreerULV1_Lepm_cut0_etagt1p5_2017_wsellep/'

set_style()
ps = plot_saver(plot_dir('data_mc_comp_%s_%s' % (year, version)))
#ps = plot_saver(plot_dir('data_mc_comp_TrackingTreer_%s' % year))


if year == '2018':
    qcd_samples = Samples.qcd_lep_samples_2018
    ttbar_samples = Samples.met_samples_2018
    #leptonic_samples = Samples.leptonic_samples_2018
    wjet_samples = [Samples.leptonic_samples_2018[0]]
    dyjet_samples = Samples.leptonic_samples_2018[1:]
    diboson_samples = Samples.diboson_samples_2018
    signal_lb = Samples.mfv_stoplb_tau001000um_M1000_2018
    signal_ld = Samples.mfv_stopld_tau001000um_M1000_2018
    data_samples = [] # Samples.data_samples_2017
    background_samples = diboson_samples + ttbar_samples + qcd_samples + dyjet_samples + wjet_samples
    lumi = ac.int_lumi_2018 * ac.scale_factor_2018
    lumi_nice = ac.int_lumi_nice_2018
    
if year == '2017p8':
    qcd_samples = Samples.qcd_samples_2018 + Samples.qcd_samples_2017[1:]
    ttbar_samples = Samples.ttbar_samples_2017
    signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
    data_samples = [] # Samples.data_samples_2017
    background_samples = qcd_samples + ttbar_samples
    lumi = ac.int_lumi_2017p8 * ac.scale_factor_2017p8
    lumi_nice = ac.int_lumi_nice_2017p8

if year == '2017':
    qcd_samples = Samples.qcd_lep_samples_2017
    ttbar_samples = Samples.met_samples_2017
    leptonic_samples = Samples.leptonic_samples_2017
    wjet_sample = [Samples.leptonic_samples_2017[0]]
    dyjet_samples = Samples.leptonic_samples_2017[1:]
    diboson_samples = Samples.diboson_samples_2017
    #data_samples = Samples.auxiliary_data_samples_2017
    data_samples = Samples.Lepton_data_samples_2017
    signal_sample = []
    background_samples = qcd_samples + diboson_samples + ttbar_samples + dyjet_samples + wjet_sample
    #lumi = ac.int_lumi_2017 * ac.scale_factor_2017 * 0.10
    #lumi = ac.int_lumi_2017 * ac.scale_factor_2017 * 0.10
    #lumi_nice = ac.int_lumi_nice_2017

    #unnormalized
    lumi = 1
    lumi_nice = ac.int_lumi_nice_2017

for s in diboson_samples:
    s.join_info = True, 'Diboson', ROOT.kBlue-9
for s in qcd_samples:
    s.join_info = True, 'QCD lept enriched', ROOT.kMagenta+3
for s in ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-3
for s in dyjet_samples:
    s.join_info = True, 'DY+jets', ROOT.kMagenta-3
for s in wjet_samples:
    s.join_info = True, 'W+jets', ROOT.kPink-3

signal_samples = [signal_lb, signal_ld]
signal_lb.nice_name = 'Stoplb: #sigma = 1 fb, c#tau = 1 mm, M = 1000 GeV'
signal_lb.color = 8
signal_ld.nice_name = 'Stopld: #sigma = 1 fb, c#tau = 1 mm, M = 1000 GeV'
signal_ld.color = 6

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = [],
            #signal_samples = [],
            #data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = lumi,
            int_lumi_nice = lumi_nice,
            canvas_top_margin = 0.08,
            poisson_intervals = True,
            legend_pos = (0.48, 0.78, 0.88, 0.88),
            enable_legend = True,
            res_fit = False,
            verbose = False,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = True,
            )


C('tight_electron_track_pt',
  histogram_path = 'mfvEventHistosPreSel/h_electron_pt_tight',
  x_title = 'tight-cutbased electron pt ',
  y_title = 'Events',
  y_range = (1e-1,1e4),
)

C('presel_selele_pt',
  histogram_path = 'mfvEventHistosPreSel/h_selele_pt',
  x_title = 'selected electron pt ',
  y_title = 'Events',
  y_range = (1e-1,1e4),
)

C('presel_tight_ele_dxybs',
  histogram_path = 'mfvEventHistosPreSel/h_electron_absdxybs_tight',
  x_title = 'tight-cutbased electron absdxybs ',
  y_title = 'Events',
  y_range = (1e-1,1e4),
  x_range = (0, 0.4),
)

C('presel_selele_dxybs',
  histogram_path = 'mfvEventHistosPreSel/h_selele_dxybs',
  x_title = 'selected electron dxybs ',
  y_title = 'Events',
  y_range = (1e-1,1e4),
  x_range = (0, 0.4),
)

C('presel_medium_mu_pt',
  histogram_path = 'mfvEventHistosPreSel/h_muon_pt_medium',
  x_title = 'medium-cutbased muon pt ',
  y_title = 'Events'
)

C('presel_selmu_pt',
  histogram_path = 'mfvEventHistosPreSel/h_selmu_pt',
  x_title = 'selected muon pt ',
  y_title = 'Events'
)

C('presel_medium_mu_dxybs',
  histogram_path = 'mfvEventHistosPreSel/h_muon_pt_medium',
  x_title = 'medium-cutbased muon dxybs ',
  y_title = 'Events',
  #rebin = 8,
  y_range = (1e-1,1e4),
  x_range = (0, 0.4),
)

C('presel_selmu_dxybs',
  histogram_path = 'mfvEventHistosPreSel/h_selmu_dxybs',
  x_title = 'selected muon pt ',
  y_title = 'Events',
  #rebin = 8,
  y_range = (1e-1,1e4),
  x_range = (0, 0.4),

)


C('presel_nelectrons',
  histogram_path = 'mfvEventHistosPreSel/h_nelectrons_tight',
  x_title = 'Number of tight-cutbased electrons ',
  y_title = 'Events'
)

C('presel_nselele',
  histogram_path = 'mfvEventHistosPreSel/h_nselele',
  x_title = 'Number selected electrons ',
  y_title = 'Events'
)

C('presel_nmuons',
  histogram_path = 'mfvEventHistosPreSel/h_nmuons',
  x_title = 'Number of medium-cutbased muons ',
  y_title = 'Events'
)

C('presel_nselmu',
  histogram_path = 'mfvEventHistosPreSel/h_nselmu',
  x_title = 'Number of selected muons ',
  y_title = 'Events'
)

C('presel_njets',
  histogram_path = 'mfvEventHistosPreSel/h_njets',
  x_title = 'Number of jets',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_nbjets',
  histogram_path = 'mfvEventHistosPreSel/h_nbtags_2',
  x_title = 'Number of tight bjets',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_bjet_pt',
  histogram_path = 'mfvEventHistosPreSel/h_bjet_pt',
  x_title = 'bjet p_{T} (GeV)',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_bjet_eta',
  histogram_path = 'mfvEventHistosPreSel/h_bjet_eta',
  x_title = 'bjet #eta',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_bjet_phi',
  histogram_path = 'mfvEventHistosPreSel/h_bjet_phi',
  x_title = 'bjet #phi',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

C('presel_ht40',
  histogram_path = 'mfvEventHistosPreSel/h_jet_ht_40',
  #rebin = 4,
  x_title = 'Jet H_{T} (GeV)',
  y_title = 'Events/100 GeV',
  y_range = (1, 1e8),
  )

#C('presel_htall',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_ht',
#  )
#
#C('presel_jetpt1',
#  histogram_path = 'mfvEventHistosPreSel/h_jetpt1',
#  y_range = (1,1e6),
#  )
#
#C('presel_jetpt4',
#  histogram_path = 'mfvEventHistosPreSel/h_jetpt4',
#  y_range = (1,5e6),
#  )
#
#C('presel_jetpt',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_pt',
#  y_range = (1,5e7),
#  )
#
#C('presel_jeteta',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_eta',
#  )
#
#C('presel_jetphi',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_phi',
#  )
#
#C('presel_jetpairdphi',
#  histogram_path = 'mfvEventHistosPreSel/h_jet_pairdphi',
#  )
#
#C('presel_met',
#  histogram_path = 'mfvEventHistosPreSel/h_met',
#  )
#
#C('presel_metphi',
#  histogram_path = 'mfvEventHistosPreSel/h_metphi',
#  )
#
#C('presel_nbtags_tight',
#  histogram_path = 'mfvEventHistosPreSel/h_nbtags_tight',
#  )
#
#C('presel_npv',
#  histogram_path = 'mfvEventHistosPreSel/h_npv',
#  y_range = (1,1e6),
#  )
#
#C('presel_pvntracks',
#  histogram_path = 'mfvEventHistosPreSel/h_pvntracks',
#  )
#
#C('presel_pvscore',
#  histogram_path = 'mfvEventHistosPreSel/h_pvscore',
#  )
#
#C('presel_pvrho',
#  histogram_path = 'mfvEventHistosPreSel/h_pvrho',
#  )
#
#C('presel_nseedtracks',
#  histogram_path = 'mfvEventHistosPreSel/h_n_vertex_seed_tracks',
#  y_range = (1,1e7)
#  )
#
#C('presel_seedtrack_npxlayers',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_npxlayers',
#  y_range = (1,1e8),
#  )
#
#C('presel_seedtrack_nstlayers',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_nstlayers',
#  y_range = (1,1e8),
#  )
#
#C('presel_seedtrack_chi2dof',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_chi2dof',
#  y_range = (1,1e8),
#  )
#
#C('presel_seedtrack_pt',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_pt',
#  y_range = (1,1e8),
#  )
#
#C('presel_seedtrack_eta',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_eta',
#  y_range = (1,6e6),
#  )
#
#C('presel_seedtrack_phi',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_phi',
#  y_range = (1,6e6),
#  )
#
#C('presel_seedtrack_dxy',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_dxy',
#  y_range = (1,1e6),
#  )
#
#C('presel_seedtrack_dz',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_dz',
#  y_range = (1,1e6),
#  )


# C('onevtx_ntracks',
#   histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
#   x_title = 'Number of tracks per vertex',
#   y_title = 'Vertices',
#   y_range = (0.1, 1e6),
#   cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#   )

C('nsv_4track',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 4-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1, 1e8),
  )

C('sv_ntracks_min4tk',
  histogram_path = 'MinNtk4mfvVertexHistosPreSel/h_sv_all_ntracks',
  x_title = 'Number of tracks per min4-track vertices',
  y_title = 'Events',
  )

C('onevtx_bs2derr_ntk4',
  histogram_path = 'MinNtk4vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e6),
  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
  )

C('onevtx_dbv_ntk4',
  histogram_path = 'MinNtk4vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e6),
  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
  )

C('nsv_3track',
  histogram_path = 'MinNtk3mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 3-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1, 1e8),
  )

C('sv_ntracks_min3tk',
  histogram_path = 'MinNtk3mfvVertexHistosPreSel/h_sv_all_ntracks',
  x_title = 'Number of tracks per min3-track vertices',
  y_title = 'Events',
  )

C('onevtx_bs2derr_ntk3',
  histogram_path = 'MinNtk3vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e6),
  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
  )

C('onevtx_dbv_ntk3',
  histogram_path = 'MinNtk3vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e6),
  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
  )


C('nsv_5track',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 5-or-more-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-3, 1e8),
  cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
  )

C('sv_ntracks_min5tk',
  histogram_path = 'mfvVertexHistosPreSel/h_sv_all_ntracks',
  x_title = 'Number of tracks per min5-track vertices',
  y_title = 'Events',
  )

C('onevtx_bs2derr_ntk5',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e6),
  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
  )

C('onevtx_dbv_ntk5',
  histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e6),
  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
  )

# C('dbv',
#   histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#   x_title = 'd_{BV} (cm)',
#   y_title = 'Vertices/50 #mum',
#   x_range = (0, 0.4),
#   y_range = (1, 1e4),
#   )

# C('dvv',
#   histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
#   rebin = 10,
#   x_title = 'd_{VV} (cm)',
#   y_title = 'Events/200 #mum',
#   y_range = (1e-2, 10),
#   )

# C('track_pt',
#   file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
#   histogram_path = 'TrackerMapper/h_all_tracks_pt',
#   x_title = 'Track p_{T} (GeV)',
#   y_title = 'Tracks/0.1 GeV',
#   y_range = (1, 1e10),
#   #cut_line = ((1, 0, 1, 2.8e10), 2, 5, 1),
# )

#if year == '2016':
#    C('track_pt',
#      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
#      histogram_path = 'TrackerMapper/h_nm1_tracks_pt',
#      x_title = 'Track p_{T} (GeV)',
#      y_title = 'Tracks/0.1 GeV',
#      y_range = (1, 1e10),
#      cut_line = ((1, 0, 1, 2.8e10), 2, 5, 1),
#      )
#
#    C('track_min_r',
#      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
#      histogram_path = 'TrackerMapper/h_nm1_tracks_min_r',
#      x_title = 'Minimum layer number',
#      y_title = 'Tracks',
#      y_range = (1, 1e10),
#      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
#      )
#
#    C('track_npxlayers',
#      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
#      histogram_path = 'TrackerMapper/h_nm1_tracks_npxlayers',
#      x_title = 'Number of pixel layers',
#      y_title = 'Tracks',
#      y_range = (1, 1e10),
#      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
#      )
#
#    C('track_nstlayers_etalt2',
#      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
#      histogram_path = 'TrackerMapper/h_nm1_tracks_nstlayers_etalt2',
#      x_title = 'Number of strip layers (|#eta| < 2)',
#      y_title = 'Tracks',
#      y_range = (1, 1e10),
#      cut_line = ((6, 0, 6, 2.8e10), 2, 5, 1),
#      )
#
#    C('track_nstlayers_etagt2',
#      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
#      histogram_path = 'TrackerMapper/h_nm1_tracks_nstlayers_etagt2',
#      x_title = 'Number of strip layers (|#eta| #geq 2)',
#      y_title = 'Tracks',
#      y_range = (1, 1e10),
#      cut_line = ((7, 0, 7, 2.8e10), 2, 5, 1),
#      )
#
#    C('track_nsigmadxy',
#      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
#      histogram_path = 'TrackerMapper/h_nm1_tracks_nsigmadxy',
#      x_title = 'N#sigma(dxy)',
#      y_title = 'Tracks',
#      x_range = (0, 10),
#      y_range = (1, 1e10),
#      cut_line = ((4, 0, 4, 2.8e10), 2, 5, 1),
#      )
#


#C('100pc_3t1v_ntracks',
#  histogram_path = 'Ntk3vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_bs2derr',
#  histogram_path = 'Ntk3vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_dbv',
#  histogram_path = 'Ntk3vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_onevtx_dbv',
#  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_3t1v_onevtx_dbv_unzoom',
#  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_3t2v_dvv',
#  histogram_path = 'Ntk3mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  )
#
#C('100pc_4t1v_ntracks',
#  histogram_path = 'Ntk4vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_bs2derr',
#  histogram_path = 'Ntk4vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_dbv',
#  histogram_path = 'Ntk4vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_onevtx_dbv',
#  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_4t1v_onevtx_dbv_unzoom',
#  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_4t2v_dvv',
#  histogram_path = 'Ntk4mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  res_fit = False,
#  )
#
#C('100pc_5t1v_ntracks',
#  histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_bs2derr',
#  histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_dbv',
#  histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_onevtx_dbv',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_5t1v_onevtx_dbv_unzoom',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_5t2v_dvv',
#  histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  res_fit = False,
#  )

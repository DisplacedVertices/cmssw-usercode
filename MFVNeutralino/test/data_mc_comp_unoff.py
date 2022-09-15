#!/usr/bin/env python

import os
from functools import partial
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

# year = '2017p8'
# version = 'V23m'
# root_file_dir = '/uscms_data/d2/tucker/crab_dirs/Histos%s' % version

year = '2017'
version = 'ULV1Lepm'
root_file_dir = 'afs/hep.wisc.edu/home/acwarden/crabdirs/Histos%s' % version

set_style()
ps = plot_saver(plot_dir('data_mc_comp_%s_%s' % (year, version)))

if year == '2018':
    qcd_samples = Samples.qcd_samples_2018
    ttbar_samples = []
    signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
    data_samples = [] # Samples.data_samples_2017
    background_samples = qcd_samples
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
    wjet_samples = [Samples.leptonic_samples_2017[0]]
    dyjet_samples = Samples.leptonic_samples_2017[1:]
    diboson_samples = Samples.diboson_samples_2017
    data_samples = Samples.Lepton_data_samples_2017
    signal_sample = []
    #background_samples = qcd_samples + ttbar_samples + leptonic_samples + diboson_samples
    background_samples = diboson_samples + ttbar_samples + qcd_samples + dyjet_samples + wjet_samples
    lumi = ac.int_lumi_2017 * ac.scale_factor_2017 * 0.10
    lumi_nice = ac.int_lumi_nice_2017

#kblue-9 -3 magenta-3 +3
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


tracker_sel = ["all", "sel", "seed"]
C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = [],
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = lumi,
            int_lumi_nice = lumi_nice,
            canvas_top_margin = 0.08,
            poisson_intervals = False,
            legend_pos = (0.66, 0.78, 0.96, 0.88),
            enable_legend = True,
            res_fit = False,
            verbose = False,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = False,
            simulation = False,
            )

#C('ntuple_njets',
#  histogram_path = 'evtHst0VNoHt/h_njets',
#  x_title = 'Number of jets',
#  y_title = 'Events',
#  y_range = (1, 1e8),
#  )
#
#C('ntuple_ht40',
#  histogram_path = 'evtHst0VNoHt/h_jet_ht_40',
#  rebin = 4,
#  x_title = 'Jet H_{T} (GeV)',
#  y_title = 'Events/100 GeV',
#  y_range = (1, 1e8),
#  cut_line = ((1200, 0, 1200, 2.5e8), 2, 5, 1),
#  )
#
# C('presel_njets',
#   histogram_path = 'mfvEventHistosPreSel/h_njets',
#   x_title = 'Number of jets',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_nbjets',
#   histogram_path = 'mfvEventHistosPreSel/h_nbtags_2',
#   x_title = 'Number of tight bjets',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_bjet_pt',
#   histogram_path = 'mfvEventHistosPreSel/h_bjet_pt',
#   x_title = 'bjet p_{T} (GeV)',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_bjet_eta',
#   histogram_path = 'mfvEventHistosPreSel/h_bjet_eta',
#   x_title = 'bjet #eta',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_bjet_phi',
#   histogram_path = 'mfvEventHistosPreSel/h_bjet_phi',
#   x_title = 'bjet #phi',
#   y_title = 'Events',
#   y_range = (1, 1e8),
#   )

# C('presel_ht40',
#   histogram_path = 'mfvEventHistosPreSel/h_jet_ht_40',
#   rebin = 4,
#   x_title = 'Jet H_{T} (GeV)',
#   y_title = 'Events/100 GeV',
#   y_range = (1, 1e8),
#   )

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
#C('presel_nmuons_any',
#  histogram_path = 'mfvEventHistosPreSel/h_nmuons_any',
#  )
#
#C('presel_nmuons_selected',
#  histogram_path = 'mfvEventHistosPreSel/h_nmuons_selected',
#  )
#
#C('presel_nelectrons_any',
#  histogram_path = 'mfvEventHistosPreSel/h_nelectrons_any',
#  )
#
#C('presel_nelectrons_selected',
#  histogram_path = 'mfvEventHistosPreSel/h_nelectrons_selected',
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

# C('onevtx_bs2derr',
#   histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#   x_title = 'Uncertainty in d_{BV} (cm)',
#   y_title = 'Vertices/5 #mum',
#   y_range = (1, 1e6),
#   cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#   )

# C('onevtx_dbv',
#   histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#   x_title = 'd_{BV} (cm)',
#   y_title = 'Vertices/50 #mum',
#   x_range = (0, 0.4),
#   y_range = (1, 1e6),
#   cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#   )

# C('nsv_3track',
#   histogram_path = 'Ntk3mfvVertexHistosPreSel/h_nsv',
#   x_title = 'Number of 3-track vertices',
#   y_title = 'Events',
#   x_range = (0, 8),
#   y_range = (1, 1e8),
#   )

# C('nsv_4track',
#   histogram_path = 'Ntk4mfvVertexHistosPreSel/h_nsv',
#   x_title = 'Number of 4-track vertices',
#   y_title = 'Events',
#   x_range = (0, 8),
#   y_range = (1, 1e8),
#   )

# C('nsv_5track',
#   histogram_path = 'mfvVertexHistosPreSel/h_nsv',
#   x_title = 'Number of 5-or-more-track vertices',
#   y_title = 'Events',
#   x_range = (0, 8),
#   y_range = (1e-3, 1e8),
#   cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
#   )

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
for track in tracker_sel : 
    C( track +'_track_pt',
      file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_' + track + '_tracks_pt',
      x_title = track + 'track p_{T} (GeV)',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 1e10),
    )
    C( track +'_track_eta',
      file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_' + track + '_tracks_eta',
      x_title = track + 'track eta',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 6e8),
    )
    C( track +'_track_phi',
      file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_' + track + '_tracks_phi',
      x_title = track + 'track phi',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 4e8),
    )
    C( track +'_track_npxhits',
      file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_' + track + '_tracks_npxhits',
      x_title = track + 'track npxhits',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 3e9),
    )
    C( track +'_track_nsthits',
      file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_' + track + '_tracks_nsthits',
      x_title = track + 'track nsthits',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 2e9),
    )
    C( track +'_track_dxy',
       file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
       histogram_path = 'TrackerMapper/h_' + track + '_tracks_dxy',
       x_title = track + 'track dxy to beamspot',
       y_title = 'Tracks/0.1 GeV',
       y_range = (1, 1e10),
    )
    C( track +'_track_dxyerr',
       file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
       histogram_path = 'TrackerMapper/h_' + track + '_tracks_dxyerr',
       x_title = track + 'track dxyerr',
       y_title = 'Tracks/0.1 GeV',
       y_range = (1, 1e10),
    )
    C( track +'_track_nsigmadxy',
       file_path = os.path.join('/afs/hep.wisc.edu/home/acwarden/crabdirs/TrackerMapperV1UL', '%(name)s.root'),
       histogram_path = 'TrackerMapper/h_' + track + '_tracks_nsigmadxy',
       x_title = track + 'track nsigmadxy',
       y_title = 'Tracks/0.1 GeV',
       y_range = (1, 1e10),
    )

#!/usr/bin/env python

import os
from functools import partial
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver

year = '2016'

root_file_dir = '/uscms_data/d2/tucker/crab_dirs/HistosV12'
plot_dir = 'plots/data_mc_comp/HistosV12_%s' % year

set_style()
ps = plot_saver(plot_dir)

int_lumi = ac.int_lumi_2016 * ac.scale_factor_2016
int_lumi_nice = ac.int_lumi_nice_2016
qcd_samples = Samples.qcd_samples_sum
ttbar_samples = Samples.ttbar_samples
signal_sample = Samples.official_mfv_neu_tau01000um_M0800
data_samples = Samples.data_samples

if year == '2015':
    int_lumi = ac.int_lumi_2015 * ac.scale_factor_2015
    int_lumi_nice = ac.int_lumi_nice_2015
    qcd_samples = Samples.qcd_samples_sum_2015
    ttbar_samples = Samples.ttbar_samples_2015
    signal_sample = Samples.mfv_neu_tau01000um_M0800_2015
    data_samples = Samples.data_samples_2015

background_samples = ttbar_samples + qcd_samples
for s in qcd_samples:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
for s in ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7

signal_samples = [signal_sample]
signal_sample.nice_name = 'Signal: #sigma = 1 fb, c#tau = 1 mm, M = 800 GeV'
signal_sample.color = 8

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = [],
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = int_lumi,
            int_lumi_nice = int_lumi_nice,
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            legend_pos = (0.48, 0.78, 0.88, 0.88),
            enable_legend = True,
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = True,
            )

if year == '2015' or year == '2016':
    C('presel_njets',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_1', '%(name)s.root'),
      histogram_path = 'Ntk3evtHst0VNoNjets/h_njets',
      x_title = 'Number of jets',
      y_title = 'Events',
      y_range = (1, 1e8),
      cut_line = ((4, 0, 4, 2.5e8), 2, 5, 1),
      )

    C('presel_ht40',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_1', '%(name)s.root'),
      histogram_path = 'Ntk3evtHst0VNoHt/h_jet_ht_40',
      rebin = 4,
      x_title = 'Jet H_{T} (GeV)',
      y_title = 'Events/100 GeV',
      x_range = (800, 5000),
      y_range = (1, 1e8),
      cut_line = ((1000, 0, 1000, 2.5e8), 2, 5, 1),
      )

    C('onevtx_ntracks',
      histogram_path = 'vtxHst1VNoNtracks/h_sv_best0_ntracks',
      x_title = 'Number of tracks per vertex',
      y_title = 'Vertices',
      y_range = (1, 1e6),
      cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
      )

    C('onevtx_bs2derr',
      histogram_path = 'vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
      x_title = 'Uncertainty in d_{BV} (cm)',
      y_title = 'Vertices/5 #mum',
      y_range = (1, 1e6),
      cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
      )

    C('onevtx_dbv',
      histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_best0_bsbs2ddist',
      x_title = 'd_{BV} (cm)',
      y_title = 'Vertices/50 #mum',
      x_range = (0, 0.4),
      y_range = (1, 1e6),
      cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
      )

    C('nsv_3track',
      histogram_path = 'Ntk3mfvVertexHistosPreSel/h_nsv',
      x_title = 'Number of 3-track vertices',
      y_title = 'Events',
      x_range = (0, 8),
      y_range = (1, 1e8),
      )

    C('nsv_4track',
      histogram_path = 'Ntk4mfvVertexHistosPreSel/h_nsv',
      x_title = 'Number of 4-track vertices',
      y_title = 'Events',
      x_range = (0, 8),
      y_range = (1, 1e8),
      )

    C('nsv_5track',
      histogram_path = 'mfvVertexHistosPreSel/h_nsv',
      x_title = 'Number of 5-or-more-track vertices',
      y_title = 'Events',
      x_range = (0, 8),
      y_range = (1, 1e8),
      cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
      )

    C('dbv',
      histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
      x_title = 'd_{BV} (cm)',
      y_title = 'Vertices/50 #mum',
      x_range = (0, 0.4),
      y_range = (1, 1e4),
      )

    C('dvv',
      histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
      rebin = 10,
      x_title = 'd_{VV} (cm)',
      y_title = 'Events/200 #mum',
      y_range = (1e-2, 10),
      )

    C('track_pt',
      file_path = os.path.join('/uscms_data/d2/tucker/crab_dirs/VertexerHistosV12', '%(name)s.root'),
      histogram_path = 'mfvVertices/h_seed_nm1_pt',
      x_title = 'Track p_{T} (GeV)',
      y_title = 'Tracks/0.2 GeV',
      y_range  = (1, 1e10),
      cut_line = ((1, 0, 1, 2.8e10), 2, 5, 1),
      )

    C('track_npxlayers',
      file_path = os.path.join('/uscms_data/d2/tucker/crab_dirs/VertexerHistosV12', '%(name)s.root'),
      histogram_path = 'mfvVertices/h_seed_nm1_npxlayers',
      x_title = 'Number of pixel layers',
      y_title = 'Tracks',
      y_range  = (1, 1e10),
      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
      )

    C('track_nstlayers',
      file_path = os.path.join('/uscms_data/d2/tucker/crab_dirs/VertexerHistosV12', '%(name)s.root'),
      histogram_path = 'mfvVertices/h_seed_nm1_nstlayers',
      x_title = 'Number of strip layers',
      y_title = 'Tracks',
      y_range  = (1, 1e10),
      cut_line = ((3, 0, 3, 2.8e10), 2, 5, 1),
      )

    C('track_sigmadxybs',
      file_path = os.path.join('/uscms_data/d2/tucker/crab_dirs/VertexerHistosV12', '%(name)s.root'),
      histogram_path = 'mfvVertices/h_seed_nm1_sigmadxybs',
      x_title = 'N#sigma(dxy)',
      y_title = 'Tracks',
      x_range = (0, 10),
      y_range  = (1, 1e10),
      cut_line = ((4, 0, 4, 2.8e10), 2, 5, 1),
      )

if year == '2015':
    int_lumi = 268.3 * (247663.0 / 273176.706743)
    int_lumi_nice = '0.27 fb^{-1} (13 TeV)'
    data_samples = Samples.data_samples_2015
elif year == '2016':
    int_lumi = 3586.7 * (3103098.0 / 3452501.33131)
    int_lumi_nice = '3.59 fb^{-1} (13 TeV)'
    data_samples = Samples.data_samples
elif year == '2016BCD':
    int_lumi = 1259. * (1116774.0 / 1211893.72059)
    int_lumi_nice = '1.26 fb^{-1} (13 TeV)'
    data_samples = [Samples.JetHT2016B3, Samples.JetHT2016C, Samples.JetHT2016D]
elif year == '2016EF':
    int_lumi = 711. * (627209.0 / 684397.479668)
    int_lumi_nice = '0.71 fb^{-1} (13 TeV)'
    data_samples = [Samples.JetHT2016E, Samples.JetHT2016F]
elif year == '2016G':
    int_lumi = 763. * (708704.0 / 734451.869958)
    int_lumi_nice = '0.76 fb^{-1} (13 TeV)'
    data_samples = [Samples.JetHT2016G]
elif year == '2016H':
    int_lumi = 855. * (650411.0 / 823009.636355)
    int_lumi_nice = '0.86 fb^{-1} (13 TeV)'
    data_samples = [Samples.JetHT2016H2, Samples.JetHT2016H3]

D = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_0', '%(name)s.root'),
            int_lumi = int_lumi,
            int_lumi_nice = int_lumi_nice,
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            legend_pos = (0.50, 0.80, 0.90, 0.90),
            enable_legend = True,
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = False,
            )

D('3t1v_presel_njets',
  file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_1', '%(name)s.root'),
  histogram_path = 'Ntk3evtHst0VNoNjets/h_njets',
  x_title = 'Number of jets',
  y_title = 'Events',
  cut_line = ((4, 0, 4, 2.5e8), 2, 5, 1),
  )

D('3t1v_presel_ht40',
  file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_1', '%(name)s.root'),
  histogram_path = 'Ntk3evtHst0VNoHt/h_jet_ht_40',
  rebin = 4,
  x_title = 'Jet H_{T} (GeV)',
  y_title = 'Events/100 GeV',
  x_range = (800, 5000),
  cut_line = ((1000, 0, 1000, 2.5e8), 2, 5, 1),
  )

D('3t1v_presel_npv',
  histogram_path = 'Ntk3mfvEventHistosPreSel/h_npv',
  x_title = 'Number of primary vertices',
  y_title = 'Events',
  )

D('3t1v_presel_nseedtracks',
  histogram_path = 'Ntk3mfvEventHistosPreSel/h_n_vertex_seed_tracks',
  x_title = 'Number of seed tracks',
  y_title = 'Events',
  )

D('3t1v_presel_seedtrack_pt',
  histogram_path = 'Ntk3mfvEventHistosPreSel/h_vertex_seed_track_pt',
  x_title = 'Seed track p_{T} (GeV)',
  y_title = 'Tracks/GeV',
  )

D('3t1v_presel_seedtrack_npxlayers',
  histogram_path = 'Ntk3mfvEventHistosPreSel/h_vertex_seed_track_npxlayers',
  x_title = 'Seed track number of pixel layers',
  y_title = 'Tracks',
  )

D('3t1v_presel_seedtrack_nstlayers',
  histogram_path = 'Ntk3mfvEventHistosPreSel/h_vertex_seed_track_nstlayers',
  x_title = 'Seed track number of strip layers',
  y_title = 'Tracks',
  )

D('3t1v_onevtx_ntracks',
  histogram_path = 'Ntk3vtxHst1VNoNtracks/h_sv_best0_ntracks',
  x_title = 'Number of tracks per vertex',
  y_title = 'Vertices',
  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
  )

D('3t1v_onevtx_bs2derr',
  histogram_path = 'Ntk3vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
  )

D('3t1v_onevtx_dbv',
  histogram_path = 'Ntk3vtxHst1VNoBsbs2ddist/h_sv_best0_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
  )

D('3t1v_dbv',
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  )

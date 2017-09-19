#!/usr/bin/env python

import os
from functools import partial
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver

year = '2015p6'

root_file_dir = '/uscms_data/d2/tucker/crab_dirs/HistosV15'
plot_dir = 'plots/data_mc_comp/HistosV15_v2_%s' % year

set_style()
ps = plot_saver(plot_dir)

int_lumi_2015 = ac.int_lumi_2015 * ac.scale_factor_2015
int_lumi_2016 = ac.int_lumi_2016 * ac.scale_factor_2016

int_lumi = int_lumi_2016
int_lumi_nice = ac.int_lumi_nice_2016
qcd_samples = Samples.qcd_samples_sum
ttbar_samples = Samples.ttbar_samples
signal_sample = Samples.mfv_neu_tau01000um_M0800

if year == '2015':
    int_lumi = int_lumi_2015
    int_lumi_nice = ac.int_lumi_nice_2015
    qcd_samples = Samples.qcd_samples_sum_2015
    ttbar_samples = Samples.ttbar_samples_2015
    signal_sample = Samples.mfv_neu_tau01000um_M0800_2015

if year == '2015p6':
    int_lumi = ac.int_lumi_2015p6 * ac.scale_factor_2015p6
    int_lumi_nice = ac.int_lumi_nice_2015p6
    qcd_samples = Samples.qcd_samples_sum_2015 + Samples.qcd_samples_sum
    ttbar_samples = Samples.ttbar_samples_2015 + Samples.ttbar_samples

if year == '2015':
    data_samples = Samples.data_samples_2015
elif year == '2016':
    data_samples = Samples.data_samples
elif year == '2015p6':
    data_samples = Samples.data_samples_2015 + Samples.data_samples
elif year == '2016BCD':
    data_samples = [Samples.JetHT2016B3, Samples.JetHT2016C, Samples.JetHT2016D]
elif year == '2016EF':
    data_samples = [Samples.JetHT2016E, Samples.JetHT2016F]
elif year == '2016G':
    data_samples = [Samples.JetHT2016G]
elif year == '2016H':
    data_samples = [Samples.JetHT2016H2, Samples.JetHT2016H3]

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
            int_lumi_2015 = int_lumi_2015 if year == '2015p6' else None,
            int_lumi_2016 = int_lumi_2016 if year == '2015p6' else None,
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

if year == '2015' or year == '2016' or year == '2015p6':
    C('presel_njets',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_2', '%(name)s.root'),
      histogram_path = 'evtHst0VNoNjets/h_njets',
      x_title = 'Number of jets',
      y_title = 'Events',
      y_range = (1, 1e8),
      cut_line = ((4, 0, 4, 2.5e8), 2, 5, 1),
      )

    C('presel_ht40',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_2', '%(name)s.root'),
      histogram_path = 'evtHst0VNoHt/h_jet_ht_40',
      rebin = 4,
      x_title = 'Jet H_{T} (GeV)',
      y_title = 'Events/100 GeV',
      x_range = (800, 5000),
      y_range = (1, 1e8),
      cut_line = ((1000, 0, 1000, 2.5e8), 2, 5, 1),
      )

    C('onevtx_ntracks',
      histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
      x_title = 'Number of tracks per vertex',
      y_title = 'Vertices',
      y_range = (1, 1e6),
      cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
      )

    C('onevtx_bs2derr',
      histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
      x_title = 'Uncertainty in d_{BV} (cm)',
      y_title = 'Vertices/5 #mum',
      y_range = (1, 1e6),
      cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
      )

    C('onevtx_dbv',
      histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
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
      histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
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

    C('dvv_nm1_ntracks',
      histogram_path = 'vtxHst2VNoNtracks/h_svdist2d',
      rebin = 10,
      x_title = 'd_{VV} (cm)',
      y_title = 'Events/200 #mum',
      y_range = (1e-2, 1e3),
      )

if year == '2016':
    C('track_pt',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_nm1_tracks_pt',
      x_title = 'Track p_{T} (GeV)',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 1e10),
      cut_line = ((1, 0, 1, 2.8e10), 2, 5, 1),
      )

    C('track_min_r',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_nm1_tracks_min_r',
      x_title = 'Minimum layer number',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
      )

    C('track_npxlayers',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_nm1_tracks_npxlayers',
      x_title = 'Number of pixel layers',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
      )

    C('track_nstlayers_etalt2',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_nm1_tracks_nstlayers_etalt2',
      x_title = 'Number of strip layers (|#eta| < 2)',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((6, 0, 6, 2.8e10), 2, 5, 1),
      )

    C('track_nstlayers_etagt2',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_nm1_tracks_nstlayers_etagt2',
      x_title = 'Number of strip layers (|#eta| #geq 2)',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((7, 0, 7, 2.8e10), 2, 5, 1),
      )

    C('track_nsigmadxy',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_nm1_tracks_nsigmadxy',
      x_title = 'N#sigma(dxy)',
      y_title = 'Tracks',
      x_range = (0, 10),
      y_range = (1, 1e10),
      cut_line = ((4, 0, 4, 2.8e10), 2, 5, 1),
      )

int_lumi_2015 = 261.3 * (247778.0 / 266070.538021)
int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999)
if year == '2015':
    int_lumi = int_lumi_2015
    int_lumi_nice = '0.26 fb^{-1} (13 TeV)'
elif year == '2016':
    int_lumi = int_lumi_2016
    int_lumi_nice = '3.59 fb^{-1} (13 TeV)'
elif year == '2015p6':
    int_lumi = 3852.9 * (3269530.0 / 37324922.4333)
    int_lumi_nice = '3.85 fb^{-1} (13 TeV)'
elif year == '2016BCD':
    int_lumi = 1256. * (1069513.0 / 1212224.52201)
    int_lumi_nice = '1.26 fb^{-1} (13 TeV)'
elif year == '2016EF':
    int_lumi = 714. * (600771.0 / 689114.910163)
    int_lumi_nice = '0.71 fb^{-1} (13 TeV)'
elif year == '2016G':
    int_lumi = 758. * (643368.0 / 731581.373748)
    int_lumi_nice = '0.76 fb^{-1} (13 TeV)'
elif year == '2016H':
    int_lumi = 865. * (708100.0 / 834852.091914)
    int_lumi_nice = '0.87 fb^{-1} (13 TeV)'

D = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = int_lumi,
            int_lumi_2015 = int_lumi_2015 if year == '2015p6' else None,
            int_lumi_2016 = int_lumi_2016 if year == '2015p6' else None,
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

D('10pc_presel_njets',
  file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_2', '%(name)s.root'),
  histogram_path = 'evtHst0VNoNjets/h_njets',
  x_title = 'Number of jets',
  y_title = 'Events',
  y_range = (1, 1e7),
  cut_line = ((4, 0, 4, 2.4e7), 2, 5, 1),
  )

D('10pc_presel_ht40',
  file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV12_2', '%(name)s.root'),
  histogram_path = 'evtHst0VNoHt/h_jet_ht_40',
  rebin = 4,
  x_title = 'Jet H_{T} (GeV)',
  y_title = 'Events/100 GeV',
  x_range = (800, 5000),
  y_range = (1, 1e7),
  cut_line = ((1000, 0, 1000, 2.4e7), 2, 5, 1),
  )

D('10pc_presel_npv',
  histogram_path = 'mfvEventHistosPreSel/h_npv',
  x_title = 'Number of primary vertices',
  y_title = 'Events',
  y_range = (1, 1e6),
  )

if year == '2016':
     D('10pc_presel_ntracks',
      file_path = os.path.join('/uscms_data/d1/jchu/crab_dirs/mfv_8025/TrackerMapperV2', '%(name)s.root'),
      histogram_path = 'TrackerMapper/h_all_ntracks',
      rebin = 10,
      x_title = 'Number of tracks',
      y_title = 'Events',
      y_range = (1, 1e6),
      )

D('10pc_presel_nseedtracks',
  histogram_path = 'mfvEventHistosPreSel/h_n_vertex_seed_tracks',
  x_title = 'Number of seed tracks',
  y_title = 'Events',
  )

D('10pc_presel_seedtrack_pt',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_pt',
  x_title = 'Seed track p_{T} (GeV)',
  y_title = 'Tracks/GeV',
  )

D('10pc_presel_seedtrack_npxlayers',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_npxlayers',
  x_title = 'Seed track number of pixel layers',
  y_title = 'Tracks',
  )

D('10pc_presel_seedtrack_nstlayers',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_nstlayers',
  x_title = 'Seed track number of strip layers',
  y_title = 'Tracks',
  )

D('10pc_3t1v_ntracks',
  histogram_path = 'Ntk3vtxHst1VNoNtracks/h_sv_all_ntracks',
  x_title = 'Number of tracks per vertex',
  y_title = 'Vertices',
  y_range = (1, 1e6),
  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
  )

D('10pc_3t1v_bs2derr',
  histogram_path = 'Ntk3vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  int_lumi_2015 = 261.3 * (247778.0 / 266070.538021) * (527.0 / 757.461440872) if year == '2015p6' else None,
  int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999) * (10361.0 / 15073.8297692) if year == '2015p6' else None,
  int_lumi = 3852.9 * (3269530.0 / 37324922.4333) * (10888.0 / 15831.2912256) if year == '2015p6' else int_lumi,
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e4),
  cut_line = ((0.0025, 0, 0.0025, 1.8e4), 2, 5, 1),
  )

D('10pc_3t1v_dbv',
  histogram_path = 'Ntk3vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  int_lumi_2015 = 261.3 * (247778.0 / 266070.538021) * (527.0 / 757.461440872) if year == '2015p6' else None,
  int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999) * (10361.0 / 15073.8297692) if year == '2015p6' else None,
  int_lumi = 3852.9 * (3269530.0 / 37324922.4333) * (10888.0 / 15831.2912256) if year == '2015p6' else int_lumi,
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e4),
  cut_line = ((0.01, 0, 0.01, 1.8e4), 2, 5, 1),
  )

D('10pc_3t1v_onevtx_dbv',
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e4),
  )

D('10pc_3t1v_onevtx_dbv_unzoom',
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  y_range = (1, 1e4),
  )

D('10pc_3t2v_dvv',
  histogram_path = 'Ntk3mfvVertexHistosFullSel/h_svdist2d',
  rebin = 5,
  x_title = 'd_{VV} (cm)',
  y_title = 'Events/100 #mum',
  x_range = (0, 0.4),
  y_range = (1e-2, 1e2),
  )

D('10pc_4t1v_ntracks',
  histogram_path = 'Ntk4vtxHst1VNoNtracks/h_sv_all_ntracks',
  x_title = 'Number of tracks per vertex',
  y_title = 'Vertices',
  y_range = (1, 1e6),
  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
  )

D('10pc_4t1v_bs2derr',
  histogram_path = 'Ntk4vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  int_lumi_2015 = 261.3 * (247778.0 / 266070.538021) * (64.0 / 90.8345997062) if year == '2015p6' else None,
  int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999) * (1129.0 / 1914.68320949) if year == '2015p6' else None,
  int_lumi = 3852.9 * (3269530.0 / 37324922.4333) * (1193.0 / 2005.51782284) if year == '2015p6' else int_lumi,
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e4),
  cut_line = ((0.0025, 0, 0.0025, 1.8e4), 2, 5, 1),
  )

D('10pc_4t1v_dbv',
  histogram_path = 'Ntk4vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  int_lumi_2015 = 261.3 * (247778.0 / 266070.538021) * (64.0 / 90.8345997062) if year == '2015p6' else None,
  int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999) * (1129.0 / 1914.68320949) if year == '2015p6' else None,
  int_lumi = 3852.9 * (3269530.0 / 37324922.4333) * (1193.0 / 2005.51782284) if year == '2015p6' else int_lumi,
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e4),
  cut_line = ((0.01, 0, 0.01, 1.8e4), 2, 5, 1),
  )

D('10pc_4t1v_onevtx_dbv',
  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e4),
  )

D('10pc_4t1v_onevtx_dbv_unzoom',
  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  y_range = (1, 1e4),
  )

D('10pc_4t2v_dvv',
  histogram_path = 'Ntk4mfvVertexHistosFullSel/h_svdist2d',
  rebin = 5,
  x_title = 'd_{VV} (cm)',
  y_title = 'Events/100 #mum',
  x_range = (0, 0.4),
  y_range = (1e-2, 1e2),
  res_fit = False,
  )

D('10pc_5t1v_ntracks',
  histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
  x_title = 'Number of tracks per vertex',
  y_title = 'Vertices',
  y_range = (1, 1e6),
  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
  )

D('10pc_5t1v_bs2derr',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  int_lumi_2015 = 261.3 * (247778.0 / 266070.538021) * (12.0 / 14.6054833307) if year == '2015p6' else None,
  int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999) * (104.0 / 302.469814438) if year == '2015p6' else None,
  int_lumi = 3852.9 * (3269530.0 / 37324922.4333) * (116.0 / 317.075296402) if year == '2015p6' else int_lumi,
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e4),
  cut_line = ((0.0025, 0, 0.0025, 1.8e4), 2, 5, 1),
  )

D('10pc_5t1v_dbv',
  histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  int_lumi_2015 = 261.3 * (247778.0 / 266070.538021) * (12.0 / 14.6054833307) if year == '2015p6' else None,
  int_lumi_2016 = 3591.6 * (3021752.0 / 3466421.6999) * (104.0 / 302.469814438) if year == '2015p6' else None,
  int_lumi = 3852.9 * (3269530.0 / 37324922.4333) * (116.0 / 317.075296402) if year == '2015p6' else int_lumi,
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e4),
  cut_line = ((0.01, 0, 0.01, 1.8e4), 2, 5, 1),
  )

D('10pc_5t1v_onevtx_dbv',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e4),
  )

D('10pc_5t1v_onevtx_dbv_unzoom',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  y_range = (1, 1e4),
  )

int_lumi_2015 = 2613. * (2482166.0 / 2660705.41664)
int_lumi_2016 = 35916. * (30206710.0 / 34709587.7891)
if year == '2015':
    int_lumi = int_lumi_2015
    int_lumi_nice = '2.6 fb^{-1} (13 TeV)'
elif year == '2016':
    int_lumi = int_lumi_2016
    int_lumi_nice = '35.9 fb^{-1} (13 TeV)'
elif year == '2015p6':
    int_lumi = 38529. * (32688876.0 / 37370293.037)
    int_lumi_nice = '38.5 fb^{-1} (13 TeV)'
elif year == '2016BCD':
    int_lumi = 12560. * (10714065.0 / 12138111.5891)
    int_lumi_nice = '12.6 fb^{-1} (13 TeV)'
elif year == '2016EF':
    int_lumi = 7140. * (5994415.0 / 6900168.65957)
    int_lumi_nice = '7.1 fb^{-1} (13 TeV)'
elif year == '2016G':
    int_lumi = 7580. * (6365977.0 / 7325389.10296)
    int_lumi_nice = '7.6 fb^{-1} (13 TeV)'
elif year == '2016H':
    int_lumi = 8650. * (7132253.0 / 8359447.89656)
    int_lumi_nice = '8.7 fb^{-1} (13 TeV)'

E = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join('/uscms_data/d2/tucker/crab_dirs/HistosV15_v2', '%(name)s.root'),
            int_lumi = int_lumi,
            int_lumi_2015 = int_lumi_2015 if year == '2015p6' else None,
            int_lumi_2016 = int_lumi_2016 if year == '2015p6' else None,
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

E('100pc_presel_njets',
  histogram_path = 'mfvEventHistosPreSel/h_njets',
  x_title = 'Number of jets',
  y_title = 'Events',
  y_range = (1, 1e8),
  )

E('100pc_presel_ht40',
  histogram_path = 'mfvEventHistosPreSel/h_jet_ht_40',
  rebin = 4,
  x_title = 'Jet H_{T} (GeV)',
  y_title = 'Events/100 GeV',
  y_range = (1, 1e8),
  )

E('100pc_presel_npv',
  histogram_path = 'mfvEventHistosPreSel/h_npv',
  x_title = 'Number of primary vertices',
  y_title = 'Events',
  y_range = (1, 1e7),
  )

E('100pc_presel_nseedtracks',
  histogram_path = 'mfvEventHistosPreSel/h_n_vertex_seed_tracks',
  x_title = 'Number of seed tracks',
  y_title = 'Events',
  )

E('100pc_presel_seedtrack_pt',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_pt',
  x_title = 'Seed track p_{T} (GeV)',
  y_title = 'Tracks/GeV',
  )

E('100pc_presel_seedtrack_npxlayers',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_npxlayers',
  x_title = 'Seed track number of pixel layers',
  y_title = 'Tracks',
  )

E('100pc_presel_seedtrack_nstlayers',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_nstlayers',
  x_title = 'Seed track number of strip layers',
  y_title = 'Tracks',
  )

E('100pc_3t1v_ntracks',
  histogram_path = 'Ntk3vtxHst1VNoNtracks/h_sv_all_ntracks',
  x_title = 'Number of tracks per vertex',
  y_title = 'Vertices',
  y_range = (1, 1e6),
  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
  )

E('100pc_3t1v_bs2derr',
  histogram_path = 'Ntk3vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  int_lumi_2015 = 2613. * (2482166.0 / 2660705.41664) * (5422.0 / 7588.02237446) if year == '2015p6' else None,
  int_lumi_2016 = 35916. * (30206710.0 / 34709587.7891) * (103668.0 / 150677.855772) if year == '2015p6' else None,
  int_lumi = 38529. * (32688876.0 / 37370293.037) * (109090.0 / 158265.880129) if year == '2015p6' else int_lumi,
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1, 1e6),
  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
  )

E('100pc_3t1v_dbv',
  histogram_path = 'Ntk3vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  int_lumi_2015 = 2613. * (2482166.0 / 2660705.41664) * (5422.0 / 7588.02237446) if year == '2015p6' else None,
  int_lumi_2016 = 35916. * (30206710.0 / 34709587.7891) * (103668.0 / 150677.855772) if year == '2015p6' else None,
  int_lumi = 38529. * (32688876.0 / 37370293.037) * (109090.0 / 158265.880129) if year == '2015p6' else int_lumi,
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e6),
  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
  )

E('100pc_3t1v_onevtx_dbv',
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e6),
  )

E('100pc_3t1v_onevtx_dbv_unzoom',
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  y_range = (1, 1e6),
  )

E('100pc_3t2v_dvv',
  histogram_path = 'Ntk3mfvVertexHistosFullSel/h_svdist2d',
  rebin = 5,
  x_title = 'd_{VV} (cm)',
  y_title = 'Events/100 #mum',
  x_range = (0, 0.4),
  y_range = (1e-1, 1e3),
  )

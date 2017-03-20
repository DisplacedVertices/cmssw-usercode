#!/usr/bin/env python

import os
from functools import partial
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver

root_file_dir = '/uscms_data/d2/tucker/crab_dirs/HistosV11/2016'
plot_dir = 'plots/data_mc_comp/HistosV11_2016'

set_style()
ps = plot_saver(plot_dir)

scale_factor = 1. #245750.0 / 264843.310478

data_samples = [] #Samples.data_samples
background_samples = Samples.ttbar_samples + Samples.qcd_samples_sum

signal_samples = [Samples.official_mfv_neu_tau00100um_M0800, Samples.official_mfv_neu_tau00300um_M0800, Samples.official_mfv_neu_tau01000um_M0800, Samples.official_mfv_neu_tau10000um_M0800]
y = ['100 #mum', '300 #mum', '1 mm', '10 mm']
c = [7, 4, 6, 8]
for i, signal_sample in enumerate(signal_samples):
    signal_sample.xsec = 0.001
    signal_sample.nice_name = 'Signal: #sigma = 1 fb, c#tau = %s, M = 800 GeV' % y[i]
    signal_sample.color = c[i]
Samples.official_mfv_neu_tau00300um_M0800.color = 8
signal_samples = [Samples.official_mfv_neu_tau00300um_M0800]

for s in Samples.qcd_samples_sum:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
for s in Samples.ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = ac.int_lumi * scale_factor, 
            int_lumi_nice = ac.int_lumi_nice,
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

C('nocuts_njets',
  histogram_path = 'mfvEventHistosNoCuts/h_njets',
  x_title = 'Number of jets',
  y_title = 'Events',
  y_range = (1, 1e8),
  cut_line = ((4, 0, 4, 2.5e8), 2, 5, 1),
  )

C('nocuts_ht40',
  histogram_path = 'mfvEventHistosNoCuts/h_jet_ht_40',
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

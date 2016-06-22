#!/usr/bin/env python

import os
from functools import partial
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver

root_file_dir = '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/HistosV6p1_76x_nstlays3_27'
plot_dir = 'plots/data_mc_comp/HistosV6p1_76x_nstlays3_27'

set_style()
ps = plot_saver(plot_dir)

ac.int_lumi *= 0.01
ac.int_lumi_nice = '260 pb^{-1} (13 TeV)'
scale_factor = 245750.0 / 264843.310478

data_samples = Samples.data_samples
background_samples = Samples.ttbar_samples + Samples.qcd_samples

signal_samples = [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]
y = ['100 #mum', '300 #mum', '1 mm', '10 mm']
c = [7, 4, 6, 8]
for i, signal_sample in enumerate(signal_samples):
    signal_sample.xsec = 1.0
    signal_sample.nice_name = '#sigma = 1 pb, M = 800 GeV, #tau = %s' % y[i]
    signal_sample.color = c[i]

for s in Samples.qcd_samples:
    s.join_info = True, 'multijet events', ROOT.kBlue-9
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
            legend_pos = (0.5, 0.7, 0.9, 0.9),
            enable_legend = True,
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncert.', 0, 1, 3002),
            )

C('njets_nocuts',
  histogram_path = 'mfvEventHistosNoCuts/h_njets',
  x_title = 'number of particle-flow jets',
  y_title = 'events',
  cut_line = (4, 2, 5, 1),
  )

C('ht40_nocuts',
  histogram_path = 'mfvEventHistosNoCuts/h_jet_ht_40',
  rebin = 4,
  x_title = 'particle-flow jet H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (800, 5000),
  cut_line = (1000, 2, 5, 1),
  )

C('npv_presel',
  histogram_path = 'mfvEventHistosPreSel/h_npv',
  x_title = 'number of PV',
  y_title = 'events',
  x_range = (0, 32),
  )

C('nsv_presel',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  overflow_in_last = False,
  x_title = 'number of vertices',
  y_title = 'events',
  x_range = (0, 2),
  y_range = (1, 1e6),
  cut_line = (2, 2, 5, 1),
  )

C('ntracks_onevtx',
  histogram_path = 'vtxHst1VNoNtracks/h_sv_best0_ntracks',
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  x_range = (2, 20),
  cut_line = (5, 2, 5, 1),
  )

C('ntracksptgt3_onevtx',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  )

C('drmin_onevtx',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_drmin',
  rebin = 10,
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.1',
  )

C('drmax_onevtx',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  )

C('njetsntks_onevtx',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  )

C('bs2derr_onevtx',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
  rebin = 5,
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/25 #mum',
  cut_line = (0.0025, 2, 5, 1),
  )

C('bs2derr_onevtx_zoom',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.01),
  cut_line = (0.0025, 2, 5, 1),
  )

C('sumnhitsbehind_onevtx',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_sumnhitsbehind',
  x_title = 'sum number of hits behind SV',
  y_title = 'vertices',
  )

C('tksjetsntkmass_onevtx',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_tksjetsntkmass',
  rebin = 4,
  x_title = 'tracks + jets mass (GeV)',
  y_title = 'vertices/200 GeV',
  )

dbv_bins = [j*0.005 for j in range(8)] + [0.04]

C('dbv_onevtx',
  histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_best0_bsbs2ddist',
  overflow_in_last = False,
  rebin = dbv_bins,
  bin_width_to = 0.005,
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  cut_line = (0.01, 2, 5, 1),
  )

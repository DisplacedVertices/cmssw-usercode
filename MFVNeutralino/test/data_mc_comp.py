#!/usr/bin/env python

import os
from functools import partial
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver

root_file_dir = '~/nobackup/crab_dirs/HistosV6p1_76x_puw'
plot_dir = 'plots/HistosV6p1_76x_puw_datamccomp'

set_style()
ps = plot_saver(plot_dir)

ac.int_lumi *= 0.1
ac.int_lumi_nice = '260 pb^{-1} (13 TeV)'
scale_factor = 1. #56.0/298.0

data_samples = Samples.data_samples
if 0:
    Samples.qcd_samples.pop(1)
    background_samples = Samples.ttbar_samples + Samples.qcd_samples
else:
    background_samples = Samples.ttbar_samples + Samples.qcdpt_samples
    scale_factor = 299554.0 / 366268.314515 #* 328.0 / 315.886929274

signal_samples = [] #[Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]
y= ['100 #mum, #sigma = 100 fb', '300 #mum, #sigma = 5 fb', '1 mm, #sigma = 1 fb', '10 mm, #sigma = 1 fb']
c=[7,4,6,8]
s=[0.1,0.005,0.001, 0.001]
for i, signal_sample in enumerate(signal_samples):
    signal_sample.xsec = s[i]
    signal_sample.nice_name = '#tau = %s' % y[i]
    signal_sample.color = c[i]

for s in Samples.qcd_samples:
    s.join_info = True, 'Multi-jet events', ROOT.kBlue-9
for s in Samples.qcdpt_samples:
    s.join_info = True, 'Multi-jet events', ROOT.kOrange
for s in Samples.ttbar_samples: # + Samples.smaller_background_samples + Samples.leptonic_background_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7 #, single t, V+jets, t#bar{t}+V, VV', ROOT.kBlue-7

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = ac.int_lumi * scale_factor, 
            int_lumi_nice = ac.int_lumi_nice,
            #background_uncertainty = ('Uncert. on MC bkg', 0.2, ROOT.kBlack, 3004),
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            enable_legend = False,
            #legend_pos = (0.67, 0.67, 0.90, 0.90),
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncert.', 0, 1, 3002),
            )

C('nsv',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'number of vertices',
  y_title = 'events',
  x_range = (0,5),
  y_range = (1, 3e5),
  cut_line = (2, 2, 5, 1),
  )

C('npv_presel',
  histogram_path = 'mfvEventHistosPreSel/h_npv',
  x_title = 'number of PV',
  y_title = 'events',
  x_range = (0, 32),
  )

C('npv_1vtx',
  histogram_path = 'mfvEventHistosOnlyOneVtx/h_npv',
  x_title = 'number of PV',
  y_title = 'events',
  x_range = (0, 32),
  )

C('jetht_presel',
  histogram_path = 'mfvEventHistosPreSel/h_jet_sum_ht',
  rebin = 5,
  x_title = 'particle-flow jet H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (900, 5000),
  y_range = (1, 1.45e5),
  #legend_pos = (0.67, 0.67, 0.90, 0.90),
  )

C('jetht_1vtx',
  histogram_path = 'mfvEventHistosOnlyOneVtx/h_jet_sum_ht',
  rebin = 5,
  x_title = 'particle-flow jet H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (900, 3500),
  y_range = (0.3, 120),
  #legend_pos = (0.67, 0.67, 0.90, 0.90),
  )

C('sv_best0_ntracks_nm1',
  histogram_path = 'vtxHst1VNoNtracks/h_sv_best0_ntracks',
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  x_range = (2, 20),
  y_range = (0.3, None),
  #legend_pos = (0.67, 0.67, 0.90, 0.90),
  cut_line = (5,ROOT.kRed,5,1),
  )

C('sv_best0_ntracksptgt3_nm1',
  histogram_path = 'vtxHst1VNoNtracks/h_sv_best0_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (0, 20),
  y_range = (0.3, None),
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

C('sv_best0_drmin_nm1',
  histogram_path = 'vtxHst1VNoDrmin/h_sv_best0_drmin',
  rebin = 5,
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.05',
  x_range = (0, 0.8),
  y_range = (0.3, None),
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = (0.4,ROOT.kRed,5,1),
  )

C('sv_best0_drmax_nm1',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  x_range = (0, 5.6),
  #legend_pos = (0.13, 0.70, 0.43, 0.90),
  )

C('sv_best0_njetsntks_nm1',
  histogram_path = 'vtxHst1VNoNjets/h_sv_best0_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  x_range = (0, 7),
  y_range = (0.03, 175),
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = (1,ROOT.kRed,5,1),
  )

C('sv_best0_bs2derr_nm1_zoomout',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/25 #mum',
  rebin = 5,
  #x_range = (0, 0.01),
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = (0.0025,ROOT.kRed,5,1),
  )

C('sv_best0_bs2derr_nm1',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_best0_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.01),
  overflow_in_last = False,
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = (0.0025,ROOT.kRed,5,1),
  )

C('sv_best0_tksjetsntkmass',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_tksjetsntkmass',
  rebin = 5,
  x_title = 'tracks + jets mass (GeV)',
  y_title = 'vertices/200 GeV',
  y_range = (0.3, 82),
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

dbv_bins = [j*0.005 for j in range(8)] + [0.04] #, 0.05, 0.06, 0.07, 0.085, 0.1]

C('sv_best0_bsbs2ddist',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
  rebin = dbv_bins,
  bin_width_to = 0.005,
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  y_range = (0.3, 300),

  overflow_in_last = False,
  #legend_pos = (0.47, 0.70, 0.87, 0.90),
  )


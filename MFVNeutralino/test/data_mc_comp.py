#!/usr/bin/env python

import os,sys
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, tdr_style, plot_saver
from functools import partial

root_file_dir = '/uscms/home/jchu/nobackup/crab_dirs/mfv_5313/HistosV20'
plot_dir = 'plots/paper_draft'

set_style()
ps = plot_saver(plot_dir, size=(1,1), root_log=True, pdf_log=True)

data_samples = Samples.data_samples
background_samples = Samples.smaller_background_samples + Samples.leptonic_background_samples + Samples.ttbar_samples + Samples.qcd_samples
signal_sample = Samples.mfv_neutralino_tau1000um_M0400
signal_sample.cross_section = 0.001
signal_sample.nice_name = '#tau = 1 mm, M = 400 GeV, #sigma = 1 fb signal'
signal_sample.color = 8

for s in Samples.qcd_samples:
    s.join_info = True, 'Multi-jet events', ROOT.kBlue-9
for s in Samples.ttbar_samples + Samples.smaller_background_samples + Samples.leptonic_background_samples:
    s.join_info = True, 't#bar{t}, single t, V+jets, t#bar{t}+V, VV', ROOT.kBlue-7

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = [signal_sample],
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi_nice = ac.int_lumi_nice,
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            enable_legend = True,
            legend_pos = (0.27, 0.70, 0.87, 0.90),
            res_fit = False,
            verbose = True,
            )

dbv_bins = [j*0.005 for j in range(8)] + [0.04, 0.05, 0.06, 0.07, 0.085, 0.1]

C('dbv',
#  output_fn = 'plots/paper_draft/duh.pdf',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
  int_lumi = ac.int_lumi * ac.scale_factor * 181076.0 / 135591.837455,
  rebin = dbv_bins,
  bin_width_to = 0.005,
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  x_range = (0, 0.1),
  y_range = (0.5, 100000),
  y_title_offset = 1.19,
  res_y_range = (0,2.5),
  legend_pos = (0.425, 0.679, 0.864, 0.901),
  )

if 0:
    C('sv_all_bsbs2ddist',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_all_bsbs2ddist',
      int_lumi = ac.int_lumi * ac.scale_factor * 251.0 / 139.30171468,
      x_title = 'd_{BV} (cm)',
      y_title = 'vertices/50 #mum',
      x_range = (0, 0.1),
      y_range = (0.1, 100000),
      )

    C('sv_all_svdist2d',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_svdist2d',
      int_lumi = ac.int_lumi * ac.scale_factor * 251.0 / 139.30171468,
      x_title = 'd_{VV} (cm)',
      y_title = 'events/0.01 cm',
      x_range = (0, 0.3),
      y_range = (0.1, 200),
      rebin = 10,
      )

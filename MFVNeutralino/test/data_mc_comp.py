#!/usr/bin/env python

import os,sys
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver
from functools import partial

root_file_dir = 'crab/HistosV20'
plot_dir = 'plots/paper_draft'

set_style()
ps = plot_saver(plot_dir, size=(600,600))

data_samples = Samples.data_samples
background_samples = Samples.smaller_background_samples + Samples.leptonic_background_samples + Samples.ttbar_samples + Samples.qcd_samples
signal_samples = [Samples.mfv_neutralino_tau1000um_M0400]
Samples.mfv_neutralino_tau1000um_M0400.nice_name = '#tau = 1 mm, M = 400 GeV, #sigma = %d fb signal'%(1000*Samples.mfv_neutralino_tau1000um_M0400.cross_section)
Samples.mfv_neutralino_tau1000um_M0400.color = 8

for s in Samples.qcdht0100, Samples.qcdht0250, Samples.qcdht0500, Samples.qcdht1000:
    s.join_info = True, 'QCD', ROOT.kBlue-9
for s in Samples.ttbardilep, Samples.ttbarsemilep, Samples.ttbarhadronic:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7
for s in Samples.auxiliary_background_samples:
    s.join_info = True, 'other', ROOT.kBlue-5
for s in Samples.smaller_background_samples + Samples.leptonic_background_samples:
    s.join_info = True, 'other', ROOT.kBlue-3

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi_nice = ac.int_lumi_nice,
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            #enable_legend = False,
            legend_pos = (0.27, 0.70, 0.87, 0.90),
            )

C('sv_best0_bsbs2ddist',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
  int_lumi = ac.int_lumi * ac.scale_factor * 181076.0 / 135591.837455,
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

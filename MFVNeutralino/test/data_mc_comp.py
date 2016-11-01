#!/usr/bin/env python

import os,sys
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, tdr_style, plot_saver
from functools import partial

root_file_dir = 'HistosV20_rebin_for_paper' # '/uscms/home/jchu/nobackup/crab_dirs/mfv_5313/HistosV20'
plot_dir = 'plots/after_referee_dmc'

set_style()
ps = plot_saver(plot_dir, size=(1,1), root_log=True, pdf_log=True)

data_samples = Samples.data_samples
background_samples = Samples.smaller_background_samples + Samples.leptonic_background_samples + Samples.ttbar_samples + Samples.qcd_samples
signal_sample = Samples.mfv_neutralino_tau1000um_M0400
signal_sample.cross_section = 0.001
signal_sample.nice_name = 'Signal: #sigma = 1 fb,'
signal_sample.color = 8

for s in Samples.qcd_samples:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
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
            legend_pos = (0.428, 0.681, 0.865, 0.909),
            res_fit = False,
            verbose = True,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3002),
            )

dbv_bins = [j*0.05 for j in range(8)] + [0.4, 0.5, 0.6, 0.7, 0.85, 1.]

C('dbv',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_best0_bsbs2ddist',
  int_lumi = ac.int_lumi * ac.scale_factor, 
  int_lumi_bkg_scale = 181076.0 / 135591.837455,
  rebin = dbv_bins,
  bin_width_to = 0.05,
  x_title = 'd_{BV} (mm)',
  y_title = 'Events/50 #mum',
  y_range = (0.5, 200000),
  y_title_offset = 1.1,
  y_title_size = 0.05,
  res_x_title_size = 0.05,
  res_x_title_offset = 0.95,
  y_label_size = 0.04,
  res_x_label_size = 0.04,
  res_y_label_size = 0.04,
  res_y_title_size = 0.05,
  res_y_range = (0,2.5),
  legend_pos = (0.438, 0.671, 0.875, 0.899),
  )

dvv_bins = [j*0.2 for j in range(6)] + [2.]

C('dvv',
  histogram_path = 'mfvVertexHistosWAnaCuts/h_svdist2d',
  data_samples = [],
  int_lumi = ac.int_lumi * ac.scale_factor,
  int_lumi_bkg_scale = 251.0 / 139.30171468,
  x_title = 'd_{VV} (mm)',
  y_title = 'Events',
  rebin = dvv_bins,
#  bin_width_to = 0.2,
  y_title_offset = 1.,
  x_title_offset = 0.92,
  x_title_size = 0.05,
  y_title_size = 0.05,
  y_label_size = 0.04,
#  res_y_range = (0, 6.5),
  y_range = (0.2, 300),
  legend_pos = (0.438, 0.641, 0.875, 0.869),
  simulation = True,
  )

# NEED TO PUT THIS IN ROOTTOOLS TO ZERO THE LAST BIN IN RATIO
#
#        ddd = data_sample.hist.Clone('ddd')
#        if ddd.GetNbinsX() == 6:
#            ddd.SetBinContent(6, 0)
#            ddd.SetBinError(6, 0)
#
# AND THIS FOR THE "WRONG" ERROR BAR
#
#        if res_g.GetN() == 5 and abs(res_g.GetY()[3] - 6.11046924755) < 1e-4:
#            print 'hi from the hack!'
#            res_g.SetPointEYlow(3, 4.22)
#            res_g.SetPointEYhigh(3, 17.3)

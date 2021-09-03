#!/usr/bin/env python

import os
from functools import partial
import DVCode.Tools.Samples as Samples
import DVCode.MFVNeutralino.AnalysisConstants as ac
from DVCode.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver, plot_dir

year = '2017p8'
version = 'V23m'
root_file_dir = '/uscms_data/d2/tucker/crab_dirs/Histos%s' % version

set_style()
ps = plot_saver(plot_dir('dbv_%s_%s' % (year, version)), pdf_log=True)

int_lumi = ac.int_lumi_2017p8 * ac.scale_factor_2017p8
int_lumi_nice = ac.int_lumi_nice_2017p8

qcd_samples = Samples.qcd_samples_2017[1:] + Samples.qcd_samples_2018
ttbar_samples = Samples.ttbar_samples_2017
signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
data_samples = Samples.data_samples_2017

background_samples = ttbar_samples + qcd_samples
for s in qcd_samples:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
for s in ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7

signal_samples = [signal_sample]
signal_sample.nice_name = 'Multijet signal: #sigma = 1 fb,\\c#tau = 1 mm, M = 800 GeV'
signal_sample.color = 8

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = int_lumi,
            int_lumi_nice = int_lumi_nice,
            canvas_top_margin = 0.08,
            overflow_in_last = True,
            poisson_intervals = True,
            legend_pos = (0.28, 0.58, 0.88, 0.88),
            res_fit = False,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = True,
            )

C('dbv',
#  data_samples = data_samples,
#  normalize_to_data = True,
#  simulation = False,
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Events/50 #mum',
  x_range = (0, 0.4),
  y_range = (1, 1e5),
  )

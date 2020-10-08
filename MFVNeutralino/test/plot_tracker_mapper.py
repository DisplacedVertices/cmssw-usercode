#!/usr/bin/env python

import os
from functools import partial
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

year = '2017'
version = 'V27p1Bm'
root_file_dir = '/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1'

set_style()
ps = plot_saver(plot_dir('plot_tracker_mapper_%s_%s' % (year, version)))

qcd_samples = Samples.qcd_samples_2017 + Samples.bjet_samples_2017[:-1]
ttbar_samples = Samples.bjet_samples_2017[-1:]
signal_sample = Samples.mfv_neu_tau001000um_M0400_2017
data_samples = []
background_samples = ttbar_samples + qcd_samples
lumi = ac.int_lumi_2017 * ac.scale_factor_2017
lumi_nice = ac.int_lumi_nice_2017

for s in qcd_samples:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
for s in ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7

signal_samples = [signal_sample]
signal_sample.nice_name = 'Multijet Signal: #sigma = 1 fb, c#tau = 1000 um, M = 400 GeV'
signal_sample.color = 8

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = [],
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = lumi,
            int_lumi_nice = lumi_nice,
            canvas_top_margin = 0.08,
            #overflow_in_last = True,
            poisson_intervals = True,
            legend_pos = (0.48, 0.78, 0.88, 0.88),
            enable_legend = True,
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = True,
            )

C('track_pt',
  file_path = os.path.join('/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1', '%(name)s.root'),
  histogram_path = 'TrackerMapper/h_nm1_sel_tracks_pt',
  x_title = 'Track p_{T} (GeV)',
  y_title = 'Tracks/0.1 GeV',
  y_range = (1, 1e10),
  cut_line = ((1, 0, 1, 2.8e10), 2, 5, 1),
  )

C('track_min_r',
  file_path = os.path.join('/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1', '%(name)s.root'),
  histogram_path = 'TrackerMapper/h_nm1_sel_tracks_min_r',
  x_title = 'Minimum layer number',
  y_title = 'Tracks',
  y_range = (1, 1e10),
  cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
  )

C('track_npxlayers',
  file_path = os.path.join('/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1', '%(name)s.root'),
  histogram_path = 'TrackerMapper/h_nm1_sel_tracks_npxlayers',
  x_title = 'Number of pixel layers',
  y_title = 'Tracks',
  y_range = (1, 1e10),
  cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
  )

C('track_nstlayers_etalt2',
  file_path = os.path.join('/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1', '%(name)s.root'),
  histogram_path = 'TrackerMapper/h_nm1_sel_tracks_nstlayers_etalt2',
  x_title = 'Number of strip layers (|#eta| < 2)',
  y_title = 'Tracks',
  y_range = (1, 1e10),
  cut_line = ((6, 0, 6, 2.8e10), 2, 5, 1),
  )

C('track_nstlayers_etagt2',
  file_path = os.path.join('/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1', '%(name)s.root'),
  histogram_path = 'TrackerMapper/h_nm1_sel_tracks_nstlayers_etagt2',
  x_title = 'Number of strip layers (|#eta| #geq 2)',
  y_title = 'Tracks',
  y_range = (1, 1e10),
  cut_line = ((7, 0, 7, 2.8e10), 2, 5, 1),
  )

C('track_nsigmadxy',
  file_path = os.path.join('/uscms/home/joeyr/crabdirs/TrackerMapperBtagTriggeredV1', '%(name)s.root'),
  histogram_path = 'TrackerMapper/h_nm1_sel_tracks_nsigmadxy',
  x_title = 'N#sigma(dxy)',
  y_title = 'Tracks',
  x_range = (0, 10),
  y_range = (1, 1e10),
  cut_line = ((4, 0, 4, 2.8e10), 2, 5, 1),
  )


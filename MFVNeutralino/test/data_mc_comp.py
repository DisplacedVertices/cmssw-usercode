#!/usr/bin/env python

import os
from functools import partial
import JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples

year = 'run2'
version = 'ULV30BvetoLHTm'
root_file_dir = '/uscms/home/pkotamni/nobackup/crabdirs/Histos_FixAnCut_OnnormdzULV30BvetoLHTm'
#root_file_dir = '~/nobackup/crabdirs/NtupleOnnormdzULV30BvetoLHTm/'


#year = 'run2'
#version = 'ULV30Lepm'
#root_file_dir = '~/nobackup/crabdirs/HistosOnnormdzULV30Lepm' 
#root_file_dir = '/eos/uscms/store/user/pkotamni/NtupleOnnormdzULV30Lepm_ROOT/'#'~/nobackup/crabdirs/NtupleOnnormdzULV30Lepm' 

#year = '2017p8'
#version = 'V27m'
#root_file_dir = '/uscms_data/d2/tucker/crab_dirs/HistosV27m'

set_style()
ps = plot_saver(plot_dir('/uscms/home/pkotamni/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/BjetDispl_repsig_mc_comp_part1_%s_%s_FixAnCut' % (year, version)), pdf=True, log=True)
#ps = plot_saver(plot_dir('/uscms/home/pkotamni/work/CMSSW_10_6_27/src/JMTucker/MFVNeutralino/test/Lepton_repsig_mc_comp_part3_%s_%s' % (year, version)), pdf=True, log=True)

qcd_samples = Samples.qcd_samples_2017[:-1]
qcdlep_samples = Samples.qcd_lep_samples_2017[14:-1]
qcdmupt5_samples = Samples.qcd_lep_samples_2017[1:13]
ttbar_samples = Samples.ttbar_samples_2017[0:1]
wjetstolnu_samples = Samples.leptonic_samples_2017[0:3]
dyjets_samples = Samples.leptonic_samples_2017[3:-1] 
diboson_samples = Samples.diboson_samples_2017
signal_sample = [Samples.mfv_neu_tau001000um_M0400_2017, Samples.mfv_stopdbardbar_tau001000um_M0200_2017, Samples.mfv_stopdbardbar_tau000300um_M0400_2017, Samples.ggHToSSTodddd_tau1mm_M55_2017]
#signal_sample = [Samples.ZHToSSTodddd_tau1mm_M55_2017, Samples.WplusHToSSTodddd_tau1mm_M55_2017, Samples.WminusHToSSTodddd_tau1mm_M55_2017]
#signal_sample = [Samples.VHToSSTodddd_tau1mm_M55_2017, Samples.VHToSSTodddd_tau10mm_M55_2017]
data_samples = [] #Samples.Lepton_data_samples_2017
#background_samples = wjetstolnu_samples + ttbar_samples + dyjets_samples + diboson_samples + qcdlep_samples + qcdmupt5_samples 
background_samples = ttbar_samples + qcd_samples 
lumi = ac.int_lumi_2017 * ac.scale_factor_2017
lumi_nice = ac.int_lumi_nice_2017

if year == '2018':
    qcd_samples = Samples.qcd_samples_2018
    ttbar_samples = Samples.ttbar_samples_2018
    signal_sample = Samples.mfv_stopdbardbar_tau001000um_M0300_2018
    data_samples = [] # Samples.data_samples_2017
    background_samples = ttbar_samples + qcd_samples
    lumi = ac.int_lumi_2018 * ac.scale_factor_2018
    lumi_nice = ac.int_lumi_nice_2018

if year == '2017p8':
    qcd_samples = Samples.qcd_samples_2018[4:] + Samples.qcd_samples_2017[2:]
    ttbar_samples = Samples.ttbar_pl_samples_2017 + Samples.ttbar_pl_samples_2018
    signal_sample = Samples.mfv_neu_tau001000um_M0800_2017
    data_samples = [] # Samples.data_samples_2017
    background_samples = qcd_samples + ttbar_samples
    lumi = ac.int_lumi_2017p8 * ac.scale_factor_2017p8
    lumi_nice = ac.int_lumi_nice_2017p8

if year == 'run2':
    qcdlep_samples = Samples.qcd_lep_samples_20161[14:-1] + Samples.qcd_lep_samples_20162[14:-1] +  Samples.qcd_lep_samples_2017[14:-1] + Samples.qcd_lep_samples_2018[14:-1]
    qcdmupt5_samples = Samples.qcd_lep_samples_20161[1:13] + Samples.qcd_lep_samples_20162[1:13] + Samples.qcd_lep_samples_2017[1:13] + Samples.qcd_lep_samples_2018[1:13]
    ttbar_samples = Samples.ttbar_samples_20161[0:1] + Samples.ttbar_samples_20162[0:1] + Samples.ttbar_samples_2017[0:1] + Samples.ttbar_samples_2018[0:1]
    wjetstolnu_samples = Samples.leptonic_samples_20161[0:3] + Samples.leptonic_samples_20162[0:3] + Samples.leptonic_samples_2017[0:3] + Samples.leptonic_samples_2018[0:3]
    dyjets_samples = Samples.leptonic_samples_20161[3:-1] + Samples.leptonic_samples_20162[3:-1] + Samples.leptonic_samples_2017[3:-1] + Samples.leptonic_samples_2018[3:-1] 
    diboson_samples = Samples.diboson_samples_20161 + Samples.diboson_samples_20162 + Samples.diboson_samples_2017 + Samples.diboson_samples_2018
    qcd_samples = Samples.qcd_samples_20161 + Samples.qcd_samples_20162 + Samples.qcd_samples_2017 + Samples.qcd_samples_2018
    ttbar_samples = Samples.ttbar_samples_20161 + Samples.ttbar_samples_20162 + Samples.ttbar_samples_2017 + Samples.ttbar_samples_2018
    
    signal_sample = [Samples.mfv_neu_tau001000um_M0400_run2, Samples.mfv_stopdbardbar_tau001000um_M0200_run2, Samples.mfv_stopdbardbar_tau000300um_M0400_run2, Samples.ggHToSSTodddd_tau1mm_M55_run2]
    #data_samples = []
     
    #signal_sample = [Samples.VHToSSTodddd_tau1mm_M55_run2, Samples.VHToSSTodddd_tau10mm_M55_run2]
    data_samples = [] 
    
    #background_samples = wjetstolnu_samples + ttbar_samples + dyjets_samples + diboson_samples + qcdlep_samples + qcdmupt5_samples 
    background_samples = qcd_samples + ttbar_samples
    lumi = ac.int_lumi_run2
    lumi_nice = ac.int_lumi_nice_run2

for s in qcd_samples:
    s.join_info = True, 'Multijet events', ROOT.kBlue-9
for s in ttbar_samples:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7
for s in qcdlep_samples:
    s.join_info = True, 'Multijet events,EM enriched', ROOT.kAzure+7
for s in qcdmupt5_samples:
    s.join_info = True, 'Multijet events, #mu p_{T} > 5 GeV', ROOT.kAzure+10
for s in wjetstolnu_samples:
    s.join_info = True, 'W + jets #rightarrow l#nu', ROOT.kViolet+6
for s in dyjets_samples:
    s.join_info = True, 'DY + jets #rightarrow ll', ROOT.kPink+6
for s in diboson_samples:
    s.join_info = True, 'Diboson', ROOT.kRed


signal_samples = signal_sample
#signal_sample.nice_name = 'Signal: #sigma = 1 fb, c#tau = 1 mm, M = 300 GeV'
#signal_sample[0].nice_name = 'Z(#rightarrow #mu/e #bar{#mu}/#bar{e}) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}, c#tau = 1 mm, M = 55 GeV'
#signal_sample[0].nice_name = 'W/ZH #rightarrow SS #rightarrow d#bar{d}d#bar{d}, c#tau = 1 mm, M = 55 GeV'
signal_sample[0].nice_name = '#tilde{N} #rightarrow tbs: #sigma = 1 fb, c#tau = 1 mm, M = 400 GeV'
signal_sample[0].color = ROOT.kYellow + 2
#signal_sample[1].nice_name = 'Wplus(#rightarrow #mu/e #nu) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}, c#tau = 1 mm, M = 55 GeV'
#signal_sample[1].nice_name = 'W/ZH #rightarrow SS #rightarrow d#bar{d}d#bar{d}, c#tau = 10 mm, M = 55 GeV'
signal_sample[1].nice_name = '#tilde{t} #rightarrow #bar{d}#bar{d}: #sigma = 1 fb, c#tau = 1 mm, M = 200 GeV'
signal_sample[1].color = ROOT.kGreen + 2
#signal_sample[2].nice_name = 'Wminus(#rightarrow #mu/e #nu) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}, c#tau = 1 mm, M = 55 GeV'
signal_sample[2].nice_name = '#tilde{t} #rightarrow #bar{b}#bar{b}: #sigma = 1 fb, c#tau = 0.3 mm, M = 400 GeV'
signal_sample[2].color = ROOT.kGreen -3

signal_sample[3].nice_name = ' ggH #rightarrow SS #rightarrow d#bar{d}d#bar{d}, c#tau = 1 mm, M = 55 GeV'
signal_sample[3].color = ROOT.kAzure+10

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = [],
            plot_saver = ps,
            file_path = os.path.join(root_file_dir,'%(name)s.root'),
            int_lumi = lumi,
            int_lumi_nice = lumi_nice,
            canvas_top_margin = 0.08,
            poisson_intervals = True,
            legend_pos = (0.38, 0.68, 0.88, 0.88),
            enable_legend = True,
            res_fit = True,
            verbose = True,
            background_uncertainty = ('MC stat. uncertainty', 0, 1, 3254),
            preliminary = True,
            simulation = True,
            )

#C('ntuple_njets',
#  histogram_path = 'evtHst0VNoHt/h_njets',
#  x_title = 'Number of jets',
#  y_title = 'Events',
#  y_range = (1, 1e8),
#  )
#
#C('ntuple_ht40',
#  histogram_path = 'evtHst0VNoHt/h_jet_ht_40',
#  rebin = 4,
#  x_title = 'Jet H_{T} (GeV)',
#  y_title = 'Events/100 GeV',
#  y_range = (1, 1e8),
#  cut_line = ((1200, 0, 1200, 2.5e8), 2, 5, 1),
#  )
#
"""
('presel_njets',
 histogram_path = 'mfvEventHistosPreSel/h_njets',
 x_title = 'Number of jets',
 y_title = 'Events',
# y_range = (1, 1e8),
 )

('presel_nbjets',
 histogram_path = 'mfvEventHistosPreSel/h_nbtags_2',
 x_title = 'Number of tight bjets',
 y_title = 'Events',
# y_range = (1, 1e8),
 )
#
('presel_bjet_pt',
 histogram_path = 'mfvEventHistosPreSel/h_bjet_pt',
 x_title = 'bjet p_{T} (GeV)',
 y_title = 'Events',
# y_range = (1, 1e8),
 )
#
('presel_bjet_eta',
 histogram_path = 'mfvEventHistosPreSel/h_bjet_eta',
 x_title = 'bjet #eta',
 y_title = 'Events',
# y_range = (1, 1e8),
 )
#
('presel_bjet_phi',
 histogram_path = 'mfvEventHistosPreSel/h_bjet_phi',
 x_title = 'bjet #phi',
 y_title = 'Events',
# y_range = (1, 1e8),
 )
#
('presel_ht40',
 histogram_path = 'mfvEventHistosPreSel/h_jet_ht_40',
 rebin = 4,
 x_title = 'Jet H_{T} (GeV)',
 y_title = 'Events/100 GeV',
# y_range = (1, 1e8),
 )
#
C('presel_htall',
  histogram_path = 'mfvEventHistosPreSel/h_jet_ht',
  )
#
C('presel_jetpt1',
  histogram_path = 'mfvEventHistosPreSel/h_jetpt1',
#  y_range = (1,1e6),
  )
#
C('presel_jetpt4',
  histogram_path = 'mfvEventHistosPreSel/h_jetpt4',
#  y_range = (1,5e6),
  )
#
C('presel_jetpt',
  histogram_path = 'mfvEventHistosPreSel/h_jet_pt',
#  y_range = (1,5e7),
  )
#
C('presel_jeteta',
  histogram_path = 'mfvEventHistosPreSel/h_jet_eta',
  )
#
C('presel_jetphi',
  histogram_path = 'mfvEventHistosPreSel/h_jet_phi',
  )
#
C('presel_jetpairdphi',
  histogram_path = 'mfvEventHistosPreSel/h_jet_pairdphi',
  )
#
C('presel_met',
  histogram_path = 'mfvEventHistosPreSel/h_met',
  )
#
C('presel_metphi',
  histogram_path = 'mfvEventHistosPreSel/h_metphi',
  )
#
C('presel_nbtags_tight',
  histogram_path = 'mfvEventHistosPreSel/h_nbtags_tight',
  )
#
C('presel_nmuons_any',
  histogram_path = 'mfvEventHistosPreSel/h_nmuons_any',
  )
#
C('presel_nmuons_selected',
  histogram_path = 'mfvEventHistosPreSel/h_nmuons_selected',
  )
#
C('presel_nelectrons_any',
  histogram_path = 'mfvEventHistosPreSel/h_nelectrons_any',
  )
#
C('presel_nelectrons_selected',
  histogram_path = 'mfvEventHistosPreSel/h_nelectrons_selected',
  )
#
C('presel_npv',
  histogram_path = 'mfvEventHistosPreSel/h_npv',
#  y_range = (1,1e6),
  )
#
C('presel_pvntracks',
  histogram_path = 'mfvEventHistosPreSel/h_pvntracks',
  )
#
#C('presel_pvscore',
#  histogram_path = 'mfvEventHistosPreSel/h_pvscore',
#  )
#
#C('presel_pvrho',
#  histogram_path = 'mfvEventHistosPreSel/h_pvrho',
#  )
#
C('presel_nlep',
  histogram_path = 'mfvEventHistosPreSel/h_nleptons',
  )


#C('presel_nseedtracks',
#  histogram_path = 'mfvEventHistosPreSel/h_n_vertex_seed_tracks',
#  y_range = (1,1e7)
#  )
#
"""

#part2
"""
C('vertexerhistos_nm1_seedtrack_nsigmadxybs',
  histogram_path = 'mfvVertexTracks/h_seed_nm1_sigmadxybs',
  y_range = (1e5, 1e16),
  x_range = (0.0, 10.0),
  x_title = 'N#sigma(d_{xy})',
  cut_line = ((4, 0, 4, 2.8e16), 2, 5, 1),
  )

C('vertexerhistos_nm1_seedtrack_pt',
  histogram_path = 'mfvVertexTracks/h_seed_nm1_pt',
  y_range = (1e-1, 1e16),
  x_title = 'p_{t} (GeV)',
  cut_line = ((1, 0, 1, 2.8e16), 2, 5, 1),
  )

C('vertexerhistos_nm1_seedtrack_npxlayers',
  histogram_path = 'mfvVertexTracks/h_seed_nm1_npxlayers',
  y_range = (1e-1, 1e16),
  x_title = 'N pixel-layers',
  cut_line = ((2, 0, 2, 2.8e16), 2, 5, 1),
  )

C('vertexerhistos_nm1_seedtrack_nstlayers',
  histogram_path = 'mfvVertexTracks/h_seed_nm1_nstlayers',
  y_range = (1e-1, 1e16),
  x_title = 'N strip-layers',
  cut_line = ((6, 0, 6, 2.8e16), 2, 5, 1),
  )
C('vertexerhistos_seedtrack_eta',
  histogram_path = 'mfvVertexTracks/h_seed_track_eta',
  y_range = (1e6, 1e16),
  x_title = 'seed track #eta',
  )
C('vertexerhistos_alltrack_eta',
  histogram_path = 'mfvVertexTracks/h_all_track_eta',
  y_range = (1e7, 1e16),
  x_title = 'all track #eta',
  )
"""
#part3
"""
C('vertexerhistos_n_all_tracks',
  histogram_path = 'mfvVertexTracks/h_n_all_tracks',
  y_range = (1e-3, 2e8),
  x_title = 'Number of all tracks',
  y_title = 'Events',
  )
C('vertexerhistos_n_seed_tracks',
  histogram_path = 'mfvVertexTracks/h_n_seed_tracks',
  y_range = (1e-3, 6e8),
  x_range = (0, 60),
  x_title = 'Number of seed tracks',
  y_title = 'Events',
  )
"""
"""
C('presel_seedtrack_npxlayers',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_npxlayers',
  #y_range = (1,1e8),
  )

C('presel_seedtrack_nstlayers',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_nstlayers',
  #y_range = (1,1e8),
  )

C('presel_seedtrack_chi2dof',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_chi2dof',
  #y_range = (1,1e8),
  )

C('presel_seedtrack_pt',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_pt',
  #y_range = (1,1e8),
  )

C('presel_seedtrack_eta',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_eta',
  #y_range = (1,6e6),
  )

C('presel_seedtrack_phi',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_phi',
  #y_range = (1,6e6),
  )

C('presel_seedtrack_dxy',
  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_dxy',
  #y_range = (1,1e6),
  )
"""
#C('presel_seedtrack_dz',
#  histogram_path = 'mfvEventHistosPreSel/h_vertex_seed_track_dz',
#  y_range = (1,1e6),
#  )
#
#
#part1 starts here
C('onevtx_ntracks',
  histogram_path   = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
  #signal_hist_path = 'vtxHst2VNoNtracks/h_sv_all_ntracks',
  x_title = 'Number of tracks per vertex',
  y_title = 'Vertices',
  y_range = (1e-1, 1e7),
  cut_line = ((5, 0, 5, 2.3e7), 2, 5, 1),
  )

C('onevtx_bs2derr',
  histogram_path   = 'vtxHst1VNoBs2derr/h_sv_all_rescale_bs2derr',
  #signal_hist_path = 'vtxHst2VNoBs2derr/h_sv_all_bs2derr',
  rebin = 10,
  x_title = 'Uncertainty in d_{BV} (cm)',
  y_title = 'Vertices/5 #mum',
  y_range = (1e-1, 1e7),
  cut_line = ((0.0050, 0, 0.0050, 2.3e7), 2, 5, 1),
  )

C('onevtx_dbv',
  histogram_path   = 'vtxHst1VNoBsbs2ddist/h_sv_all_rescale_bsbs2ddist',
  #signal_hist_path = 'vtxHst2VNoBsbs2ddist/h_sv_all_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  x_range = (0, 1.0),
  y_range = (1e-1, 1e7),
  rebin = 4,
  cut_line = ((0.01, 0, 0.01, 2.3e7), 2, 5, 1),
  )

C('nsv_3track',
  histogram_path = 'Ntk3mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 3-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-1, 1e8),
  )

C('nsv_4track',
  histogram_path = 'Ntk4mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 4-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-1, 1e8),
  )

C('nsv_5track',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'Number of 5-or-more-track vertices',
  y_title = 'Events',
  x_range = (0, 8),
  y_range = (1e-1, 1e8),
  cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
  )

C('nbtags_0_presel',
  histogram_path = 'mfvEventHistosPreSel/h_nbtags_0',
  x_title = 'Number of loose btagged jets',
  y_title = 'Events',
  x_range = (0, 10),
  y_range = (1e-1, 1e8),
  )

C('nbtags_1_presel',
  histogram_path = 'mfvEventHistosPreSel/h_nbtags_1',
  x_title = 'Number of medium btagged jets',
  y_title = 'Events',
  x_range = (0, 10),
  y_range = (1e-1, 1e8),
  )

C('nbtags_2_presel',
  histogram_path = 'mfvEventHistosPreSel/h_nbtags_2',
  x_title = 'Number of tight btagged jets',
  y_title = 'Events',
  x_range = (0, 10),
  y_range = (1e-1, 1e8),
  )

C('dbv_1v_3track',
  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_rescale_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  rebin = 4,
  x_range = (0, 1.0),
  y_range = (1e-1, 1e7),
  )

C('dbv_1v_4track',
  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_rescale_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  rebin = 4,
  x_range = (0, 1.0),
  y_range = (1e-1, 1e7),
  )

C('dbv_1v_5track',
  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_rescale_bsbs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'Vertices/50 #mum',
  rebin = 4,
  x_range = (0, 1.0),
  y_range = (1e-1, 1e7),
  )
#
#C('dbv',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e4),
#  )
#
#C('dvv',
#  histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 10,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/200 #mum',
#  y_range = (1e-2, 10),
#  )
if year == '2018':
    C('track_pt',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_pt',
      x_title = 'Track p_{T} (GeV)',
      y_title = 'Tracks/0.1 GeV',
      y_range = (1, 1e10),
      cut_line = ((1, 0, 1, 2.8e10), 2, 5, 1),
      )

    C('track_min_r',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_min_r',
      x_title = 'Minimum layer number',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
      )

    C('track_npxlayers',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_npxlayers',
      x_title = 'Number of pixel layers',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((2, 0, 2, 2.8e10), 2, 5, 1),
      )

    C('track_nstlayers',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_nstlayers',
      x_title = 'Number of strip layers',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((6, 0, 6, 2.8e10), 2, 5, 1),
      )

    C('track_nstlayers_etalt2',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_nstlayers_etalt2',
      x_title = 'Number of strip layers (|#eta| < 2)',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((6, 0, 6, 2.8e10), 2, 5, 1),
      )

    C('track_nstlayers_etagt2',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_nstlayers_etagt2',
      x_title = 'Number of strip layers (|#eta| #geq 2)',
      y_title = 'Tracks',
      y_range = (1, 1e10),
      cut_line = ((7, 0, 7, 2.8e10), 2, 5, 1),
      )

    C('track_nsigmadxy',
      histogram_path = 'TrackerMapper/h_nm1_seed_tracks_nsigmadxy',
      x_title = 'N#sigma(d_{xy})',
      y_title = 'Tracks',
      x_range = (0, 10),
      y_range = (1, 1e10),
      cut_line = ((4, 0, 4, 2.8e10), 2, 5, 1),
      )



#C('100pc_3t1v_ntracks',
#  histogram_path = 'Ntk3vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_bs2derr',
#  histogram_path = 'Ntk3vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_dbv',
#  histogram_path = 'Ntk3vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_3t1v_onevtx_dbv',
#  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_3t1v_onevtx_dbv_unzoom',
#  histogram_path = 'Ntk3mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_3t2v_dvv',
#  histogram_path = 'Ntk3mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  )
#
#C('100pc_4t1v_ntracks',
#  histogram_path = 'Ntk4vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_bs2derr',
#  histogram_path = 'Ntk4vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_dbv',
#  histogram_path = 'Ntk4vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_4t1v_onevtx_dbv',
#  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_4t1v_onevtx_dbv_unzoom',
#  histogram_path = 'Ntk4mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_4t2v_dvv',
#  histogram_path = 'Ntk4mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  res_fit = False,
#  )
#
#C('100pc_5t1v_ntracks',
#  histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
#  x_title = 'Number of tracks per vertex',
#  y_title = 'Vertices',
#  y_range = (1, 1e6),
#  cut_line = ((5, 0, 5, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_bs2derr',
#  histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
#  x_title = 'Uncertainty in d_{BV} (cm)',
#  y_title = 'Vertices/5 #mum',
#  y_range = (1, 1e6),
#  cut_line = ((0.0025, 0, 0.0025, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_dbv',
#  histogram_path = 'vtxHst1VNoBsbs2ddist/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  cut_line = ((0.01, 0, 0.01, 2.1e6), 2, 5, 1),
#  )
#
#C('100pc_5t1v_onevtx_dbv',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  x_range = (0, 0.4),
#  y_range = (1, 1e6),
#  )
#
#C('100pc_5t1v_onevtx_dbv_unzoom',
#  histogram_path = 'mfvVertexHistosOnlyOneVtx/h_sv_all_bsbs2ddist',
#  x_title = 'd_{BV} (cm)',
#  y_title = 'Vertices/50 #mum',
#  y_range = (1, 1e6),
#  )
#
#C('100pc_5t2v_dvv',
#  histogram_path = 'mfvVertexHistosFullSel/h_svdist2d',
#  rebin = 5,
#  x_title = 'd_{VV} (cm)',
#  y_title = 'Events/100 #mum',
#  x_range = (0, 0.4),
#  y_range = (1e-1, 1e3),
#  res_fit = False,
#  )

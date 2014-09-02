#!/usr/bin/env python

import os,sys
import JMTucker.MFVNeutralino.AnalysisConstants as ac

verbose = True
root_file_dir = '/uscms_data/d2/tucker/crab_dirs/mfv_535/HistosV19'
plot_dir = os.path.join('plots', os.path.basename(root_file_dir))
event_histo_path = 'mfvEventHistosOnlyOneVtx'
vertex_histo_path = 'mfvVertexHistosOnlyOneVtx'
hist_path_for_nevents_check = None # 'mfvEventHistosNoCuts/h_npu',
plot_size = (600,600)
scale_factor = ac.scale_factor * 186076.0 / 137183.984375

################################################################################

from functools import partial
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver
import JMTucker.Tools.Samples as Samples

set_style()
ps = plot_saver(plot_dir, size=plot_size)

data_samples = Samples.data_samples

#background_samples = Samples.smaller_background_samples + Samples.ttbar_samples + Samples.qcd_samples #+ Samples.leptonic_background_samples
background_samples = Samples.ttbar_samples + Samples.qcd_samples #+ Samples.leptonic_background_samples
for sample in background_samples:
    sample.total_events = sample.nevents_orig/2

#signal_samples = [Samples.mfv_neutralino_tau0300um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]
signal_samples = [Samples.mfv_neutralino_tau1000um_M0400]
Samples.mfv_neutralino_tau0300um_M0400.nice_name = '#tau = 300 #mum, M = 400 GeV signal'
Samples.mfv_neutralino_tau1000um_M0400.nice_name = '#tau = 1 mm, M = 400 GeV signal'
Samples.mfv_neutralino_tau9900um_M0400.nice_name = '#tau = 10 mm, M = 400 GeV signal'
Samples.mfv_neutralino_tau0300um_M0400.color = 6
Samples.mfv_neutralino_tau1000um_M0400.color = 8
Samples.mfv_neutralino_tau9900um_M0400.color = 2

for s in Samples.qcdht0100, Samples.qcdht0250, Samples.qcdht0500, Samples.qcdht1000:
    s.join_info = True, 'QCD', ROOT.kBlue-9 # Samples.qcdht0100.color
for s in Samples.ttbardilep, Samples.ttbarsemilep, Samples.ttbarhadronic:
    s.join_info = True, 't#bar{t}', ROOT.kBlue-7 # Samples.ttbardilep.color
for s in Samples.leptonic_background_samples + Samples.auxiliary_background_samples:
     s.join_info = True, 'other', ROOT.kBlue-5
for s in Samples.smaller_background_samples:
     s.join_info = True, 'other', ROOT.kBlue-3

    
if verbose:
    print 'weights:'
    for sample in background_samples:
        print (sample.name, sample.nevents, sample.nevents_orig, sample.cross_section, sample.partial_weight*ac.int_lumi)

B = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = ac.int_lumi,
            background_uncertainty = ('Uncert. on MC bkg', 0.2, ROOT.kBlack, 3004),
            hist_path_for_nevents_check = hist_path_for_nevents_check,
            overflow_in_last = True,
            poisson_intervals = True,
            enable_legend = True,
            verbose = verbose,
            )

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,            
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = ac.int_lumi * scale_factor,
            int_lumi_nice = ac.int_lumi_nice,
            background_uncertainty = ('Uncert. on MC bkg', 0.2, ROOT.kBlack, 3004),
            hist_path_for_nevents_check = hist_path_for_nevents_check,
            overflow_in_last = True,
            poisson_intervals = True,
            enable_legend = False,
            verbose = verbose,
            )

def event_histo(s):
    return event_histo_path + '/' + s
def vertex_histo(s):
    return vertex_histo_path + '/' + s

signalmccomp = [x.strip() for x in '''
calojetpt4_nocuts
jetsumht_nocuts
nsv
sv_all_ntracks_nm1
sv_all_ntracksptgt3_nm1
sv_all_tksjetsntkmass
sv_all_drmin_nm1
sv_all_maxdrmax_nm1
sv_all_mindrmax_nm1
sv_all_njetsntks_nm1
sv_all_bs2ddist
sv_all_bs2derr_nm1
sv_all_svdist2d
'''.split('\n') if not x.strip().startswith('#')]

datamccomp = [x.strip() for x in '''
npv
ncalojets
calojetpt1
calojetpt2
calojetpt3
calojetpt4
calojetpt5
npfjets
pfjetpt1
pfjetpt2
pfjetpt3
pfjetpt4
pfjetpt5
jetsumht
sv_best0_ntracks_nm1
sv_best0_ntracksptgt3_nm1
sv_best0_njetsntks_nm1
sv_best0_drmin_nm1
sv_best0_drmax_nm1
sv_best0_bs2ddist
sv_best0_bs2derr_nm1
'''.split('\n') if not x.strip().startswith('#')]

def D(*args, **kwargs):
    if (args[0] in signalmccomp):
        B(*args, **kwargs)
    if (args[0] in datamccomp):
        C(*args, **kwargs)

################################################################################

D('npv',
  histogram_path = event_histo('h_npv'),
  x_title = 'number of PV',
  y_title = 'events/2',
  x_range = (0, 40),
  y_range = (None, 50000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('ncalojets',
  histogram_path = event_histo('h_ncalojets'),
  x_title = 'number of calorimeter jets',
  y_title = 'events',
  x_range = (3,16),
  y_range = (None, 70000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt1',
  histogram_path = event_histo('h_calojetpt1'),
  x_title = 'calorimeter jet #1 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  y_range = (None, 16000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt2',
  histogram_path = event_histo('h_calojetpt2'),
  x_title = 'calorimeter jet #2 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  y_range = (None, 25000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt3',
  histogram_path = event_histo('h_calojetpt3'),
  x_title = 'calorimeter jet #3 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (50,250),
  y_range = (None, 50000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt4',
  histogram_path = event_histo('h_calojetpt4'),
  x_title = 'calorimeter jet #4 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (50,250),
  y_range = (None, 70000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt5',
  histogram_path = event_histo('h_calojetpt5'),
  x_title = 'calorimeter jet #5 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (0,250),
  y_range = (None, 35000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('npfjets',
  histogram_path = event_histo('h_njets'),
  x_title = 'number of particle-flow jets',
  y_title = 'events',
  x_range = (3,16),
  y_range = (None, 70000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt1',
  histogram_path = event_histo('h_jetpt1'),
  x_title = 'particle-flow jet #1 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  y_range = (None, 16000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt2',
  histogram_path = event_histo('h_jetpt2'),
  x_title = 'particle-flow jet #2 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  y_range = (None, 25000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt3',
  histogram_path = event_histo('h_jetpt3'),
  x_title = 'particle-flow jet #3 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (50,250),
  y_range = (None, 50000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt4',
  histogram_path = event_histo('h_jetpt4'),
  x_title = 'particle-flow jet #4 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (50,250),
  y_range = (None, 50000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt5',
  histogram_path = event_histo('h_jetpt5'),
  x_title = 'particle-flow jet #5 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (0,250),
  y_range = (None, 35000),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('jetsumht',
  histogram_path = event_histo('h_jet_sum_ht'),
  rebin = 4,
  x_title = 'particle-flow jet #Sigma H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (400, 2500),
  y_range = (None, 80000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('sv_best0_ntracks_nm1',
  histogram_path = 'vtxHstOnly1VNoNtracks/h_sv_best0_ntracks',
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  x_range = (2, 20),
  y_range = (None, 60000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((5.,0.0,5.,63000),ROOT.kRed,5,1),
  )

D('sv_best0_ntracksptgt3_nm1',
  histogram_path = 'vtxHstOnly1VNoNtracksptgt3/h_sv_best0_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (0, 9),
  y_range = (None, 350000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((3.,0.0,3.,367000),ROOT.kRed,5,1),
  )

D('sv_best0_drmin_nm1',
  histogram_path = 'vtxHstOnly1VNoDrmin/h_sv_best0_drmin',
  rebin = 4,
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.04',
  x_range = (0, 0.6),
  y_range = (None, 60000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((0.4,0.0,0.4,63000),ROOT.kRed,5,1),
  )

D('sv_best0_drmax_nm1',
  histogram_path = 'vtxHstOnly1VNoDrmax/h_sv_best0_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  y_range = (None, 70000),
  legend_pos = (0.13, 0.70, 0.43, 0.90),
  cut_line = ((4,0.0,4,73500),ROOT.kRed,5,1),
  )

D('sv_best0_njetsntks_nm1',
  histogram_path = 'vtxHstOnly1VNoNjets/h_sv_best0_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  y_range = (None, 120000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((1.,0.0,1.,126000),ROOT.kRed,5,1),
  )

D('sv_best0_bs2ddist',
  histogram_path = vertex_histo('h_sv_best0_bs2ddist'),
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  x_range = (0, 0.1),
  y_range = (None, 180e3),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('sv_best0_bs2derr_nm1',
  histogram_path = 'vtxHstOnly1VNoBs2derr/h_sv_best0_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.01),
  y_range = (None, 140000),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((0.0025,0.0,0.0025,147000),ROOT.kRed,5,1),
  )

################################################################################

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 10000
D('calojetpt4_nocuts',
  histogram_path = 'mfvEventHistosNoCuts/h_calojetpt4',
  x_title = 'calorimeter jet #4 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (0,250),
  y_range = (None, 250e6),
  rebin = 2,
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((60, 0, 60, 262e6), 2, 5, 1),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 10000
D('jetsumht_nocuts',
  histogram_path = 'mfvEventHistosNoCuts/h_jet_sum_ht',
  rebin = 4,
  x_title = 'particle-flow jet #Sigma H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (0, 3000),
  y_range = (None, 250e6),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((500, 0, 500, 262e6), 2, 5, 1),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('nsv',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'number of vertices',
  y_title = 'events',
  x_range = (0,5),
  y_range = (1, 1e8),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_ntracks_nm1',
  histogram_path = 'vtxHst1VNoNtracks/h_sv_all_ntracks',
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  y_range = (None, 50000),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((5, 0, 5, 52500), 2, 5, 1),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_ntracksptgt3_nm1',
  histogram_path = 'vtxHst1VNoNtracksptgt3/h_sv_all_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (0, 20),
  y_range = (None, 300000),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((3, 0, 3, 315000), 2, 5, 1),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 1
D('sv_all_tksjetsntkmass',
  histogram_path = 'mfvVertexHistosOneVtx/h_sv_all_tksjetsntkmass',
  rebin = 6,
  x_title = 'tracks + associated jets\' mass (GeV)',
  y_title = 'vertices/90 GeV',
  y_range = (None, 25000),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_drmin_nm1',
  histogram_path = 'vtxHst1VNoDrmin/h_sv_all_drmin',
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.08',
  rebin = 8,
  y_range = (None, 250000),
  cut_line = ((0.4, 0, 0.4, 262500), 2, 5, 1),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_maxdrmax_nm1',
  histogram_path = 'vtxHst1VNoDrmax/h_sv_all_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  y_range = (None, 100000),
  cut_line = ((4, 0, 4, 105000), 2, 5, 1),
  legend_pos = (0.5, 0.67, 0.87, 0.87),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_mindrmax_nm1',
  histogram_path = 'vtxHst1VNoMindrmax/h_sv_all_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  y_range = (None, 100000),
  cut_line = ((1.2, 0, 1.2, 105000), 2, 5, 1),
  legend_pos = (0.5, 0.67, 0.87, 0.87),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_njetsntks_nm1',
  histogram_path = 'vtxHst1VNoNjets/h_sv_all_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  y_range = (None, 100000),
  cut_line = ((1, 0, 1, 105000), 2, 5, 1),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_bs2ddist',
  histogram_path = 'mfvVertexHistosOneVtx/h_sv_all_bs2ddist',
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  x_range = (0, 0.1),
  y_range = (None, 150e3),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 17.4
D('sv_all_bs2derr_nm1',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_all_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.01),
  y_range = (None, 150000),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((0.0025, 0, 0.0025, 157000), 2, 5, 1),
  )

Samples.mfv_neutralino_tau1000um_M0400.cross_section = 0.1
D('sv_all_svdist2d',
  histogram_path = 'mfvVertexHistosWAnaCuts/h_svdist2d',
  x_title = 'd_{VV} (cm)',
  y_title = 'events/0.01 cm',
  x_range = (0,0.3),
  y_range = (None, 125),
  rebin = 5,
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

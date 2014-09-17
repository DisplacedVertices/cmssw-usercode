#!/usr/bin/env python

import os,sys
import JMTucker.MFVNeutralino.AnalysisConstants as ac

verbose = True
root_file_dir = '/uscms_data/d2/tucker/crab_dirs/mfv_535/HistosV20'
event_histo_path = 'mfvEventHistos'
vertex_histo_path = 'mfvVertexHistosWAnaCuts'
plot_dir = os.path.join('plots', os.path.basename(root_file_dir), event_histo_path)
hist_path_for_nevents_check = None # 'mfvEventHistosNoCuts/h_npu',
plot_size = (600,600)
scale_factor = ac.scale_factor * 251.0 / 139.30171468 #* 181076.0 / 135591.837455

################################################################################

from functools import partial
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver
import JMTucker.Tools.Samples as Samples

set_style()
ps = plot_saver(plot_dir, size=plot_size)

data_samples = Samples.data_samples

background_samples = Samples.smaller_background_samples + Samples.leptonic_background_samples + Samples.ttbar_samples + Samples.qcd_samples

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
for s in Samples.auxiliary_background_samples:
     s.join_info = True, 'other', ROOT.kBlue-5
for s in Samples.smaller_background_samples + Samples.leptonic_background_samples:
     s.join_info = True, 'other', ROOT.kBlue-3

    
if verbose:
    print 'weights:'
    for sample in background_samples:
        print (sample.name, sample.nevents, sample.nevents_orig, sample.cross_section, sample.partial_weight*ac.int_lumi)

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

enabled = [x.strip() for x in '''
#npv
#ncalojets
#calojetpt1
#calojetpt2
#calojetpt3
#calojetpt4
#calojetpt5
#npfjets
#pfjetpt1
#pfjetpt2
#pfjetpt3
#pfjetpt4
#pfjetpt5
#jetsumht
#sv_best0_ntracks_nm1
#sv_best0_ntracksptgt3_nm1
#sv_best0_njetsntks_nm1
#sv_best0_drmin_nm1
#sv_best0_drmax_nm1
#sv_best0_bs2ddist
#sv_best0_bs2derr_nm1
npv
calojetpt4
jetsumht
nsv
sv_all_ntracks_nm1
sv_all_ntracksptgt3_nm1
sv_all_drmin_nm1
sv_all_maxdrmax_nm1
sv_all_mindrmax_nm1
sv_all_njetsntks_nm1
sv_all_bsbs2ddist
sv_all_bs2derr_nm1
sv_all_svdist2d
'''.split('\n') if not x.strip().startswith('#')]

def is_enabled(s):
    return s in enabled # or s.startswith('clean')

def D(*args, **kwargs):
    if is_enabled(args[0]):
        C(*args, **kwargs)

################################################################################

D('npv',
  histogram_path = event_histo('h_npv'),
  x_title = 'number of PV',
  y_title = 'events/2',
  x_range = (0, 40),
  rebin = 2,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('ncalojets',
  histogram_path = event_histo('h_ncalojets'),
  x_title = 'number of calorimeter jets',
  y_title = 'events',
  x_range = (3,16),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt1',
  histogram_path = event_histo('h_calojetpt1'),
  x_title = 'calorimeter jet #1 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (50,500),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt2',
  histogram_path = event_histo('h_calojetpt2'),
  x_title = 'calorimeter jet #2 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (50,500),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt3',
  histogram_path = event_histo('h_calojetpt3'),
  x_title = 'calorimeter jet #3 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (50,500),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt4',
  histogram_path = event_histo('h_calojetpt4'),
  x_title = 'calorimeter jet #4 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (50,250),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('calojetpt5',
  histogram_path = event_histo('h_calojetpt5'),
  x_title = 'calorimeter jet #5 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (0,250),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('npfjets',
  histogram_path = event_histo('h_njets'),
  x_title = 'number of particle-flow jets',
  y_title = 'events',
  x_range = (3,16),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt1',
  histogram_path = event_histo('h_jetpt1'),
  x_title = 'particle-flow jet #1 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt2',
  histogram_path = event_histo('h_jetpt2'),
  x_title = 'particle-flow jet #2 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt3',
  histogram_path = event_histo('h_jetpt3'),
  x_title = 'particle-flow jet #3 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt4',
  histogram_path = event_histo('h_jetpt4'),
  x_title = 'particle-flow jet #4 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (0,250),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('pfjetpt5',
  histogram_path = event_histo('h_jetpt5'),
  x_title = 'particle-flow jet #5 p_{T} (GeV)',
  y_title = 'events/20 GeV',
  x_range = (0,250),
  rebin = 4,
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('jetsumht',
  histogram_path = event_histo('h_jet_sum_ht'),
  rebin = 4,
  x_title = 'particle-flow jet #Sigma H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (400, 2500),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('sv_best0_ntracks_nm1',
  histogram_path = 'vtxHstOnly1VNoNtracks/h_sv_best0_ntracks',
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  x_range = (2, 20),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((5.,0.0,5.,52200),ROOT.kRed,5,1),
  )

D('sv_best0_ntracksptgt3_nm1',
  histogram_path = 'vtxHstOnly1VNoNtracksptgt3/h_sv_best0_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (0, 9),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((3.,0.0,3.,380000),ROOT.kRed,5,1),
  )

D('sv_best0_drmin_nm1',
  histogram_path = 'vtxHstOnly1VNoDrmin/h_sv_best0_drmin',
  rebin = 4,
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.04',
  x_range = (0, 0.6),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((0.4,0.0,0.4,67700),ROOT.kRed,5,1),
  )

D('sv_best0_drmax_nm1',
  histogram_path = 'vtxHstOnly1VNoDrmax/h_sv_best0_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  legend_pos = (0.13, 0.70, 0.43, 0.90),
  cut_line = ((4,0.0,4,71800),ROOT.kRed,5,1),
  )

D('sv_best0_njetsntks_nm1',
  histogram_path = 'vtxHstOnly1VNoNjets/h_sv_best0_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((1.,0.0,1.,128000),ROOT.kRed,5,1),
  )

D('sv_best0_bs2ddist',
  histogram_path = vertex_histo('h_sv_best0_bs2ddist'),
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  x_range = (0, 0.1),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  )

D('sv_best0_bs2derr_nm1',
  histogram_path = 'vtxHstOnly1VNoBs2derr/h_sv_best0_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.01),
  legend_pos = (0.47, 0.70, 0.87, 0.90),
  cut_line = ((0.0025,0.0,0.0025,148000),ROOT.kRed,5,1),
  )

################################################################################

D('calojetpt4_nocuts',
  histogram_path = 'mfvEventHistosNoCuts/h_calojetpt4',
  x_title = 'calorimeter jet #4 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (0,250),
  rebin = 2,
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((60, 0, 60, 205e6), 2, 5, 1),
  )

D('jetsumht_nocuts',
  histogram_path = 'mfvEventHistosNoCuts/h_jet_sum_ht',
  rebin = 4,
  x_title = 'particle-flow jet #Sigma H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (0, 3000),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((500, 0, 500, 200e6), 2, 5, 1),
  )

D('nsv',
  histogram_path = 'mfvVertexHistosPreSel/h_nsv',
  x_title = 'number of vertices',
  y_title = 'events',
  x_range = (0,5),
  y_range = (1, 1e8),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((2, 0, 2, 2.5e8), 2, 5, 1),
  )

D('sv_all_ntracks_nm1',
  histogram_path = 'vtxHst2VNoNtracks/h_sv_all_ntracks',
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((5, 0, 5, 440), 2, 5, 1),
  )

D('sv_all_ntracksptgt3_nm1',
  histogram_path = 'vtxHst2VNoNtracksptgt3/h_sv_all_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (0, 20),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((3, 0, 3, 2970), 2, 5, 1),
  )

D('sv_all_tksjetsntkmass',
  histogram_path = vertex_histo('h_sv_all_tksjetsntkmass'),
  rebin = 6,
  x_title = 'tracks + associated jets\' mass (GeV)',
  y_title = 'vertices/90 GeV',
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

D('sv_all_drmin_nm1',
  histogram_path = 'vtxHst2VNoDrmin/h_sv_all_drmin',
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.08',
  rebin = 8,
  cut_line = ((0.4, 0, 0.4, 435), 2, 5, 1),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

D('sv_all_maxdrmax_nm1',
  histogram_path = 'vtxHst2VNoDrmax/h_sv_all_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  cut_line = ((4, 0, 4, 333), 2, 5, 1),
  legend_pos = (0.13, 0.70, 0.43, 0.90),
  )

D('sv_all_mindrmax_nm1',
  histogram_path = 'vtxHst2VNoMindrmax/h_sv_all_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  cut_line = ((1.2, 0, 1.2, 163), 2, 5, 1),
  legend_pos = (0.13, 0.70, 0.43, 0.90),
  )

D('sv_all_njetsntks_nm1',
  histogram_path = 'vtxHst2VNoNjets/h_sv_all_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  cut_line = ((1, 0, 1, 352), 2, 5, 1),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

D('sv_all_bsbs2ddist',
  histogram_path = vertex_histo('h_sv_all_bsbs2ddist'),
  x_title = 'd_{BV} (cm)',
  y_title = 'vertices/50 #mum',
  x_range = (0, 0.1),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

D('sv_all_bs2derr_nm1',
  histogram_path = 'vtxHst2VNoBs2derr/h_sv_all_bs2derr',
  x_title = '#sigma(d_{BV}) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.01),
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  cut_line = ((0.0025, 0, 0.0025, 960), 2, 5, 1),
  )

D('sv_all_svdist2d',
  histogram_path = vertex_histo('h_svdist2d'),
  x_title = 'd_{VV} (cm)',
  y_title = 'events/0.01 cm',
  x_range = (0,0.3),
  rebin = 10,
  legend_pos = (0.47, 0.67, 0.87, 0.87),
  )

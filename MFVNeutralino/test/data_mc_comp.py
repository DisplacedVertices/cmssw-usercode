#!/usr/bin/env python

import os

verbose = True
root_file_dir = 'crab/HistosV18_Data0'
plot_dir = os.path.join('plots', os.path.basename(root_file_dir)) # 'plots/MFVHistosV17SideBandBetterPUweights'
event_histo_path = 'mfvEventHistosOnlyOneVtx'
vertex_histo_path = 'mfvVertexHistosOnlyOneVtx'
hist_path_for_nevents_check = None # 'mfvEventHistosNoCuts/h_npu',
plot_size = (600,600)
int_lumi = 18200. # /pb
int_lumi_nice = '18.2 fb^{-1}'
scale_factor = 1970/682.47/2

################################################################################

from functools import partial
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver
import JMTucker.Tools.Samples as Samples

set_style()
ps = plot_saver(plot_dir, size=plot_size)

data_samples = Samples.data_samples

background_samples = Samples.ttbar_samples + Samples.qcd_samples
for sample in background_samples:
    sample.total_events = sample.nevents_orig/2

signal_samples = [Samples.mfv_neutralino_tau0300um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]
#signal_samples = [Samples.mfv_neutralino_tau1000um_M0400]
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

if verbose:
    print 'weights:'
    for sample in background_samples:
        print (sample.name, sample.nevents, sample.nevents_orig, sample.cross_section, sample.partial_weight*int_lumi)

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_samples = data_samples,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = int_lumi * scale_factor,
            int_lumi_nice = int_lumi_nice,
            background_uncertainty = ('Stat. uncert. on MC bkg', None, ROOT.kBlack, 3004),
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
npv
#pvntracks
#pvsumpt2
#pvrho
#pvz
njets
#njetsnoputight
jetpt4
#jetpt5
#jetpt6
jetsumht
#nbtags
#nsemimuons
#nsemielectrons
#nsemileptons
#nsvnocut
nsv
sv_best0_ntracks
sv_best0_ntracksptgt3
sv_best0_njetsntks
sv_best0_drmin
sv_best0_drmax
sv_best0_bs2derr
'''.split('\n') if not x.strip().startswith('#')]

def is_enabled(s):
#    return not s.startswith('clean')
    return s in enabled # or s.startswith('clean')

def D(*args, **kwargs):
    if is_enabled(args[0]):
        C(*args, **kwargs)

################################################################################

for i in xrange(20):
    D('clean%i' % i,
      histogram_path = event_histo('h_pass_clean_%i' % i),
      legend_pos = (0.435, 0.687, 0.878, 0.920)
      )

D('npv',
  histogram_path = event_histo('h_npv'),
  x_title = 'number of PV',
  y_title = 'events/2',
  x_range = (0, 40),
  #y_range = (None, 350),
  rebin = 2,
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('pvntracks',
  histogram_path = event_histo('h_pv_ntracks'),
  rebin = 10,
  x_title = 'number of tracks in PV',
  y_title = 'events/10',
  y_range = (None, 450),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('pvsumpt2',
  histogram_path = event_histo('h_pv_sumpt2'),
  rebin = 10,
  x_title = '#Sigma p_{T}^{2} of tracks in PV (GeV^{2})',
  y_title = 'events/1000 GeV^{2}',
  y_range = (None, 400),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('pvrho',
  histogram_path = event_histo('h_pv_rho'),
  x_title = 'PV #rho (cm)',
  y_title = 'events/??0.005 cm',
  x_range = (0, 0.01),
  y_range = (None, 400),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('pvz',
  histogram_path = event_histo('h_pvz'),
  x_title = 'PV z (cm)',
  y_title = 'events/1.5 cm',
  rebin = 10,
  y_range = (None, 250),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('njets',
  histogram_path = event_histo('h_njets'),
  x_title = 'number of jets',
  y_title = 'events',
  x_range = (4,16),
  #y_range = (None, 660),
  legend_pos = (0.572, 0.687, 0.884, 0.920),
  )

D('njetsnoputight',
  histogram_path = event_histo('h_njetsnopu_tight'),
  x_title = 'number of jets (tight PU id)',
  y_title = 'events',
  x_range = (4,16),
  y_range = (None, 650),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('jetpt4',
  histogram_path = event_histo('h_jetpt4'),
  x_title = 'jet #4 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (60,250),
  #y_range = (None, 550),
  rebin = 2,
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('jetpt5',
  histogram_path = event_histo('h_jetpt5'),
  x_title = 'jet #5 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  x_range = (60,250),
  y_range = (None, 330),
  rebin = 2,
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('jetpt6',
  histogram_path = event_histo('h_jetpt6'),
  x_title = 'jet #6 p_{T} (GeV)',
  y_title = 'events/10 GeV',
  rebin = 2,
  x_range = (60,250),
  y_range = (None, 100),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('jetsumht',
  histogram_path = event_histo('h_jet_sum_ht'),
  rebin = 4,
  x_title = '#Sigma H_{T} (GeV)',
  y_title = 'events/100 GeV',
  x_range = (500, 3000),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('nbtags',
  histogram_path = event_histo('h_nbtags_medium'),
  x_title = '# CSVM b-tagged jets',
  y_title = 'events',
  x_range = (0,10),
  y_range = (None, 950),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('nsemimuons',
  histogram_path = event_histo('h_nmuons_semilep'),
  x_title = 'number of semilep muons',
  y_title = 'events',
  y_range = (None, 2200),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('nsemielectrons',
  histogram_path = event_histo('h_nelectrons_semilep'),
  x_title = 'number of semilep electrons',
  y_title = 'events',
  y_range = (None, 2200),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('nsemileptons',
  histogram_path = event_histo('h_nleptons_semilep'),
  x_title = 'number of semilep leptons',
  y_title = 'events',
  y_range = (None, 2200),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('nsvnocut',
  histogram_path = 'mfvVertexHistosTrigCut/h_nsv',
  x_title = 'number of vertices',
  y_title = 'events/(20 fb^{-1})',
  x_range = (0,5),
  legend_pos = (0.424, 0.631, 0.868, 0.865),
  )

if 0:
    D('svdist2d',
  histogram_path = 'vtxHst2VNoSvdist2d/h_svdist2d',
  x_title = 'xy distance between top two vertices (cm)',
  y_title = 'events/(0.01 cm)/(20 fb^{-1})',
  x_range = (0,0.3),
  y_range = (0,4),
  int_lumi_nice = None,
  overflow_in_last = True,
  rebin = 5,
  background_uncertainty = ('Stat. uncert. on MC bkg', None, ROOT.kBlack, 3004),
  cut_line = ((0.04, 0, 0.04, 4.2), 2, 5, 1),
  legend_pos = (0.424, 0.631, 0.868, 0.865),
  )

    D('ntracks01',
  histogram_path = 'vtxHst2VNoNtracks01/h_sv_sumtop2_ntracks',
  x_title = 'sum of number of tracks in top two vertices',
  y_title = 'events/(20 fb^{-1})',
  x_range = (10,35),
  y_range = (0.02, 40),
  int_lumi_nice = None,
  overflow_in_last = True,
  background_uncertainty = ('Stat. uncert. on MC bkg', None, ROOT.kBlack, 3004),
  cut_line = ((16, 0, 16, 64), 2, 5, 1),
  legend_pos = (0.424, 0.631, 0.868, 0.865),
  )

D('nsv',
  histogram_path = vertex_histo('h_nsv'),
  x_title = 'number of SV',
  y_title = 'events',
  x_range = (1,5),
  #y_range = (None, 2200),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_best0_ntracks',
  histogram_path = vertex_histo('h_sv_best0_ntracks'),
  x_title = 'number of tracks/vertex',
  y_title = 'vertices',
  x_range = (5, 8),
  #y_range = (None, 900),
  legend_pos = (0.435, 0.687, 0.878, 0.920)
  )

D('sv_best0_ntracksptgt3',
  histogram_path = vertex_histo('h_sv_best0_ntracksptgt3'),
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (3, 9),
  #y_range = (None, 1800),
  legend_pos = (0.553, 0.687, 0.878, 0.920)
  )

D('sv_top2_ntracksptgt3_nm1',
  histogram_path = 'vtxHst1VNoNtracksptgt3/h_sv_top2_ntracksptgt3',
  x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
  y_title = 'vertices',
  x_range = (0, 9),
  y_range = (None, 3500),
  legend_pos = (0.553, 0.687, 0.878, 0.920)
  )

D('sv_top2_chi2dof',
  histogram_path = vertex_histo('h_sv_top2_chi2dof'),
  x_title = '#chi^{2}/dof for vertex fit',
  y_title = 'vertices/0.14',
  x_range = (0, 5),
  rebin = 2,
  y_range = (None, 260),
  legend_pos = (0.435, 0.687, 0.878, 0.920)
  )

D('sv_top2_chi2dofprob',
  histogram_path = vertex_histo('h_sv_top2_chi2dofprob'),
  x_title = 'P(#chi^{2},dof) for vertex fit',
  y_title = 'vertices/0.024',
  x_range = (0,1),
  rebin = 2,
  legend_pos = (0.435, 0.687, 0.878, 0.920)
  )

D('sv_top2_tkonlyp',
  histogram_path = vertex_histo('h_sv_top2_tkonlyp'),
  rebin = 5,
  x_title = 'track-only vertex momentum (GeV)',
  y_title = 'vertices/15 GeV',
  y_range = (None, 550),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_top2_tkonlypt',
  histogram_path = vertex_histo('h_sv_top2_tkonlypt'),
  rebin = 5,
  x_title = 'track-only vertex p_{T} (GeV)',
  y_title = 'vertices/15 GeV',
  legend_pos = (0.570, 0.748, 0.878, 0.921),
  )

D('sv_top2_tkonlymass',
  histogram_path = vertex_histo('h_sv_top2_tkonlymass'),
  rebin = 6,
  x_title = 'track-only vertex mass (GeV)',
  y_title = 'vertices/15 GeV',
  y_range = (None, 650),
  legend_pos = (0.45, 0.687, 0.878, 0.920),
  )

D('sv_top2_jetsntkmass',
  histogram_path = vertex_histo('h_sv_top2_jetsntkmass'),
  rebin = 6,
  x_title = 'associated jets\' mass (GeV)',
  y_title = 'vertices/90 GeV',
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_top2_tksjetsntkmass',
  histogram_path = vertex_histo('h_sv_top2_tksjetsntkmass'),
  rebin = 6,
  x_title = 'tracks + associated jets\' mass (GeV)',
  y_title = 'vertices/90 GeV',
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_top2_costhtkonlymombs',
  histogram_path = vertex_histo('h_sv_top2_costhtkonlymombs'),
  rebin = 5,
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  overflow_in_last = False,
  )

D('sv_top2_maxtrackpt',
  histogram_path = vertex_histo('h_sv_top2_maxtrackpt'),
  rebin = 6,
  x_title = 'max{track p_{T,i}} (GeV)',
  y_title = 'vertices/9 GeV',
  y_range = (None, 820),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_top2_sumpt2',
  histogram_path = vertex_histo('h_sv_top2_sumpt2'),
  rebin = 15,
  x_title = '#Sigma p_{T}^{2} (GeV^{2})',
  y_title = 'vertices/300 GeV^{2}',
  y_range = (None, 820),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_best0_drmin',
  histogram_path = vertex_histo('h_sv_best0_drmin'),
  rebin = 4,
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.04',
  x_range = (0, 0.4),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_top2_drmin_nm1',
  histogram_path = 'vtxHst1VNoDrmin/h_sv_top2_drmin',
  x_title = 'min{#Delta R{track i,j}}',
  y_title = 'vertices/0.08',
  rebin = 8,
  #x_range = (0, 0.4),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_best0_drmax',
  histogram_path = vertex_histo('h_sv_best0_drmax'),
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}}',
  y_title = 'vertices/0.28',
  x_range = (1.2, 4.2),
  #y_range = (None, 550),
  legend_pos = (0.135, 0.687, 0.578, 0.920)
  )

D('sv_top2_drmax_nm1',
  histogram_path = 'vtxHst1VNoDrmax/h_sv_top2_drmax',
  rebin = 6,
  x_title = 'max{#Delta R{track i,j}} for two "best" SV (GeV)',
  y_title = 'vertices/0.28',
  x_range = (1.2, 4),
  legend_pos = (0.135, 0.687, 0.578, 0.920)
  )

D('sv_best0_njetsntks',
  histogram_path = vertex_histo('h_sv_best0_njetsntks'),
  x_title = 'number of associated jets',
  y_title = 'vertices',
  x_range = (1, 6),
  #y_range = (None, 1350),
  legend_pos = (0.589, 0.704, 0.878, 0.921),
  )

D('sv_top2_njetsntks_nm1',
  histogram_path = 'vtxHst1VNoNjets/h_sv_top2_njetsntks',
  x_title = 'number of associated jets',
  y_title = 'vertices',
  x_range = (0, 6),
  y_range = (None, 1350),
  legend_pos = (0.589, 0.704, 0.878, 0.921),
  )

D('sv_top2_bs2ddist',
  histogram_path = vertex_histo('h_sv_top2_bs2ddist'),
  x_title = 'xy distance to beamspot (cm)',
  y_title = 'vertices/50 #mum',
  x_range = (0, 0.1),
  y_range = (None, 1200),
  legend_pos = (0.547, 0.755, 0.878, 0.921),
  )

D('sv_best0_bs2derr',
  histogram_path = vertex_histo('h_sv_best0_bs2derr'),
  x_title = '#sigma(xy distance to beamspot) (cm)',
  y_title = 'vertices/5 #mum',
  x_range = (0, 0.003),
  )

D('sv_top2_bs2derr_nm1',
  histogram_path = 'vtxHst1VNoBs2derr/h_sv_top2_bs2derr',
  x_title = '#sigma(xy distance to beamspot) (cm)',
  y_title = 'vertices/25 #mum',
  rebin = 5,
  )

D('sv_top2_bs2dsig',
  histogram_path = vertex_histo('h_sv_top2_bs2dsig'),
  x_title = 'N#sigma(2D distance to BS) for two "best" SV',
  y_title = 'vertices/2',
  rebin = 2,
  x_range = (10, 50),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

D('sv_top2_bs2dsig_nm1',
  histogram_path = 'vtxHst1VNoBs2dsig/h_sv_top2_bs2dsig',
  x_title = 'N#sigma(2D distance to BS) for two "best" SV',
  y_title = 'vertices/2',
  rebin = 2,
  x_range = (0, 50),
  legend_pos = (0.435, 0.687, 0.878, 0.920),
  )

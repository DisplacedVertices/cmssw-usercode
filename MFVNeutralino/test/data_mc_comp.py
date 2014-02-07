#!/usr/bin/env python

verbose = True
plot_dir = 'plots/MFVDataMCCompV15'
plot_size = (600,600)
int_lumi = 950. # /pb
int_lumi_nice = '0.95 fb^{-1}'
scale_factor = 1. #720/768.
root_file_dir = 'crab/MFVHistosV15_looser'
root_file_dir = 'crab/MFVHistosV15_looser_fixnm1'
hist_path_for_nevents_check = None # 'mfvEventHistosNoCuts/h_npu',

################################################################################

import os
from functools import partial
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver
import JMTucker.Tools.Samples as Samples

set_style()
ps = plot_saver(plot_dir, size=plot_size)

data_sample = Samples.MultiJetPk2012B

background_samples = Samples.smaller_background_samples + Samples.ttbar_samples + Samples.qcd_samples
signal_samples = [Samples.mfv_neutralino_tau0100um_M1000, Samples.mfv_neutralino_tau1000um_M1000, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]
Samples.mfv_neutralino_tau0100um_M1000.color = 6
Samples.mfv_neutralino_tau1000um_M0400.color = 8
Samples.mfv_neutralino_tau1000um_M1000.color = 7
Samples.mfv_neutralino_tau9900um_M0400.color = 2

for s in Samples.qcdht0100, Samples.qcdht0250, Samples.qcdht0500, Samples.qcdht1000:
    s.join_info = True, 'QCD', Samples.qcdht0100.color
for s in Samples.ttbardilep, Samples.ttbarsemilep, Samples.ttbarhadronic:
    s.join_info = True, 't#bar{t}', Samples.ttbardilep.color
for s in Samples.dyjetstollM10, Samples.dyjetstollM50:
    s.join_info = True, 'DY + jets #rightarrow ll', Samples.dyjetstollM10.color
for s in Samples.smaller_background_samples:
    s.join_info = True, 'single t, VV, ttV', 46

if verbose:
    print 'weights:'
    for sample in background_samples:
        print '%20s: %e' % (sample.name, sample.partial_weight*int_lumi)

C = partial(data_mc_comparison,
            background_samples = background_samples,
            signal_samples = signal_samples,
            data_sample = data_sample,
            plot_saver = ps,
            file_path = os.path.join(root_file_dir, '%(name)s.root'),
            int_lumi = int_lumi * scale_factor,
            int_lumi_nice = int_lumi_nice,
            hist_path_for_nevents_check = hist_path_for_nevents_check,
            overflow_in_last = False,
            poisson_intervals = True,
            verbose = verbose,
            )

################################################################################

legend_pos = (0.435, 0.687, 0.878, 0.920)

if 0:
    for i in xrange(20):
        C('clean%i' % i,
          histogram_path = 'mfvEventHistos/h_pass_clean_%i' % i,
          legend_pos = (0.435, 0.687, 0.878, 0.920)
          )

if 0:
    C('npv',
      histogram_path = 'mfvEventHistos/h_npv',
      x_title = 'number of PV',
      y_title = 'events',
      x_range = (0, 40),
      y_range = (None, 140),
      rebin = 2,
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('pvntracks',
      histogram_path = 'mfvEventHistos/h_pv_ntracks',
      rebin = 10,
      x_title = 'number of tracks in PV',
      y_title = 'events/10',
      y_range = (None, 250),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('pvsumpt2',
      histogram_path = 'mfvEventHistos/h_pv_sumpt2',
      rebin = 10,
      x_title = '#Sigma p_{T}^{2} of tracks in PV (GeV^{2})',
      y_title = 'events/1000 GeV^{2}',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('pvrho',
      histogram_path = 'mfvEventHistos/h_pv_rho',
      x_title = 'PV #rho (cm)',
      y_title = 'events/0.01 cm',
      x_range = (0, 0.1),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('pvz',
      histogram_path = 'mfvEventHistos/h_pvz',
      x_title = 'PV z (cm)',
      y_title = 'events/cm',
      rebin = 10,
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('njets',
      histogram_path = 'mfvEventHistos/h_njets',
      x_title = 'number of jets',
      y_title = 'events',
      x_range = (4,16),
      y_range = (None, 230),
      legend_pos = (0.572, 0.687, 0.884, 0.920),
      )

if 0:
    C('njetsnoputight',
      histogram_path = 'mfvEventHistos/h_njetsnopu_tight',
      x_title = 'number of jets (tight PU id)',
      y_title = 'events',
      x_range = (4,16),
      y_range = (None, 230),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('jetpt4',
      histogram_path = 'mfvEventHistos/h_jetpt4',
      x_title = 'jet #4 p_{T} (GeV)',
      y_title = 'events/5 GeV',
      x_range = (60,250),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('jetpt5',
      histogram_path = 'mfvEventHistos/h_jetpt5',
      x_title = 'jet #5 p_{T} (GeV)',
      y_title = 'events/5 GeV',
      x_range = (60,250),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('jetpt6',
      histogram_path = 'mfvEventHistos/h_jetpt6',
      x_title = 'jet #6 p_{T} (GeV)',
      y_title = 'events/5 GeV',
      x_range = (60,250),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('jetsumht',
      histogram_path = 'mfvEventHistos/h_jet_sum_ht',
      rebin = 4,
      x_title = '#Sigma H_{T} (GeV)',
      y_title = 'events/100 GeV',
      x_range = (500, 3000),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('nbtags',
      histogram_path = 'mfvEventHistos/h_nbtags_medium',
      x_title = '# CSVM b-tagged jets',
      y_title = 'events',
      x_range = (0,10),
      y_range = (None, 6e2),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('nsemimuons',
      histogram_path = 'mfvEventHistos/h_nmuons_semilep',
      x_title = 'number of semilep muons',
      y_title = 'events',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('nsemielectrons',
      histogram_path = 'mfvEventHistos/h_nelectrons_semilep',
      x_title = 'number of semilep electrons',
      y_title = 'events',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('nsemileptons',
      histogram_path = 'mfvEventHistos/h_nleptons_semilep',
      x_title = 'number of semilep electrons',
      y_title = 'events',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('nsvnocut',
      histogram_path = 'mfvVertexHistosTrigCut/h_nsv',
      x_title = 'number of SV',
      y_title = 'events',
      x_range = (0,5),
      y_range = (1, 1e7),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('nsv',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_nsv',
      x_title = 'number of SV',
      y_title = 'events',
      x_range = (2,5),
      y_range = (None, 1e3),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_ntracks',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_ntracks',
      x_title = 'number of tracks/vertex',
      y_title = 'vertices',
      x_range = (5, 20),
      legend_pos = (0.435, 0.687, 0.878, 0.920)
      )

if 0:
    C('sv_top2_ntracksptgt3',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_ntracksptgt3',
      x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
      y_title = 'vertices',
      x_range = (1, 10),
      y_range = (None, 700),
      legend_pos = (0.553, 0.687, 0.878, 0.920)
      )

if 1:
    C('sv_top2_ntracksptgt3_nm1',
      histogram_path = 'hstNoNtracksptgt3/h_sv_top2_ntracksptgt3',
      x_title = 'number of tracks with p_{T} > 3 GeV/vertex',
      y_title = 'vertices',
      x_range = (0, 10),
    #  y_range = (None, 700),
      legend_pos = (0.553, 0.687, 0.878, 0.920)
      )

if 0:
    C('sv_top2_chi2dof',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_chi2dof',
      x_title = '#chi^{2}/dof for vertex fit',
      y_title = 'vertices/0.14',
      x_range = (0, 5),
      y_range = (None, 180),
      legend_pos = (0.435, 0.687, 0.878, 0.920)
      )

if 0:
    C('sv_top2_chi2dofprob',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_chi2dofprob',
      x_title = 'P(#chi^{2},dof) for vertex fit',
      y_title = 'vertices/0.024',
      x_range = (0,1),
      legend_pos = (0.435, 0.687, 0.878, 0.920)
      )

if 0:
    C('sv_top2_tkonlyp',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_tkonlyp',
      rebin = 4,
      x_title = 'track-only vertex momentum (GeV)',
      y_title = 'vertices/12 GeV',
      y_range = (None, 450),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_tkonlypt',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_tkonlypt',
      rebin = 4,
      x_title = 'track-only vertex p_{T} (GeV)',
      y_title = 'vertices/12 GeV',
      legend_pos = (0.570, 0.748, 0.878, 0.921),
      )

if 0:
    C('sv_top2_tkonlymass',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_tkonlymass',
      rebin = 4,
      x_title = 'track-only vertex mass (GeV)',
      y_title = 'vertices/10 GeV',
      legend_pos = (0.45, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_jetsntkmass',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_jetsntkmass',
      rebin = 4,
      x_title = 'associated jets\' mass (GeV)',
      y_title = 'vertices/60 GeV',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_tksjetsntkmass',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_tksjetsntkmass',
      rebin = 4,
      x_title = 'tracks + associated jets\' mass (GeV)',
      y_title = 'vertices/60 GeV',
      y_range = (None, 500),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_costhtkonlymombs',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_costhtkonlymombs',
      rebin = 4,
      y_range = (1e-4, 270),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_maxtrackpt',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_maxtrackpt',
      rebin = 4,
      x_title = 'max{track p_{T,i}} (GeV)',
      y_title = 'vertices/6 GeV',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_sumpt2',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_sumpt2',
      rebin = 10,
      x_title = '#Sigma p_{T}^{2} (GeV^{2})',
      y_title = 'vertices/200 GeV^{2}',
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_drmin',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_drmin',
      rebin = 2,
      x_title = 'min{#Delta R{track i,j}}',
      y_title = 'vertices/0.02',
      x_range = (0, 0.4),
      #y_range = (1e-1, 2e2),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 1:
    C('sv_top2_drmin_nm1',
      histogram_path = 'hstNoDrmin/h_sv_top2_drmin',
      x_title = 'min{#Delta R{track i,j}}',
      y_title = 'vertices/0.05',
      rebin = 5,
      #x_range = (0, 0.4),
      #y_range = (1e-1, 2e2),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_top2_drmax',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_drmax',
      rebin = 3,
      x_title = 'max{#Delta R{track i,j}} for two "best" SV (GeV)',
      y_title = 'vertices/0.14',
      x_range = (0, 4),
      legend_pos = (0.135, 0.687, 0.578, 0.920)
      )

if 1:
    C('sv_top2_drmax_nm1',
      histogram_path = 'hstNoDrmax/h_sv_top2_drmax',
      rebin = 3,
      x_title = 'max{#Delta R{track i,j}} for two "best" SV (GeV)',
      y_title = 'vertices/0.14',
#      x_range = (0, 4),
      legend_pos = (0.135, 0.687, 0.578, 0.920)
      )

if 0:
    C('sv_top2_njetsntks',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_njetsntks',
      x_title = 'number of associated jets',
      y_title = 'vertices',
      x_range = (1, 6),
      y_range = (None, 1100),
      legend_pos = (0.589, 0.704, 0.878, 0.921),
      )

if 1:
    C('sv_top2_njetsntks_nm1',
      histogram_path = 'hstNoNjets/h_sv_top2_njetsntks',
      x_title = 'number of associated jets',
      y_title = 'vertices',
#      x_range = (1, 6),
      y_range = (None, 1100),
      legend_pos = (0.589, 0.704, 0.878, 0.921),
      )

if 0:
    C('sv_top2_bs2ddist',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_bs2ddist',
      x_title = 'xy distance to beamspot (cm)',
      y_title = 'vertices/50 #mum',
      x_range = (0, 0.1),
      legend_pos = (0.547, 0.755, 0.878, 0.921),
      )

if 0:
    C('sv_top2_bs2derr',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_bs2derr',
      x_title = '#sigma(xy distance to beamspot) (cm)',
      y_title = 'vertices/5 #mum',
      x_range = (0, 0.008),
      y_range = (None, 275),
      )

if 1:
    C('sv_top2_bs2derr_nm1',
      histogram_path = 'hstNoBs2derr/h_sv_top2_bs2derr',
      x_title = '#sigma(xy distance to beamspot) (cm)',
      y_title = 'vertices/25 #mum',
      rebin = 5,
#      y_range = (None, 275),
      )

if 0:
    C('sv_top2_bs2dsig',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_bs2dsig',
      x_title = 'N#sigma(2D distance to BS) for two "best" SV',
      y_title = 'vertices/2',
      rebin = 2,
      x_range = (10, 50),
      #y_range = (1e-1, 2e2),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 1:
    C('sv_top2_bs2dsig_nm1',
      histogram_path = 'hstNoBs2dsig/h_sv_top2_bs2dsig',
      x_title = 'N#sigma(2D distance to BS) for two "best" SV',
      y_title = 'vertices/2',
#      rebin = 0,
      x_range = (0, 10),
      #y_range = (1e-1, 2e2),
      legend_pos = (0.435, 0.687, 0.878, 0.920),
      )

if 0:
    C('sv_sumtop2_ntracks',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_sumtop2_ntracks',
      x_title = 'ntracks01',
      y_title = 'events',
      x_range = (10, 40),
      legend_pos = (0.435, 0.687, 0.878, 0.920)
      )

if 0:
    C('sv_sumtop2_maxtrackpt',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_sumtop2_maxtrackpt',
      x_title = 'maxtrackpt01 (GeV)',
      y_title = 'events/6 GeV',
      rebin = 4,
#      x_range = (0, 40),
      legend_pos = (0.435, 0.687, 0.878, 0.920)
      )

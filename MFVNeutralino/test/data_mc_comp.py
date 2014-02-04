#!/usr/bin/env python

verbose = True
plot_dir = 'plots/MFVDataMCCompV15'
plot_size = (600,600)
int_lumi = 950. # /pb
int_lumi_nice = '0.95 fb^{-1}'
scale_factor = 1.
root_file_dir = 'crab/MFVHistosV15_looser'
hist_path_for_nevents_check = None # 'mfvEventHistosNoCuts/h_npu',

################################################################################

from functools import partial
from JMTucker.Tools.ROOTTools import ROOT, data_mc_comparison, set_style, plot_saver
import JMTucker.Tools.Samples as Samples

set_style()
ps = plot_saver(plot_dir, size=plot_size)

data_sample = Samples.MultiJetPk2012B

background_samples = Samples.smaller_background_samples + Samples.ttbar_samples + Samples.qcd_samples
signal_samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]
Samples.mfv_neutralino_tau0100um_M0400.color = 6
Samples.mfv_neutralino_tau1000um_M0400.color = 8
Samples.mfv_neutralino_tau9900um_M0400.color = 9

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
            int_lumi = int_lumi * scale_factor
            int_lumi_nice = int_lumi_nice,
            hist_path_for_nevents_check = hist_path_for_nevents_check,
            verbose = verbose,
            )

################################################################################

if 1:
    C('nsv',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_nsv',
      x_title = 'number of SV',
      y_title = 'events',
      x_range = (2,6),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

raise 1

if 1:
    C('sv_top2_tkonlymass',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_tkonlymass',
      rebin = 4,
      x_title = 'mass for two "best" SV (GeV)',
      y_title = 'events/10 GeV',
      y_range = (1e-1, 2.5e3),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )


if 1:
    C('npv',
      histogram_path = 'mfvEventHistos/h_npv',
      x_title = 'number of PV',
      y_title = 'events',
      x_range = (0, 34),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('njets',
      histogram_path = 'mfvEventHistos/h_njets',
      x_title = 'number of jets',
      y_title = 'events',
      y_range = (1e-1, 8e4),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('nsemilepmuons',
      histogram_path = 'mfvEventHistos/h_nmuons_semilep',
      x_title = 'number of semilep muons',
      y_title = 'events',
      y_range = (1, 1.2e5),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('jetsumht',
      histogram_path = 'mfvEventHistos/h_jet_sum_ht',
      rebin = 4,
      x_title = '#Sigma H_{T} (GeV)',
      y_title = 'events/100 GeV',
      x_range = (0, 2000),
      y_range = (1e-1, 7e4),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 0:
    C('nbtags',
      histogram_path = 'mfvEventHistos/h_nbtags',
      x_title = 'number of b-tags',
      y_title = 'events',
      x_range = (0,8),
      y_range = (1e-1, 1.3e5),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('pvntracks',
      histogram_path = 'mfvEventHistos/h_pv_ntracks',
      rebin = 10,
      x_title = 'number of tracks in PV',
      y_title = 'events/10',
      y_range = (1e-1, 3.2e4),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('pvsumpt2',
      histogram_path = 'mfvEventHistos/h_pv_sumpt2',
      rebin = 5,
      x_title = '#Sigma p_{T}^{2} of tracks in PV (GeV^{2})',
      y_title = 'events/500 GeV^{2}',
      y_range = (1e-1, 1.5e4),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('pvrho',
      histogram_path = 'mfvEventHistos/h_pv_rho',
      x_title = 'PV #rho (cm)',
      y_title = 'events/0.01 cm',
      x_range = (0, 0.1),
      y_range = (1e-1, 1.4e5),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_ntracks',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_ntracks',
      x_title = 'number of tracks for two "best" SV',
      y_title = 'events',
      x_range = (5, 20),
      y_range = (1e-1, 2e3),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_maxtrackpt',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_maxtrackpt',
      rebin = 4,
      x_title = 'max{track p_{T,i}} for two "best" SV (GeV)',
      y_title = 'events/6 GeV',
      y_range = (1e-1, 2e3),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_drmin',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_drmin',
      rebin = 10,
      x_title = 'min{#Delta R{track i,j}} for two "best" SV (GeV)',
      y_title = 'events/0.1',
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_drmax',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_drmax',
      rebin = 10,
      x_title = 'max{#Delta R{track i,j}} for two "best" SV (GeV)',
      y_title = 'events/0.47',
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_njetsntks',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_njetsntks',
      x_title = 'number of jets assoc. by tracks for two "best" SV',
      y_title = 'events',
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 0:
    C('sv_top2_jetsmassntks',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_jetsmassntks',
      x_title = 'inv. mass of jets assoc. by tracks for two "best" SV (GeV)',
      rebin = 10,
      y_title = 'events/100 GeV',
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_bs2ddist',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_bs2ddist',
      x_title = '2D distance to BS for two "best" SV (cm)',
#      rebin = 10,
      y_title = 'events/0.005 cm',
      x_range = (0, 0.1),
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_bs2derr',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_bs2derr',
      x_title = '#sigma(2D distance to BS) for two "best" SV (cm)',
#      rebin = 10,
      y_title = 'events/0.0005 cm',
      x_range = (0, 0.0075),
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )

if 1:
    C('sv_top2_bs2dsig',
      histogram_path = 'mfvVertexHistosWAnaCuts/h_sv_top2_bs2dsig',
      x_title = 'N#sigma(2D distance to BS) for two "best" SV',
      rebin = 4,
      y_title = 'events/4',
      x_range = (0, 28),
      y_range = (1e-1, 2e2),
      legend_pos = (0.589, 0.686, 0.861, 0.919),
      )


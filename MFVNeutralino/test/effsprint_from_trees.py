#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

file_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV14'
year = 2016

int_lumi = ac.int_lumi_2016 * ac.scale_factor_2016
background_samples = Samples.qcd_samples_sum + Samples.ttbar_samples
signal_samples = [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]

if year == 2015:
    int_lumi = ac.int_lumi_2015 * ac.scale_factor_2015
    background_samples = Samples.qcd_samples_sum_2015 + Samples.ttbar_samples_2015
    signal_samples = [] #[Samples.mfv_neu_tau00100um_M0800_2015, Samples.mfv_neu_tau00300um_M0800_2015, Samples.mfv_neu_tau01000um_M0800_2015, Samples.mfv_neu_tau10000um_M0800_2015]

for ntk in ['mfvMiniTree', 'mfvMiniTreeNtk3', 'mfvMiniTreeNtk3or4', 'mfvMiniTreeNtk4']:
    print ntk

    raw_n1v = 0
    sum_n1v = 0
    var_n1v = 0
    raw_n2v = 0
    sum_n2v = 0
    var_n2v = 0
    for sample in background_samples:
        w = int_lumi * sample.xsec / sample.nevents_orig if sample.is_mc else 1.
        f = ROOT.TFile('%s/%s.root' % (file_path, sample.name))
        t = f.Get('%s/t' % ntk)
        if not t:
            continue
        n1v = t.Draw('dist0', 'nvtx==1')
        n2v = t.Draw('dist0', 'nvtx==2')
        if ntk == 'mfvMiniTreeNtk3or4':
            n2v = t.Draw('dist0', 'nvtx==2 && ntk0==4 && ntk1==3')
        print '%24s %d %9.3f %8d %8.5f raw n1v = %6d +/- %3d, weighted n1v = %9.2f +/- %6.2f, raw n2v = %4d +/- %2d, weighted n2v = %7.2f +/- %5.2f' % (sample.name, int_lumi, sample.xsec if sample.is_mc else -1, sample.nevents_orig, w, n1v, n1v**0.5, w*n1v, w*n1v**0.5, n2v, n2v**0.5, w*n2v, w*n2v**0.5)
        raw_n1v += n1v
        sum_n1v += n1v * w
        var_n1v += n1v * w**2
        raw_n2v += n2v
        sum_n2v += n2v * w
        var_n2v += n2v * w**2
    print '%24s %d %9s %8s %8s raw n1v = %6d %7s, weighted n1v = %9.2f +/- %6.2f, raw n2v = %4d %6s, weighted n2v = %7.2f +/- %5.2f' % ('total background', int_lumi, '', '', '', raw_n1v, '', sum_n1v, var_n1v**0.5, raw_n2v, '', sum_n2v, var_n2v**0.5)
    print

    for sample in signal_samples:
        w = int_lumi * sample.xsec / sample.nevents_orig
        f = ROOT.TFile('%s/%s.root' % (file_path, sample.name))
        t = f.Get('%s/t' % ntk)
        n1v = t.Draw('dist0', 'nvtx==1')
        n2v = t.Draw('dist0', 'nvtx==2')
        if ntk == 'mfvMiniTreeNtk3or4':
            n2v = t.Draw('dist0', 'nvtx==2 && ntk0==4 && ntk1==3')
        print '%s %d %.3f %6d %7.5f raw n1v = %5d +/- %3d, weighted n1v = %5.2f +/- %4.2f, raw n2v = %5d +/- %3d, weighted n2v = %6.3f +/- %5.3f' % (sample.name, int_lumi, sample.xsec, sample.nevents_orig, w, n1v, n1v**0.5, w*n1v, w*n1v**0.5, n2v, n2v**0.5, w*n2v, w*n2v**0.5)
    print

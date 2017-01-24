#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

for ntk in ['', '_ntk3', '_ntk3or4', '_ntk4']:
    print ntk

    raw_n1v = 0
    sum_n1v = 0
    var_n1v = 0
    raw_n2v = 0
    sum_n2v = 0
    var_n2v = 0
    for sample in Samples.qcd_samples_sum + Samples.ttbar_samples:
        w = ac.int_lumi * sample.xsec / sample.nevents_orig
        f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/MinitreeV10%s/%s.root' % (ntk, sample.name))
        t = f.Get('mfvMiniTree/t')
        n1v = t.Draw('dist0', 'nvtx==1')
        n2v = t.Draw('dist0', 'nvtx==2')
        if ntk == '_ntk3or4':
            n2v = t.Draw('dist0', 'nvtx==2 && ntk0==4 && ntk1==3')
        print '%24s %d %9.3f %8d %8.5f raw n1v = %6d +/- %3d, weighted n1v = %9.2f +/- %7.2f, raw n2v = %4d +/- %2d, weighted n2v = %7.2f +/- %5.2f' % (sample.name, ac.int_lumi, sample.xsec, sample.nevents_orig, w, n1v, n1v**0.5, w*n1v, w*n1v**0.5, n2v, n2v**0.5, w*n2v, w*n2v**0.5)
        raw_n1v += n1v
        sum_n1v += n1v * w
        var_n1v += n1v * w**2
        raw_n2v += n2v
        sum_n2v += n2v * w
        var_n2v += n2v * w**2
    print '%24s %d %9s %8s %8s raw n1v = %6d %7s, weighted n1v = %9.2f +/- %7.2f, raw n2v = %4d %6s, weighted n2v = %7.2f +/- %5.2f' % ('total background', ac.int_lumi, '', '', '', raw_n1v, '', sum_n1v, var_n1v**0.5, raw_n2v, '', sum_n2v, var_n2v**0.5)
    print

    for sample in [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]:
        w = ac.int_lumi * sample.xsec / sample.nevents_orig
        f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/MinitreeV10%s/%s.root' % (ntk, sample.name))
        t = f.Get('mfvMiniTree/t')
        n1v = t.Draw('dist0', 'nvtx==1')
        n2v = t.Draw('dist0', 'nvtx==2')
        if ntk == '_ntk3or4':
            n2v = t.Draw('dist0', 'nvtx==2 && ntk0==4 && ntk1==3')
        print '%24s %d %9.3f %8d %8.5f raw n1v = %6d +/- %3d, weighted n1v = %9.2f +/- %7.2f, raw n2v = %4d +/- %2d, weighted n2v = %7.2f +/- %5.2f' % (sample.name, ac.int_lumi, sample.xsec, sample.nevents_orig, w, n1v, n1v**0.5, w*n1v, w*n1v**0.5, n2v, n2v**0.5, w*n2v, w*n2v**0.5)
    print

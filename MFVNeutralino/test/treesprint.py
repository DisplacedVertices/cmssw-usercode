#!/usr/bin/env python

import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools import Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

ROOT.gErrorIgnoreLevel = 6000

fns = [x for x in sys.argv[1:] if x.endswith('.root') and os.path.isfile(x)]
include = [1 if 'sum' in sys.argv else 0]*len(fns)

year = typed_from_argv(int, 2016)
if year == 2015:
    int_lumi = ac.int_lumi_2015 * ac.scale_factor_2015
elif year == 2016:
    int_lumi = ac.int_lumi_2016 * ac.scale_factor_2016

if not fns:
    file_path = None
    for x in sys.argv:
        if os.path.isdir(x) and os.path.isfile(os.path.join(x, 'ttbar.root')):
            file_path = x
    if file_path is None:
        file_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15'
    print 'using', file_path

    if year == 2015:
        background_samples = Samples.qcd_samples_sum_2015 + Samples.ttbar_samples_2015
        signal_samples = [Samples.mfv_neu_tau00100um_M0800_2015, Samples.mfv_neu_tau00300um_M0800_2015, Samples.mfv_neu_tau01000um_M0800_2015, Samples.mfv_neu_tau10000um_M0800_2015]
    elif year == 2016:
        background_samples = Samples.qcd_samples_sum + Samples.ttbar_samples
        signal_samples = [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]

    fns = ['%s/%s.root' % (file_path, sample.name) for sample in background_samples + signal_samples]
    include = [1]*len(background_samples) + [0]*len(signal_samples)

def getit(fn, ntk):
    f = ROOT.TFile(fn)
    t = f.Get('%s/t' % ntk)
    if not t:
        return None
    n1v = t.Draw('dist0', 'nvtx==1', 'goff')
    n2v = t.Draw('dist0', 'nvtx>=2', 'goff')
    if ntk == 'mfvMiniTreeNtk3or4':
        n2v = t.Draw('dist0', 'nvtx>=2 && ntk0==4 && ntk1==3', 'goff')
    return n1v, n2v

for ntk in ['mfvMiniTree', 'mfvMiniTreeNtk3', 'mfvMiniTreeNtk3or4', 'mfvMiniTreeNtk4']:
    print ntk
    raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0, 0, 0, 0, 0, 0
    summaried = None
    for fn, inc in zip(fns, include) + [(None, None)]:
        if inc:
            summaried = False
        if not inc and summaried == False:
            summaried = True
            print '%36s %d %9s %8s %8s raw n1v = %6d %7s, weighted n1v = %9.2f +/- %6.2f, raw n2v = %6d %6s, weighted n2v = %7.2f +/- %5.2f' % ('total background', int_lumi, '', '', '', raw_n1v, '', sum_n1v, var_n1v**0.5, raw_n2v, '', sum_n2v, var_n2v**0.5)
            print
        if fn is None:
            break

        x = getit(fn, ntk)
        if x:
            n1v, n2v = x

            sname = os.path.basename(fn).replace('.root', '')
            if hasattr(Samples, sname):
                sample = getattr(Samples, sname)
                w = int_lumi * sample.xsec / sample.nevents_orig if sample.is_mc else 1.
                print '%36s %d %9.3f %8d %8.5f raw n1v = %6d +/- %3d, weighted n1v = %9.2f +/- %6.2f, raw n2v = %6d +/- %2d, weighted n2v = %7.2f +/- %5.2f' % (sample.name, int_lumi, sample.xsec if sample.is_mc else -1, sample.nevents_orig, w, n1v, n1v**0.5, w*n1v, w*n1v**0.5, n2v, n2v**0.5, w*n2v, w*n2v**0.5)
            else:
                print '%36s  n1v = %9.2f  n2v = %9.2f' % (sname, n1v, n2v)

            if inc:
                raw_n1v += n1v
                sum_n1v += n1v * w
                var_n1v += n1v * w**2
                raw_n2v += n2v
                sum_n2v += n2v * w
                var_n2v += n2v * w**2
    print

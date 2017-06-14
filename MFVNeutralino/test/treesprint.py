#!/usr/bin/env python

import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
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
    hr = draw_hist_register(t, True)
    def c(cut):
        h,n = hr.draw('weight', cut, binning='1,0,1', get_n=True, goff=True)
        return n, h.Integral(0,h.GetNbinsX()+2)
    n1v = c('nvtx==1')
    if ntk == 'mfvMiniTreeNtk3or4':
        n2v = c('nvtx>=2 && ntk0==4 && ntk1==3')
    else:
        n2v = c('nvtx>=2')
    return n1v, n2v

fmt = '%40s %9s %9s %9s %9s   %9s +/- %9s  %9s +/- %9s  %9s +/- %9s  %9s +/- %9s'
print fmt % ('sample', 'int.lumi', 'xsec', 'nevents', 'weight', 'rn1v', 'unc', 'wn1v', 'unc', 'rn2v', 'unc', 'wn2v', 'unc')

for ntk in ['mfvMiniTree', 'mfvMiniTreeNtk3', 'mfvMiniTreeNtk3or4', 'mfvMiniTreeNtk4']:
    print ntk
    raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0, 0, 0, 0, 0, 0
    summaried = None
    for fn, inc in zip(fns, include) + [(None, None)]:
        if inc:
            summaried = False
        if not inc and summaried == False:
            summaried = True
            print fmt % ('total background', '%.0f' % int_lumi, '', '', '',
                         raw_n1v, '-',
                         '%9.2f' % sum_n1v, '%9.2f' % (var_n1v**0.5),
                         raw_n2v, '-',
                         '%9.2f' % sum_n2v, '%9.2f' % (var_n2v**0.5))
            print
        if fn is None:
            break

        x = getit(fn, ntk)
        if x:
            (r1v, n1v), (r2v, n2v) = x

            sname = os.path.basename(fn).replace('.root', '')
            if hasattr(Samples, sname):
                sample = getattr(Samples, sname)
                w = int_lumi * sample.partial_weight(fn)
                if sample.is_signal:
                    xsec = '%9.3f' % sample.xsec
                else:
                    xsec = '%9.0f' % (sample.xsec if sample.is_mc else -1)
                print fmt % (sample.name,
                             '%.0f' % int_lumi,
                             xsec,
                             '%.0f' % sample.nevents(fn),
                             '%9.3g' % w,
                             r1v,
                             '%9.2f' % (r1v**0.5),
                             '%9.2f' % (w*n1v),
                             '%9.2f' % (w*n1v**0.5),
                             r2v,
                             '%9.2f' % (n2v**0.5),
                             '%9.2f' % (w*n2v),
                             '%9.2f' % (w*n2v**0.5))
            else:
                print '%36s  n1v = %9.2f  n2v = %9.2f' % (sname, n1v, n2v)

            if inc:
                raw_n1v += r1v
                sum_n1v += n1v * w
                var_n1v += n1v * w**2
                raw_n2v += r2v
                sum_n2v += n2v * w
                var_n2v += n2v * w**2
    print

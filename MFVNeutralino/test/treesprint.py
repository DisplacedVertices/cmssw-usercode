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

if not fns:
    doing_default = True
    file_path = None
    for x in sys.argv:
        if os.path.isdir(x) and os.path.isfile(os.path.join(x, 'ttbar.root')):
            file_path = x
    if file_path is None:
        file_path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15'
    print 'using', file_path

    background_samples_2015 = Samples.qcd_samples_sum_2015 + Samples.ttbar_samples_2015
    default_bkg_samples = background_samples_2016 = Samples.qcd_samples_sum + Samples.ttbar_samples

    signal_samples_2015 = [Samples.mfv_neu_tau00100um_M0800_2015, Samples.mfv_neu_tau00300um_M0800_2015, Samples.mfv_neu_tau01000um_M0800_2015, Samples.mfv_neu_tau10000um_M0800_2015]
    signal_samples_2016 = [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800]

    samples = background_samples_2015 + signal_samples_2015 + background_samples_2016 + signal_samples_2016
    fns = ['%s/%s.root' % (file_path, sample.name) for sample in samples]
    include = [(0 if s.is_signal else (2015 if s.name.endswith('_2015') else 2016)) for s in samples]
else:
    doing_default = False
    default_bkg_samples = []

def getit(fn, ntk):
    f = ROOT.TFile(fn)
    t = f.Get('%s/t' % ntk)
    hr = draw_hist_register(t, True)
    def c(cut):
        #cut = '(%s) && njets >= 4 && jetht > 700 && jetht < 1000' % cut
        #cut = '(%s) && njets >= 4 && jetht > 700' % cut
        h,n = hr.draw('weight', cut, binning='1,0,1', get_n=True, goff=True)
        return (n,) + get_integral(h)
    n1v = c('nvtx==1')
    if ntk == 'mfvMiniTreeNtk3or4':
        n2v = c('nvtx>=2 && ntk0==4 && ntk1==3')
    else:
        n2v = c('nvtx>=2')
    return n1v, n2v

fmt = '%40s %9s %9s %9s %9s   %9s +/- %9s  %9s +/- %9s  %9s +/- %9s  %9s +/- %9s'

for ntk in ['mfvMiniTree', 'mfvMiniTreeNtk3', 'mfvMiniTreeNtk3or4', 'mfvMiniTreeNtk4']:
    print ntk
    print fmt % ('sample', 'int.lumi', 'xsec', 'nevents', 'weight', 'rn1v', 'unc', 'wn1v', 'unc', 'rn2v', 'unc', 'wn2v', 'unc')

    raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0, 0, 0, 0, 0, 0
    seen = {}
    last_inc = include[0]
    for fn, inc in zip(fns, include) + [(None, None)]:
#        print fn,last_inc,inc,inc!=last_inc,not inc,inc != last_inc and not inc
        if inc != last_inc and last_inc == 0:
            print
        if inc != last_inc and last_inc != 0:
            x = seen['background_%s' % last_inc] = (raw_n1v, raw_n1v**0.5, sum_n1v, var_n1v**0.5), (raw_n2v, raw_n2v**0.5, sum_n2v, var_n2v**0.5)
            print fmt % ('total background', '', '', '', '',
                         x[0][0], '%9.2f' % x[0][1],
                         '%9.2f' % x[0][2], '%9.2f' % x[0][3],
                         x[1][0], '%9.2f' % x[1][1],
                         '%9.2f' % x[1][2], '%9.2f' % x[1][3])
            print
            raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0, 0, 0, 0, 0, 0
        last_inc = inc
        if fn is None:
            break

        x = getit(fn, ntk)
        if x:
            (r1v, n1v, en1v), (r2v, n2v, en2v) = x
            sname = os.path.basename(fn).replace('.root', '')
            seen[sname] = x

            if hasattr(Samples, sname):
                sample = getattr(Samples, sname)
                if not sample.is_mc:
                    w = 1.
                    print fmt % (sample.name, '', '', '', '',
                                 r1v, '%9.0f' % r1v**0.5, '', '', 
                                 r2v, '%9.0f' % r2v**0.5, '', '')
                else:
                    if sample.name.endswith('_2015'):
                        int_lumi = ac.int_lumi_2015 * ac.scale_factor_2015
                    else:
                        int_lumi = ac.int_lumi_2016 * ac.scale_factor_2016
                    w = int_lumi * sample.partial_weight(fn)
                    if sample.is_signal:
                        xsec = '%9.3f' % sample.xsec
                    else:
                        xsec = '%9.0f' % sample.xsec

                    x = seen[sname] = (r1v, r1v**0.5, w*n1v, w*en1v), (r2v, r2v**0.5, w*n2v, w*en2v)
                    print fmt % (sample.name,
                                 '%.0f' % int_lumi,
                                 xsec,
                                 '%.0f' % sample.nevents(fn),
                                 '%9.3g' % w,
                                 x[0][0],
                                 '%9.2f' % x[0][1],
                                 '%9.2f' % x[0][2],
                                 '%9.2f' % x[0][3],
                                 x[1][0],
                                 '%9.2f' % x[1][1],
                                 '%9.2f' % x[1][2],
                                 '%9.2f' % x[1][3],
                                 )
            else:
                print '%36s  n1v = %9.2f  n2v = %9.2f' % (sname, n1v, n2v)

            if inc:
                raw_n1v += r1v
                sum_n1v += n1v * w
                var_n1v += (en1v * w)**2
                raw_n2v += r2v
                sum_n2v += n2v * w
                var_n2v += (en2v * w)**2
    print

    if doing_default:
        int_lumi_2015p6 = ac.int_lumi_2015 * ac.scale_factor_2015 + ac.int_lumi_2016 * ac.scale_factor_2016

        def doit(name, xsec, a,b):
            (r1v_2015, er1v_2015, n1v_2015, en1v_2015), (r2v_2015, er2v_2015, n2v_2015, en2v_2015) = seen[a]
            (r1v, er1v, n1v, en1v), (r2v, er2v, n2v, en2v) = seen[b]
            print fmt % (name,
                         '%.0f' % int_lumi_2015p6,
                         ('%.3f' if 'mfv' in name else '%.0f') % xsec if xsec > 0 else '',
                         '', #'%.0f' % s.nevents(fn),
                         '', #'%9.3g' % w,
                         '',
                         '',
                         '%9.2f' % (n1v_2015 + n1v),
                         '%9.2f' % (en1v_2015**2 + en1v**2)**0.5,
                         '', 
                         '',
                         '%9.2f' % (n2v_2015 + n2v),
                         '%9.2f' % (en2v_2015**2 + en2v**2)**0.5,
                         )

        for s in default_bkg_samples:
            doit(s.name + '_2015p6', s.xsec, s.name + '_2015', s.name)
        doit('background_2015p6', -1, 'background_2015', 'background_2016')
        print
        for s in signal_samples_2016:
            doit(s.name + '_2015p6', s.xsec, s.name + '_2015', s.name)
        print

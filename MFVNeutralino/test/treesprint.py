#!/usr/bin/env python

import sys, os
from glob import glob
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools.general import typed_from_argv, bool_from_argv
from JMTucker.Tools import Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

nosig = bool_from_argv('nosig')
which = typed_from_argv(int, -1)
ntks = ('mfvMiniTreeNtk3', 'mfvMiniTreeNtk4', 'mfvMiniTree')
if which != -1:
    if which < 3 or which > 5:
        raise ValueError('bad ntks %s' % which)
    ntks = ntks[which-3:which-2]

ROOT.gErrorIgnoreLevel = 6000
fns = []
for x in sys.argv[1:]:
    if x.endswith('.root') and (os.path.isfile(x) or x.startswith('root://')):
        fns.append(x)
    elif os.path.isdir(x):
        x2 = os.path.join(x, '*.root')
        print 'using', x2
        fns.extend(glob(x2))
if not fns:
    gg = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV21m/*.root'
    print 'using default', gg
    fns = glob(gg)

if len(fns) != 2: # leave in specified order if there are two, user wants to print a ratio
    fns.sort()
    fns.sort(key=lambda fn: not os.path.basename(fn).startswith('mfv_')) # puts signals first, then bkg

def getit(fn, ntk):
    f = ROOT.TFile.Open(fn)
    t = f.Get('%s/t' % ntk)
    if not t:
        return (-1,-1,-1), (-1,-1,-1), (-1,-1,-1), (-1,-1,-1)
    hr = draw_hist_register(t, True)
    def c(cut):
        #cut = '(%s) && njets >= 4 && jetht > 700 && jetht < 1000' % cut
        #cut = '(%s) && njets >= 4 && jetht > 700' % cut
        #cut = '(%s) && gen_flavor_code == 2' % cut
        h,n = hr.draw('weight', cut, binning='1,0,1', get_n=True, goff=True)
        return (n,) + get_integral(h)
    n1v = c('nvtx==1')
    n1vb = c('nvtx==1 && gen_flavor_code==2')
    if ntk == 'mfvMiniTreeNtk3or4':
        n2v = c('nvtx>=2 && ntk0==4 && ntk1==3')
    else:
        n2v = c('nvtx>=2')
        n2vb = c('nvtx>=2 && gen_flavor_code==2')
    return n1v, n1vb, n2v, n2vb

fmt = '%50s %9s %9s %9s      %7s  %9s +- %9s  %9s +- %9s     %7s  %9s +- %9s  %9s +- %9s'

int_lumi = ac.int_lumi_2017 * ac.scale_factor_2017
print 'MC scaled to int. lumi. %.3f/fb' % (int_lumi/1000)

for ntk in ntks:
    print
    print ntk
    print fmt % ('sample', 'xsec', 'nevents', 'weight', 'f1vb', 'rn1v', 'unc', 'wn1v', 'unc', 'f2vb', 'rn2v', 'unc', 'wn2v', 'unc')

    raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0, 0, 0, 0, 0, 0
    seen_bkg, seen_data = False, False

    weighted = []
    for fn in fns:
        (r1v, n1v, en1v), (_, n1vb, _), (r2v, n2v, en2v), (_, n2vb, _) = getit(fn, ntk)
        f1vb = float(n1vb) / n1v if r1v > 0 else 0.
        f2vb = float(n2vb) / n2v if r2v > 0 else 0.

        sname = os.path.basename(fn).replace('.root', '')
        is_sig = sname.startswith('mfv_')
        is_data = sname.startswith('ReRecoJetHT') or sname.startswith('JetHT') or sname.startswith('SingleMuon') or sname.startswith('SingleElectron')
        is_bkg = sname in ['qcdht0700_2017', 'qcdht1000_2017', 'qcdht1500_2017', 'qcdht2000_2017', 'ttbarht0600_2017', 'ttbarht0800_2017', 'ttbarht1200_2017', 'ttbarht2500_2017']
        include_in_sum = is_bkg

        if is_sig and nosig:
            continue
        if is_bkg and not seen_bkg:
            seen_bkg = True
            print
        if is_data and not seen_data:
            seen_data = True
            print

        #if '_2017' not in sname:
        #    sname += '_2017'
        #    sname = sname.replace('tau','tau0')

        if hasattr(Samples, sname):
            sample = getattr(Samples, sname)
            if not sample.is_mc:
                w = 1.
                print fmt % (sample.name, '', '', '',
                             '', r1v, '%9.0f' % abs(r1v)**0.5, '', '',
                             '', r2v, '%9.0f' % abs(r2v)**0.5, '', '')
            else:
                w = int_lumi * sample.partial_weight(fn)
                if sample.is_signal:
                    xsec = '%9.3f' % sample.xsec
                else:
                    xsec = '%9.0f' % sample.xsec

                x = (r1v, r1v**0.5, w*n1v, w*en1v), (r2v, r2v**0.5, w*n2v, w*en2v)
                weighted.append((w*n1v, w*en1v, w*n2v, w*en2v))
                print fmt % (sample.name,
                             xsec,
                             '%.0f' % sample.nevents(fn),
                             '%9.3g' % w,
                             '%7.2f' % f1vb,
                             x[0][0],
                             '%9.0f' % x[0][1],
                             '%9.2f' % x[0][2],
                             '%9.2f' % x[0][3],
                             '%7.2f' % f2vb,
                             x[1][0],
                             '%9.0f' % x[1][1],
                             '%9.2f' % x[1][2],
                             '%9.2f' % x[1][3],
                             )
        else:
            print '%36s  n1v = %9.2f  n2v = %9.2f' % (sname, n1v, n2v)

        if include_in_sum:
            raw_n1v += r1v
            sum_n1v += n1v * w
            var_n1v += (en1v * w)**2
            raw_n2v += r2v
            sum_n2v += n2v * w
            var_n2v += (en2v * w)**2

    if len(weighted) == 2:
        (n1v1, en1v1, n2v1, en2v1), (n1v2, en1v2, n2v2, en2v2) = weighted
        ratn1 = (-1, -1) if n1v1 == 0 else interval_to_vpme(*propagate_ratio(n1v2, n1v1, en1v2, en1v1))
        ratn2 = (-1, -1) if n2v1 == 0 else interval_to_vpme(*propagate_ratio(n2v2, n2v1, en2v2, en2v1))
        print 'ratio second/first: n1v %.2f +- %.2f   n2v %.2f +- %.2f' % (ratn1 + ratn2)

    if raw_n1v or raw_n2v:
        x = (raw_n1v, raw_n1v**0.5, sum_n1v, var_n1v**0.5), (raw_n2v, raw_n2v**0.5, sum_n2v, var_n2v**0.5)
        print
        print fmt % ('total background', '', '', '',
                     '', x[0][0], '%9.2f' % x[0][1], '%9.2f' % x[0][2], '%9.2f' % x[0][3],
                     '', x[1][0], '%9.2f' % x[1][1], '%9.2f' % x[1][2], '%9.2f' % x[1][3])

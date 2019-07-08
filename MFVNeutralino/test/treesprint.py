#!/usr/bin/env python

import sys, os
from glob import glob
from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools.Year import year
from JMTucker.Tools.general import typed_from_argv, bool_from_argv
from JMTucker.Tools import Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

year = typed_from_argv(int, year, name='year')
yearcheck = not bool_from_argv('noyearcheck')
nosig = bool_from_argv('nosig')
nodata = bool_from_argv('nodata')
nobkg = bool_from_argv('nobkg')
onlysig = bool_from_argv('onlysig')
onlydata = bool_from_argv('onlydata')
onlybkg = bool_from_argv('onlybkg')
sumall = bool_from_argv('sumall')

which = typed_from_argv(int, -1)
ntks = ('mfvMiniTreeNtk3', 'mfvMiniTreeNtk4', 'mfvMiniTree')
if which != -1:
    ntks_to_trees = {3: 'mfvMiniTreeNtk3', 4: 'mfvMiniTreeNtk4', 5: 'mfvMiniTree', 7: 'mfvMiniTreeNtk3or4'}
    if which not in ntks_to_trees:
        raise ValueError('bad ntks %s' % which)
    ntks = (ntks_to_trees[which],)

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
    gg = '/uscms_data/d2/tucker/crab_dirs/MiniTree%s/*.root' % version
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
        n2vb = c('nvtx>=2 && ntk0==4 && ntk1==3 && gen_flavor_code==2')
    else:
        n2v = c('nvtx>=2')
        n2vb = c('nvtx>=2 && gen_flavor_code==2')
    return n1v, n1vb, n2v, n2vb

fmt = '%40s %9s %9s %9s      %14s  %9s +- %9s  %9s +- %9s     %12s  %9s +- %9s  %9s +- %9s'

if year == 2017:
    int_lumi = ac.int_lumi_2017 * ac.scale_factor_2017
elif year == 2018:
    int_lumi = ac.int_lumi_2018 * ac.scale_factor_2018

print 'MC scaled to int. lumi. %.3f/fb' % (int_lumi/1000)

for ntk in ntks:
    print
    print ntk
    print fmt % ('sample', 'xsec', 'nevents', 'weight', 'f1vb', 'rn1v', 'unc', 'wn1v', 'unc', 'f2vb', 'rn2v', 'unc', 'wn2v', 'unc')

    raw_n1v, sum_n1v, var_n1v, sum_n1vb, raw_n2v, sum_n2v, var_n2v, sum_n2vb = 0, 0, 0, 0, 0, 0, 0, 0
    seen_bkg, seen_data = False, False

    weighted = []
    for fn in fns:
        if yearcheck and str(year) not in fn:
            continue

        (r1v, n1v, en1v), (_, n1vb, _), (r2v, n2v, en2v), (_, n2vb, _) = getit(fn, ntk)
        f1vb = float(n1vb) / n1v if r1v > 0 else 0.
        ef1vb = (f1vb * (1-f1vb) / effective_n(n1v,en1v))**0.5 if r1v > 0 else 0.
        f2vb = float(n2vb) / n2v if r2v > 0 else 0.
        ef2vb = (f2vb * (1-f2vb) / effective_n(n2v,en2v))**0.5 if r2v > 0 else 0.

        sname = os.path.basename(fn).replace('.root', '')
        is_sig = sname.startswith('mfv_')
        is_data = sname.startswith('JetHT') or sname.startswith('SingleMuon') or sname.startswith('SingleElectron')
        is_bkg = any((sname.startswith(s) for s in ('qcdht0700', 'qcdht1000', 'qcdht1500', 'qcdht2000', 'ttbarht0600', 'ttbarht0800', 'ttbarht1200', 'ttbarht2500')))
        is_other = not any((is_sig, is_data, is_bkg))
        include_in_sum = sumall or is_bkg

        if any((onlysig  and (is_other or is_data or is_bkg),
                onlydata and (is_other or is_sig or is_bkg),
                onlybkg  and (is_other or is_sig or is_data),
                is_sig and nosig,
                is_data and nodata,
                is_bkg and nobkg)):
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
                             '%5.3f +- %5.3f' % (f1vb, ef1vb),
                             x[0][0],
                             '%9.0f' % x[0][1],
                             '%9.2f' % x[0][2],
                             '%9.2f' % x[0][3],
                             '%4.2f +- %4.2f' % (f2vb, ef2vb),
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
            sum_n1vb += n1vb * w
            sum_n2v += n2v * w
            var_n2v += (en2v * w)**2
            sum_n2vb += n2vb * w

    if len(weighted) == 2:
        (n1v1, en1v1, n2v1, en2v1), (n1v2, en1v2, n2v2, en2v2) = weighted
        ratn1 = (-1, -1) if n1v1 == 0 else interval_to_vpme(*propagate_ratio(n1v2, n1v1, en1v2, en1v1))
        ratn2 = (-1, -1) if n2v1 == 0 else interval_to_vpme(*propagate_ratio(n2v2, n2v1, en2v2, en2v1))
        print 'ratio second/first: n1v %.2f +- %.2f   n2v %.2f +- %.2f' % (ratn1 + ratn2)

    if raw_n1v or raw_n2v:
        x = (raw_n1v, raw_n1v**0.5, sum_n1v, var_n1v**0.5), (raw_n2v, raw_n2v**0.5, sum_n2v, var_n2v**0.5)
        f1vb = float(sum_n1vb) / sum_n1v if raw_n1v > 0 else 0.
        ef1vb = (f1vb * (1-f1vb) / effective_n(sum_n1v,var_n1v**0.5))**0.5 if raw_n1v > 0 else 0.
        f2vb = float(sum_n2vb) / sum_n2v if raw_n2v > 0 else 0.
        ef2vb = (f2vb * (1-f2vb) / effective_n(sum_n2v,var_n2v**0.5))**0.5 if raw_n2v > 0 else 0.
        print
        print fmt % ('total background', '', '', '',
                     '%5.3f +- %5.3f' % (f1vb, ef1vb), x[0][0], '%9.2f' % x[0][1], '%9.2f' % x[0][2], '%9.2f' % x[0][3],
                     '%4.2f +- %4.2f' % (f2vb, ef2vb), x[1][0], '%9.2f' % x[1][1], '%9.2f' % x[1][2], '%9.2f' % x[1][3])

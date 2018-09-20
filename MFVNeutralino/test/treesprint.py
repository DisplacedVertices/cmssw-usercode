#!/usr/bin/env python

import sys, os, glob
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools.general import typed_from_argv
from JMTucker.Tools import Samples
import JMTucker.MFVNeutralino.AnalysisConstants as ac

ROOT.gErrorIgnoreLevel = 6000
fns = [x for x in sys.argv[1:] if x.endswith('.root') and (os.path.isfile(x) or x.startswith('root://'))]
if not fns:
    gg = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV18m/*.root'
    print 'using default', gg
    fns = glob.glob(gg)
fns = [x for x in fns if '2015' not in x and not 'hip1p0' in x]
fns.sort()
fns.sort(key=lambda fn: not os.path.basename(fn).startswith('mfv_')) # puts signals first, then bkg

def getit(fn, ntk):
    f = ROOT.TFile.Open(fn)
    t = f.Get('%s/t' % ntk)
    hr = draw_hist_register(t, True)
    def c(cut):
        #cut = '(%s) && njets >= 4 && jetht > 700 && jetht < 1000' % cut
        #cut = '(%s) && njets >= 4 && jetht > 700' % cut
        h,n = hr.draw('weight', cut, binning='1,0,1', get_n=True, goff=True)
        return (n,) + get_integral(h)
    dbvreq = '0.01'
    n1v = c('nvtx==1 && dist0 >= %s' % dbvreq) # ignores the % of events where two-vertex events become one-vertex events
    if ntk == 'mfvMiniTreeNtk3or4':
        n2v = c('nvtx>=2 && ntk0==4 && ntk1==3')
    else:
        n2v = c('nvtx>=2 && dist0 >= %s && dist1 >= %s' % (dbvreq, dbvreq))
    return n1v, n2v

fmt = '%40s %9s %9s %9s   %9s +- %9s  %9s +- %9s  %9s +- %9s  %9s +- %9s'

int_lumi = ac.int_lumi_2017 * ac.scale_factor_2017
print 'scaled to int. lumi. %.3f/fb' % (int_lumi/1000)

for ntk in 'mfvMiniTreeNtk3', 'mfvMiniTreeNtk4', 'mfvMiniTree':
    print
    print ntk
    print fmt % ('sample', 'xsec', 'nevents', 'weight', 'rn1v', 'unc', 'wn1v', 'unc', 'rn2v', 'unc', 'wn2v', 'unc')

    raw_n1v, sum_n1v, var_n1v, raw_n2v, sum_n2v, var_n2v = 0, 0, 0, 0, 0, 0
    seen_bkg, seen_data = False, False

    for fn in fns:
        (r1v, n1v, en1v), (r2v, n2v, en2v) = getit(fn, ntk)

        sname = os.path.basename(fn).replace('.root', '')
        is_sig = sname.startswith('mfv_')
        is_data = sname.startswith('JetHT') or sname.startswith('SingleMuon') or sname.startswith('SingleElectron')
        is_bkg = not is_sig and not is_data

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
                print fmt % (sample.name, '', '', '', '',
                             r1v, '%9.0f' % r1v**0.5, '', '', 
                             r2v, '%9.0f' % r2v**0.5, '', '')
            else:
                w = int_lumi * sample.partial_weight(fn)
                if sample.is_signal:
                    xsec = '%9.3f' % sample.xsec
                else:
                    xsec = '%9.0f' % sample.xsec

                x = (r1v, r1v**0.5, w*n1v, w*en1v), (r2v, r2v**0.5, w*n2v, w*en2v)
                print fmt % (sample.name,
                             xsec,
                             '%.0f' % sample.nevents(fn),
                             '%9.3g' % w,
                             x[0][0],
                             '%9.0f' % x[0][1],
                             '%9.2f' % x[0][2],
                             '%9.2f' % x[0][3],
                             x[1][0],
                             '%9.0f' % x[1][1],
                             '%9.2f' % x[1][2],
                             '%9.2f' % x[1][3],
                             )
        else:
            print '%36s  n1v = %9.2f  n2v = %9.2f' % (sname, n1v, n2v)

        if is_bkg:
            raw_n1v += r1v
            sum_n1v += n1v * w
            var_n1v += (en1v * w)**2
            raw_n2v += r2v
            sum_n2v += n2v * w
            var_n2v += (en2v * w)**2

    if raw_n1v or raw_n2v:
        x = (raw_n1v, raw_n1v**0.5, sum_n1v, var_n1v**0.5), (raw_n2v, raw_n2v**0.5, sum_n2v, var_n2v**0.5)
        print
        print fmt % ('total background', '', '', '',
                     x[0][0], '%9.2f' % x[0][1], '%9.2f' % x[0][2], '%9.2f' % x[0][3],
                     x[1][0], '%9.2f' % x[1][1], '%9.2f' % x[1][2], '%9.2f' % x[1][3])

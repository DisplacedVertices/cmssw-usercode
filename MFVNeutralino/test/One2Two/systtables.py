import sys
from array import array
from collections import defaultdict
from DVCode.Tools.ROOTTools import *
set_style()

def mean(l,w=None):
    if w is None:
        return sum(l)/len(l)
    else:
        s, sw = 0., 0.
        for c,e in zip(l,w):
            s += c*e
            sw += e
        return s/sw

def median(l,w=None):
    if w is None:
        l = l[:]
        l.sort()
        n = len(l)
        if n % 2 == 0:
            return 0.5*(l[n/2] + l[n/2-1])
        else:
            return l[n/2]
    else:
        l = zip(l,w)
        l.sort(key=lambda x: x[0])
        sw = sum(w)
        mid = sw/2
        cum = 0.
        for x,e in l:
            cum += e
            if cum > mid:
                return x

def rms(l,w=None):
    mu = mean(l,w)
    if w is None:
        w = [1.]*len(l)
    l = zip(l,w)
    s, sw = 0., 0.
    for x,e in l:
        c = (x - mu)**2
        s += c*e
        sw += e
    return (s/(sw-1))**0.5

if 0:
    stats = {}

    fns = [
        'default320110.root',
        'dphivv340160.root',
        'sum300100.root',
        'sum300100qcddown.root',
        'sum300100qcdup.root',
    ]

    for fn in fns:
        print fn
        f = ROOT.TFile('~/jen/scratch/%s' % fn)
        c1 = f.Get('c1')
        hs = list(c1.GetListOfPrimitives())
        means, medians, mins, maxes = [], [], [], []
        print '%10s %15s %15s %15s %15s %15s' % ('ibin', 'mean', 'rms', 'median', 'min', 'max')
        for i in xrange(1,7):
            cs = [h.GetBinContent(i) for h in hs]
            es = [h.GetBinError(i) for h in hs]
            mean_ = mean(cs, es)
            rms_ = rms(cs, es)
            median_ = median(cs, es)
            min_ = min(cs)
            max_ = max(cs)
            print '%10i %15.4f %15.4f %15.4f %15.4f %15.4f' % (i, mean_, rms_, median_, min_, max_)
            means.append(mean_)
            medians.append(median_)
        stats[fn] = (means, medians)
        print

if 1:
    # grep ibin -A6 tentimes_wthrowbsd2d_wpoisnum.txt | grep 'e-0' > tentimes_wthrowbsd2d_wpoisnum_grepped.txt
    class datum:
        def __init__(self, l):
            self.normval, self.normerr, self.val, self.err, self.norig, self.relerr = [float(x) for x in l]
        def __repr__(self):
            return '%f +- %f' % (self.val, self.err)

    nbins = 6
    times = int(sys.argv[1])
    fns = sys.argv[2:]

    for fn in fns:
        print fn
        d = defaultdict(list)
        for line in open(fn):
            line = line.split()
            if len(line) == nbins+1:
                ibin = int(line.pop(0))
                if len(d[ibin]) < times:
                    d[ibin].append(datum(line))

        d = dict(d)
        assert len(d) == nbins
        assert all(len(x) == times for x in d.values())

        print '%4s %10s %10s %10s %10s %10s' % ('ibin', 'mean(vals)', 'rms(vals)', 'mean(errs)', 'min(vals)', 'max(vals)')
        for ibin in xrange(1,nbins+1):
            #print ibin
            #print d[ibin]

            vals = [x.val for x in d[ibin]]
            errs = [x.err for x in d[ibin]]
            print '%4i %10.6f %10.6f %10.6f %10.6f %10.6f' % (ibin, mean(vals), rms(vals), mean(errs), min(vals), max(vals))

    if 1:
        ps = plot_saver('plots/systtables_statspread_cwr', size=(600,600))

        binning = [0.02*i for i in xrange(5)] + [0.1, .15] # JMTBAD keep in sync with Templates.cc
        hs = [ROOT.TH1D('h%i' % i, ';d_{VV}^{C} (cm);events', len(binning)-1, array('d', binning)) for i in xrange(times)]

        colors = [1] * times #range(1, ) + [46]
        assert len(colors) == times

        for h,c in zip(hs, colors):
            h.SetLineColor(c)
            h.SetLineWidth(2)
            h.Scale(251.)
            h.SetStats(0)

        for ibin in xrange(1, nbins+1):
            for ih, x in enumerate(d[ibin]):
                hs[ih].SetBinContent(ibin, x.val)
                hs[ih].SetBinError  (ibin, x.err)

        for i,h in enumerate(hs):
            if i == 0:
                h.Draw('hist e')
            else:
                h.Draw('hist e same')
            h.GetYaxis().SetRangeUser(5e-2, 350)

        ps.save('statspread')

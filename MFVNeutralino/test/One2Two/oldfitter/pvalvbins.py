#!/usr/bin/env python

from base_draw_fit import *

ps = plot_saver('plots/pval_v_bins')

hbin = [ROOT.TH2F('bin%i' % i, ';p;c', 40, 0, 1, 100, 0, 1) for i in xrange(6)]
hnbin = ROOT.TH2F('nbin', '', 40, 0, 1, 7, 0, 7)

for h in hbin + [hnbin]:
    h.SetStats(0)

pvfn = []

for fn in batch_fns:
    f = ROOT.TFile(fn)
    t = f.Get('Fitter/t_fit_info')
    pv = None
    for j in ttree_iterator(t):
        if pv is not None:
            raise 'problem with ' + fn
        pv = t.pval_signif
    pvfn.append((pv,fn))

    h = None
    for key in f.Get('Fitter').GetListOfKeys():
        n = key.GetName()
        if n.startswith('seed'):
            h = f.Get('Fitter/%s/finalized_templates/h_data_rebinned' % n)
            break
    if h is None:
        print 'skipping', fn
        continue

    h.Scale(1/h.Integral())
    nbin = 0
    for i in xrange(6):
        c = h.GetBinContent(i+1)
        hbin[i].Fill(pv, c)
        if c > 0.001:
            nbin += 1
    hnbin.Fill(pv, nbin)

for i in xrange(6):
    hbin[i].Draw('colz')
    ps.save(hbin[i].GetName())

hnbin.Draw('colz')
ps.save('nbin')

pvfn.sort()
for pv,fn in pvfn[:5]:
    print pv, fn

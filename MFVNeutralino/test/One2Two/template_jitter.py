#!/usr/bin/env python

from JMTucker.MFVNeutralino.MiniTreeBase import *
ps = plot_saver('plots/hme', size=(600,600))

nec = 5000 # ROOT.TColor.GetNumberOfColors() + 1
nc = 200
colors = [(ic, ROOT.TColor(ic, 0.3 + ic*0.4/float(nc), 0, 0)) for ic in xrange(nec+1, nec+1+nc)]

f = ROOT.TFile('mfvo2t.root')
orig = False
if orig:
    d = f.Get('ClearedJetsTemplater/seed0000_toy0000/templates')
else:
    d = f.Get('Fitter/seed00_toy00/fit_results/bkg_template_scan_nuis_b')

for nuis0_d in d.GetListOfKeys():
    nuis0_d = nuis0_d.ReadObj()
    nuis0_n = nuis0_d.GetName()
    print nuis0_n
    if nuis0_n != 'imu_22' and nuis0_n != 'nuis0_022':
        continue

    first = True
    means = []
    rmses = []
    vals = []
    for i in xrange(10):
        vals.append([])

    for i, h in enumerate(nuis0_d.GetListOfKeys()):
        h = h.ReadObj()
        h.SetLineWidth(2)
        h.SetStats(0)
        h.GetXaxis().SetRangeUser(0, 0.25)
        h.SetTitle(';d_{VV} (cm);frac.')
        h.SetLineColor(colors[i][0])

        means.append(h.GetMean())
        rmses.append(h.GetRMS())
        for ibin in xrange(1,11):
            vals[ibin-1].append(h.GetBinContent(ibin))

        if first:
            h.Draw('hist')
            first = False
        else:
            h.Draw('hist same')

    ps.save(nuis0_n)

    names = ['means', 'rmses'] + ['val%i' % i for i in xrange(10)]
    n = len(means)
    start1 = 0.0005
    stop1 = 0.04
    delta1_orig = (stop1 - start1)/100
    delta1_draw = (stop1 - start1)/200
    x = arrit([start1 + delta1_draw * i for i in xrange(200)])
    for i, thing in enumerate([means, rmses] + vals):
        g = ROOT.TGraph(n, x, arrit(thing))
        g.SetTitle(names[i])
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.8)
        g.Draw('ALP')
        ls = []
        for j in xrange(100):
            xx = start1 + j * delta1_orig
            l = ROOT.TLine(xx,-1000,xx,1000)
            ls.append(l)
            l.Draw()

        ps.save(nuis0_n + '_' + names[i])

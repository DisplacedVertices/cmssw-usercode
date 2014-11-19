#!/usr/bin/env python

from array import array
from JMTucker.Tools.ROOTTools import *
set_style()

c = ROOT.TCanvas('c', '', 50, 50, 900, 500)
c.SetLogx()
c.SetLogy()

f = ROOT.TFile('trees/MultiJetPk2012.root')
t = f.Get('mfvMiniTree/t')
title = ';d_{BV} (cm);events'

bins = [j*0.002 for j in range(20)] + [0.04, 0.0425, 0.045, 0.05, 0.055, 0.06, 0.07, 0.085, 0.1, 0.2, 0.4, 2.5]
bins = array('d', bins)

h = ROOT.TH1D('h', title, len(bins)-1, bins)
hfine = ROOT.TH1D('hfine', title, 1250, 0, 2.5)

h.SetLineWidth(2)
hfine.SetLineColor(4)
h.SetStats(0)
hfine.SetStats(0)

t.SetAlias('dbv0', '(x0*x0 + y0*y0)**0.5')
cut = 'nvtx == 1'
t.Draw('dbv0 >> +h',     cut)
t.Draw('dbv0 >> +hfine', cut)
#assert not h.GetBinContent(h.GetNbinsX()+1)

h.Draw('e')
h.GetXaxis().SetRangeUser(0.02, 2.5)
hfine.GetXaxis().SetRangeUser(0.02, 2.5)
hfine.Draw('same e')
c.SaveAs('~/asdf/a.png')

h.Scale(1, 'width')
h.SetTitle(title + '/bin width')
h.Draw('e')
hfine.Draw('same e')
c.SaveAs('~/asdf/a2.png')

#fc = ROOT.TF1('fc', '[0]*exp(-[1]*x**[2])', 0.02, 0.05)
#fc.SetLineColor(2)
#fc.SetLineWidth(1)
#fc.SetParameters(h.Integral()*h.GetBinWidth(1), 1, 1)
#hfine.Fit(fc, 'RV')
#
#c.SaveAs('~/asdf/a.png')

#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../plots/bkgest/deltaphi', size=(700,700), log=False, root=False)

ROOT.TH1.AddDirectory(0)
colors = [1, 1, 1, ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2]

n1s = ['dphijv', 'dphijvmin', 'dphijj', 'dphijj', 'dphijj', 'dphijj', 'dphijj', 'dphijj']
n2s = ['dphijv', 'dphijvmin', 'jetswr1_dphijj', 'jetswr1_dphivv_dphijv', 'jetswr1_dphivv_dphijvmin', 'jetswr0_dphijj', 'jetswr0_dphivv_dphijv', 'jetswr0_dphivv_dphijvmin']

for j in range(len(n1s)):
  h1s = []
  h2s = []
  l = ROOT.TLegend(0.50,0.65,0.85,0.85) if j==0 or j==1 else ROOT.TLegend(0.15,0.65,0.85,0.85)
  for i in [3,4,5]:
    f = ROOT.TFile('2v_from_jets_deltaphi_%itrack.root' % i)
    h1 = f.Get('h_1v_%s' % n1s[j])
    h2 = f.Get('h_c1v_%s' % n2s[j])
    l.AddEntry(h1, '%i-track %s' % (i,h1.GetXaxis().GetTitle()))
    l.AddEntry(h2, '%i-track %s' % (i,h2.GetXaxis().GetTitle()))
    h1.Rebin(10)
    h2.Rebin(10)
    h1.SetStats(0)
    h1.SetLineColor(colors[i])
    h2.SetStats(0)
    h2.SetLineColor(colors[i])
    h2.SetLineWidth(3)
    if i == 3:
      h1.SetTitle(';#Delta#phi;')
      h1.Scale(1./h1.Integral())
      h1.GetYaxis().SetRangeUser(0, 1 if j==1 else 0.3)
      h1.Draw()
    else:
      h1.DrawNormalized('sames')
    h2.DrawNormalized('sames')
    h1s.append(h1)
    h2s.append(h2)
  l.SetFillColor(0)
  l.Draw()
  ps.save(n2s[j])

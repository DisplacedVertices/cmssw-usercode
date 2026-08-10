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

l = ROOT.TLegend(0.15,0.75,0.85,0.85)
for i in [3,4,5]:
  f = ROOT.TFile('2v_from_jets_%itrack_average%i_dphijvmin_v11.root' % (i,i))
  h = f.Get('h_c1v_absdphivv_dphijvmin')
  l.AddEntry(h, 'constructed from %i-%strack one-vertex events' % (i, 'or-more-' if i==5 else ''), 'LE')
  h.Rebin(10)
  h.SetStats(0)
  h.SetLineColor(colors[i])
  h.SetLineWidth(3)
  if i == 3:
    h.SetTitle(';%s;' % h.GetXaxis().GetTitle())
    h.Scale(1./h.Integral())
    h.GetYaxis().SetRangeUser(0,0.4)
    h.Draw()
  else:
    h.DrawNormalized('sames')
l.SetFillColor(0)
l.Draw()
ps.save('absdphivv_dphijvmin')

f1s = []
f2s = []
l = ROOT.TLegend(0.15,0.65,0.85,0.85)
for i in [3,4,5]:
  f = ROOT.TFile('2v_from_jets_%itrack_average%i_dphijvmin_v11.root' % (i,i))
  f_dphi1 = f.Get('f_dphi')
  f_dphi2 = f.Get('f_dphi2')
  print '%i-track: f1(x) = (x - %.2f)^%i + %.2f, f2(x) = %8.2f * cos(2x) + %8.2f' % (i, f_dphi1.GetParameter(0), f_dphi1.GetParameter(1), f_dphi1.GetParameter(2), f_dphi2.GetParameter(0), f_dphi2.GetParameter(1))
  integral1 = f_dphi1.Integral(0,3.1416)
  integral2 = f_dphi2.Integral(0,3.1416)
  f_dphi1_norm = ROOT.TF1("f1", "((abs(x)-[0])**[1] + [2]) / [3]", 0, 3.1416)
  f_dphi1_norm.SetParameters(f_dphi1.GetParameter(0), f_dphi1.GetParameter(1), f_dphi1.GetParameter(2), integral1)
  f_dphi2_norm = ROOT.TF1("f2", "([0]*cos(2*x) + [1]) / [2]", 0, 3.1416)
  f_dphi2_norm.SetParameters(f_dphi2.GetParameter(0), f_dphi2.GetParameter(1), integral2)
  if i == 3:
    f_dphi1_norm.SetTitle(';|#Delta#phi|;')
    f_dphi1_norm.GetYaxis().SetRangeUser(0,1)
    f_dphi1_norm.SetLineColor(ROOT.kBlack)
    f_dphi1_norm.Draw()
    l.AddEntry(f_dphi1_norm, 'default: (x - %.2f)^%i + %.2f' % (f_dphi1.GetParameter(0), f_dphi1.GetParameter(1), f_dphi1.GetParameter(2)))
  f_dphi2_norm.SetLineColor(colors[i])
  f_dphi2_norm.Draw('sames')
  l.AddEntry(f_dphi2_norm, '%i-track: %8.2f * cos(2x) + %8.2f' % (i, f_dphi2.GetParameter(0), f_dphi2.GetParameter(1)))
  f1s.append(f_dphi1_norm)
  f2s.append(f_dphi2_norm)
l.SetFillColor(0)
l.Draw()
ps.save('f_dphi')

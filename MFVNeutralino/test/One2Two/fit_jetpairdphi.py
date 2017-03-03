#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../plots/bkgest/fit_jetpairdphi', size=(700,700), log=False, root=False)

ntk = ['presel', '3-track', '3-or-4-track', '4-track', '5-or-more-track']
fns = ['/uscms_data/d2/tucker/crab_dirs/HistosV10/ntk5/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10/ntk3/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10/ntk3or4/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10/ntk4/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10/ntk5/background.root']

for i,n in enumerate(ntk):
  f1 = ROOT.TFile(fns[i])
  h1 = f1.Get('mfvEventHistosOnlyOneVtx/h_jet_pairdphi')
  if n == 'presel':
    h1 = f1.Get('mfvEventHistosPreSel/h_jet_pairdphi')
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kBlue)
  h1.SetLineWidth(3)
  h1.Scale(1./h1.Integral())
  h1.GetYaxis().SetRangeUser(0,0.02)
  f_dphi = ROOT.TF1("f_dphi", "[1]*((abs(x)-[0])**2 + [2])", 0.8, 3.15)
  if n == 'presel':
    f_dphi = ROOT.TF1("f_dphi", "[1]*((abs(x)-[0])**2 + [2])", 1.0, 3.15)
  f_dphi.SetParameters(0,0,0)
  h1.Fit('f_dphi', 'R')
  h1.SetTitle(';#Delta#phi;')
  h1.Draw()
  l1 = ROOT.TLegend(0.15,0.75,0.85,0.85)
  l1.AddEntry(h1, '#Delta#phi_{JJ}, %s one-vertex events' % n, 'LE')
  l1.AddEntry(f_dphi, '(|#Delta#phi| - c)^{2} + a: c = %.2f #pm %.2f, a = %.2f #pm %.2f' % (f_dphi.GetParameter(0), f_dphi.GetParError(0), f_dphi.GetParameter(2), f_dphi.GetParError(2)), 'L')
  l1.SetFillColor(0)
  l1.Draw()
  ps.save('%s_jetpairdphi' % n)

ROOT.TH1.AddDirectory(0)
for n in ['mfvEventHistosOnlyOneVtx/h_jet_pairdphi', 'mfvVertexHistosOnlyOneVtx/h_sv_best0_jets_deltaphi']:
  colors = [1, ROOT.kRed, 1, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kViolet]
  l = ROOT.TLegend(0.15,0.75,0.85,0.85)
  h2s = []
  for i in [1,3,4]:
    f = ROOT.TFile(fns[i])
    h = f.Get(n)
    h.SetStats(0)
    h.SetLineColor(colors[i])
    h.SetLineWidth(3)
    h.Scale(1./h.Integral())
    if 'best0' in n:
      h.Rebin(5)
    h.GetYaxis().SetRangeUser(0,2./h.GetNbinsX())
    h.SetTitle(';#Delta#phi_{%s};' % ('JV' if 'best0' in n else 'JJ'))
    if i == 1:
      h.Draw()
    else:
      h.Draw('sames')
    l.AddEntry(h, '%s one-vertex events' % ntk[i], 'LE')
    h2 = ROOT.TH1F(h.GetName(), ';|#Delta#phi_{%s}|' % ('JV' if 'best0' in n else 'JJ'), h.GetNbinsX()/2, 0, 3.1416)
    for j in range(1, h2.GetNbinsX()+1):
      h2.SetBinContent(j, h.GetBinContent(h.GetNbinsX()/2-j+1) + h.GetBinContent(h.GetNbinsX()/2+j))
      h2.SetBinError(j, (h.GetBinError(h.GetNbinsX()/2-j+1)**2 + h.GetBinError(h.GetNbinsX()/2+j)**2)**0.5)
    h2s.append(h2)
  l.SetFillColor(0)
  l.Draw()
  ps.save(n.split('/')[1])

  colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kViolet]
  for i,h2 in enumerate(h2s):
    h2.SetStats(0)
    h2.SetLineColor(colors[i])
    h2.SetLineWidth(3)
    h2.Scale(1./h2.Integral())
    h2.GetYaxis().SetRangeUser(0,2./h2.GetNbinsX())
    if i == 0:
      h2.Draw()
    else:
      h2.Draw('sames')
  l.Draw()
  ps.save('abs_%s'%n.split('/')[1])

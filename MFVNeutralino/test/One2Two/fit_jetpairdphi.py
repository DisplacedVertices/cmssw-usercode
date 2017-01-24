#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../plots/bkgest/fit_jetpairdphi', size=(700,700), log=False, root=False)

ntk = ['presel', '3-track', '3-or-4-track', '4-track', '5-or-more-track']
fns = ['/uscms_data/d2/tucker/crab_dirs/HistosV10/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10_ntk3/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10_ntk3or4/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10_ntk4/background.root', '/uscms_data/d2/tucker/crab_dirs/HistosV10/background.root']

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
  f_dphi = ROOT.TF1("f_dphi", "[1]*(abs(x - [0])**2 + [2])", 0.8, 3.15)
  if n == 'presel':
    f_dphi = ROOT.TF1("f_dphi", "[1]*(abs(x - [0])**2 + [2])", 1.0, 3.15)
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

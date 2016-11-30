from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('../plots/bkgest/divide_dphi', size=(600,600), log=False, root=False)

for maxtk in ['maxtk3', 'maxtk3_merge', 'ntk3', 'ntk3_wevent', 'ntk3_deltasvgaus', 'ntk3_deltasvgaus_wevent', 'average3']:
  f = ROOT.TFile('2v_from_jets_3track_%s_c0p0_e0p0_a0p0.root' % maxtk)

  h2 = f.Get('h_2v_absdphivv')
  h2.SetStats(0)
  h2.SetLineColor(ROOT.kBlue)
  h2.SetLineWidth(3)
  h2.SetTitle('%s;|#Delta#phi_{VV}|;' % maxtk)
  h2.SetMinimum(0)
  h2.Draw()

  h1 = f.Get('h_c1v_absdphivv')
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kRed)
  h1.SetLineWidth(3)
  h1.Scale(h2.Integral() / h1.Integral())
  h1.Draw('sames')

  l1 = ROOT.TLegend(0.2,0.75,0.7,0.85)
  l1.AddEntry(h2, 'two-vertex')
  l1.AddEntry(h1, 'constructed from one-vertex')
  l1.SetFillColor(0)
  l1.Draw()
  ps.save('%s_dphi' % maxtk)

  h3 = h2.Clone()
  h3.Divide(h1)
  h3.SetStats(0)
  h3.GetYaxis().SetRangeUser(0,2)
  h3.Draw()
  f_dphi = ROOT.TF1("f_dphi", "[1]*(abs(x - [0])**2 + [2])", 0, 3.15)
  f_dphi.SetParameters(0,0,0)
  h3.Fit('f_dphi')

  l2 = ROOT.TLegend(0.2,0.75,0.8,0.85)
  l2.AddEntry(h3, 'two-vertex / constructed from one-vertex')
  l2.AddEntry(f_dphi, '|#Delta#phi - c|^{2} + a: c = %.1f #pm %.1f, a = %.1f #pm %.1f' % (f_dphi.GetParameter(0), f_dphi.GetParError(0), f_dphi.GetParameter(2), f_dphi.GetParError(2)))
  l2.SetFillColor(0)
  l2.Draw()
  ps.save('%s_dphi_2v_divide_c1v' % maxtk)

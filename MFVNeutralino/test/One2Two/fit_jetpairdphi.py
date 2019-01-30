#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *

is_mc = True
year = '2017'
version = 'v22m'

set_style()
ps = plot_saver(plot_dir('fit_jetpairdphi%s%s_%s' % (version.capitalize(), '' if is_mc else '_data', year)), size=(700,700), log=False, root=False)

fn = '/uscms_data/d2/tucker/crab_dirs/Histos%s/background_%s.root' % (version.capitalize(), year)
if not is_mc:
  fn = '/uscms_data/d2/tucker/crab_dirs/HistosV15_v2/JetHT%s.root' % year

ntk = ['Ntk3', 'Ntk3or4', 'Ntk4', '']
ntracks = ['3-track', '3-or-4-track', '4-track', '5-or-more-track']
if not is_mc:
  ntk = ['Ntk3']
  ntracks = ['3-track']

f = ROOT.TFile(fn)
for i,n in enumerate(ntk):
  h = f.Get('%smfvEventHistosOnlyOneVtx/h_jet_pairdphi' % n)
  h.SetStats(0)
  h.SetLineColor(ROOT.kBlue)
  h.SetLineWidth(3)
  h.Scale(1./h.Integral())
  h.GetYaxis().SetRangeUser(0,0.02)
  f_dphi = ROOT.TF1("f_dphi", "[1]*((abs(x)-[0])**2 + [2])", 0.8, 3.15)
  f_dphi.SetParameters(0,0,0)
  h.Fit('f_dphi', 'R')
  h.SetTitle(';#Delta#phi;')
  h.Draw()
  l = ROOT.TLegend(0.15,0.75,0.85,0.85)
  l.AddEntry(h, '#Delta#phi_{JJ}, %s one-vertex events' % ntracks[i], 'LE')
  l.AddEntry(f_dphi, '(|#Delta#phi| - c)^{2} + a: c = %.2f #pm %.2f, a = %.2f #pm %.2f' % (f_dphi.GetParameter(0), f_dphi.GetParError(0), f_dphi.GetParameter(2), f_dphi.GetParError(2)), 'L')
  l.SetFillColor(0)
  l.Draw()
  ps.save('%s_jetpairdphi' % ntracks[i])


if is_mc:
  f = ROOT.TFile(fn)
  ROOT.TH1.AddDirectory(0)
  for n in ['mfvEventHistosOnlyOneVtx/h_jet_pairdphi', 'mfvVertexHistosOnlyOneVtx/h_sv_all_jets_deltaphi']:
    colors = [ROOT.kRed, 1, ROOT.kBlue, ROOT.kGreen+2]
    l = ROOT.TLegend(0.15,0.75,0.85,0.85)
    h2s = []
    for i in [0,2,3]:
      h = f.Get('%s%s' % (ntk[i], n))
      h.SetStats(0)
      h.SetLineColor(colors[i])
      h.SetLineWidth(3)
      h.Scale(1./h.Integral())
      if 'sv_all' in n:
        h.Rebin(5)
      h.GetYaxis().SetRangeUser(0,2./h.GetNbinsX())
      h.SetTitle(';#Delta#phi_{%s};' % ('JV' if 'sv_all' in n else 'JJ'))
      if i == 0:
        h.Draw()
      else:
        h.Draw('sames')
      l.AddEntry(h, '%s one-vertex events' % ntracks[i], 'LE')
      h2 = ROOT.TH1F(h.GetName(), ';|#Delta#phi_{%s}|' % ('JV' if 'sv_all' in n else 'JJ'), h.GetNbinsX()/2, 0, 3.1416)
      for j in range(1, h2.GetNbinsX()+1):
        h2.SetBinContent(j, h.GetBinContent(h.GetNbinsX()/2-j+1) + h.GetBinContent(h.GetNbinsX()/2+j))
        h2.SetBinError(j, (h.GetBinError(h.GetNbinsX()/2-j+1)**2 + h.GetBinError(h.GetNbinsX()/2+j)**2)**0.5)
      h2s.append(h2)
    l.SetFillColor(0)
    l.Draw()
    ps.save(n.split('/')[1])

    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2]
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

  for n in ['mfvVertexHistosOnlyOneVtx/h_sv_all_jet0_deltaphi0']:
    colors = [ROOT.kRed, 1, ROOT.kBlue, ROOT.kGreen+2]
    l = ROOT.TLegend(0.15,0.75,0.85,0.85)
    h2s = []
    for i in [0,2,3]:
      h = f.Get('%s%s' % (ntk[i], n))
      h.SetStats(0)
      h.SetLineColor(colors[i])
      h.SetLineWidth(3)
      h.Scale(1./h.Integral())
      h.Rebin(5)
      h.GetYaxis().SetRangeUser(0,1)
      h.SetTitle(';#Delta#phi_{JV}^{min};')
      if i == 0:
        h.Draw()
      else:
        h.Draw('sames')
      l.AddEntry(h, '%s one-vertex events' % ntracks[i], 'LE')
    l.SetFillColor(0)
    l.Draw()
    ps.save(n.split('/')[1])

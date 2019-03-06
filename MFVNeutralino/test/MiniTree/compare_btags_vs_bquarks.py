from JMTucker.Tools.ROOTTools import *

ntk = 3

set_style()
ps = plot_saver(plot_dir('compare_btags_vs_bquarks_MiniTreeV23m_ntk%s' % ntk), size=(600,600))

f = ROOT.TFile('output_btags_vs_bquarks_MiniTreeV23m_ntk%s/background.root' % ntk)
btags = ['1loose', '2loose', '1medium', '2medium', '1tight', '2tight']
btag_names = ['#geq1 loose', '#geq2 loose', '#geq1 medium', '#geq2 medium', '#geq1 tight', '#geq2 tight']

#plot jet bdisc in events with and without b quarks
for nvtx in [1,2]:
  h_jet_bdisc = f.Get('h_%dv_jet_bdisc' % nvtx)
  h_jet_bdisc.SetStats(0)
  h_jet_bdisc.SetLineColor(ROOT.kBlack)
  h_jet_bdisc.SetLineWidth(3)
  h_jet_bdisc.Scale(1./h_jet_bdisc.Integral())
  h_jet_bdisc.GetYaxis().SetRangeUser(1e-9,0.045)
  h_jet_bdisc.GetYaxis().SetTitleOffset(1.55)
  h_jet_bdisc.Draw('hist')
  h_jet_bdisc_bquarks = f.Get('h_bquarks_%dv_jet_bdisc' % nvtx)
  h_jet_bdisc_bquarks.SetStats(0)
  h_jet_bdisc_bquarks.SetLineColor(ROOT.kRed)
  h_jet_bdisc_bquarks.SetLineWidth(3)
  h_jet_bdisc_bquarks.DrawNormalized('sames')
  h_jet_bdisc_nobquarks = f.Get('h_nobquarks_%dv_jet_bdisc' % nvtx)
  h_jet_bdisc_nobquarks.SetStats(0)
  h_jet_bdisc_nobquarks.SetLineColor(ROOT.kBlue)
  h_jet_bdisc_nobquarks.SetLineWidth(3)
  h_jet_bdisc_nobquarks.DrawNormalized('sames')
  l = ROOT.TLegend(0.15,0.75,0.50,0.85)
  l.AddEntry(h_jet_bdisc, 'all events')
  l.AddEntry(h_jet_bdisc_bquarks, 'events with b quarks')
  l.AddEntry(h_jet_bdisc_nobquarks, 'events without b quarks')
  l.Draw()
  ls = []
  for bdisc_wp, bdisc_min in [('loose', 0.5803), ('med', 0.8838), ('tight', 0.9693)]:
    line = ROOT.TLine(bdisc_min, 1e-9, bdisc_min, 0.045)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()
    t = ROOT.TLatex()
    t.SetTextSize(0.03)
    t.DrawLatex(bdisc_min, 0.04, bdisc_wp)
    ls.append((line,t))
  ps.save('%dv_jet_bdisc' % nvtx)

#plot fraction of events with btag
for nvtx in [1,2]:
  x = []
  y = []
  for i,btag in enumerate(btags):
    h = f.Get('h_%dv_%s_btag_flavor_code' % (nvtx,btag))
    x.append(i+1)
    y.append(h.GetBinContent(2)/h.Integral())

  g = ROOT.TGraph(len(btags), array('d',x), array('d',y))
  g.SetTitle('%s-track %s-vertex events;;fraction with btag' % (ntk, 'one' if nvtx==1 else 'two' if nvtx==2 else ''))
  for i,name in enumerate(btag_names):
    g.GetXaxis().SetBinLabel(g.GetXaxis().FindBin(x[i]), name.replace('medium','med'))
  g.GetXaxis().SetLabelSize(0.04)
  g.GetYaxis().SetRangeUser(0,1)
  g.SetMarkerStyle(21)
  g.Draw('AP')
  h = f.Get('h_%dv_bquark_flavor_code' % nvtx)
  bquark_fraction = h.GetBinContent(2)/h.Integral()
  line = ROOT.TLine(x[0]-0.5, bquark_fraction, x[-1]+0.5, bquark_fraction)
  line.SetLineStyle(2)
  line.SetLineWidth(2)
  line.Draw()
  t = ROOT.TLatex()
  t.SetTextSize(0.03)
  t.DrawLatex(0.5*(x[0]+x[-1]), bquark_fraction, 'fraction with b quarks')
  ps.save('%dv_btag_fraction' % nvtx)

#plot fake rate vs. btag efficiency
for nvtx in [1,2]:
  if ntk == 5 and nvtx == 2:
    continue
  x = []
  y = []
  for i,btag in enumerate(btags):
    h1 = f.Get('h_bquarks_%dv_%s_btag_flavor_code' % (nvtx,btag))
    h2 = f.Get('h_nobquarks_%dv_%s_btag_flavor_code' % (nvtx,btag))
    x.append(h1.GetBinContent(2)/h1.Integral())
    y.append(h2.GetBinContent(2)/h2.Integral())

  g = ROOT.TGraph(len(btags), array('d',x), array('d',y))
  g.SetTitle('%s-track %s-vertex events;btag efficiency;fake rate' % (ntk, 'one' if nvtx==1 else 'two' if nvtx==2 else ''))
  g.GetXaxis().SetRangeUser(0,1)
  g.GetYaxis().SetRangeUser(0,1)
  g.SetMarkerStyle(21)
  g.Draw('AP')
  for i,name in enumerate(btag_names):
    t = ROOT.TLatex()
    t.SetTextSize(0.03)
    t.DrawLatex(x[i], y[i], name)
  ps.save('%dv_fakerate_vs_efficiency' % nvtx)

#plot mean dBV in events with and without btag
for nvtx in [1,2]:
  for dbv in ['all', 'longer', 'shorter']:
    if nvtx == 1 and dbv != 'all':
      continue
    x = []
    ex = []
    y1 = []
    ey1 = []
    y2 = []
    ey2 = []
    for i,btag in enumerate(btags):
      h1 = f.Get('h_%dv_%s_dbv_%s_btag' % (nvtx,dbv,btag))
      h2 = f.Get('h_%dv_%s_dbv_%s_nobtag' % (nvtx,dbv,btag))
      x.append(i+1)
      ex.append(0)
      y1.append(h1.GetMean()*10000)
      ey1.append(h1.GetMeanError()*10000)
      y2.append(h2.GetMean()*10000)
      ey2.append(h2.GetMeanError()*10000)

    g1 = ROOT.TGraphErrors(len(btags), array('d',x), array('d',y1), array('d',ex), array('d',ey1))
    g1.SetTitle('%s-track %s-vertex events;;mean %s d_{BV} (#mum)' % (ntk, 'one' if nvtx==1 else 'two' if nvtx==2 else '', dbv))
    for i,name in enumerate(btag_names):
      g1.GetXaxis().SetBinLabel(g1.GetXaxis().FindBin(x[i]), name.replace('medium','med'))
    g1.GetXaxis().SetLabelSize(0.04)
    if nvtx == 1:
      if ntk == 3 or ntk == 7:
        g1.GetYaxis().SetRangeUser(200,320)
      elif ntk == 4:
        g1.GetYaxis().SetRangeUser(170,290)
      elif ntk == 5:
        g1.GetYaxis().SetRangeUser(140,260)
    elif nvtx == 2:
      g1.GetYaxis().SetRangeUser(0,500)
    g1.GetYaxis().SetTitleOffset(1.5)
    g1.SetMarkerStyle(21)
    g1.SetMarkerColor(ROOT.kRed)
    g1.Draw('AP')

    g2 = ROOT.TGraphErrors(len(btags), array('d',x), array('d',y2), array('d',ex), array('d',ey2))
    g2.SetMarkerStyle(21)
    g2.SetMarkerColor(ROOT.kBlue)
    g2.Draw('P')

    l = ROOT.TLegend(0.50,0.15,0.85,0.25)
    l.AddEntry(g1, 'events with btag', 'PE')
    l.AddEntry(g2, 'events without btag', 'PE')
    l.Draw()

    mean_dbv = f.Get('h_%dv_%s_dbv' % (nvtx,dbv)).GetMean()*10000
    l0 = ROOT.TLine(x[0]-0.5, mean_dbv, x[-1]+0.5, mean_dbv)
    l0.SetLineStyle(2)
    l0.SetLineWidth(2)
    l0.Draw()
    t0 = ROOT.TLatex()
    t0.SetTextSize(0.03)
    t0.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv, 'mean d_{BV} in all events')

    mean_dbv_bquarks = f.Get('h_bquarks_%dv_%s_dbv' % (nvtx,dbv)).GetMean()*10000
    l1 = ROOT.TLine(x[0]-0.5, mean_dbv_bquarks, x[-1]+0.5, mean_dbv_bquarks)
    l1.SetLineStyle(2)
    l1.SetLineWidth(2)
    l1.SetLineColor(ROOT.kRed)
    l1.Draw()
    t1 = ROOT.TLatex()
    t1.SetTextSize(0.03)
    t1.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv_bquarks, 'mean d_{BV} in events with b quarks')

    mean_dbv_nobquarks = f.Get('h_nobquarks_%dv_%s_dbv' % (nvtx,dbv)).GetMean()*10000
    l2 = ROOT.TLine(x[0]-0.5, mean_dbv_nobquarks, x[-1]+0.5, mean_dbv_nobquarks)
    l2.SetLineStyle(2)
    l2.SetLineWidth(2)
    l2.SetLineColor(ROOT.kBlue)
    l2.Draw()
    t2 = ROOT.TLatex()
    t2.SetTextSize(0.03)
    t2.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv_nobquarks, 'mean d_{BV} in events without b quarks')

    ps.save('%dv_mean_%s_dbv' % (nvtx,dbv))

#plot dBV in events with and without btag
for nvtx in [1,2]:
  for dbv in ['all', 'longer', 'shorter']:
    if nvtx == 1 and dbv != 'all':
      continue
    h_dbv = f.Get('h_%dv_%s_dbv' % (nvtx,dbv))
    h_dbv.SetStats(0)
    h_dbv.SetLineColor(ROOT.kBlack)
    h_dbv.SetLineWidth(3)
    h_dbv.Scale(1./h_dbv.Integral())
    h_dbv.GetYaxis().SetRangeUser(1e-5,0.4)
    if ntk == 5 or nvtx == 2:
      h_dbv.GetYaxis().SetRangeUser(1e-5,0.8)
    h_dbv.GetYaxis().SetTitleOffset(1.55)
    h_dbv.Draw('hist')
    h_dbv_bquarks = f.Get('h_bquarks_%dv_%s_dbv' % (nvtx,dbv))
    h_dbv_bquarks.SetStats(0)
    h_dbv_bquarks.SetLineColor(ROOT.kRed)
    h_dbv_bquarks.SetLineWidth(3)
    h_dbv_bquarks.DrawNormalized('sames')
    h_dbv_nobquarks = f.Get('h_nobquarks_%dv_%s_dbv' % (nvtx,dbv))
    h_dbv_nobquarks.SetStats(0)
    h_dbv_nobquarks.SetLineColor(ROOT.kBlue)
    h_dbv_nobquarks.SetLineWidth(3)
    h_dbv_nobquarks.DrawNormalized('sames')
    for i,btag in enumerate(btags):
      h_dbv.Draw('hist')
      h_dbv_bquarks.DrawNormalized('sames')
      h_dbv_nobquarks.DrawNormalized('sames')
      h1 = f.Get('h_%dv_%s_dbv_%s_btag' % (nvtx,dbv,btag))
      h1.SetStats(0)
      h1.SetLineColor(ROOT.kMagenta)
      h1.SetLineWidth(2)
      h1.DrawNormalized('sames')
      h2 = f.Get('h_%dv_%s_dbv_%s_nobtag' % (nvtx,dbv,btag))
      h2.SetStats(0)
      h2.SetLineColor(ROOT.kAzure+10)
      h2.SetLineWidth(2)
      h2.DrawNormalized('sames')
      l = ROOT.TLegend(0.35,0.65,0.85,0.85)
      l.AddEntry(h_dbv, 'all events')
      l.AddEntry(h_dbv_bquarks, 'events with b quarks')
      l.AddEntry(h_dbv_nobquarks, 'events without b quarks')
      l.AddEntry(h1, 'events with %s btag' % btag_names[i])
      l.AddEntry(h2, 'events without %s btag' % btag_names[i])
      l.Draw()
      ps.save('%dv_%s_dbv_%s_btag' % (nvtx,dbv,btag))

#plot mean dBV in events (with, without) b quarks x (with, without) btag
for nvtx in [1,2]:
  for dbv in ['all', 'longer', 'shorter']:
    if nvtx == 1 and dbv != 'all':
      continue
    hists = [('','btag'), ('_bquarks','btag'), ('_nobquarks','btag'), ('','nobtag'), ('_bquarks','nobtag'), ('_nobquarks','nobtag')]
    colors = [ROOT.kRed, ROOT.kMagenta, ROOT.kViolet, ROOT.kBlue, ROOT.kAzure+10, ROOT.kAzure+1]
    gs = []
    l = ROOT.TLegend(0.30,0.10,0.80,0.30)
    for j,hist in enumerate(hists):
      x = []
      ex = []
      y = []
      ey = []
      for i,btag in enumerate(btags):
        x.append(i+1)
        ex.append(0)
        h = f.Get('h%s_%dv_%s_dbv_%s_%s' % (hist[0], nvtx, dbv, btag, hist[1]))
        y.append(h.GetMean()*10000)
        ey.append(h.GetMeanError()*10000)
      g = ROOT.TGraphErrors(len(btags), array('d',x), array('d',y), array('d',ex), array('d',ey))
      g.SetMarkerStyle(21)
      g.SetMarkerColor(colors[j])
      if j == 0:
        g.SetTitle('%s-track %s-vertex events;;mean %s d_{BV} (#mum)' % (ntk, 'one' if nvtx==1 else 'two' if nvtx==2 else '', dbv))
        for i,name in enumerate(btag_names):
          g.GetXaxis().SetBinLabel(g.GetXaxis().FindBin(x[i]), name.replace('medium','med'))
        g.GetXaxis().SetLabelSize(0.04)
        if nvtx == 1:
          if ntk == 3 or ntk == 7:
            g.GetYaxis().SetRangeUser(200,320)
          elif ntk == 4:
            g.GetYaxis().SetRangeUser(170,290)
          elif ntk == 5:
            g.GetYaxis().SetRangeUser(140,260)
        elif nvtx == 2:
          g.GetYaxis().SetRangeUser(0,500)
        g.GetYaxis().SetTitleOffset(1.5)
        g.Draw('AP')
      else:
        g.Draw('P')
      gs.append(g)
      l.AddEntry(g, 'events with %s%s' % (hist[1], hist[0]), 'PE')
    l.Draw()

    mean_dbv = f.Get('h_%dv_%s_dbv' % (nvtx,dbv)).GetMean()*10000
    l0 = ROOT.TLine(x[0]-0.5, mean_dbv, x[-1]+0.5, mean_dbv)
    l0.SetLineStyle(2)
    l0.SetLineWidth(2)
    l0.Draw()
    t0 = ROOT.TLatex()
    t0.SetTextSize(0.03)
    t0.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv, 'mean d_{BV} in all events')

    mean_dbv_bquarks = f.Get('h_bquarks_%dv_%s_dbv' % (nvtx,dbv)).GetMean()*10000
    l1 = ROOT.TLine(x[0]-0.5, mean_dbv_bquarks, x[-1]+0.5, mean_dbv_bquarks)
    l1.SetLineStyle(2)
    l1.SetLineWidth(2)
    l1.SetLineColor(ROOT.kRed)
    l1.Draw()
    t1 = ROOT.TLatex()
    t1.SetTextSize(0.03)
    t1.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv_bquarks, 'mean d_{BV} in events with b quarks')

    mean_dbv_nobquarks = f.Get('h_nobquarks_%dv_%s_dbv' % (nvtx,dbv)).GetMean()*10000
    l2 = ROOT.TLine(x[0]-0.5, mean_dbv_nobquarks, x[-1]+0.5, mean_dbv_nobquarks)
    l2.SetLineStyle(2)
    l2.SetLineWidth(2)
    l2.SetLineColor(ROOT.kBlue)
    l2.Draw()
    t2 = ROOT.TLatex()
    t2.SetTextSize(0.03)
    t2.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv_nobquarks, 'mean d_{BV} in events without b quarks')

    ps.save('%dv_mean_%s_dbv_bquarks_btags' % (nvtx,dbv))

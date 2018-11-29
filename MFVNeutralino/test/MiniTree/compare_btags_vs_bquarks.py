from JMTucker.Tools.ROOTTools import *

ntk = 3

set_style()
ps = plot_saver(plot_dir('compare_btags_vs_bquarks_MiniTreeV21m_ntk%s' % ntk), size=(600,600))

f = ROOT.TFile('output/background.root')
btags = ['loose_btag1', 'loose_btag2', 'medium_btag1', 'medium_btag2', 'tight_btag1', 'tight_btag2']
btag_names = ['#geq1 loose', '#geq2 loose', '#geq1 medium', '#geq2 medium', '#geq1 tight', '#geq2 tight']

#plot fraction of one-vertex events with btag
x = []
y = []
for i,btag in enumerate(btags):
  h = f.Get('h_1v_%s_flavor_code' % btag)
  x.append(i+1)
  y.append(h.GetBinContent(2)/h.Integral())

g = ROOT.TGraph(len(btags), array('d',x), array('d',y))
g.SetTitle('%s-track one-vertex events;;fraction with btag' % ntk)
for i,name in enumerate(btag_names):
  g.GetXaxis().SetBinLabel(g.GetXaxis().FindBin(x[i]), name.replace('medium','med'))
g.GetXaxis().SetLabelSize(0.04)
g.GetYaxis().SetRangeUser(0,1)
g.SetMarkerStyle(21)
g.Draw('AP')
h = f.Get('h_1v_bquark_flavor_code')
bquark_fraction = h.GetBinContent(2)/h.Integral()
line = ROOT.TLine(x[0]-0.5, bquark_fraction, x[-1]+0.5, bquark_fraction)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw()
t = ROOT.TLatex()
t.SetTextSize(0.03)
t.DrawLatex(0.5*(x[0]+x[-1]), bquark_fraction, 'fraction with bquarks')
ps.save('btag_fraction')

#plot fake rate vs. btag efficiency in one-vertex events
x = []
y = []
for i,btag in enumerate(btags):
  h1 = f.Get('h_1v_%s_flavor_code_bquarks' % btag)
  h2 = f.Get('h_1v_%s_flavor_code_nobquarks' % btag)
  x.append(h1.GetBinContent(2)/h1.Integral())
  y.append(h2.GetBinContent(2)/h2.Integral())

g = ROOT.TGraph(len(btags), array('d',x), array('d',y))
g.SetTitle('%s-track one-vertex events;btag efficiency;fake rate' % ntk)
g.GetXaxis().SetRangeUser(0,1)
g.GetYaxis().SetRangeUser(0,1)
g.SetMarkerStyle(21)
g.Draw('AP')
for i,name in enumerate(btag_names):
  t = ROOT.TLatex()
  t.SetTextSize(0.03)
  t.DrawLatex(x[i], y[i], name)
ps.save('fakerate_vs_efficiency')

#plot mean dBV in one-vertex events with and without btag
x = []
ex = []
y1 = []
ey1 = []
y2 = []
ey2 = []
for i,btag in enumerate(btags):
  h1 = f.Get('h_1v_dbv_%s' % btag)
  h2 = f.Get('h_1v_dbv_%s' % btag.replace('btag','nobtag'))
  x.append(i+1)
  ex.append(0)
  y1.append(h1.GetMean()*10000)
  ey1.append(h1.GetMeanError()*10000)
  y2.append(h2.GetMean()*10000)
  ey2.append(h2.GetMeanError()*10000)

g1 = ROOT.TGraphErrors(len(btags), array('d',x), array('d',y1), array('d',ex), array('d',ey1))
g1.SetTitle('%s-track one-vertex events;;mean d_{BV} (#mum)' % ntk)
for i,name in enumerate(btag_names):
  g1.GetXaxis().SetBinLabel(g1.GetXaxis().FindBin(x[i]), name.replace('medium','med'))
g1.GetXaxis().SetLabelSize(0.04)
g1.GetYaxis().SetRangeUser(200,320)
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

mean_dbv = f.Get('h_1v_dbv').GetMean()*10000
l0 = ROOT.TLine(x[0]-0.5, mean_dbv, x[-1]+0.5, mean_dbv)
l0.SetLineStyle(2)
l0.SetLineWidth(2)
l0.Draw()
t0 = ROOT.TLatex()
t0.SetTextSize(0.03)
t0.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv, 'mean d_{BV} in all events')

mean_dbv_bquarks = f.Get('h_1v_dbv_bquarks').GetMean()*10000
l1 = ROOT.TLine(x[0]-0.5, mean_dbv_bquarks, x[-1]+0.5, mean_dbv_bquarks)
l1.SetLineStyle(2)
l1.SetLineWidth(2)
l1.SetLineColor(ROOT.kRed)
l1.Draw()
t1 = ROOT.TLatex()
t1.SetTextSize(0.03)
t1.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv_bquarks, 'mean d_{BV} in events with b quarks')

mean_dbv_nobquarks = f.Get('h_1v_dbv_nobquarks').GetMean()*10000
l2 = ROOT.TLine(x[0]-0.5, mean_dbv_nobquarks, x[-1]+0.5, mean_dbv_nobquarks)
l2.SetLineStyle(2)
l2.SetLineWidth(2)
l2.SetLineColor(ROOT.kBlue)
l2.Draw()
t2 = ROOT.TLatex()
t2.SetTextSize(0.03)
t2.DrawLatex(0.5*(x[0]+x[-1]), mean_dbv_nobquarks, 'mean d_{BV} in events without b quarks')

ps.save('mean_dbv')

#plot dBV in one-vertex events with and without btag
h_dbv = f.Get('h_1v_dbv')
h_dbv.SetStats(0)
h_dbv.SetLineColor(ROOT.kBlack)
h_dbv.SetLineWidth(3)
h_dbv.Scale(1./h_dbv.Integral())
h_dbv.GetYaxis().SetRangeUser(1e-5,0.4)
h_dbv.GetYaxis().SetTitleOffset(1.55)
h_dbv.Draw('hist')
h_dbv_bquarks = f.Get('h_1v_dbv_bquarks')
h_dbv_bquarks.SetStats(0)
h_dbv_bquarks.SetLineColor(ROOT.kRed)
h_dbv_bquarks.SetLineWidth(3)
h_dbv_bquarks.DrawNormalized('sames')
h_dbv_nobquarks = f.Get('h_1v_dbv_nobquarks')
h_dbv_nobquarks.SetStats(0)
h_dbv_nobquarks.SetLineColor(ROOT.kBlue)
h_dbv_nobquarks.SetLineWidth(3)
h_dbv_nobquarks.DrawNormalized('sames')
for i,btag in enumerate(btags):
  h_dbv.Draw('hist')
  h_dbv_bquarks.DrawNormalized('sames')
  h_dbv_nobquarks.DrawNormalized('sames')
  h1 = f.Get('h_1v_dbv_%s' % btag)
  h1.SetStats(0)
  h1.SetLineColor(ROOT.kMagenta)
  h1.SetLineWidth(2)
  h1.DrawNormalized('sames')
  h2 = f.Get('h_1v_dbv_%s' % btag.replace('btag','nobtag'))
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
  ps.save('dbv_%s' % btag)

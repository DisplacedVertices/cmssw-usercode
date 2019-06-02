from JMTucker.Tools.ROOTTools import *

year = 2018
version = 'V25m'

set_style()
ps = plot_saver(plot_dir('compare_btags_vs_bquarks_PreselHistos%s' % version), size=(600,600))

f = ROOT.TFile('/uscms_data/d2/tucker/crab_dirs/PreselHistos%s/background_%s.root' % (version, year) )
btag_names = ['#geq1 loose', '#geq2 loose', '#geq1 medium', '#geq2 medium', '#geq1 tight', '#geq2 tight']

#plot jet bdisc in events with and without b quarks
h_jet_bdisc = f.Get('mfvEventHistosJetPreSel/h_jet_bdisc')
h_jet_bdisc.SetTitle('preselected events;jet bdisc;Number of jets')
h_jet_bdisc.SetStats(0)
h_jet_bdisc.SetLineColor(ROOT.kBlack)
h_jet_bdisc.SetLineWidth(3)
h_jet_bdisc.Scale(1./h_jet_bdisc.Integral())
h_jet_bdisc.GetYaxis().SetRangeUser(1e-9,0.1)
h_jet_bdisc.GetYaxis().SetTitleOffset(1.55)
h_jet_bdisc.Draw('hist')
h_jet_bdisc_bquarks = f.Get('mfvEventHistosJetPreSel/h_jet_bdisc_v_bquark_code').ProjectionY('h_jet_bdisc_bquarks', 3, 3)
h_jet_bdisc_bquarks.SetStats(0)
h_jet_bdisc_bquarks.SetLineColor(ROOT.kRed)
h_jet_bdisc_bquarks.SetLineWidth(3)
h_jet_bdisc_bquarks.DrawNormalized('sames')
h_jet_bdisc_nobquarks = f.Get('mfvEventHistosJetPreSel/h_jet_bdisc_v_bquark_code').ProjectionY('h_jet_bdisc_nobquarks', 1, 2)
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

if year == 2017 :
  bdisc_arr = [('loose', 0.0521), ('med', 0.3033), ('tight', 0.7489)]
elif year == 2018 :
  bdisc_arr = [('loose', 0.0494), ('med', 0.2770), ('tight', 0.7264)]
else :
  exit("Invalid year!")

for bdisc_wp, bdisc_min in bdisc_arr :
  line = ROOT.TLine(bdisc_min, 1e-9, bdisc_min, 0.1)
  line.SetLineStyle(2)
  line.SetLineWidth(2)
  line.Draw()
  t = ROOT.TLatex()
  t.SetTextSize(0.03)
  t.DrawLatex(bdisc_min, 0.09, bdisc_wp)
  ls.append((line,t))
ps.save('jet_bdisc')

#plot fraction of events with btag
x = []
y = []
for i,btag in enumerate([0,1,2]):
  h = f.Get('mfvEventHistosJetPreSel/h_nbtags_%s' % btag)
  x.append(2*i+1)
  y.append(h.Integral(2,11)/h.Integral(1,11))
  x.append(2*i+2)
  y.append(h.Integral(3,11)/h.Integral(1,11))

g = ROOT.TGraph(len(x), array('d',x), array('d',y))
g.SetTitle('preselected events;;fraction with btag')
for i,name in enumerate(btag_names):
  g.GetXaxis().SetBinLabel(g.GetXaxis().FindBin(x[i]), name.replace('medium','med'))
g.GetXaxis().SetLabelSize(0.04)
g.GetYaxis().SetRangeUser(0,1)
g.SetMarkerStyle(21)
g.Draw('AP')
h = f.Get('mfvEventHistosJetPreSel/h_gen_flavor_code')
bquark_fraction = h.GetBinContent(3)/h.Integral()
line = ROOT.TLine(x[0]-0.5, bquark_fraction, x[-1]+0.5, bquark_fraction)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw()
t = ROOT.TLatex()
t.SetTextSize(0.03)
t.DrawLatex(0.5*(x[0]+x[-1]), bquark_fraction, 'fraction with b quarks')
ps.save('btag_fraction')

#plot fake rate vs. btag efficiency
x = []
y = []
for i,btag in enumerate([0,1,2]):
  h1 = f.Get('mfvEventHistosJetPreSel/h_nbtags_v_bquark_code_%s' % btag).ProjectionY('h_nbtags_%s_bquarks' % btag, 3, 3)
  h2 = f.Get('mfvEventHistosJetPreSel/h_nbtags_v_bquark_code_%s' % btag).ProjectionY('h_nbtags_%s_nobquarks' % btag, 1, 2)
  x.append(h1.Integral(2,4)/h1.Integral(1,4))
  y.append(h2.Integral(2,4)/h2.Integral(1,4))
  x.append(h1.Integral(3,4)/h1.Integral(1,4))
  y.append(h2.Integral(3,4)/h2.Integral(1,4))

g = ROOT.TGraph(len(x), array('d',x), array('d',y))
g.SetTitle('preselected events;btag efficiency;fake rate')
g.GetXaxis().SetRangeUser(0,1)
g.GetYaxis().SetRangeUser(0,1)
g.SetMarkerStyle(21)
g.Draw('AP')
for i,name in enumerate(btag_names):
  t = ROOT.TLatex()
  t.SetTextSize(0.03)
  t.DrawLatex(x[i], y[i], name)
ps.save('fakerate_vs_efficiency')

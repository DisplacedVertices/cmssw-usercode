from ROOT import *
TH1.AddDirectory(0)

f = TFile('bkgestsyst_default.root')
h_mix = f.Get('h_1v_dbv')

c = TCanvas('c1','c1',700,700)
h_mix.GetXaxis().SetRangeUser(0,0.1)
h_mix.GetYaxis().SetTitle('arb. units')
h_mix.SetStats(0)
h_mix.SetLineColor(kBlack)
h_mix.SetLineWidth(3)
h_mix.DrawNormalized()

l = TLegend(0.3,0.6,0.9,0.9)
l.AddEntry(h_mix, 'mix: mean d_{BV} = %4.1f +/- %2.1f #mum'%(10000*h_mix.GetMean(),10000*h_mix.GetRMS()/sqrt(h_mix.GetEntries())))

samples = ['qcdht0500_0b','qcdht1000_0b','qcdht0500_2b','qcdht1000_2b','ttbarhadronic','ttbarsemilep','ttbardilep']
names = ['QCD, 500 < H_{T} < 1000 GeV, 0 bquarks', 'QCD, H_{T} > 1000 GeV, 0 bquarks', 'QCD, 500 < H_{T} < 1000 GeV, #geq 2 bquarks', 'QCD, H_{T} > 1000 GeV, #geq 2 bquarks', 't#bar{t}, hadronic', 't#bar{t}, semileptonic', 't#bar{t}, dileptonic']
colors = [kBlue, kBlue+1, kPink, kPink+1, kPink+2, kPink+3, kPink+4]
for i, sample in enumerate(samples):
  f = TFile('bkgestsyst_%s.root' % sample)
  h = f.Get('h_1v_dbv')
  h.SetStats(0)
  h.SetLineColor(colors[i])
  h.SetLineWidth(3)
  h.DrawNormalized('sames')
  l.AddEntry(h, '%s: mean d_{BV} = %4.1f +/- %2.1f #mum' % (names[i], 10000*h.GetMean(), 10000*h.GetRMS()/sqrt(h.GetEntries())))

l.SetFillColor(0)
l.Draw()

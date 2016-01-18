from ROOT import *
TH1.AddDirectory(0)

f = TFile('../2v_from_jets_all.root')
h_mix = f.Get('h_c1v_dvv')

#f2 = TFile('../2v_from_jets_b.root')
#h_sum = f2.Get('h_c1v_dvv')

h_sum = TH1F('h_sum', ';d_{VV}^{C};events', 6, 0, 0.12)
samples = ['nob','b']
n2v = [0.560, 0.827]
for i, sample in enumerate(samples):
  f = TFile('../2v_from_jets_%s.root' % sample)
  h = f.Get('h_c1v_dvv')
  h_sum.Add(h, 1./h.Integral() * n2v[i]/1.387)

c1 = TCanvas('c1','c1',700,700)
c1.SetTickx()
c1.SetTicky()
h_mix.SetStats(0)
h_mix.SetLineColor(kBlack)
h_mix.SetLineWidth(3)
h_mix.Scale(251./h_mix.Integral())
h_mix.Draw()
h_sum.SetStats(0)
h_sum.SetLineColor(kBlue)
h_sum.SetLineWidth(3)
h_sum.Scale(251./h_sum.Integral())
h_sum.Draw('sames')

l1 = TLegend(0.5,0.8,0.7,0.9)
l1.AddEntry(h_mix, 'default')
l1.AddEntry(h_sum, 'b quarks')
l1.SetFillColor(0)
l1.Draw()

c2 = TCanvas('c2','c2',700,350)
c2.SetTickx()
c2.SetTicky()
h_diff = TH1F('h_diff', ';d_{VV}^{C} (cm);difference', 6, 0, 0.12)
h_ratio = TH1F('h_ratio', ';d_{VV}^{C} (cm);ratio', 6, 0, 0.12)
for i in range(1,h_ratio.GetNbinsX()+1):
  a = h_sum.GetBinContent(i)
  ea = h_sum.GetBinError(i)
  b = h_mix.GetBinContent(i)
  eb = h_mix.GetBinError(i)
  h_diff.SetBinContent(i, a-b)
  h_diff.SetBinError(i, (ea**2 + eb**2)**0.5)
  h_ratio.SetBinContent(i, a/b)
  h_ratio.SetBinError(i, a/b * ((ea/a)**2 + (eb/b)**2)**0.5)
  print 'bin %i: default = %.2f +/- %.2f, b quarks = %.2f +/- %.2f'%(i,b,eb,a,ea)
  print '\tdifference = %.2f +/- %.2f'%(h_diff.GetBinContent(i), h_diff.GetBinError(i))
  print '\tratio = %.2f +/- %.2f'%(h_ratio.GetBinContent(i), h_ratio.GetBinError(i))
h_ratio.SetStats(0)
h_ratio.SetLineWidth(3)
h_ratio.Draw('e')

l2 = TLegend(0.2,0.8,0.4,0.9)
l2.AddEntry(h_ratio, 'b quarks / default')
l2.SetFillColor(0)
l2.Draw()

line = TLine(0,1,0.12,1)
line.SetLineWidth(2)
line.SetLineStyle(2)
line.Draw()

c3 = TCanvas('c3','c3',700,350)
c3.SetTickx()
c3.SetTicky()
h_diff.SetStats(0)
h_diff.SetLineWidth(3)
h_diff.Draw('e')

l3 = TLegend(0.2,0.8,0.4,0.9)
l3.AddEntry(h_diff, 'b quarks - default')
l3.SetFillColor(0)
l3.Draw()

line2 = TLine(0,0,0.12,0)
line2.SetLineWidth(2)
line2.SetLineStyle(2)
line2.Draw()


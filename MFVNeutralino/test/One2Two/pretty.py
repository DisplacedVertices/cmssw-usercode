import sys
from JMTucker.Tools.ROOTTools import *
ts = tdr_style()

rainbow_palette()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

#ROOT.gStyle.SetPalette(53)
#ROOT.gStyle.SetNumberContours(500)

ts.SetPadTopMargin(0.1)
ts.SetPadBottomMargin(0.1)
ts.SetPadLeftMargin(0.1)
ts.SetPadRightMargin(0.15)


f = ROOT.TFile('newplots.root')

c = ROOT.TCanvas('c', '', 1000, 800)
h = f.Get('h_eff_600')
yax = h.GetYaxis()
yax.SetTitle('neutralino lifetime c#tau')
yax.SetTitleOffset(1.3)
yax.SetRangeUser(300, 32000)
yax.SetBinLabel(yax.FindBin(300), '300 #mum')
yax.SetBinLabel(yax.FindBin(1000), '1 mm')
yax.SetBinLabel(yax.FindBin(5000), '5 mm')
yax.SetBinLabel(yax.FindBin(10000), '1 cm')
yax.SetBinLabel(yax.FindBin(20000), '2 cm')
yax.SetBinLabel(yax.FindBin(30000), '3 cm')
h.GetZaxis().SetTitleOffset(1.2)
h.SetZTitle('efficiency for d_{VV} > 600 #mum')
h.Draw('colz')
cms = write(61, 0.050, 0.10, 0.92, 'CMS')
pre = write(52, 0.040, 0.19, 0.92, 'Preliminary')
sim = write(42, 0.050, 0.68, 0.92, 'Simulation')
c.SaveAs('/uscms/home/tucker/afshome/scan_eff.pdf')
del c

c = ROOT.TCanvas('c', '', 1000, 800)
c.SetLogx()
c.SetLogy()
c.SetLogz()
h = f.Get('hlim_observed')
xax = h.GetXaxis()
xax.SetTitleOffset(1.2)
yax = h.GetYaxis()
#yax.SetMoreLogLabels()
yax.SetTitle('neutralino lifetime c#tau (#mum)')
yax.SetTitleOffset(1.15)
yax.SetLabelSize(0.055)
yax.SetRangeUser(300, 32000)
yax.SetBinLabel(yax.FindBin(300), '300 #mum')
yax.SetBinLabel(yax.FindBin(1000), '1 mm')
yax.SetBinLabel(yax.FindBin(5000), '5 mm')
yax.SetBinLabel(yax.FindBin(10000), '1 cm')
yax.SetBinLabel(yax.FindBin(20000), '2 cm')
yax.SetBinLabel(yax.FindBin(30000), '3 cm')
h.GetZaxis().SetTitleOffset(1.2)
h.SetZTitle('95% CL upper limit on #sigma #times BR (fb)')
h.Draw('colz')
cms = write(61, 0.050, 0.10, 0.92, 'CMS')
pre = write(52, 0.040, 0.19, 0.92, 'Preliminary')
lum = write(42, 0.050, 0.60, 0.92, '17.6 fb^{-1} (8 TeV)')
c.SaveAs('/uscms/home/tucker/afshome/scan_lim_obs.pdf')
del c

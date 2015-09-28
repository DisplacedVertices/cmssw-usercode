import sys
from array import array
from JMTucker.Tools.ROOTTools import *
from limitplot import exc_graph_dumb

ts = tdr_style()
rainbow_palette()
#ROOT.gStyle.SetPalette(1)

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
f2 = ROOT.TFile('newplots_fromr.root')

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

if 1:
    n = 6
    r = array('d', [1, 0, 0, 0, 1, 1])
    g = array('d', [0.3, 0, 1, 1, 1, 0])
    b = array('d', [1, 1, 1, 0, 0, 0])
    stops = array('d', [float(i)/(n-1) for i in xrange(n)])
    stops[-1] = 1
    num_colors = 500
    ROOT.TColor.CreateGradientColorTable(5, stops, r, g, b, num_colors)
    ROOT.gStyle.SetNumberContours(num_colors)

#    n = 3
#    r = array('d', [0,  1, 1])
#    g = array('d', [0,  0., 0])
#    b = array('d', [1,  0.5, 0.5])
#    stops = array('d', [float(i)/(n-1) for i in xrange(n)])
#    num_colors = 500
#    ROOT.TColor.CreateGradientColorTable(n, stops, r, g, b, num_colors)
#    ROOT.gStyle.SetNumberContours(num_colors)

c = ROOT.TCanvas('c', '', 1000, 800)
c.SetLogz()
h = f.Get('hlim_observed')
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
h.SetZTitle('95% CL upper limit on #sigma #times BR (fb)')
h.Draw('colz')
#g_obs = exc_graph_dumb(f.Get('hlim_observed_exc'), 3, ROOT.kWhite, 1, 300)
#g_exp = exc_graph_dumb(f.Get('hlim_expect50_exc'), 3, ROOT.kWhite, 7, 300)
#for g in g_obs + g_exp:
#    g.Draw('L')
g_obs = f2.Get('hlim_observed_fromrinterp_exc_g')
g_exp = f2.Get('hlim_expect50_fromrinterp_exc_g')
g_exp.SetLineStyle(7)
g_obs.Draw('L')
g_exp.Draw('L')
cms = write(61, 0.050, 0.10, 0.92, 'CMS')
pre = write(52, 0.040, 0.19, 0.92, 'Preliminary')
lum = write(42, 0.050, 0.60, 0.92, '17.6 fb^{-1} (8 TeV)')
c.SaveAs('/uscms/home/tucker/afshome/scan_lim_obs.pdf')
c.SaveAs('/uscms/home/tucker/afshome/scan_lim_obs.root')
del c

'''
c = ROOT.TCanvas('c', '', 1000, 800)
c.SetLogx()
c.SetLogy()
c.SetLogz()
h = f.Get('hlim_observed')
for ix in xrange(0, h.GetNbinsX()+2):
    for iy in xrange(0, h.GetNbinsY()+2):
        h.SetBinContent(ix, iy, 0)
        h.SetBinError  (ix, iy, 0)
h.Draw()
xax = h.GetXaxis()
xax.SetTitleOffset(1.2)
yax = h.GetYaxis()
xax.SetTitle('gluino mass (GeV)')
yax.SetTitle('gluino lifetime c#tau (#mum)')
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
h.Draw('col')
g_obs = exc_graph_dumb(f.Get('hlim_observed_exc'), 3, 1, 1)
for g in g_obs:
    g.Draw('L')
cms = write(61, 0.050, 0.10, 0.92, 'CMS')
pre = write(52, 0.040, 0.19, 0.92, 'Preliminary')
lum = write(42, 0.050, 0.60, 0.92, '17.6 fb^{-1} (8 TeV)')
c.SaveAs('/uscms/home/tucker/afshome/scan_lim_exc.pdf')
del c
'''


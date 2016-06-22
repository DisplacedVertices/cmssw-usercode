import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
from limitplot import exc_graph_dumb

preliminary = True
if preliminary:
    path = 'plots/prelim'
else:
    path = 'plots/not_prelim'

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
xax = h.GetXaxis()
xax.SetTitle('neutralino/gluino mass (GeV)')
xax.CenterLabels()
xax.SetTitle('neutralino/gluino mass (GeV)')
xax.SetNdivisions(1300, 0)
xax.SetLabelSize(0.055)
xax.SetBinLabel(xax.FindBin(400), '400')
xax.SetBinLabel(xax.FindBin(600), '600')
xax.SetBinLabel(xax.FindBin(800), '800')
xax.SetBinLabel(xax.FindBin(1000), '1000')
xax.SetBinLabel(xax.FindBin(1200), '1200')
xax.SetBinLabel(xax.FindBin(1400), '1400')
yax = h.GetYaxis()
yax.SetTitle('neutralino/gluino c#tau (mm)')
yax.SetTitleOffset(1)
yax.SetLabelSize(0.055)
yax.SetRangeUser(300, 32000)
yax.SetBinLabel(yax.FindBin(300), '0.3')
yax.SetBinLabel(yax.FindBin(1000), '1')
yax.SetBinLabel(yax.FindBin(5000), '5')
yax.SetBinLabel(yax.FindBin(10000), '10')
yax.SetBinLabel(yax.FindBin(20000), '20')
yax.SetBinLabel(yax.FindBin(30000), '30')
h.GetZaxis().SetTitleOffset(1.2)
h.SetZTitle('efficiency for d_{VV} > 600 #mum')
h.Draw('colz')
cms = write(61, 0.050, 0.10, 0.92, 'CMS')
if preliminary:
    sim = write(52, 0.040, 0.19, 0.92, 'Simulation Preliminary')
else:
    sim = write(52, 0.040, 0.19, 0.92, 'Simulation')
lum = write(42, 0.050, 0.735, 0.92, '(8 TeV)')
c.SaveAs(os.path.join(path, 'scan_eff.pdf'))
c.SaveAs(os.path.join(path, 'scan_eff.png'))
c.SaveAs(os.path.join(path, 'scan_eff.root'))
del c

for xxx in ('small', 'big'):
    if 1:
        n = 2
        r = array('d', [1.0, 0.])
        g = array('d', [0.6, 0.])
        b = array('d', [0.6, 1.])
        stops = array('d', [float(i)/(n-1) for i in xrange(n)])
        stops[-1] = 1
        num_colors = 26 if xxx == 'big' else 29
        ROOT.TColor.CreateGradientColorTable(n, stops, r, g, b, num_colors)
        ROOT.gStyle.SetNumberContours(num_colors)

    c = ROOT.TCanvas('c', '', 1000, 800)
    #c.SetLogz()
    h = f.Get('hlim_observed')
    xax = h.GetXaxis()
    xax.CenterLabels()
    xax.SetTitle('neutralino/gluino mass (GeV)')
    xax.SetNdivisions(1300, 0)
    xax.SetLabelSize(0.055)
    xax.SetBinLabel(xax.FindBin(400), '400')
    xax.SetBinLabel(xax.FindBin(600), '600')
    xax.SetBinLabel(xax.FindBin(800), '800')
    xax.SetBinLabel(xax.FindBin(1000), '1000')
    xax.SetBinLabel(xax.FindBin(1200), '1200')
    xax.SetBinLabel(xax.FindBin(1400), '1400')
    yax = h.GetYaxis()
    yax.SetTitle('neutralino/gluino c#tau (mm)')
    yax.SetTitleOffset(1.25)
    yax.SetLabelSize(0.055)
    if xxx == 'small':
        yax.SetRangeUser(300, 999)
    else:
        yax.SetRangeUser(1000, 32000)
    if xxx == 'small':
        for tau in range(400, 801, 200):
            yax.SetBinLabel(yax.FindBin(tau), '%.1f' % (tau/1000.))
    else:
        yax.SetBinLabel(yax.FindBin(1000), '1')
        yax.SetBinLabel(yax.FindBin(5000), '5')
        yax.SetBinLabel(yax.FindBin(10000), '10')
        yax.SetBinLabel(yax.FindBin(20000), '20')
        yax.SetBinLabel(yax.FindBin(30000), '30')
    zax = h.GetZaxis()
    zax.SetTitleOffset(1.2)
    #zax.SetBinLabel(zax.FindBin(30), '30')
    h.SetZTitle('95% CL upper limit on #sigma B^{2} (fb)')
    h.Draw('colz')
    if xxx == 'big':
        h.SetMinimum(0.4)
        h.SetMaximum(3)
    else:
        h.SetMinimum(1.5)
        h.SetMaximum(30.5)
    
    #g_obs = exc_graph_dumb(f.Get('hlim_observed_exc'), 3, ROOT.kWhite, 1, 300)
    #g_exp = exc_graph_dumb(f.Get('hlim_expect50_exc'), 3, ROOT.kWhite, 7, 300)
    #for g in g_obs + g_exp:
    #    g.Draw('L')
    g_obs = f2.Get('hlim_observed_fromrinterp_nm_exc_g')
    g_exp = f2.Get('hlim_expect50_fromrinterp_nm_exc_g')
    g_thup = f2.Get('hlim_observed_fromrinterp_up_exc_g')
    g_thdn = f2.Get('hlim_observed_fromrinterp_dn_exc_g')
    g_exp.SetLineStyle(7)
    g_obs.SetLineWidth(3)
    for g in (g_thup, g_thdn):
        #g.SetLineColor(ROOT.kBlue)
        g.SetLineWidth(2)
    g_obs.Draw('L')
    g_exp.Draw('L')
    g_thup.Draw('L')
    g_thdn.Draw('L')
    leg = ROOT.TLegend(0.279, 0.330, 0.563, 0.478)
    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.SetHeader('#tilde{g} #rightarrow tbs:')
    leg.AddEntry(g_obs, 'Observed #pm 1 #sigma_{th} ', 'L')
    leg.AddEntry(g_exp, 'Expected', 'L')
    leg.Draw()
    if xxx == 'big':
        l1 = ROOT.TLine(627.13, 13046.8, 713.15, 13046.8)
        l2 = ROOT.TLine(627.13, 12484.6, 713.15, 12484.6)
    else:
        l1 = ROOT.TLine(627.13, 572.9, 713.15, 572.9)
        l2 = ROOT.TLine(627.13, 559.5, 713.15, 559.5)
    l1.Draw()
    l2.Draw()
    cms = write(61, 0.050, 0.10, 0.92, 'CMS')
    if preliminary:
        pre = write(52, 0.040, 0.19, 0.92, 'Preliminary')
    lum = write(42, 0.050, 0.60, 0.92, '17.6 fb^{-1} (8 TeV)')
    fn = os.path.join(path, 'scan_lim_obs_%s' % xxx)
    c.SaveAs(fn + '.pdf')
    c.SaveAs(fn + '.png')
    c.SaveAs(fn + '.root')
    del c

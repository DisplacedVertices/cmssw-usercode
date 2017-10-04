import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
from limitplot import exc_graph_dumb

path = 'plots/after_proofs'

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

f = ROOT.TFile('newplots.root')
f2 = ROOT.TFile('newplots_fromr.root')

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

    c = ROOT.TCanvas('c', '', 800, 800)
    c.SetTopMargin(0.1)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.11)
    c.SetRightMargin(0.16)
    #c.SetLogz()
    h = f.Get('hlim_observed')
    xax = h.GetXaxis()
    xax.CenterLabels()
    xax.SetTitle('M_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
    xax.SetNdivisions(1300, 0)
    xax.SetBinLabel(xax.FindBin(400), '400')
    xax.SetBinLabel(xax.FindBin(600), '600')
    xax.SetBinLabel(xax.FindBin(800), '800')
    xax.SetBinLabel(xax.FindBin(1000), '1000')
    xax.SetBinLabel(xax.FindBin(1200), '1200')
    xax.SetBinLabel(xax.FindBin(1400), '1400')
    xax.SetLabelSize(0.065)
    xax.SetTitleSize(0.05)
    xax.SetTitleOffset(1.05)
    xax.LabelsOption('h')
    yax = h.GetYaxis()
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
    yax.SetTitle('c#tau (mm)')
    yax.SetTitleOffset(1.05)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.065)
    zax = h.GetZaxis()
    zax.SetTitleOffset(1.2)
    #zax.SetBinLabel(zax.FindBin(30), '30')
    zax.SetTitle('95% CL upper limit on #sigma B^{2} (fb)')
    zax.SetTitleSize(0.05)
    zax.SetTitleOffset(1.06)
    zax.SetLabelSize(0.045)
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
    x1, x2 = 620, 708
    if xxx == 'big':
        y1, y2 = 11970, 12610.9
    else:
        y1, y2 = 547.1, 562.2
    l1 = ROOT.TLine(x1, y1, x2, y1)
    l2 = ROOT.TLine(x1, y2, x2, y2)
    l1.Draw()
    l2.Draw()
    cms = write(61, 0.050, 0.109, 0.913, 'CMS')
    lum = write(42, 0.050, 0.528, 0.913, '17.6 fb^{-1} (8 TeV)')
    fn = os.path.join(path, 'scan_lim_obs_%s' % xxx)
    c.SaveAs(fn + '.pdf')
    c.SaveAs(fn + '.png')
    c.SaveAs(fn + '.root')
    del c

import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
from limitplot import exc_graph_dumb

path = plot_dir('pretty_limits', make=True)

ts = tdr_style()
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetNumberContours(20) #500 for smooth gradation

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

f = ROOT.TFile('limits.root')
f2 = ROOT.TFile('limits_fromr.root')

for kind in 'mfv_ddbar', 'mfv_neu':
    for xxx in ('small', 'big'):
        if 0:
            n = 2
            r = array('d', [1.0, 0.])
            g = array('d', [0.6, 0.])
            b = array('d', [0.6, 1.])
            stops = array('d', [float(i)/(n-1) for i in xrange(n)])
            stops[-1] = 1
            num_colors = 26 if xxx == 'big' else 29
            ROOT.TColor.CreateGradientColorTable(n, stops, r, g, b, num_colors)
            ROOT.gStyle.SetNumberContours(num_colors)

        c = ROOT.TCanvas('c', '', 900, 800)
        c.SetTopMargin(0.1)
        c.SetBottomMargin(0.12)
        c.SetLeftMargin(0.11)
        c.SetRightMargin(0.18)
        c.SetLogz()
        h = f.Get('%s/observed' % kind)
        xax = h.GetXaxis()
        if kind == 'mfv_neu':
            xax.SetTitle('M_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
        else:
            xax.SetTitle('M_{X} (GeV)')
#        xax.CenterLabels()
#        xax.SetNdivisions(1300, 0)
#        xax.SetBinLabel(xax.FindBin(400), '400')
#        xax.SetBinLabel(xax.FindBin(600), '600')
#        xax.SetBinLabel(xax.FindBin(800), '800')
#        xax.SetBinLabel(xax.FindBin(1000), '1000')
#        xax.SetBinLabel(xax.FindBin(1200), '1200')
#        xax.SetBinLabel(xax.FindBin(1400), '1400')
        xax.SetLabelSize(0.045)
        xax.SetTitleSize(0.05)
        xax.SetTitleOffset(1.05)
#        xax.LabelsOption('h')
        yax = h.GetYaxis()
        if xxx == 'small':
            yax.SetRangeUser(0.1, 1)
        else:
            yax.SetRangeUser(1, 40)
#        if xxx == 'small':
#            for tau in range(400, 801, 200):
#                yax.SetBinLabel(yax.FindBin(tau), '%.1f' % (tau/1000.))
#        else:
#            yax.SetBinLabel(yax.FindBin(1000), '1')
#            yax.SetBinLabel(yax.FindBin(5000), '5')
#            yax.SetBinLabel(yax.FindBin(10000), '10')
#            yax.SetBinLabel(yax.FindBin(20000), '20')
#            yax.SetBinLabel(yax.FindBin(30000), '30')
        yax.SetTitle('c#tau (mm)')
        yax.SetTitleOffset(1.1)
        yax.SetTitleSize(0.05)
        yax.SetLabelSize(0.045)
        zax = h.GetZaxis()
#        zax.SetTitleOffset(1.2)
        #zax.SetBinLabel(zax.FindBin(30), '30')
#     zax.SetRangeUser(0., 0.85)
        zax.SetTitle('95% CL upper limit on #sigma B^{2} (fb)')
        zax.SetLabelSize(0.045)
        zax.SetLabelOffset(0.00005)
        zax.SetTitleSize(0.05)
        zax.SetTitleOffset(1.22)
        h.Draw('colz')
        print kind, xxx, h.GetMinimum(), h.GetMaximum()
        if xxx == 'big':
            h.SetMinimum(0.15)
            h.SetMaximum(37)
        else:
            h.SetMinimum(0.3)
            h.SetMaximum(240)
        if xxx == 'big':
            tt = ROOT.TText(213.5,0.039,'1')
            tt.SetNDC(0)
            tt.SetTextColor(ROOT.kBlack)
            tt.SetTextFont(43)
            tt.SetTextSize(38)
            tt.Draw()

        if kind == 'mfv_neu':
            g_obs = f2.Get('%s_observed_fromrinterp_nm_exc_g' % kind)
            g_exp = f2.Get('%s_expect50_fromrinterp_nm_exc_g' % kind)
            g_thup = f2.Get('%s_observed_fromrinterp_up_exc_g' % kind)
            g_thdn = f2.Get('%s_observed_fromrinterp_dn_exc_g' % kind)
            g_exp.SetLineStyle(7)
            g_obs.SetLineWidth(3)
            for g in (g_thup, g_thdn):
                #g.SetLineColor(ROOT.kBlue)
                g.SetLineWidth(2)
            g_obs.Draw('L')
            g_exp.Draw('L')
            g_thup.Draw('L')
            g_thdn.Draw('L')
#            leg = ROOT.TLegend(0.279, 0.330, 0.563, 0.478)
            leg = ROOT.TLegend(0.259, 0.437, 0.534, 0.584)
            leg.SetTextFont(42)
            leg.SetFillColor(ROOT.kWhite)
            leg.SetBorderSize(0)
            leg.SetHeader('#tilde{g} #rightarrow tbs:')
            leg.AddEntry(g_obs, 'Observed #pm 1 #sigma_{th} ', 'L')
            leg.AddEntry(g_exp, 'Expected', 'L')
            leg.Draw()
            # these lines make the bands for the observed line in the legend, sigh
            x1, x2 = 950, 1145
            if xxx == 'big':
                y1, y2 = 20.1, 20.969
            else:
                y1, y2 = .54, .56
            l1 = ROOT.TLine(x1, y1, x2, y1)
            l2 = ROOT.TLine(x1, y2, x2, y2)
            l1.Draw()
            l2.Draw()
        cms = write(61, 0.050, 0.109, 0.913, 'CMS')
        lum = write(42, 0.050, 0.528, 0.913, '38.5 fb^{-1} (13 TeV)')
        fn = os.path.join(path, '%s_limit_%s' % (kind, xxx))
        c.SaveAs(fn + '.pdf')
        c.SaveAs(fn + '.png')
        c.SaveAs(fn + '.root')
        del c

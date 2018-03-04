import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *

path = plot_dir('pretty_limits_abomination', make=True)

ts = tdr_style()
ROOT.gStyle.SetPalette(ROOT.kBird)
ROOT.gStyle.SetNumberContours(20) #500 for smooth gradation
#ROOT.TColor.InvertPalette()

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
    for xxx in 'big', 'small':
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
        c.SetTopMargin(0.123)
        c.SetBottomMargin(0.12)
        c.SetLeftMargin(0.11)
        c.SetRightMargin(0.18)
        c.SetLogz()
        h = f.Get('%s/observed' % kind)
        xax = h.GetXaxis()
        if kind == 'mfv_neu':
            xax.SetTitle('M_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
        else:
            xax.SetTitle('M_{#tilde{t}} (GeV)')
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
        xax.SetRangeUser(300, 2800)
#        xax.LabelsOption('h')
        yax = h.GetYaxis()
        if xxx == 'small':
            yax.SetRangeUser(0.1, 1)
        else:
            yax.SetRangeUser(1, 100)
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
            h.SetMinimum(0.15)
            h.SetMaximum(240)
        if xxx == 'big':
            tt = ROOT.TText(213.5,-1.,'1')
            tt.SetNDC(0)
            tt.SetTextColor(ROOT.kBlack)
            tt.SetTextFont(43)
            tt.SetTextSize(38)
            tt.Draw()

        g_obs = f2.Get('%s_observed_fromrinterp_nm_exc_g' % kind)
        g_exp = f2.Get('%s_expect50_fromrinterp_nm_exc_g' % kind)
#        g_thup = f2.Get('%s_observed_fromrinterp_up_exc_g' % kind)
 #       g_thdn = f2.Get('%s_observed_fromrinterp_dn_exc_g' % kind)
        g_exp.SetLineStyle(7)
        g_obs.SetLineWidth(3)
    #    for g in (g_thup, g_thdn):
            #g.SetLineColor(ROOT.kBlue)
     #       g.SetLineWidth(2)
        g_obs.Draw('L')
#        g_exp.SetMarkerStyle(20)
 #       g_exp.SetMarkerSize(2)

        if kind == 'mfv_neu':
            for i in xrange(20):
                print 'ugh'
            g_exp.SetPoint(85,2273.164179,77.03205233);
            g_exp.SetPoint(86,2269.243102,77.98952421);
            g_exp.SetPoint(87,2265.322025,79.00331796);
            g_exp.SetPoint(88,2261.400949,80.01711171);
            g_exp.SetPoint(99,2233.953412,90.99987733);
            g_exp.SetPoint(102,2233.953412,94.02491511);
            g_exp.SetPoint(103,2230.032336,95.02334834);
            g_exp.SetPoint(104,2230.032336,95.94497903);
            g_exp.SetPoint(105,2226.111259,96.99275073);

        g_exp.Draw('L')
  #      g_thup.Draw('L')
   #     g_thdn.Draw('L')

        c.Update()
        palette = h.GetListOfFunctions().FindObject("palette")
        palette.SetY2NDC(0.932)

        leg = ROOT.TLegend(0.110, 0.877, 0.820, 0.932)
        leg.SetTextFont(42)
        leg.SetTextSize(0.0362)
        leg.SetTextAlign(22)
        leg.SetNColumns(3)
        leg.SetFillColor(ROOT.kWhite)
        leg.SetBorderSize(1)
        if kind == 'mfv_neu':
            model = '#kern[-0.22]{#tilde{g} #rightarrow tbs}'
        else:
            model = '#kern[-0.22]{#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}}'
        leg.AddEntry(0, model, '')
        leg.AddEntry(g_obs, '#kern[-0.22]{Observed}', 'L')
        leg.AddEntry(g_exp, '#kern[-0.22]{Expected}', 'L')
        leg.Draw()
#        # these lines make the bands for the observed line in the legend, sigh
#        x1, x2 = 950, 1145
#        if xxx == 'big':
#            y1, y2 = 20.1, 20.969
#        else:
#            y1, y2 = .54, .56
#        l1 = ROOT.TLine(x1, y1, x2, y1)
#        l2 = ROOT.TLine(x1, y2, x2, y2)
#        l1.Draw()
#        l2.Draw()

        cms = write(61, 0.050, 0.109, 0.950, 'CMS')
        lum = write(42, 0.050, 0.515, 0.950, '38.5 fb^{-1} (13 TeV)')
        fn = os.path.join(path, '%s_limit_%s' % (kind, xxx))
        c.SaveAs(fn + '.pdf')
        c.SaveAs(fn + '.png')
        c.SaveAs(fn + '.root')
        del c

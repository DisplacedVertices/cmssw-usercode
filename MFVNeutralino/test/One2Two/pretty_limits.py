import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *

draw_pm1sigma_excl = True

which = '2017p8' if '2017p8' in sys.argv else 'run2'
intlumi = 140 if which == 'run2' else 101
path = plot_dir('pretty_limits_%s_maybefinal_logy_fixed_pm1sigma' % which, make=True)

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

f = ROOT.TFile('limits_%s.root' % which)
f2 = ROOT.TFile('limits_fromr_%s.root' % which)
f3 = ROOT.TFile('limits_fromr_neu_%s.root' % which)

for kind in 'mfv_stopdbardbar', 'mfv_neu':
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

        c = ROOT.TCanvas('c', '', 954, 899)
        c.SetTopMargin(0.123)
        c.SetBottomMargin(0.15)
        c.SetLeftMargin(0.13)
        c.SetRightMargin(0.20)
        c.SetLogz()
        c.SetLogy()
        h = f.Get('%s/observed' % kind)
        xax = h.GetXaxis()
        if kind == 'mfv_neu':
            xax.SetTitle('m_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
        else:
            xax.SetTitle('m_{#tilde{t}} (GeV)')
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
        xax.SetTitleOffset(0.98)
        xax.SetRangeUser(300, 3000)
#        xax.LabelsOption('h')
        yax = h.GetYaxis()
        if xxx == 'small':
            yax.SetRangeUser(0.1, 1)
        else:
            yax.SetRangeUser(0.1, 100)
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
        zax.SetTitle('95% CL upper limit on #sigma#bf{#it{#Beta}}^{2} (fb)')
        zax.SetLabelSize(0.045)
        zax.SetLabelOffset(0.00005)
        zax.SetTitleSize(0.05)
        zax.SetTitleOffset(1.20)
        h.Draw('colz')
        print kind, xxx, h.GetMinimum(), h.GetMaximum()
        if xxx == 'big':
            h.SetMinimum(0.01)
            h.SetMaximum(100)
        else:
            h.SetMinimum(0.01)
            h.SetMaximum(240)
        if False and  xxx == 'big':
            tt = ROOT.TText(213.5,-1.,'1')
            tt.SetNDC(0)
            tt.SetTextColor(ROOT.kBlack)
            tt.SetTextFont(43)
            tt.SetTextSize(38)
            tt.Draw()

        if   kind == 'mfv_stopdbardbar' :
            theories = ['stopstop']
        elif kind == 'mfv_neu' :
            theories = ['gluglu', 'higgsino_N2N1']

        for theory in theories :

            if theory == 'gluglu' :
                theory_color = ROOT.kMagenta-4
            elif theory == 'higgsino_N2N1' :
                theory_color = ROOT.kRed
            else :
                theory_color = ROOT.kRed

            if theory == 'higgsino_N2N1':
                g_obs   = f3.Get('%s_observed_fromrinterp_%s_nm_exc_g' % (kind, theory))
                g_obsup = f3.Get('%s_observed_fromrinterp_%s_up_exc_g' % (kind, theory))
                g_obsdn = f3.Get('%s_observed_fromrinterp_%s_dn_exc_g' % (kind, theory))
                g_exp   = f3.Get('%s_expect50_fromrinterp_%s_nm_exc_g' % (kind, theory))
                g_expup = f3.Get('%s_expect84_fromrinterp_%s_nm_exc_g' % (kind, theory))
                g_expdn = f3.Get('%s_expect16_fromrinterp_%s_nm_exc_g' % (kind, theory))
            else:
                g_obs   = f2.Get('%s_observed_fromrinterp_%s_nm_exc_g' % (kind, theory))
                g_obsup = f2.Get('%s_observed_fromrinterp_%s_up_exc_g' % (kind, theory))
                g_obsdn = f2.Get('%s_observed_fromrinterp_%s_dn_exc_g' % (kind, theory))
                g_exp   = f2.Get('%s_expect50_fromrinterp_%s_nm_exc_g' % (kind, theory))
                g_expup = f2.Get('%s_expect84_fromrinterp_%s_nm_exc_g' % (kind, theory))
                g_expdn = f2.Get('%s_expect16_fromrinterp_%s_nm_exc_g' % (kind, theory))

            if draw_pm1sigma_excl:
                for g in g_obs, g_exp:
                    g.SetLineWidth(2)
            else:
                g_obs.SetLineWidth(3)
            for g in g_obs, g_obsup, g_obsdn:
                g.SetLineColor(ROOT.kBlack)#theory_color)
            for g in g_exp, g_expup, g_expdn:
                g.SetLineStyle(7 if draw_pm1sigma_excl else 7)
                g.SetLineColor(theory_color)#ROOT.kRed if draw_pm1sigma_excl else theory_color)
            for g in (g_obsup, g_obsdn, g_expup, g_expdn):
                g.SetLineWidth(1)

            if False and kind == 'mfv_stopdbardbar':
                for i in xrange(20):
                    print 'ugh'
                assert h.FindBin(1600,82) == 633
                assert h.FindBin(1800,82) == 634
                assert h.FindBin(2000,82) == 635
                h.SetBinContent(634, (h.GetBinContent(633) + h.GetBinContent(635))/2)

                assert h.FindBin(2000,0.2) == 43
                assert h.FindBin(2200,0.2) == 44
                assert h.FindBin(2400,0.2) == 45
                h.SetBinContent(44, (h.GetBinContent(43) + h.GetBinContent(45))/2)
                
            if False and kind == 'mfv_neu':
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

            if kind == 'mfv_neu':
                disp_jet_excl = array('d', [2229, 2498, 2616, 2645, 2641])
            else:
                disp_jet_excl = array('d', [1479, 1711, 1805, 1823, 1802])
            ys = array('d', [1., 3., 10., 30., 100.])
            g_dispjet_excl = ROOT.TGraph(len(ys), disp_jet_excl, ys)
            g_dispjet_excl.SetLineColor(ROOT.kGreen-4)
            g_dispjet_excl.SetLineWidth(2)
            g_dispjet_excl.SetLineStyle(8)

            excl_to_draw = [g_dispjet_excl, g_obs, g_obsup, g_obsdn, g_exp, g_expup, g_expdn] if draw_pm1sigma_excl else [g_exp, g_obs]
            for g in excl_to_draw:
                print g
                g.Draw('L')

        c.Update()
        palette = h.GetListOfFunctions().FindObject("palette")
        palette.SetY2NDC(0.932)

        leg = ROOT.TLegend(0.13, 0.877, 0.80, 0.931)
        leg.SetTextFont(42)
        leg.SetTextSize(0.0362)
        leg.SetTextAlign(22)
        leg.SetNColumns(3)
        leg.SetFillColor(ROOT.kWhite)
        leg.SetBorderSize(1)
        if kind == 'mfv_neu':
            model = '#kern[-0.%i]{#color[2]{#tilde{#chi}^{0}} / #color[612]{#tilde{g}} #rightarrow tbs}' % (32 if draw_pm1sigma_excl else 22)
        else:
            model = '#kern[-0.%i]{#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}}' % (52 if draw_pm1sigma_excl else 22)
        leg.AddEntry(0, model, '')
        if draw_pm1sigma_excl:
            leg.AddEntry(g_obs, 'Obs. #pm 1 #sigma_{th}', 'L')
            if kind == 'mfv_neu':
                g_exp_clone = g_exp.Clone()
                g_exp_clone.SetLineColor(ROOT.kBlack)
                leg.AddEntry(g_exp_clone, 'Exp. #pm 1 #sigma_{exp}', 'L')
            else:
                leg.AddEntry(g_exp, 'Exp. #pm 1 #sigma_{exp}', 'L')
        else:
            # force the lines in the legend to be black
            g_obs_clone = g_obs.Clone()
            g_exp_clone = g_exp.Clone()
            g_obs_clone.SetLineColor(ROOT.kBlack)
            g_exp_clone.SetLineColor(ROOT.kBlack)

            leg.AddEntry(g_obs_clone, '#kern[-0.22]{Obs.}', 'L')
            leg.AddEntry(g_exp_clone, '#kern[-0.22]{Exp.}', 'L')
        leg.Draw()

        if draw_pm1sigma_excl:
            # these lines make the bands for the lines in the legend, sigh
            if kind == 'mfv_neu':
                x00, x01 = 0.321, 0.360
                x10, x11 = 0.557, 0.596
            else:
                x00, x01 = 0.254, 0.294
                x10, x11 = 0.522, 0.561
            y0, y1 = 0.894, 0.914
            ll = [
                ROOT.TLine(x00, y0, x01, y0),
                ROOT.TLine(x10, y0, x11, y0),
                ROOT.TLine(x00, y1, x01, y1),
                ROOT.TLine(x10, y1, x11, y1),
                ]
            for l in ll[1], ll[3]:
                l.SetLineStyle(7)
                if kind == 'mfv_neu':
                    l.SetLineColor(ROOT.kBlack)
                else:
                    l.SetLineColor(theory_color)
            for l in ll:
                l.SetLineWidth(1)
                l.SetNDC(1)
                l.Draw()

        cms = write(61, 0.050, 0.129, 0.945, 'CMS')
        lum = write(42, 0.050, 0.470, 0.945, '%s fb^{-1} (13 TeV)' % intlumi)
        fn = os.path.join(path, '%s_limit_%s' % (kind, xxx))
        c.SaveAs(fn + '.pdf')
        c.SaveAs(fn + '.png')
        c.SaveAs(fn + '.root')

        pre = write(52, 0.047, 0.229, 0.945, 'Preliminary')
        c.SaveAs(fn + '_prelim.pdf')
        c.SaveAs(fn + '_prelim.png')
        c.SaveAs(fn + '_prelim.root')

        del c

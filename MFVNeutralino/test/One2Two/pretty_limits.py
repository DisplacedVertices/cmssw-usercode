import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *

draw_pm1sigma_excl = True
swap_axes = True

which = '2017p8' if '2017p8' in sys.argv else 'run2'
intlumi = 140 if which == 'run2' else 101
path = plot_dir('pretty_limits_%s_pm1sigma_switchaxes' % which, make=True)

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

def do_swap_axes(obj) :
    if obj.Class().GetName() == 'TH2D' :
        nbinx = obj.GetNbinsX()
        nbiny = obj.GetNbinsY()
        xbins = obj.GetXaxis().GetXbins().GetArray()
        ybins = obj.GetYaxis().GetXbins().GetArray()

        hnew = ROOT.TH2D("swap","swap",nbiny,ybins,nbinx,xbins)
        # FIXME I always forget if it's nbins+1 or +2, so fix it before sending it off
        for ibinx in xrange(1,nbinx+1) :
            for ibiny in xrange(1,nbiny+1) :
                content = obj.GetBinContent(ibinx, ibiny)
                hnew.SetBinContent(ibiny, ibinx, content)

        name = obj.GetName()
        title = obj.GetTitle()
        del obj
        hnew.SetName(name)
        hnew.SetTitle(title)
        return hnew
    elif obj.Class().GetName() == 'TGraph' :
        xvals = obj.GetX()
        yvals = obj.GetY()
        nvals = len(xvals)
        gnew = ROOT.TGraph(nvals, yvals, xvals)
        ROOT.SetOwnership(gnew, False) # so that the graph can't go out of scope from the TCanvas...
        del obj
        return gnew

    else :
        print obj.Class().GetName()
        os.abort()
    return obj

f = ROOT.TFile('limits_%s.root' % which)
f2 = ROOT.TFile('limits_fromr_%s.root' % which)
f3 = ROOT.TFile('limits_fromr_neu_%s.root' % which)

for kind in 'mfv_stopdbardbar', 'mfv_neu':
    c = ROOT.TCanvas('c', '', 950, 900)
    c.SetTopMargin(0.160)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.17)
    c.SetRightMargin(0.17)

    c.SetLogz()
    if swap_axes :
        c.SetLogx()
    else :
        c.SetLogy()

    h = f.Get('%s/observed' % kind)

    xax = h.GetXaxis()
    yax = h.GetYaxis()

    if swap_axes :
        h = do_swap_axes(h)
        xax = h.GetYaxis()
        yax = h.GetXaxis()
    yax.SetTitle('c#tau (mm)')
    if kind == 'mfv_neu':
        xax.SetTitle('m_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
    else:
        xax.SetTitle('m_{#tilde{t}} (GeV)')

    xax.SetLabelSize(0.045)
    xax.SetTitleSize(0.05)
    xax.SetTitleOffset(1.6)
    xax.SetRangeUser(300, 3000)

    yax.SetRangeUser(0.1, 100)
    yax.SetTitleOffset(0.98)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.045)
    zax = h.GetZaxis()

    zax.SetTitle('95% CL upper limit on #sigma#bf{#it{#Beta}}^{2} (fb)')
    zax.SetLabelSize(0.045)
    zax.SetLabelOffset(0.00005)
    zax.SetTitleSize(0.05)
    zax.SetTitleOffset(1.20)
    h.Draw('colz')
    print kind, h.GetMinimum(), h.GetMaximum()
    h.SetMinimum(0.01)
    h.SetMaximum(100)

    if   kind == 'mfv_stopdbardbar' :
        theories = ['stopstop']
    elif kind == 'mfv_neu' :
        theories = ['gluglu', 'higgsino_N2N1']

    for theory in theories :
        if theory == 'gluglu' :
            #theory_color = ROOT.kOrange-3
            theory_color = ROOT.kRed-9
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

        if swap_axes :
            g_obs   = do_swap_axes(g_obs)
            g_obsup = do_swap_axes(g_obsup)
            g_obsdn = do_swap_axes(g_obsdn)
            g_exp   = do_swap_axes(g_exp)
            g_expup = do_swap_axes(g_expup)
            g_expdn = do_swap_axes(g_expdn)

        g_obs.SetName("g_obs_%s" % theory)
        g_obsup.SetName("g_obsup_%s" % theory)
        g_obsdn.SetName("g_obsdn_%s" % theory)
        g_exp.SetName("g_exp_%s" % theory)
        g_expup.SetName("g_expup_%s" % theory)
        g_expdn.SetName("g_expdn_%s" % theory)

        if draw_pm1sigma_excl:
            for g in g_obs, g_exp:
                g.SetLineWidth(3)
        else:
            g_obs.SetLineWidth(3)
        for g in g_obs, g_obsup, g_obsdn:
            g.SetLineColor(ROOT.kBlack)#theory_color)
        for g in g_exp, g_expup, g_expdn:
            g.SetLineStyle(7 if draw_pm1sigma_excl else 7)
            g.SetLineColor(theory_color)#ROOT.kRed if draw_pm1sigma_excl else theory_color)
        for g in (g_obsup, g_obsdn, g_expup, g_expdn):
            g.SetLineWidth(1)

        if kind == 'mfv_neu':
            disp_jet_excl = array('d', [2229, 2498, 2616, 2645, 2641])
        else:
            disp_jet_excl = array('d', [1479, 1711, 1805, 1823, 1802])
        ys = array('d', [1., 3., 10., 30., 100.])
        g_dispjet_excl = ROOT.TGraph(len(ys), disp_jet_excl, ys)
        if swap_axes :
            g_dispjet_excl = do_swap_axes(g_dispjet_excl)
        g_dispjet_excl.SetName("g_dispjet_excl")
        g_dispjet_excl.SetLineColor(ROOT.kTeal+2)
        g_dispjet_excl.SetLineWidth(3)
        g_dispjet_excl.SetLineStyle(4)

        excl_to_draw = [g_dispjet_excl, g_obs, g_obsup, g_obsdn, g_exp, g_expup, g_expdn] if draw_pm1sigma_excl else [g_exp, g_obs]
        for g in excl_to_draw:
            g.Draw('L')

    c.Update()
    palette = h.GetListOfFunctions().FindObject("palette")
    palette.SetY2NDC(0.932)

    leg = ROOT.TLegend(0.17, 0.840, 0.83, 0.931)
    leg.SetTextFont(42)
    leg.SetTextSize(0.03)
    leg.SetTextAlign(22)
    leg.SetNColumns(2)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(1)
    leg.AddEntry(0, '', '')
    if draw_pm1sigma_excl:
        leg.AddEntry(g_obs, '#kern[-0.22]{Observed #pm 1 #sigma_{th}}', 'L')
        if kind == 'mfv_neu':
            g_exp_clone = g_exp.Clone()
            g_exp_clone.SetLineColor(ROOT.kBlack)
            leg.AddEntry(g_dispjet_excl, '#kern[-0.2]{CMS disp. jets (#tilde{g})}', 'L')
            leg.AddEntry(g_exp_clone, '#kern[-0.16]{Expected #pm 1 #sigma_{exp}}', 'L')
        else:
            leg.AddEntry(g_dispjet_excl, '#kern[-0.2]{CMS disp. jets}', 'L')
            leg.AddEntry(g_exp, '#kern[-0.16]{Expected #pm 1 #sigma_{exp}}', 'L')
    else:
        # force the lines in the legend to be black
        g_obs_clone = g_obs.Clone()
        g_exp_clone = g_exp.Clone()
        g_obs_clone.SetLineColor(ROOT.kBlack)
        g_exp_clone.SetLineColor(ROOT.kBlack)

        leg.AddEntry(g_obs_clone, '#kern[-0.22]{Obs.}', 'L')
        leg.AddEntry(g_exp_clone, '#kern[-0.22]{Exp.}', 'L')
    leg.Draw()

    t = ROOT.TLatex()
    t.SetTextFont(42)
    t.SetTextColor(1)
    t.SetTextSize(0.03)
    if kind == 'mfv_neu':
        glu_color = ROOT.kRed-9
        neu_color = ROOT.kRed
        model = '#kern[-0.%i]{#color[%i]{#tilde{#chi}^{0}} / #color[%i]{#tilde{g}} #rightarrow tbs}' % (60 if draw_pm1sigma_excl else 22, neu_color, glu_color)
        t.DrawLatexNDC(0.26, 0.895, model)
        t.SetTextSize(0.075)
        t.DrawLatexNDC(0.238,0.70,'#color[%i]{#tilde{g}}' % glu_color)
        t.DrawLatexNDC(0.238,0.32,'#color[%i]{#tilde{#chi}^{0}}' % neu_color)
    else:
        stop_color = ROOT.kRed
        model = '#kern[-0.%i]{#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}}' % (52 if draw_pm1sigma_excl else 22)
        t.DrawLatexNDC(0.22, 0.895, model)
        t.SetTextSize(0.075)
        t.DrawLatexNDC(0.245,0.47,'#color[%i]{#tilde{t}}' % stop_color)

    if draw_pm1sigma_excl:
        # these lines make the bands for the lines in the legend, sigh
        if kind == 'mfv_neu':
            x00, x01 = 0.508, 0.566
        else:
            x00, x01 = 0.484, 0.542
        shift = 0.046
        y00, y01 = 0.897, 0.92
        y10, y11 = y00 - shift, y01 - shift
        ll = [
            ROOT.TLine(x00, y00, x01, y00),
            ROOT.TLine(x00, y10, x01, y10),
            ROOT.TLine(x00, y01, x01, y01),
            ROOT.TLine(x00, y11, x01, y11),
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

    xshift = 0.04
    cms = write(61, 0.050, 0.129+xshift, 0.945, 'CMS')
    lum = write(42, 0.050, 0.470+xshift, 0.945, '%s fb^{-1} (13 TeV)' % intlumi)
    fn = os.path.join(path, '%s_limit' % kind)
    c.SaveAs(fn + '.pdf')
    c.SaveAs(fn + '.png')
    c.SaveAs(fn + '.root')

    pre = write(52, 0.047, 0.231+xshift, 0.945, 'Preliminary')
    c.SaveAs(fn + '_prelim.pdf')
    c.SaveAs(fn + '_prelim.png')
    c.SaveAs(fn + '_prelim.root')

    del c

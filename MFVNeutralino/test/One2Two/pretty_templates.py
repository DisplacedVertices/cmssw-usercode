from JMTucker.Tools.ROOTTools import *
from limitsinput import name2isample
from signal_efficiency import SignalEfficiencyCombiner
set_style()
ps = plot_saver(plot_dir('pretty_templates_2017p8_diff_xsecs'), size=(700,700), log=True, pdf=True, pdf_log=True)

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)
ps.c.SetLogy()

f = ROOT.TFile('limitsinput.root')
#raise ValueError('propagate change to use stored rate already normalized to int lumi')
combiner = SignalEfficiencyCombiner()

# excluded xsec from previous analysis (2016) is:
# 0.8 at 300 microns, 0.25 at 1mm, 0.15 at 10mm

which = [
    ('mfv_neu_tau000300um_M1600', 'c#tau = 0.3 mm', ROOT.kRed,     2, 0.8), 
    ('mfv_neu_tau001000um_M1600', 'c#tau = 1.0 mm', ROOT.kGreen+2, 5, 0.25), 
    ('mfv_neu_tau010000um_M1600', 'c#tau = 10 mm',  ROOT.kBlue,    7, 0.15), 
    ]

def fmt(z, title, color, style, xsec=None, save=[]):
    if type(z) == str: # signal name
        name = z
        h = f.Get('h_signal_%i_dvv_2017' % name2isample(f, z))
        g = f.Get('h_signal_%i_dvv_2018' % name2isample(f, z))
        h.Add(g)
    else: # background hist
        name = title
        h = z

    if '#tau' in title:
        h.Rebin(1)
    h.Sumw2()
    h = cm2mm(h)
    h.SetStats(0)
    h.SetLineStyle(style)
    h.SetLineWidth(4)
    h.SetLineColor(color)
    h.SetTitle(';d_{VV} (mm);Events/0.1 mm')
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.35)
    move_above_into_bin(h, 3.999)
    if title == 'bkg_2017': 
        norm = 0.241
    elif title == 'bkg_2018': 
        norm = 0.111
    else:
        rate_per_bin_2017 = combiner.combine(name2isample(combiner.inputs[0].f, name)).rates['2017']
        rate_per_bin_2018 = combiner.combine(name2isample(combiner.inputs[0].f, name)).rates['2018']

        uncert_per_bin_2017 = combiner.combine(name2isample(combiner.inputs[0].f, name)).uncerts['2017']
        uncert_per_bin_2018 = combiner.combine(name2isample(combiner.inputs[0].f, name)).uncerts['2018']

        # just to be safe
        assert(len(rate_per_bin_2017) == len(uncert_per_bin_2017))
        assert(len(rate_per_bin_2018) == len(uncert_per_bin_2018))
        assert(len(rate_per_bin_2017) == len(rate_per_bin_2018))

        # scale rate by the xsec of interest
        yield_per_bin_2017 = tuple([rate*xsec for rate in rate_per_bin_2017])
        yield_per_bin_2018 = tuple([rate*xsec for rate in rate_per_bin_2018])

        yield_per_bin_tot = tuple(map(lambda val17, val18 : val17 + val18, yield_per_bin_2017, yield_per_bin_2018))
        norm = sum(yield_per_bin_tot)

        # turn the 1+x uncertainties into the actual abs uncertainties on the yield
        abs_err_per_bin_2017 = tuple(map(lambda val, err : val*(err-1), yield_per_bin_2017, uncert_per_bin_2017))
        abs_err_per_bin_2018 = tuple(map(lambda val, err : val*(err-1), yield_per_bin_2018, uncert_per_bin_2018))

        # years are correlated ==> add errors linearly rather than adding in quadrature
        abs_err_per_bin_tot = tuple(map(lambda err17, err18 : err17 + err18, abs_err_per_bin_2017, abs_err_per_bin_2018))

        for ibin, (val, err) in enumerate(zip(yield_per_bin_tot, abs_err_per_bin_tot)) :
            print("bin %i: %.2f \pm %.2f" % (ibin, val, round(err,2)))

    h.Scale(norm/h.Integral(0,h.GetNbinsX()+2))
    save.append(h)
    return h

hbkg = fmt(f.Get('h_bkg_dvv_2017'), 'bkg_2017', ROOT.kBlack, ROOT.kSolid)
hbkg2018 = fmt(f.Get('h_bkg_dvv_2018'), 'bkg_2018', ROOT.kBlack, ROOT.kSolid)
hbkg.Add(hbkg2018)
hbkg.SetFillColor(ROOT.kGray)
hbkg.SetFillStyle(3002)

xoffset = -0.01
yoffset = -0.05
leg1 = ROOT.TLegend(0.400+xoffset, 0.805+yoffset, 0.909+xoffset, 0.862+yoffset)
leg1.AddEntry(hbkg, 'Background template', 'F')
leg2 = ROOT.TLegend(0.400+xoffset, 0.748+yoffset, 0.909+xoffset, 0.815+yoffset)
leg2.AddEntry(0, '#kern[-0.22]{Multijet signals, m = 1600 GeV}', '')
leg3 = ROOT.TLegend(0.400+xoffset, 0.612+yoffset, 0.909+xoffset, 0.745+yoffset)
legs = leg1, leg2, leg3

for lg in legs:
    lg.SetBorderSize(0)
    lg.SetTextSize(0.04)
    lg.SetFillStyle(0)

hbkg.Draw('hist')
ymin = 4e-3
ymax = 20
xmax = 4
hbkg.GetXaxis().SetRangeUser(0,xmax)
hbkg.GetYaxis().SetRangeUser(ymin,ymax)

for zzz, (name, title, color, style, xsec) in enumerate(which):
    h = fmt(name, title, color, style, xsec)

    # Sort of hacky way to not have the vertical line drawn for the signals w/ many entries in last bin
    # while keeping the other signal's cosmetics looking okay. Should revisit someday.
    if h.GetBinContent(h.FindBin(xmax)-1) < ymin :
        h.Draw('hist same')
    else :
        h.Draw('hist ][ same')

    if xsec :
        print "assuming xsec = %s fb for %s" % (xsec, name)

    leg3.AddEntry(h, title, 'L')
    print name, h.Integral(0,h.GetNbinsX()+2)

for lg in legs:
    lg.Draw()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

write(61, 0.050, 0.415+xoffset, 0.825, 'CMS')
write(42, 0.050, 0.595, 0.913, '101 fb^{-1} (13 TeV)')

dvvlines = [
        ROOT.TLine(0.4, 0, 0.4, ymax),
        ROOT.TLine(0.7, 0, 0.7, ymax),
        ]

for ll in dvvlines:
        ll.SetLineColor(ROOT.kRed)
        ll.SetLineWidth(2)
        ll.SetLineStyle(2)
        ll.Draw()

ps.save('templates')

write(52, 0.047, 0.52+xoffset, 0.825, 'Preliminary')

ps.save('templates_prelim')

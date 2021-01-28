from JMTucker.Tools.ROOTTools import *
from limitsinput import name2isample
from signal_efficiency import SignalEfficiencyCombiner
set_style()
ps = plot_saver(plot_dir('pretty_templates_2017p8_latest'), size=(700,700), log=True, pdf=True, pdf_log=True)

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)
ps.c.SetLogy()

f = ROOT.TFile('limitsinput.root')
#raise ValueError('propagate change to use stored rate already normalized to int lumi')
combiner = SignalEfficiencyCombiner()

#xsec = 0.25 # fb FIXME when moving to larger mass point!!
xsec = 0.3 # fb

which = [
    ('mfv_neu_tau000300um_M0800', 'c#tau = 0.3 mm', ROOT.kRed,     2), 
    ('mfv_neu_tau001000um_M0800', 'c#tau = 1.0 mm',   ROOT.kGreen+2, 5), 
    ('mfv_neu_tau010000um_M0800', 'c#tau = 10 mm',  ROOT.kBlue,    7), 
    ]

def fmt(z, title, color, style, save=[]):
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

xoffset = 0.04
const = 0.05
leg1 = ROOT.TLegend(0.400+xoffset, 0.810-const, 0.909+xoffset, 0.867-const)
leg1.AddEntry(hbkg, 'Background template', 'F')
leg2 = ROOT.TLegend(0.383+xoffset, 0.698-const, 0.893+xoffset, 0.815-const)
leg2.AddEntry(0, '#kern[-0.22]{#splitline{Multijet signals,}{m = 800 GeV, #sigma = %s fb:}}' % xsec, '')
leg3 = ROOT.TLegend(0.400+xoffset, 0.572-const, 0.909+xoffset, 0.705-const)
legs = leg1, leg2, leg3

for lg in legs:
    lg.SetBorderSize(0)
    lg.SetTextSize(0.04)
    lg.SetFillStyle(0)

htobreak = None
ymax = 20
for zzz, (name, title, color, style) in enumerate(which):
    h = fmt(name, title, color, style)
    if name == 'mfv_neu_tau010000um_M0800':
        htobreak = h
    if zzz == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
    h.GetXaxis().SetRangeUser(0,4)
    #h.GetYaxis().SetRangeUser(0,1.05)
    h.GetYaxis().SetRangeUser(4e-3,ymax)
    leg3.AddEntry(h, title, 'L')
    print name, h.Integral(0,h.GetNbinsX()+2)

hbkg.Draw('hist same')

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

# do broken y-axis. replace the "1" label with "18.2" and replace the
# last bin of that one hist's contents with 1 + contents - 18.2.

#########yax = htobreak.GetYaxis()
#########lastibin = htobreak.FindBin(3.999)
#########lastbin = htobreak.GetBinLowEdge(lastibin)
#########lastbc = htobreak.GetBinContent(lastibin)
#########print lastbc
#########assert abs(lastbc - 9.53697440144) < 1e-6
#########htobreak.SetBinContent(lastibin, lastbc - 9.53697440144 + 1)
#########boxxcenter = 0.
#########boxxwidth = 0.06
#########boxycenter = 0.9
#########boxywidth = 0.0205
#########boxx1, boxx2 = boxxcenter - boxxwidth, boxxcenter + boxxwidth
#########boxy1, boxy2 = boxycenter - boxywidth, boxycenter + boxywidth
#########boxxcenter2 = 4.
#########boxx21, boxx22 = boxxcenter2 - boxxwidth, boxxcenter2 + boxxwidth
#########boxes = [
#########    ROOT.TBox(boxx1, boxy1, boxx2, boxy2), # this does the break in the left x-axis
#########    ROOT.TBox(boxx21,boxy1, boxx22,boxy2), # ditto right x-axis
#########    ROOT.TBox(lastbin-0.02,boxy1,lastbin+0.02,boxy2), # wipes the part of the curve
#########    ROOT.TBox(-0.3, 0.95, -0.018, 1.05) # this wipes the end "1" label
#########    ]
#########for box in boxes:
#########    box.SetLineColor(ROOT.kWhite)
#########    box.SetFillColor(ROOT.kWhite)
#########    box.Draw()

########## draw the new end label
#########lab2 = ROOT.TText(-0.408, 0.982, '9.5')
#########lab2.SetTextFont(yax.GetLabelFont())
#########lab2.SetTextSize(yax.GetLabelSize())
#########lab2.Draw()

########## draw the break lines
#########slantdy = 0.005
#########lines = [ROOT.TLine(x1, y - slantdy, x2, y + slantdy) for y in boxy1, boxy2 for x1,x2 in (boxx1, boxx2), (boxx21, boxx22)]
#########for line in lines:
#########    line.SetLineWidth(1)
#########    line.Draw()

dvvlines = [
        #ROOT.TLine(0.4, 0, 0.4, 1.05),
        #ROOT.TLine(0.7, 0, 0.7, 1.05),
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

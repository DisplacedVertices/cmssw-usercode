from JMTucker.Tools.ROOTTools import *
from limitsinput import name2isample
from signal_efficiency import SignalEfficiencyCombiner

set_style()
ps = plot_saver(plot_dir('pretty_dbv_2017p8_diff_xsecs'), size=(700,700), pdf_log=True)

hide_overlap_with_x_axis = True

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
        h = f.Get('h_signal_%i_dbv_2017' % name2isample(f, z))
        h2 = f.Get('h_signal_%i_dbv_2018' % name2isample(f, z))
        h.Add(h2)
    else: # background hist
        name = 'bkg'
        h = z

    h.Sumw2()
    h = cm2mm(h)
    h.SetStats(0)
    h.SetLineStyle(style)
    h.SetLineWidth(3 if name == 'bkg' else 4)
    h.SetLineColor(color)
    h.Rebin(5)
    h.SetTitle(';d_{BV} (mm);Events/0.1 mm')
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.15)
    move_above_into_bin(h, 3.999)
    if title != 'bkg':
        print name2isample(combiner.inputs[0].f, name)
        h_dbv_2017 = combiner.combine(name2isample(combiner.inputs[0].f, name)).hs_dbv['2017']
        h_dbv_2018 = combiner.combine(name2isample(combiner.inputs[0].f, name)).hs_dbv['2018']
        total_sig_1v = h_dbv_2017.Integral(0,h_dbv_2017.GetNbinsX()+2)
        total_sig_1v += h_dbv_2018.Integral(0,h_dbv_2018.GetNbinsX()+2)
        norm = total_sig_1v * xsec
        h.Scale(norm/h.Integral(0,h.GetNbinsX()+2))
    save.append(h)
    return h

hbkg = fmt(f.Get('h_bkg_dbv_2017'), 'bkg', ROOT.kBlack, ROOT.kSolid)
hbkg2 = fmt(f.Get('h_bkg_dbv_2018'), 'bkg', ROOT.kBlack, ROOT.kSolid)
hbkg.Add(hbkg2)
print hbkg.Integral()
hbkg = poisson_intervalize(hbkg, zero_x=True) #, include_zero_bins='surrounded')
hbkg.SetMarkerStyle(20)
hbkg.SetMarkerSize(1.3)
hbkg.SetLineWidth(3)

xoffset = -0.01
yoffset = 0.007
leg1 = ROOT.TLegend(0.400+xoffset, 0.805+yoffset, 0.909+xoffset, 0.862+yoffset)
leg1.AddEntry(hbkg, 'Data', 'PE')
leg2 = ROOT.TLegend(0.400+xoffset, 0.748+yoffset, 0.909+xoffset, 0.815+yoffset)
leg2.AddEntry(0, '#kern[-0.22]{Multijet signals, m = 1600 GeV}', '')
leg3 = ROOT.TLegend(0.400+xoffset, 0.612+yoffset, 0.909+xoffset, 0.745+yoffset)
legs = leg1, leg2, leg3

for lg in legs:
    lg.SetBorderSize(0)
    lg.SetTextSize(0.04)
    lg.SetFillStyle(0)

firsthist = None

for zzz, (name, title, color, style, xsec) in enumerate(which):
    h = fmt(name, title, color, style, xsec)
    if zzz == 0:
        h.Draw('hist')
        firsthist = h
    else:
        h.Draw('hist same')
    h.GetXaxis().SetRangeUser(0,4)
    ymin = 2e-2
    h.GetYaxis().SetRangeUser(ymin,5e3)

    if xsec :
        print "assuming xsec = %s fb for %s" % (xsec, name)

    leg3.AddEntry(h, title, 'L')
    print name, h.Integral(0,h.GetNbinsX()+2)

    if hide_overlap_with_x_axis :
        magic = 0.0131 # fun magic number for covering over bold lines on x-axis
        horiz_line = ROOT.TLine()
        horiz_line.SetLineColor(ROOT.kWhite)
        horiz_line.SetLineWidth(5)
        horiz_line.SetLineStyle(1)
        if zzz == 0 :
            horiz_line.DrawLine(1.4+magic, ymin, 4, ymin)
        elif zzz == 1 :
            horiz_line.DrawLine(2.4+magic, ymin, 3.9-magic, ymin)
            horiz_line.DrawLine(2.38, ymin*.95, 2.42, ymin*.95)
        elif zzz == 2 :
            # for 0 to 0.1
            horiz_line.DrawLine(-0.000025, ymin, 0.1-magic, ymin)
            horiz_line.DrawLine(0.08, ymin*.95, 0.12, ymin*.95)

            # for the plot itself
            horiz_line.DrawLine(3.5+magic, ymin, 3.9-magic, ymin)
            horiz_line.DrawLine(3.48, ymin*.95, 3.52, ymin*.95)

            # for the entries above ymin whose lines go beyond it
            horiz_line.DrawLine(3.28, ymin*.95, 3.42, ymin*.95)
            
            # for the weird single-pixel-wide lines that stubbornly remain
            horiz_line.DrawLine(3.98, ymin*.937, 4.02, ymin*.937)
            horiz_line.DrawLine(-0.02, ymin*.937, 0.02, ymin*.937)

hbkg.Draw('PE')

if hide_overlap_with_x_axis and firsthist : 
    firsthist.Draw('axis same')

for lg in legs:
    lg.Draw()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

xcms = 0.23
#write(61, 0.050, 0.175, 0.825, 'CMS')
write(61, 0.050, xcms, 0.825, 'CMS')
write(42, 0.050, 0.595, 0.913, '101 fb^{-1} (13 TeV)')

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)

ps.save('dbv')

xoffset_prelim = 0.105
write(52, 0.047, xcms+xoffset_prelim, 0.825, 'Preliminary')

ps.save('dbv_prelim')

if hide_overlap_with_x_axis :
    print "NOTE! hide_overlap_with_x_axis = True, so some cosmetic magic has been applied (only relevant for EXO-19-013, and should be removed/adjusted in future analyses)"

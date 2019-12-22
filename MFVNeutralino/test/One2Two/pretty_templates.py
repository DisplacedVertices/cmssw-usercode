from JMTucker.Tools.ROOTTools import *
from limitsinput import name2isample
from signal_efficiency import SignalEfficiencyCombiner
set_style()
ps = plot_saver(plot_dir('pretty_templates'), size=(700,700), log=False, pdf=True)

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)

f = ROOT.TFile('/uscms/home/tucker/public/mfv/limitsinput_100kevent_samples_used_for_Figs_1+3.root')
raise ValueError('propagate change to use stored rate already normalized to int lumi')
combiner = SignalEfficiencyCombiner()

which = [
    ('mfv_neu_tau00300um_M0800', 'c#tau = 0.3 mm', ROOT.kRed,     2), 
    ('mfv_neu_tau01000um_M0800', 'c#tau = 1.0 mm',   ROOT.kGreen+2, 5), 
    ('mfv_neu_tau10000um_M0800', 'c#tau = 10 mm',  ROOT.kBlue,    7), 
    ]

def fmt(z, title, color, style, save=[]):
    if type(z) == str: # signal name
        name = z
        h = f.Get('h_signal_%i_dvv' % name2isample(f, z))
    else: # background hist
        name = 'bkg'
        h = z

    if '#tau' in title:
        h.Rebin(10)
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
    if title == 'bkg': 
        norm = 1.
    else:
        norm = combiner.combine(name2isample(combiner.inputs[0].f, name)).total_sig_rate
    h.Scale(norm/h.Integral(0,h.GetNbinsX()+2))
    save.append(h)
    return h

hbkg = fmt(f.Get('h_bkg_dvv'), 'bkg', ROOT.kBlack, ROOT.kSolid)
hbkg.SetFillColor(ROOT.kGray)
hbkg.SetFillStyle(3002)

leg1 = ROOT.TLegend(0.400, 0.810, 0.909, 0.867)
leg1.AddEntry(hbkg, 'Background template', 'F')
leg2 = ROOT.TLegend(0.383, 0.698, 0.893, 0.815)
leg2.AddEntry(0, '#kern[-0.22]{#splitline{Multijet signals,}{m = 800 GeV, #sigma = 1 fb:}}', '')
leg3 = ROOT.TLegend(0.400, 0.572, 0.909, 0.705)
legs = leg1, leg2, leg3

for lg in legs:
    lg.SetBorderSize(0)
    lg.SetTextSize(0.04)

htobreak = None
for zzz, (name, title, color, style) in enumerate(which):
    h = fmt(name, title, color, style)
    if name == 'mfv_neu_tau10000um_M0800':
        htobreak = h
    if zzz == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
    h.GetXaxis().SetRangeUser(0,4)
    h.GetYaxis().SetRangeUser(0,1.05)
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

write(61, 0.050, 0.175, 0.825, 'CMS')
write(42, 0.050, 0.595, 0.913, '38.5 fb^{-1} (13 TeV)')

# do broken y-axis. replace the "1" label with "18.2" and replace the
# last bin of that one hist's contents with 1 + contents - 18.2.

yax = htobreak.GetYaxis()
lastibin = htobreak.FindBin(3.999)
lastbin = htobreak.GetBinLowEdge(lastibin)
lastbc = htobreak.GetBinContent(lastibin)
assert abs(lastbc - 18.202475) < 1e-6
htobreak.SetBinContent(lastibin, lastbc - 18.2 + 1)
boxxcenter = 0.
boxxwidth = 0.06
boxycenter = 0.9
boxywidth = 0.0205
boxx1, boxx2 = boxxcenter - boxxwidth, boxxcenter + boxxwidth
boxy1, boxy2 = boxycenter - boxywidth, boxycenter + boxywidth
boxxcenter2 = 4.
boxx21, boxx22 = boxxcenter2 - boxxwidth, boxxcenter2 + boxxwidth
boxes = [
    ROOT.TBox(boxx1, boxy1, boxx2, boxy2), # this does the break in the left x-axis
    ROOT.TBox(boxx21,boxy1, boxx22,boxy2), # ditto right x-axis
    ROOT.TBox(lastbin-0.02,boxy1,lastbin+0.02,boxy2), # wipes the part of the curve
    ROOT.TBox(-0.3, 0.95, -0.018, 1.05) # this wipes the end "1" label
    ]
for box in boxes:
    box.SetLineColor(ROOT.kWhite)
    box.SetFillColor(ROOT.kWhite)
    box.Draw()

# draw the new end label
lab2 = ROOT.TText(-0.408, 0.982, '18.2')
lab2.SetTextFont(yax.GetLabelFont())
lab2.SetTextSize(yax.GetLabelSize())
lab2.Draw()

# draw the break lines
slantdy = 0.005
lines = [ROOT.TLine(x1, y - slantdy, x2, y + slantdy) for y in boxy1, boxy2 for x1,x2 in (boxx1, boxx2), (boxx21, boxx22)]
for line in lines:
    line.SetLineWidth(1)
    line.Draw()

ps.save('templates')

write(52, 0.047, 0.48, 0.82, 'Preliminary')

ps.save('templates_prelim')

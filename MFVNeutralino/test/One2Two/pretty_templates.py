from JMTucker.Tools.ROOTTools import *
from limitsinput import name2isample
from signal_efficiency import SignalEfficiencyCombiner
set_style()
ps = plot_saver(plot_dir('pretty_templates'), size=(700,700), log=False, pdf=True)

f = ROOT.TFile('/uscms/home/tucker/public/mfv/limitsinput_100kevent_samples_used_for_Figs_1+3.root')
combiner = SignalEfficiencyCombiner()

which = [
    ('mfv_neu_tau00300um_M0800', 'c#tau = 0.3 mm', ROOT.kRed,     2), 
    ('mfv_neu_tau01000um_M0800', 'c#tau = 1 mm',   ROOT.kGreen+2, 5), 
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
    h.SetLineWidth(3)
    h.SetLineColor(color)
    h.SetTitle(';d_{VV} (mm);Events/0.1 mm')
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.1)
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
hbkg.SetFillStyle(3001)

leg = ROOT.TLegend(0.30, 0.65, 0.85, 0.85)
leg.SetBorderSize(0)
leg.AddEntry(hbkg, 'Background template', 'LF')
leg.AddEntry(0, '#kern[-0.22]{Multijet signals, M = 800 GeV, #sigma = 1 fb:}', '')

for zzz, (name, title, color, style) in enumerate(which):
    h = fmt(name, title, color, style)
    if zzz == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
    h.GetXaxis().SetRangeUser(0,4)
    h.GetYaxis().SetRangeUser(0,1)
    leg.AddEntry(h, title, 'L')
    print name, h.Integral(0,h.GetNbinsX()+2)

hbkg.Draw('hist same')

leg.Draw()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

write(61, 0.050, 0.109, 0.913, 'CMS')
write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.11)

ps.save('templates')

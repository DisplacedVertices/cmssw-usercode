from JMTucker.Tools.ROOTTools import *
from limitsinput import name2isample
from signal_efficiency import SignalEfficiencyCombiner

set_style()
ps = plot_saver(plot_dir('pretty_dbv'), size=(700,700), pdf_log=True)

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
        h = f.Get('h_signal_%i_dbv' % name2isample(f, z))
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
        norm = combiner.combine(name2isample(combiner.inputs[0].f, name)).total_sig_1v
        h.Scale(norm/h.Integral(0,h.GetNbinsX()+2))
    save.append(h)
    return h

hbkg = fmt(f.Get('h_bkg_dbv'), 'bkg', ROOT.kBlack, ROOT.kSolid)
hbkg = poisson_intervalize(hbkg, zero_x=True) #, include_zero_bins='surrounded')
hbkg.SetMarkerStyle(20)
hbkg.SetMarkerSize(1.3)
hbkg.SetLineWidth(3)

leg = ROOT.TLegend(0.30, 0.60, 0.85, 0.80)
leg.SetBorderSize(0)
leg.AddEntry(hbkg, 'Data', 'PE')
leg.AddEntry(0, '#kern[-0.22]{Multijet signals, M = 800 GeV, #sigma = 1 fb:}', '')

for zzz, (name, title, color, style) in enumerate(which):
    h = fmt(name, title, color, style)
    if zzz == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
    h.GetXaxis().SetRangeUser(0,4)
    h.GetYaxis().SetRangeUser(6e-2,2e3)
    leg.AddEntry(h, title, 'L')
    print name, h.Integral(0,h.GetNbinsX()+2)

hbkg.Draw('PE')

leg.Draw()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

write(61, 0.050, 0.32, 0.82, 'CMS')
write(42, 0.050, 0.595, 0.913, '38.5 fb^{-1} (13 TeV)')

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)

ps.save('dbv')

write(52, 0.047, 0.43, 0.82, 'Preliminary')

ps.save('dbv_prelim')

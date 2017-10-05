from JMTucker.Tools.ROOTTools import *

set_style()
ps = plot_saver('../plots/EXO-17-018/templates', size=(700,700), log=False, pdf=True)

f = ROOT.TFile('limits_input.root')

def name2isample(f, name):
    h = f.Get('name_list')
    ax = h.GetXaxis()
    for ibin in xrange(1, h.GetNbinsX()+1):
        if name == ax.GetBinLabel(ibin):
            return -ibin
    raise ValueError('no name %s found in %r' % (name, f))

which = [
    (name2isample(f, 'mfv_neu_tau00300um_M0800'), ROOT.kRed, 'c#tau = 300 #mum'),
    (name2isample(f, 'mfv_neu_tau01000um_M0800'), ROOT.kGreen+2, 'c#tau = 1 mm'),
    (name2isample(f, 'mfv_neu_tau10000um_M0800'), ROOT.kBlue, 'c#tau = 10 mm'),
    ]

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

def fmt(h, name, color, save=[]):
    if type(name) == tuple:
        name, signum = name

    if '#tau' in name:
        h.Rebin(10)
    h.Sumw2()
    h.SetStats(0)
    h.SetLineWidth(3)
    h.SetLineColor(color)
    h.SetTitle(';d_{VV} (cm);Events/100 #mum')
    h.GetXaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.3)
    move_above_into_bin(h, 0.3999)
    if name == 'bkg': 
        h.Scale(1./h.Integral(0,h.GetNbinsX()+2))
    else:
        norm = f.Get('h_signal_%i_norm' % signum).GetBinContent(2)
        print norm * 38500 * h.Integral(0,h.GetNbinsX()+2)
        h.Scale(norm * 38500.)
    print h.Integral()
    save.append(h)
    return h

hbkg = fmt(f.Get('h_bkg_dvv'), 'bkg', ROOT.kBlack)
hbkg.SetFillColor(ROOT.kGray)
hbkg.SetFillStyle(3001)

leg = ROOT.TLegend(0.45, 0.65, 0.85, 0.85)
leg.SetBorderSize(0)
leg.AddEntry(hbkg, 'Background template', 'LF')
leg.AddEntry(0, '#kern[-0.22]{Multijet signals, M = 800 GeV, #sigma = 1 fb:}', '')

for zzz, (isample, color, title) in enumerate(which):
    h = fmt(f.Get('h_signal_%i_dvv' % isample), (title,isample), color)
    if zzz == 0:
        h.Draw('hist')
    else:
        h.Draw('hist same')
    h.GetXaxis().SetRangeUser(0,0.4)
    h.GetYaxis().SetRangeUser(0,0.75)
    leg.AddEntry(h, title, 'L')

hbkg.Draw('hist same')

leg.Draw()

write(61, 0.040, 0.098, 0.91, 'CMS')
write(52, 0.035, 0.185, 0.91, 'Preliminary')
write(42, 0.040, 0.625, 0.91, '38.5 fb^{-1} (13 TeV)')

ps.save('templates')

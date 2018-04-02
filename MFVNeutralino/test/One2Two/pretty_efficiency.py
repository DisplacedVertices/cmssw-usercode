import sys, os
from JMTucker.Tools.ROOTTools import *

path = plot_dir('pretty_efficiency_final_really', make=True)

ts = tdr_style()
ROOT.gStyle.SetPalette(ROOT.kBird) #kColorPrintableOnGrey
ROOT.gStyle.SetNumberContours(20) #500 for smooth gradation

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w


f = ROOT.TFile('signal_efficiency.root')

for kind in 'mfv_stopdbardbar', 'mfv_neu':
    c = ROOT.TCanvas('c', '', 800, 800)
    c.SetTopMargin(0.1)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.11)
    c.SetRightMargin(0.18)
    h = f.Get('signal_efficiency_%s' % kind)
    xax = h.GetXaxis()
    if 'neu' in kind:
        xax.SetTitle('M_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
    else:
        xax.SetTitle('M_{#tilde{t}} (GeV)')
#    xax.CenterLabels()
#    xax.SetNdivisions(1300, 0)
#    xax.SetBinLabel(xax.FindBin(400), '400')
#    xax.SetBinLabel(xax.FindBin(600), '600')
#    xax.SetBinLabel(xax.FindBin(800), '800')
#    xax.SetBinLabel(xax.FindBin(1000), '1000')
#    xax.SetBinLabel(xax.FindBin(1200), '1200')
#    xax.SetBinLabel(xax.FindBin(1400), '1400')
    xax.SetRangeUser(300,2800)
    xax.SetLabelSize(0.045)
    xax.SetTitleSize(0.05)
    xax.SetTitleOffset(1.05)
#    xax.LabelsOption('h')
    yax = h.GetYaxis()
    yax.SetTitle('c#tau (mm)')
    yax.SetTitleOffset(1.105)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.045)
    yax.SetRangeUser(0.1, 100.)
#    yax.SetBinLabel(yax.FindBin(300), '0.3')
#    yax.SetBinLabel(yax.FindBin(1000), '1')
#    yax.SetBinLabel(yax.FindBin(5000), '5')
#    yax.SetBinLabel(yax.FindBin(10000), '10')
#    yax.SetBinLabel(yax.FindBin(20000), '20')
#    yax.SetBinLabel(yax.FindBin(30000), '30')
    zax = h.GetZaxis()
    zax.SetRangeUser(0., 0.85)
    zax.SetTitle('Efficiency for d_{VV} > 0.4 mm')
    zax.SetLabelSize(0.045)
    zax.SetTitleSize(0.05)
    zax.SetTitleOffset(1.22)
    #zax.SetTitleSize()
#    ROOT.gStyle.SetPaintTextFormat(".1g")
#    c.SetLogy()
#    h.SetMarkerColor(ROOT.kWhite)
#    h.Draw('colz text')
    h.Draw('colz')
    cms = write(61, 0.050, 0.109, 0.913, 'CMS')
    sim = write(52, 0.040, 0.222, 0.912, 'Simulation')
    lum = write(42, 0.050, 0.676, 0.913, '(13 TeV)')
    for ext in 'pdf', 'png', 'root':
        c.SaveAs(os.path.join(path, 'scan_eff_%s.%s' % (kind, ext)))
    del c

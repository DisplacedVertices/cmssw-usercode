import sys, os
from JMTucker.Tools.ROOTTools import *

path = plot_dir('pretty_efficiency_corrected_2', make=True)

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


for which in 'run2','2017p8':
    f = ROOT.TFile('signal_efficiency_%s.root' % which)
    for kind in 'mfv_stopdbardbar', 'mfv_neu':
        c = ROOT.TCanvas('c', '', 848, 800)
        c.SetTopMargin(0.1)
        c.SetBottomMargin(0.12)
        c.SetLeftMargin(0.13)
        c.SetRightMargin(0.20)
        h = f.Get('signal_efficiency_%s' % kind)
        xax = h.GetXaxis()
        if 'neu' in kind:
            xax.SetTitle('m_{#tilde{#chi}^{0} / #tilde{g}} (GeV)')
        else:
            xax.SetTitle('m_{#tilde{t}} (GeV)')
    #    xax.CenterLabels()
    #    xax.SetNdivisions(1300, 0)
    #    xax.SetBinLabel(xax.FindBin(400), '400')
    #    xax.SetBinLabel(xax.FindBin(600), '600')
    #    xax.SetBinLabel(xax.FindBin(800), '800')
    #    xax.SetBinLabel(xax.FindBin(1000), '1000')
    #    xax.SetBinLabel(xax.FindBin(1200), '1200')
    #    xax.SetBinLabel(xax.FindBin(1400), '1400')
        xax.SetRangeUser(300,3000)
        xax.SetLabelSize(0.045)
        xax.SetTitleSize(0.05)
        xax.SetTitleOffset(1.05)
    #    xax.LabelsOption('h')
        yax = h.GetYaxis()
        yax.SetTitle('c#tau (mm)')
        yax.SetTitleOffset(1.13)
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
        zax.SetTitle('Efficiency (full selection)')
        zax.SetLabelSize(0.045)
        zax.SetTitleSize(0.05)
        zax.SetTitleOffset(1.22)
        #zax.SetTitleSize()
    #    ROOT.gStyle.SetPaintTextFormat(".1g")
    #    c.SetLogy()
    #    h.SetMarkerColor(ROOT.kWhite)
    #    h.Draw('colz text')
        h.Draw('colz')
        cms = write(61, 0.050, 0.129, 0.913, 'CMS')
        sim = write(52, 0.040, 0.234, 0.912, 'Simulation')
        bn = 'scan_eff_%s_%s' % (which, kind)
        for ext in 'pdf', 'png', 'root':
            c.SaveAs(os.path.join(path, '%s.%s' % (bn, ext)))
        pre = write(52, 0.040, 0.406, 0.912, 'Preliminary')
        for ext in 'pdf', 'png', 'root':
            c.SaveAs(os.path.join(path, '%s_prelim.%s' % (bn, ext)))
        del c

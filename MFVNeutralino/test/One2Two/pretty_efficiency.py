import sys, os
from JMTucker.Tools.ROOTTools import *

path = plot_dir('pretty_efficiency_final', make=True)
swap_axes = True

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

def do_swap_axes(obj) :
    if obj.Class().GetName() == 'TH2D' :
        nbinx = obj.GetNbinsX()
        nbiny = obj.GetNbinsY()
        xbins = obj.GetXaxis().GetXbins().GetArray()
        ybins = obj.GetYaxis().GetXbins().GetArray()

        hnew = ROOT.TH2D("swap","swap",nbiny,ybins,nbinx,xbins)
        
        for ibinx in xrange(1,nbinx+2) :
            for ibiny in xrange(1,nbiny+2) :
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


for which in 'run2','2017p8':
    f = ROOT.TFile('signal_efficiency_%s.root' % which)
    for kind in 'mfv_stopdbardbar', 'mfv_neu':
        c = ROOT.TCanvas('c', '', 950, 900)
        c.SetTopMargin(0.1)
        c.SetBottomMargin(0.12)
        c.SetLeftMargin(0.17)
        c.SetRightMargin(0.20)

        if swap_axes :
            c.SetLogx()
        else :
            c.SetLogy()

        h = f.Get('signal_efficiency_%s' % kind)

        xax = h.GetXaxis()
        yax = h.GetYaxis()

        if swap_axes :
            h = do_swap_axes(h)
            xax = h.GetYaxis()
            yax = h.GetXaxis()

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
        xax.SetTitleOffset(1.6)
    #    xax.LabelsOption('h')
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
        h.GetXaxis().SetNoExponent()
        xshift=0.04
        cms = write(61, 0.050, 0.129+xshift, 0.913, 'CMS')
        sim = write(52, 0.040, 0.234+xshift, 0.912, 'Simulation')
        if which == '2017p8':   
            lum = write(42, 0.050, 0.495, 0.913, '101 fb^{-1} (13 TeV)')        
        else:   
            lum = write(42, 0.050, 0.495, 0.913, '140 fb^{-1} (13 TeV)')        
        bn = 'scan_eff_%s_%s' % (which, kind)
        for ext in 'pdf', 'png', 'root':
            c.SaveAs(os.path.join(path, '%s.%s' % (bn, ext)))
        pre = write(52, 0.040, 0.406+xshift, 0.912, 'Preliminary')
        for ext in 'pdf', 'png', 'root':
            c.SaveAs(os.path.join(path, '%s_prelim.%s' % (bn, ext)))
        del c

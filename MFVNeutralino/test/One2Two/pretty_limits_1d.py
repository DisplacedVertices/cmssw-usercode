import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *

path = plot_dir('pretty_limits_1d', make=True)

ts = tdr_style()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

f = ROOT.TFile('limits_1d.root')

nice = {
    'multijetM800': '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs, M_{#tilde{#chi}^{0}/#tilde{g}} = 800 GeV',
    'ddbarM800':    '#tilde{g} #rightarrow q#bar{q}, M_{#tilde{g}} = 800 GeV',
    'multijettau1mm': '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs, c#tau_{#tilde{#chi}^{0}/#tilde{g}} = 1 mm',
    'ddbartau1mm':    '#tilde{g} #rightarrow q#bar{q}, c#tau_{#tilde{g}} = 1 mm',
}

for kind in 'multijetM800', 'multijettau1mm', 'ddbarM800', 'ddbartau1mm':
    c = ROOT.TCanvas('c', '', 800, 800)
    c.SetLogy()
    if 'M800' in kind:
        c.SetLogx()
    c.SetTopMargin(0.1)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.11)
    c.SetRightMargin(0.1)

    observed = f.Get('%s/observed' % kind)
    expect50 = f.Get('%s/expect50' % kind)
    expect68 = f.Get('%s/expect68' % kind)
    expect95 = f.Get('%s/expect95' % kind)
    gluglu = f.Get('%s/gluglu' % kind)

    if 'tau' in kind:
        particle = '#tilde{g}' if 'ddbar' in kind else '#tilde{#chi}^{0} / #tilde{g}'
        xtitle = 'M_{%s} (GeV)' % particle
    elif 'M800' in kind:
        xtitle = 'c#tau (mm)'
        
    g = expect95
    g.SetTitle(';%s;#sigma B^{2} (fb)' % xtitle)
    g.Draw('A3')

    draw_gluglu = 'tau' in kind

    xax = g.GetXaxis()
    xax.SetLabelSize(0.045)
    xax.SetTitleSize(0.05)
    xax.SetTitleOffset(1.05)
    yax = g.GetYaxis()
    yax.SetTitleOffset(1.05)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.045)

    if 'M800' in kind:
        yax.SetRangeUser(0.1, 30)
    elif 'tau' in kind:
        yax.SetRangeUser(0.1, 30)

    expect95.Draw('3')
    expect68.Draw('3')
    expect50.Draw('L')
    observed.Draw('LP')
    if draw_gluglu:
        gluglu.Draw('3')
        leg = ROOT.TLegend(0.583, 0.566, 0.866, 0.851)
    else:
        leg = ROOT.TLegend(0.583, 0.632, 0.866, 0.851)

    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.AddEntry(0, '#kern[-0.22]{%s}' % nice[kind], '')
    leg.AddEntry(0, '#kern[-0.22]{95% CL upper limits:}', '')
    leg.AddEntry(observed, 'Observed', 'LP')
    leg.AddEntry(expect50, 'Expected', 'L')
    leg.AddEntry(expect68, '#pm 1 #sigma', 'F')
    leg.AddEntry(expect95, '#pm 2 #sigma', 'F')
    if draw_gluglu:
        leg.AddEntry(0, '', '')
        leg.AddEntry(gluglu, '#tilde{g}#tilde{g} production', 'F')
    leg.Draw()

    cms = write(61, 0.050, 0.109, 0.913, 'CMS')
    lum = write(42, 0.050, 0.528, 0.913, '38.5 fb^{-1} (13 TeV)')
    fn = os.path.join(path, kind)
    c.SaveAs(fn + '.pdf')
    c.SaveAs(fn + '.png')
    c.SaveAs(fn + '.root')
    del c

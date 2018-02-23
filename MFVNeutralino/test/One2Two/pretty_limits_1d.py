import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *

path = plot_dir('pretty_limits_1d_final_5', make=True)

ts = tdr_style()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

f = ROOT.TFile('limits_1d.root')

kinds = [
    'multijet_M0800',
    'multijet_M1600',
    'multijet_M2400',
    'multijet_tau300um',
    'multijet_tau1mm',
    'multijet_tau10mm',
    'ddbar_M0800',
    'ddbar_M1600',
    'ddbar_M2400',
    'ddbar_tau300um',
    'ddbar_tau1mm',
    'ddbar_tau10mm',
    ]

def tau(tau):
    if tau.endswith('um'):
        tau = int(tau.replace('um',''))/1000.
        return '%.1f mm' % tau
    else:
        assert tau.endswith('mm')
        tau = float(tau.replace('mm',''))
        return '%.0f mm' % tau

def nice(kind):
    if kind.startswith('multijet_M'):
        return '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs, M = %i GeV' % int(kind.replace('multijet_M', ''))
    elif kind.startswith('ddbar_M'):
        return '#tilde{g} #rightarrow d#bar{d}, M = %i GeV' % int(kind.replace('ddbar_M', ''))
    elif kind.startswith('multijet_tau'):
        return '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs, c#tau = ' + tau(kind.replace('multijet_tau', ''))
    elif kind.startswith('ddbar_tau'):
        return '#tilde{g} #rightarrow d#bar{d}, c#tau = ' + tau(kind.replace('ddbar_tau', ''))
        
for kind in kinds:
    versus_tau = kind[-5] == 'M'
    versus_mass = 'tau' in kind
    assert int(versus_tau) + int(versus_mass) == 1

    c = ROOT.TCanvas('c', '', 800, 800)
    c.SetLogy()
    if kind[-5] == 'M':
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

    particle = '#tilde{g}' if 'ddbar' in kind else '#tilde{#chi}^{0} / #tilde{g}'
    if versus_mass:
        xtitle = 'M_{%s} (GeV)' % particle
    elif versus_tau:
        xtitle = 'c#tau_{%s} (mm)' % particle
        
    g = expect95
    g.SetTitle(';%s;#sigma B^{2} (fb)  ' % xtitle)
    g.Draw('A3')

    draw_gluglu = 'tau' in kind

    xax = g.GetXaxis()
    xax.SetLabelSize(0.045)
    xax.SetTitleSize(0.05)
    if versus_tau:
        xax.SetLabelOffset(0.002)
    xax.SetTitleOffset(1.1)
    yax = g.GetYaxis()
    yax.SetTitleOffset(1.05)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.045)

    if versus_mass:
        xax.SetLimits(175, 3000)
    elif versus_tau:
        xax.SetLimits(0.068, 130)
    yax.SetRangeUser(0.08, 100000 if (versus_tau and draw_gluglu) else 100)

    observed.SetLineWidth(2)
    expect50.SetLineWidth(2)
    expect50.SetLineStyle(2)
    gluglu.SetLineWidth(2)
    gluglu.SetFillColorAlpha(9, 0.5)

    expect95.Draw('3')
    expect68.Draw('3')
    if draw_gluglu:
        gluglu.Draw('L3')
    expect50.Draw('L')
    observed.Draw('L')

    if versus_mass:
        legx = 0.563, 0.866
    elif versus_tau:
        legx = 0.443, 0.786
    if draw_gluglu:
        leg = ROOT.TLegend(legx[0], 0.566, legx[1], 0.851)
    else:
        leg = ROOT.TLegend(legx[0], 0.632, legx[1], 0.851)

    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.AddEntry(0, '#kern[-0.22]{%s}' % nice(kind), '')
    leg.AddEntry(0, '#kern[-0.22]{95% CL upper limits:}', '')
    leg.AddEntry(observed, 'Observed', 'L')
    leg.AddEntry(expect50, 'Expected', 'L')
    leg.AddEntry(expect68, '#pm 1 std. deviation', 'F')
    leg.AddEntry(expect95, '#pm 2 std. deviation', 'F')
    if draw_gluglu:
        leg.AddEntry(gluglu, '#tilde{g}#tilde{g} production', 'LF')
    leg.Draw()

    cms = write(61, 0.050, 0.109, 0.913, 'CMS')
    lum = write(42, 0.050, 0.548, 0.913, '38.5 fb^{-1} (13 TeV)')
    fn = os.path.join(path, 'limit1d_' + kind)
    c.SaveAs(fn + '.pdf')
    c.SaveAs(fn + '.png')
    c.SaveAs(fn + '.root')
    del c

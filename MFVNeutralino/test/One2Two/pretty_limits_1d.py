import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
ROOT.gErrorIgnoreLevel = 1001 # Suppress TCanvas::SaveAs messages.

which = 'run2' # '2017p8'
intlumi = 140 if which == 'run2' else 101
path = plot_dir('pretty_limits_1d_scanpack1D_%s' % which, make=True)

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
    'multijet_M3000',
    'multijet_tau300um',
    'multijet_tau1mm',
    'multijet_tau10mm',
    'dijet_M0800',
    'dijet_M1600',
    'dijet_M2400',
    'dijet_M3000',
    'dijet_tau300um',
    'dijet_tau1mm',
    'dijet_tau10mm',
    ]

if which == 'run2':
    kinds = [k for k in kinds if 'M3000' not in k]

def tau(tau):
    if tau.endswith('um'):
        tau = int(tau.replace('um',''))/1000.
        return '%.1f mm' % tau
    else:
        assert tau.endswith('mm')
        tau = float(tau.replace('mm',''))
        fmt = '%.1f mm' if tau < 10 else '%.0f mm'
        return fmt % tau

def nice_leg(kind):
    if kind.startswith('multijet_M'):
        return '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs, m = %i GeV' % int(kind.replace('multijet_M', ''))
    elif kind.startswith('dijet_M'):
        return '#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}, m = %i GeV' % int(kind.replace('dijet_M', ''))
    elif kind.startswith('multijet_tau'):
        return '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs, c#tau = ' + tau(kind.replace('multijet_tau', ''))
    elif kind.startswith('dijet_tau'):
        return '#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}, c#tau = ' + tau(kind.replace('dijet_tau', ''))

def nice_theory(kind):
    if kind.startswith('multijet'):
        return '#tilde{g}#tilde{g} production'
    elif kind.startswith('dijet'):
        return '#tilde{t}#kern[0.9]{#tilde{t}}* production'

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
    theory = f.Get('%s/theory' % kind)

    if 0:
        if kind == 'dijet_tau300um':
            for i in xrange(20):
                print 'ugh'
            g = expect95
            x,y = tgraph_getpoint(g, 9)
            assert x == 1800
            g.SetPointEYhigh(9, (g.GetErrorYhigh(8) + g.GetErrorYhigh(10))/2)
        elif kind == 'multijet_tau300um':
            for i in xrange(20):
                print 'ugh'
            g = expect95
            x,y = tgraph_getpoint(g, 9)
            assert x == 1800
            g.SetPointEYhigh(9, (g.GetErrorYhigh(8) + g.GetErrorYhigh(10))/2)
            x,y = tgraph_getpoint(g, 11)
            assert x == 2200
            g.SetPointEYhigh(11, (g.GetErrorYhigh(10) + g.GetErrorYhigh(12))/2)

    particle = '#tilde{t}' if 'dijet' in kind else '#tilde{#chi}^{0} / #tilde{g}'
    if versus_mass:
        xtitle = 'm_{%s} (GeV)' % particle
    elif versus_tau:
        xtitle = 'c#tau_{%s} (mm)' % particle
        
    g = expect95
    g.SetTitle(';%s;#sigma#bf{#it{#Beta}}^{2} (fb)    ' % xtitle)
    g.Draw('A3')

    draw_theory = 'tau' in kind

    xax = g.GetXaxis()
    xax.SetLabelSize(0.045)
    xax.SetTitleSize(0.05)
    if versus_tau:
        xax.SetLabelOffset(0.002)
    xax.SetTitleOffset(1.1)
    yax = g.GetYaxis()
    yax.SetTitleOffset(1.03)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.045)

    if versus_mass:
        xax.SetLimits(105, 3200)
    elif versus_tau:
        xax.SetLimits(0.068, 130)
    yax.SetRangeUser(0.01, 100000 if (versus_tau and draw_theory) else 130)

    observed.SetLineWidth(2)
    expect50.SetLineWidth(2)
    expect50.SetLineStyle(2)
    theory.SetLineWidth(2)
    if kind.startswith('multijet'):
        theory_color = 9
    elif kind.startswith('dijet'):
        theory_color = 46
    theory.SetLineColor(theory_color)
    theory.SetFillColorAlpha(theory_color, 0.5)

    expect95.SetLineColor(ROOT.kOrange)
    expect68.SetLineColor(ROOT.kGreen+1)
    expect95.SetFillColor(ROOT.kOrange)
    expect68.SetFillColor(ROOT.kGreen+1)

    expect95.Draw('3')
    expect68.Draw('3')
    if draw_theory:
        theory.Draw('L3')
    expect50.Draw('L')
#    observed.Draw('L')

    if draw_theory:
        leg = ROOT.TLegend(0.552, 0.563, 0.870, 0.867)
    else:
        leg = ROOT.TLegend(0.552, 0.603, 0.870, 0.867)

    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.AddEntry(0, '#kern[-0.22]{%s}' % nice_leg(kind), '')
    leg.AddEntry(0, '#kern[-0.22]{95% CL upper limits:}', '')
 #   leg.AddEntry(observed, 'Observed', 'L')
    leg.AddEntry(expect50, 'Median expected', 'L')
    leg.AddEntry(expect68, '68% expected', 'F')
    leg.AddEntry(expect95, '95% expected', 'F')
    if draw_theory:
        leg.AddEntry(theory, nice_theory(kind) + ', #bf{#it{#Beta}}=1', 'LF')
    leg.Draw()

    cms = write(61, 0.050, 0.142, 0.825, 'CMS')
    lum = write(42, 0.050, 0.548, 0.913, '%s fb^{-1} (13 TeV)' % intlumi)
    fn = os.path.join(path, 'limit1d_' + kind)
    c.SaveAs(fn + '.pdf')
    c.SaveAs(fn + '.png')
    c.SaveAs(fn + '.root')

    pre = write(52, 0.037, 0.145, 0.785, 'Preliminary')
    c.SaveAs(fn + '_prelim.pdf')
    c.SaveAs(fn + '_prelim.png')
    c.SaveAs(fn + '_prelim.root')

    del c

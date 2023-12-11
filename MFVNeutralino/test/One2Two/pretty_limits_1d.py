import sys, os
from array import array
from JMTucker.Tools.ROOTTools import *
ROOT.gErrorIgnoreLevel = 1001 # Suppress TCanvas::SaveAs messages.

which = '2017p8' if '2017p8' in sys.argv else 'run2'
intlumi = 140 if which == 'run2' else 101
path = plot_dir('pretty_limits_1d_DarkSectorReview_redux_%s' % which, make=True)

ts = tdr_style()

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

f = ROOT.TFile('limits_1d_%s.root' % which)

kinds = [
    #'splitSUSY_M2400_100'
    #'multijet_M0800',
    #'multijet_M1600',
    #'multijet_M2400',
    #'multijet_M3000',
    #'multijet_tau300um',
    #'multijet_tau1mm',
    #'multijet_tau10mm',
    #'dijet_M0800',
    #'dijet_M1600',
    #'dijet_M2400',
    #'dijet_M3000',
    #'dijet_tau300um',
    #'dijet_tau1mm',
    #'dijet_tau10mm',
    'HtoLLPto4j_M1000_450',
    'HtoLLPto4j_M1000_100',
    'HtoLLPto4j_M400_150', 
    'HtoLLPto4j_M600_250', 
    'HtoLLPto4j_M600_60',  
    'HtoLLPto4j_M800_350', 
    'HtoLLPto4j_M800_80',  
    'HtoLLPto4b_M1000_450',
    'HtoLLPto4b_M1000_100',
    'HtoLLPto4b_M400_150', 
    'HtoLLPto4b_M600_250', 
    'HtoLLPto4b_M800_350', 
    'HtoLLPto4b_M800_80',  
    'ZprimetoLLPto4j_M1000_100',
    'ZprimetoLLPto4j_M1000_450',
    'ZprimetoLLPto4j_M1500_150',
    'ZprimetoLLPto4j_M1500_700',
    'ZprimetoLLPto4j_M2000_200',
    'ZprimetoLLPto4j_M2000_950',
    'ZprimetoLLPto4j_M2500_1200',
    'ZprimetoLLPto4j_M2500_250',
    'ZprimetoLLPto4j_M3000_1450',
    'ZprimetoLLPto4j_M3000_300',
    'ZprimetoLLPto4j_M3500_1700',
    'ZprimetoLLPto4j_M3500_350',
    'ZprimetoLLPto4j_M4000_1950',
    'ZprimetoLLPto4j_M4000_400',
    'ZprimetoLLPto4j_M4500_2200',
    'ZprimetoLLPto4j_M4500_450',
    'ZprimetoLLPto4b_M1000_100',
    'ZprimetoLLPto4b_M1000_450',
    'ZprimetoLLPto4b_M1500_150',
    'ZprimetoLLPto4b_M1500_700',
    'ZprimetoLLPto4b_M2000_200',
    'ZprimetoLLPto4b_M2000_950',
    'ZprimetoLLPto4b_M2500_1200',
    'ZprimetoLLPto4b_M2500_250',
    'ZprimetoLLPto4b_M3000_1450',
    'ZprimetoLLPto4b_M3000_300',
    'ZprimetoLLPto4b_M3500_1700',
    'ZprimetoLLPto4b_M3500_350',
    'ZprimetoLLPto4b_M4000_1950',
    'ZprimetoLLPto4b_M4000_400',
    'ZprimetoLLPto4b_M4500_2200',
    'ZprimetoLLPto4b_M4500_450',
    ]

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
        return '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs', 'm = %i GeV' % int(kind.replace('multijet_M', ''))
    elif kind.startswith('dijet_M'):
        return '#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}', 'm = %i GeV' % int(kind.replace('dijet_M', ''))
    elif kind.startswith('multijet_tau'):
        return '#tilde{#chi}^{0}/#tilde{g} #rightarrow tbs', 'c#tau = ' + tau(kind.replace('multijet_tau', ''))
    elif kind.startswith('dijet_tau'):
        return '#tilde{t} #rightarrow #bar{d}#kern[0.1]{#bar{d}}', 'c#tau = ' + tau(kind.replace('dijet_tau', ''))
    elif kind.startswith('splitSUSY_M'):
        masses = (kind.replace('splitSUSY_M', '')).split("_")
        return 'splitSUSY #tilde{g} #rightarrow qq#tilde{#chi}, m(#tilde{g}) = %i GeV, m(#tilde{#chi}) = %i GeV' % (int(masses[0]),int(masses[1]))
    elif kind.startswith('HtoLLPto4j') :
        masses = (kind.replace('HtoLLPto4j_M', '')).split("_")
        return 'H #rightarrow XX #rightarrow 4j', 'm(H) = %i GeV, m(X) = %i GeV' % (int(masses[0]),int(masses[1]))
    elif kind.startswith('HtoLLPto4b') :
        masses = (kind.replace('HtoLLPto4b_M', '')).split("_")
        return 'H #rightarrow XX #rightarrow 4b', 'm(H) = %i GeV, m(X) = %i GeV' % (int(masses[0]),int(masses[1]))
    elif kind.startswith('ZprimetoLLPto4j') :
        masses = (kind.replace('ZprimetoLLPto4j_M', '')).split("_")
        return 'Z\' #rightarrow XX #rightarrow 4j', 'm(Z\') = %i GeV, m(X) = %i GeV' % (int(masses[0]),int(masses[1]))
    elif kind.startswith('ZprimetoLLPto4b') :
        masses = (kind.replace('ZprimetoLLPto4b_M', '')).split("_")
        return 'Z\' #rightarrow XX #rightarrow 4b', 'm(Z\') = %i GeV, m(X) = %i GeV' % (int(masses[0]),int(masses[1]))

def nice_theory(kind, idx=1):
    if kind.startswith('multijet') and idx == 1:
        return '#tilde{g}#tilde{g} production'
    elif kind.startswith('multijet') and idx == 2:
        return '#tilde{#chi}^{0}#tilde{#chi}^{0} production'
    elif kind.startswith('dijet'):
        return '#tilde{t}#kern[0.9]{#tilde{t}}* production'
    elif kind.startswith('splitSUSY'):
        return '#tilde{g}#tilde{g} production'
    else :
        return ''

for kind in kinds:
    print kind
    versus_tau = "_M" in kind
    versus_mass = 'tau' in kind
    assert int(versus_tau) + int(versus_mass) == 1

    c = ROOT.TCanvas('c', '', 800, 800)
    c.SetLogy()
    versus_tau = "_M" in kind
    if versus_tau :
        c.SetLogx()
    c.SetTopMargin(0.1)
    c.SetBottomMargin(0.12)
    c.SetLeftMargin(0.125)
    c.SetRightMargin(0.085)

    observed = f.Get('%s/observed' % kind)
    expect50 = f.Get('%s/expect50' % kind)
    expect68 = f.Get('%s/expect68' % kind)
    expect95 = f.Get('%s/expect95' % kind)
    theory = f.Get('%s/theory' % kind)

    # in case we want two theory curves on one limit plot
    theory2 = None

    if kind.startswith('multijet'):
        theory2 = f.Get('%s/theory2' % kind)

    if 0:
        if which == 'run2':
            for kk,vv in ('dijet_M0800',1.7),('dijet_M1600',0.9),('dijet_M2400',0.7),('dijet_M3000',0.7),('multijet_M0800',2.2),('multijet_M1600',1.2),('multijet_M2400',1),('multijet_M3000',1.3):
                if kind == kk:
                    for i in xrange(20): print 'ugh', which, kind
                    g = expect95
                    x,y = tgraph_getpoint(g, 0)
                    assert abs(x - 0.1) < 1e-4
                    g.SetPointEYlow(0,vv)
            if kind == 'dijet_M3000':
                for i in xrange(20): print 'ugh', which, kind
                g = expect95
                x,y = tgraph_getpoint(g, 11)
                print x,y
                assert abs(x - 28) < 1e-3
                g.SetPointEYhigh(11,0.009)
            if kind == 'dijet_M3000':
                for i in xrange(20): print 'ugh', which, kind
                g = expect95
                x,y = tgraph_getpoint(g, 1)
                assert abs(x - 0.3) < 1e-4
                g.SetPointEYlow(1,0.12)
            if kind == 'multijet_M2400':
                for i in xrange(20): print 'ugh', which, kind
                g = expect95
                x,y = tgraph_getpoint(g, 1)
                assert abs(x - 0.3) < 1e-4
                g.SetPointEYlow(1,0.15)
            if kind == 'multijet_M3000':
                for i in xrange(20): print 'ugh', which, kind
                g = expect95
                x,y = tgraph_getpoint(g, 1)
                assert abs(x - 0.3) < 1e-4
                g.SetPointEYlow(1,0.181)
            if kind == 'multijet_tau300um':
                for i in xrange(20): print 'ugh', which, kind
                g = expect95
                #x,y = tgraph_getpoint(g, g.GetN()-1)
                #assert abs(x - 0.3) < 1e-4
                for jjj in 1,2,3:
                    g.SetPointEYlow(g.GetN()-jjj,0.18+1e-3*jjj)

    if       'dijet' in kind : particle = '#tilde{t}'
    elif  'multijet' in kind : particle = '#tilde{#chi}^{0} / #tilde{g}'
    elif 'splitSUSY' in kind : particle = '#tilde{g}'
    else : particle = 'X'
    if versus_mass:
        xtitle = 'm_{%s} (GeV)' % particle
    elif versus_tau:
        xtitle = 'c#tau_{%s} (mm)' % particle
        
    g = expect95
    g.SetTitle(';%s;#sigma#bf{#it{#Beta}}^{2} (fb)    ' % xtitle)
    g.Draw('A3')

#    draw_theory = 'tau' in kind

    xax = g.GetXaxis()
    xax.SetNoExponent()
    xax.SetLabelSize(0.045)
    xax.SetTitleSize(0.05)
    if versus_tau:
        xax.SetLabelOffset(0.002)
    xax.SetTitleOffset(1.1)
    yax = g.GetYaxis()
    yax.SetTitleOffset(1.18)
    yax.SetTitleSize(0.05)
    yax.SetLabelSize(0.045)

    if versus_mass:
        xax.SetLimits(105, 3200)
        yax.SetRangeUser(0.01, 100000 if versus_tau else 130) #(versus_tau and draw_theory) else 130)
    elif versus_tau:
        if 'splitSUSY' in kind or 'HtoLLP' in kind or 'ZprimetoLLP' in kind :
            xax.SetLimits(0.068, 1.3e4)
            yax.SetRangeUser(0.01, 100000 if versus_tau else 130) #(versus_tau and draw_theory) else 130)
        else :
            xax.SetLimits(0.068, 130)
            yax.SetRangeUser(0.001, 100000 if versus_tau else 130) #(versus_tau and draw_theory) else 130)

    observed.SetLineWidth(2)
    expect50.SetLineWidth(2)
    expect50.SetLineStyle(2)

    if theory :
        theory.SetLineWidth(2)
        if kind.startswith('multijet'):
            theory_color = 9
            theory2_color = 96
        elif kind.startswith('dijet'):
            theory_color = 46
        elif kind.startswith('splitSUSY'):
            theory_color = ROOT.kBlue+3
        theory.SetLineColor(theory_color)
        theory.SetFillColorAlpha(theory_color, 0.5)

        if theory2 :
            theory2.SetLineWidth(2)
            theory2.SetLineColor(theory2_color)
            theory2.SetFillColorAlpha(theory2_color, 0.5)

    expect95.SetLineColor(ROOT.kOrange)
    expect68.SetLineColor(ROOT.kGreen+1)
    expect95.SetFillColor(ROOT.kOrange)
    expect68.SetFillColor(ROOT.kGreen+1)

    expect95.Draw('3')
    expect68.Draw('3')
#    if draw_theory:
#        theory.Draw('L3')
    if theory :
        theory.Draw('L3')
        if theory2 :
            theory2.Draw('L3')
    expect50.Draw('L')
    observed.Draw('L')

#    if draw_theory:
#        leg = ROOT.TLegend(0.552, 0.563, 0.870, 0.867)
#    else:
#        leg = ROOT.TLegend(0.552, 0.603, 0.870, 0.867)

    xoffset = 0.015
    if kind == 'multijet_M0800' :
        yoffset = -0.15
        leg = ROOT.TLegend(0.567+xoffset, 0.565+yoffset, 0.870+xoffset, 0.869+yoffset)
    else :
        leg = ROOT.TLegend(0.567+xoffset, 0.765, 0.870+xoffset, 0.869)
    leg.SetTextFont(42)
    leg.SetFillColor(ROOT.kWhite)
    leg.SetBorderSize(0)
    leg.AddEntry(0, '#kern[-0.22]{95% CL upper limits:}', '')
    leg.AddEntry(observed, 'Observed', 'L')
    leg.AddEntry(expect50, 'Median expected', 'L')
    leg.AddEntry(expect68, '68% expected', 'F')
    leg.AddEntry(expect95, '95% expected', 'F')
    if theory :
    #    if draw_theory:
    #        leg.AddEntry(theory, nice_theory(kind) + ', #bf{#it{#Beta}}=1', 'LF')
        leg.AddEntry(theory, nice_theory(kind) + ', #bf{#it{#Beta}}=1', 'LF')
        if theory2 :
            leg.AddEntry(theory2, nice_theory(kind,2) + ', #bf{#it{#Beta}}=1', 'LF')
    leg.Draw()

    labels = nice_leg(kind)
    print labels[0], labels[1]

    if "dijet_M" in kind :
        sig_text         = write(42, 0.04, 0.17, 0.655, labels[0])
        mass_or_tau_text = write(42, 0.04, 0.17, 0.605, labels[1])
        cms = write(61, 0.050, 0.16, 0.825, 'CMS')
    elif "dijet_tau" in kind :
        sig_text         = write(42, 0.04, 0.17, 0.215, labels[0])
        mass_or_tau_text = write(42, 0.04, 0.17, 0.165, labels[1])
        cms = write(61, 0.050, 0.16, 0.825, 'CMS')
    elif "multijet_M" in kind :
        sig_text         = write(42, 0.04, 0.17, 0.655, labels[0])
        mass_or_tau_text = write(42, 0.04, 0.17, 0.605, labels[1])
        cms = write(61, 0.050, 0.16, 0.825, 'CMS')
    else : # "multijet_tau"
        sig_text         = write(42, 0.04, 0.155, 0.20, labels[0])
        mass_or_tau_text = write(42, 0.04, 0.155, 0.15, labels[1])
        cms = write(61, 0.050, 0.16, 0.825, 'CMS')

    lum = write(42, 0.050, 0.563, 0.913, '%s fb^{-1} (13 TeV)' % intlumi)
    fn = os.path.join(path, 'limit1d_' + kind)
    #c.SaveAs(fn + '.pdf')
    #c.SaveAs(fn + '.png')
    #c.SaveAs(fn + '.root')

    if "_M" in kind or 'dijet' in kind :
        pre = write(52, 0.047, 0.265, 0.825, 'Preliminary')
    else :
        pre = write(52, 0.047, 0.230, 0.913, 'Preliminary')

    c.SaveAs(fn + '_prelim.pdf')
    c.SaveAs(fn + '_prelim.png')
    c.SaveAs(fn + '_prelim.root')

    del c

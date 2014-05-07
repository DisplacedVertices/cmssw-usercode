#!/usr/bin/env python

from array import array
from JMTucker.Tools.ROOTTools import *
set_style()
ps = plot_saver('plots/dummylimits')

def fmt(t, title, color):
    t.SetFillColor(color)
    t.SetTitle('%s;mass (GeV);#sigma #times BR (pb)' % title)
    return t

def tge(xye, title, color):
    x = array('f', [z[0] for z in xye])
    y = array('f', [z[1] for z in xye])
    ey = array('f', [z[2] for z in xye])
    ex = array('f', [2.5]*len(x))
    t = ROOT.TGraphErrors(len(x), x, y, ex, ey)
    return fmt(t, title, color)

def tgae(x, y, exl, exh, eyl, eyh, title, color):
    x = array('f', x)
    y = array('f', y)
    l = len(x)
    if exl is None:
        exl = [0]*l
    exl = array('f', exl)
    if exh is None:
        exh = [0]*l
    exh = array('f', exh)
    if eyl is None:
        eyl = [0]*l
    eyl = array('f', eyl)
    if eyh is None:
        eyh = [0]*l
    eyh = array('f', eyh)
    t = ROOT.TGraphAsymmErrors(l, x, y, exl, exh, eyl, eyh)
    return fmt(t, title, color)

gluglu = [eval(x.strip()) for x in open('gluglu.csv').readlines() if x.strip()]
g_gluglu = tge(gluglu, 'hi', 9)
g_gluglu.Draw('A3')
ps.save('gluglu')

taus = [
    ('0100um', '#tau = 100 #mum'),
    ('0300um', '#tau = 300 #mum'),
    ('1000um', '#tau = 1 mm'),
    ('9900um', '#tau = 9.9 mm'),
    ]

watches = [
    'Observed Limit: r < ',
    'Expected  2.5%: r < ',
    'Expected 16.0%: r < ',
    'Expected 50.0%: r < ',
    'Expected 84.0%: r < ',
    'Expected 97.5%: r < ',
    ]

for tau, tau_nice in taus:
    if tau == '0100um':
        masses = [600, 800, 1000]
    else:
        masses = [200, 300, 400, 600, 800, 1000]
    observed = []
    expect50 = []
    expect68 = []
    expect68lo = []
    expect68hi = []
    expect95 = []
    expect95lo = []
    expect95hi = []

    for mass in masses:
        fn = '/uscms/home/tucker/private/higgscombine_611/src/HiggsAnalysis/CombinedLimit/data/tutorials/out/mfv_neutralino_tau%s_M%04i_scaled.txt.output' % (tau, mass)
        vals = [None]*6

        for line in open(fn):
            for i, watch in enumerate(watches):
                if line.startswith(watch):
                    vals[i] = float(line.replace(watch, ''))/1000.

        if any(v is None for v in vals):
            print vals
            raise 'crap'

        obs, exp2p5, exp16, exp50, exp84, exp97p5 = vals

        observed.append(obs)
        expect50.append(exp50)
        exp68 = (exp84 + exp16)/2
        expect68.append(exp68)
        expect68lo.append(exp68 - exp16)
        expect68hi.append(exp84 - exp68)
        exp95 = (exp97p5 + exp2p5)/2
        expect95.append(exp95)
        expect95lo.append(exp95 - exp2p5)
        expect95hi.append(exp97p5 - exp95)

    g_expect95 = tgae(masses, expect95, None, None, expect95lo, expect95hi, tau_nice, 5)
    g_expect95.Draw('A3')

    g_expect68 = tgae(masses, expect68, None, None, expect68lo, expect68hi, tau_nice, 3)
    g_expect68.Draw('3')

    g_expect50 = tgae(masses, expect50, None, None, None, None, tau_nice, 1)
    g_expect50.SetLineStyle(2)
    g_expect50.Draw('L')

    g_observed = tgae(masses, observed, None, None, None, None, tau_nice, 1)
    g_observed.SetMarkerStyle(20)
    g_observed.SetMarkerSize(1.2)
    g_observed.Draw('LP')

    g_gluglu.SetFillStyle(3001)
    g_gluglu.Draw('3')

    leg = ROOT.TLegend(0.734, 0.716, 0.990, 0.988)
    leg.AddEntry(g_observed, 'Obs. limit', 'L')
    leg.AddEntry(g_expect50, 'Exp. limit', 'L')
    leg.AddEntry(g_expect68, 'Exp. #pm 1 #sigma', 'F')
    leg.AddEntry(g_expect95, 'Exp. #pm 2 #sigma', 'F')
    leg.AddEntry(g_gluglu,   'NLO + NLL #tilde{g} #tilde{g} production', 'F')
    leg.Draw()
    
    ps.save('tau%s' % tau)

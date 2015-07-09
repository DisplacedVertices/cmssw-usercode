#!/usr/bin/env python

from array import array
from collections import defaultdict
from JMTucker.Tools.ROOTTools import *

set_style()
ps = plot_saver('/uscms/home/tucker/asdf/plots/mfvlimits_test', log=False, size=(600,600))

which = 'v10p1'
draw_gluglu = True

def fmt(t, title, color):
    t.SetFillColor(color)
    t.SetTitle('%s;neutralino mass (GeV);#sigma #times BR (fb)' % title)
    return t

def tge(xye, title, color):
    x = array('f', [z[0] for z in xye])
    y = array('f', [z[1] for z in xye])
    ey = array('f', [z[2] for z in xye])
    ex = array('f', [2.5]*len(x))
    t = ROOT.TGraphErrors(len(x), x, y, ex, ey)
    return fmt(t, title, color)

def tgae(x, y, exl, exh, eyl, eyh, title, color):
    print 'tgae', len(x), len(y)
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

def make_gluglu():
    gluglu = [eval(x.strip()) for x in open('/afs/fnal.gov/files/home/room3/tucker/gluglu.csv').readlines() if x.strip()]
    gluglu = [(z[0], z[1]*1000, z[2]/100*z[1]*1000) for z in gluglu] # convert pb to fb and percent to absolute
    return tge(gluglu, 'hi', 9)

def parse(d, tau0, mass, observed_fn, expected_fn):
    watches = [
        'sigma_sig_limit:Observed Limit: r < ',
        'sigma_sig_limit:Expected  2.5%: r < ',
        'sigma_sig_limit:Expected 16.0%: r < ',
        'sigma_sig_limit:Expected 50.0%: r < ',
        'sigma_sig_limit:Expected 84.0%: r < ',
        'sigma_sig_limit:Expected 97.5%: r < ',
        ]

    vals = [None]*6

    for line in open(expected_fn):
        for i, watch in enumerate(watches):
            if line.startswith(watch):
                vals[i] = float(line.replace(watch, ''))
    for line in open(observed_fn):
        watch = watches[0]
        if line.startswith(watch):
            vals[0] = float(line.replace(watch, ''))
    print vals
    if any(v is None for v in vals):
        raise ValueError('crap')

    obs, exp2p5, exp16, exp50, exp84, exp97p5 = vals
    exp68 = (exp84 + exp16)/2
    exp95 = (exp97p5 + exp2p5)/2
    d['tau0'].append(tau0)
    d['mass'].append(mass)
    d['observed'].append(obs)
    d['expect50'].append(exp50)
    d['expect68'].append(exp68)
    d['expect95'].append(exp95)
    d['expect68lo'].append(exp68 - exp16)
    d['expect68hi'].append(exp84 - exp68)
    d['expect95lo'].append(exp95 - exp2p5)
    d['expect95hi'].append(exp97p5 - exp95)

def make_plot(d, name, title, y_range):
    if y_range is None:
        m = 0
        for k,vs in d.iteritems():
            if k == 'tau0' or k == 'mass':
                continue
            for v in vs:
                m = max(m, v)
        y_range = m * 2

    g_observed = tgae(d['mass'], d['observed'], None, None, None, None, title, 1)
    g_observed.SetMarkerStyle(20)
    g_observed.SetMarkerSize(1.2)
    g_observed.Draw('ALP')
    g_observed.GetYaxis().SetRangeUser(0, y_range)

    g_expect95 = tgae(d['mass'], d['expect95'], None, None, d['expect95lo'], d['expect95hi'], title, 5)
    g_expect95.Draw('3')

    g_expect68 = tgae(d['mass'], d['expect68'], None, None, d['expect68lo'], d['expect68hi'], title, 3)
    g_expect68.Draw('3')

    g_expect50 = tgae(d['mass'], d['expect50'], None, None, None, None, title, 1)
    g_expect50.SetLineStyle(2)
    g_expect50.Draw('L')

    g_observed.Draw('LP')

    if draw_gluglu:
        g_gluglu.SetFillStyle(3001)
        g_gluglu.Draw('3')

    leg = ROOT.TLegend(0.734, 0.716, 0.990, 0.988)
    leg.AddEntry(g_observed, 'Obs. limit', 'L')
    leg.AddEntry(g_expect50, 'Exp. limit', 'L')
    leg.AddEntry(g_expect68, 'Exp. #pm 1 #sigma', 'F')
    leg.AddEntry(g_expect95, 'Exp. #pm 2 #sigma', 'F')
    if draw_gluglu:
        leg.AddEntry(g_gluglu, 'NLO + NLL #tilde{g} #tilde{g} production', 'F')
    leg.Draw()
    
    ps.save(name)

####

if draw_gluglu:
    g_gluglu = make_gluglu()
    g_gluglu.Draw('A3')
    ps.save('gluglu', log=True)

def old_plots():
    tau0s = [
        ('0100um', '#tau = 100 #mum'),
        ('0300um', '#tau = 300 #mum'),
        ('1000um', '#tau = 1 mm'),
        ('9900um', '#tau = 10 mm'),
        ]

    masses = [200, 300, 400, 600, 800, 1000]

    nn = -1
    for tau0, tau0_nice in tau0s:
        if tau0 == '0100um': # or tau0 == '0300um':
            print 'skip', tau0
            nn -= len(masses)
            continue

        d = defaultdict(list)

        for mass in masses:
            if mass == 200:
                print 'skip', tau0, mass
                nn -= 1
                continue
            observed_fn = 'crab/One2Two_v10p1/lsts/%s_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-1_Sam.out' % (which, nn, nn)
            expected_fn = 'crab/One2Two_v10p1/lsts/%s_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-2_Sam.out' % (which, nn, nn)
            #observed_fn = 'combine/combine_n%ix-1.out' % nn
            #expected_fn = 'combine/combine_n%ix-2.out' % nn
            print nn, tau0, mass, observed_fn, expected_fn
            nn -= 1

            parse(d, tau0, mass, observed_fn, expected_fn)

        make_plot(d, tau0, tau0_nice, 50 if tau0 == '0300um' else (9 if tau0 == '1000um' else 4))

def new_plots():
    import bigsigscan as bss

    z = [

        ('00300um', '#tau = 300 #mum', 60, 
         [
          ('00300um', m,
           'crab3/One2Two/tau00300um/lsts/tau00300um_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-1_Sam.limits.out' % (i,i),
           'crab3/One2Two/tau00300um/lsts/tau00300um_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-2_Sam.limits.out' % (i,i)
           ) for m,i in zip(bss.masses, bss.tau2range[300])
          ]
         ),
     
        ('tau01000um', '#tau = 1 mm', 6,
         [
          ('01000um', m,
           'crab3/One2Two/tau01000um/lsts/tau01000um_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-1_Sam.limits.out' % (i,i),
           'crab3/One2Two/tau01000um/lsts/tau01000um_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-2_Sam.limits.out' % (i,i)
           ) for m,i in zip(bss.masses, bss.tau2range[1000])
          ]
         ),

        ('tau10000um', '#tau = 10 mm', 3,
         [
          ('10000um', m,
           'crab3/One2Two/tau10000um/lsts/tau10000um_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-1_Sam.limits.out' % (i,i),
           'crab3/One2Two/tau10000um/lsts/tau10000um_TmpCJ_Ntk5_SigTmp%i_SigSamn%ix-2_Sam.limits.out' % (i,i)
           ) for m,i in zip(bss.masses, bss.tau2range[10000])
          ]
         ),

        ]

    #print z

    for name, title, y_range, parse_args in z:
        d = defaultdict(list)
        for x in parse_args:
            parse(d, *x)
        make_plot(d, name, title, None)
    
#old_plots()

new_plots()

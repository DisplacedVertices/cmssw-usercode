#!/usr/bin/env python

from array import array
from collections import defaultdict
from JMTucker.Tools.ROOTTools import *

set_style()
rainbow_palette()
ps = plot_saver('/uscms/home/tucker/asdf/plots/mfvlimits_test_3', log=False, size=(600,600))

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

def parse_gluglu():
    gluglu = [eval(x.strip()) for x in open('/afs/fnal.gov/files/home/room3/tucker/gluglu.csv').readlines() if x.strip()]
    gluglu = [(z[0], z[1]*1000, z[2]/100*z[1]*1000) for z in gluglu] # convert pb to fb and percent to absolute
    return gluglu

def make_gluglu():
    return tge(parse_gluglu(), 'hi', 9)

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

    do_obs = observed_fn is not None
    do_exp = expected_fn is not None

    if do_exp:
        for line in open(expected_fn):
            for i, watch in enumerate(watches):
                if line.startswith(watch):
                    vals[i] = float(line.replace(watch, ''))
    if do_obs:
        for line in open(observed_fn):
            watch = watches[0]
            if line.startswith(watch):
                vals[0] = float(line.replace(watch, ''))
    else:
        vals[0] = None # in case it was found in exp above
    print vals
    if (do_obs and vals[0] is None) or (do_exp and any(v is None for v in vals[1:])):
        raise ValueError('crap')

    obs, exp2p5, exp16, exp50, exp84, exp97p5 = vals
    d['tau0'].append(tau0)
    d['mass'].append(mass)
    if do_obs:
        d['observed'].append(obs)
    if do_exp:
        exp68 = (exp84 + exp16)/2
        exp95 = (exp97p5 + exp2p5)/2
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

    z = []

    outs = {-1: {}, -2: {}}
    for line in open('crab3/One2Two/allouts'):
        line = line.strip()
        if line:
            x = line.split('SigSamn')[1].split('_Sam')[0].split('x')
            num, kind = int(x[0]), int(x[1])
            outs[kind][num] = 'crab3/One2Two/' + line

    if False:
        for tau0 in sorted(bss.tau2range.keys()):
            rng = bss.tau2range[tau0]
            name = 'tau%05ium' % tau0
            if tau0 / 1000 >= 1:
                title = '#tau = %i mm' % (tau0 / 1000)
            else:
                title = '#tau = %i #mum' % tau0
            y_range = None
            outs_m1 = outs[-1].get(i, None)
            outs_m2 = outs[-2].get(i, None)
            these_outs = [(i, outs[-1].get(i, None), outs[-2].get(i, None)) for i in bss.tau2range[tau0]]
            nones = [(i,x,y) for i,x,y in these_outs if x is None or y is None]
            if nones:
                print 'skipping %s, missing %r' % (name, nones)
            else:
                parse_args = [(name.replace('tau', ''), m, x, y) for m,(i,x,y) in zip(bss.masses, these_outs)]
                z.append((name, title, y_range, parse_args))
    elif True:
        for kind in (-1, -2):
            h = bss.book('hm%i' % abs(kind), str(kind))

            for num, out in outs[kind].iteritems():
                tau0 = bss.num2tau[num]
                mass = bss.num2mass[num]
                d = defaultdict(list)
                parse(d, tau0, mass,
                      out if kind is -1 else None, 
                      out if kind is -2 else None)
                val = (d['observed'] if kind == -1 else d['expect50'])[0]
                h.SetBinContent(h.FindBin(mass, tau0), val)

            h.Draw('colz')
            ps.save(h.GetName(), log=True, logz=True)

    for name, title, y_range, parse_args in z:
        print name
        d = defaultdict(list)
        for x in parse_args:
            parse(d, *x)
        make_plot(d, name, title, y_range)

def get_2d_plot(fn = '/uscms/home/tucker/asdf/plots/mfvlimits_test/hm1.root'):
    f = ROOT.TFile(fn)
    h = f.Get('c0').FindObject('hm1').Clone()
    h.SetDirectory(0)
    f.Close()
    ps.c.cd()
    return h

def book_interp(name):
    hint = ROOT.TH2F(name, '', 1200, 300, 1500, 319, 100, 32000)
    hint.SetStats(0)
    return hint

def interpolate():
    h = get_2d_plot()
    hint = book_interp('hint')
    xax = hint.GetXaxis()
    yax = hint.GetYaxis()
    for ix in xrange(1, hint.GetNbinsX()+1):
        x = xax.GetBinLowEdge(ix)
        for iy in xrange(1, hint.GetNbinsY()+1):
            y = yax.GetBinLowEdge(iy)
            hint.SetBinContent(ix, iy, h.Interpolate(x,y))
    return hint

def duh():
    import bigsigscan as bss

    gluglu = parse_gluglu()
    hgluxsec = ROOT.TH1F('hgluxsec', '', 361, 200, 2005)
    for m,s,se in gluglu:
        bin = hgluxsec.FindBin(m)
        hgluxsec.SetBinContent(bin, s)
        hgluxsec.SetBinError(bin, se)

    gluglu = dict((m, (s, es)) for m, s, es in gluglu)

    h = interpolate() # get_2d_plot()
    h.Draw('colz')
    ps.save('hint')

    hexc = book_interp('hexc')
    hexc.SetStats(0)

    for ix in xrange(1, h.GetNbinsX()+1):
        mass = h.GetXaxis().GetBinLowEdge(ix)
        for iy in xrange(1, h.GetNbinsY()+1):
            tau0 = h.GetYaxis().GetBinLowEdge(iy)
            lim = h.GetBinContent(ix, iy)

            bin = hgluxsec.FindBin(mass)
            s = hgluxsec.Interpolate(mass)
            se = (hgluxsec.GetBinError(bin)**2 + hgluxsec.GetBinError(bin+1)**2)**0.5
            #print tau0, mass, lim, s, se

            bin = hexc.FindBin(mass, tau0)
            if lim < s - se:
                hexc.SetBinContent(bin, 1)
            else:
                hexc.SetBinContent(bin, 0)

    hexc.Draw('cont2')
    ps.save('hexc')

#    img = ROOT.TImage.Open('Image.png')
#    img.Draw('x')

#    hexc.Draw('colz')
#    ps.save('haha')
    
#             //Create a transparent pad filling the full canvas
#          TPad *p = new TPad("p","p",0,0,1,1)
#          p->SetFillStyle(4000)
#          p->SetFrameFillStyle(4000)
#          p->Draw()
#          p->cd()
#          TH1F *h = new TH1F("h","test",100,-3,3)
#          h->SetFillColor(kCyan)
#          h->FillRandom("gaus",5000)
#          h->Draw()
#       }


#old_plots()

#new_plots()

#interpolate()
duh()

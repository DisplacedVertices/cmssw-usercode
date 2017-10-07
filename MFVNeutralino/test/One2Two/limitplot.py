#!/usr/bin/env python

from array import array
from collections import defaultdict
from itertools import izip
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import from_pickle
from limits_input import sample_iterator

def fmt(t, title, xtitle, color):
    t.SetFillColor(color)
    t.SetTitle('%s;%s;#sigma #times BR^{2} (fb)' % (title, xtitle))
    return t

def tge(xye, title, xtitle, color):
    x = array('f', [z[0] for z in xye])
    y = array('f', [z[1] for z in xye])
    ey = array('f', [z[2] for z in xye])
    ex = array('f', [2.5]*len(x))
    t = ROOT.TGraphErrors(len(x), x, y, ex, ey)
    return fmt(t, title, xtitle, color)

def tgae(x, y, exl, exh, eyl, eyh, title, xtitle, color):
    #print 'tgae', len(x), len(y)
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
    return fmt(t, title, xtitle, color)

def parse_gluglu():
    gluglu = [eval(x.strip()) for x in open('gluglu.csv') if x.strip()]
    gluglu = [(z[0], z[1]*1000, z[2]/100*z[1]*1000) for z in gluglu] # convert pb to fb and percent to absolute
    return gluglu

def make_gluglu():
    return tge(parse_gluglu(), '13 TeV glu-glu production', 'mass (GeV)', 9)

def draw_gluglu():
    g_gluglu = make_gluglu()
    g_gluglu.Draw('A3')

def make_gluglu_hist():
    gluglu = parse_gluglu()
    hgluxsec = ROOT.TH1F('hgluxsec', '', 561, 200, 3005)
    for m,s,se in gluglu:
        bin = hgluxsec.FindBin(m)
        hgluxsec.SetBinContent(bin, s)
        hgluxsec.SetBinError(bin, se)
    return gluglu, hgluxsec
    
def parse(d, tau, mass, observed_fn, expected_fn):
    #print d, tau, mass, observed_fn, expected_fn
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
    #print vals
    if (do_obs and vals[0] is None) or (do_exp and any(v is None for v in vals[1:])):
        raise ValueError('crap')

    obs, exp2p5, exp16, exp50, exp84, exp97p5 = vals
    d['tau'].append(tau)
    d['mass'].append(mass)
    if do_obs:
        d['observed'].append(obs)
    if do_exp:
        exp68 = (exp84 + exp16)/2
        exp95 = (exp97p5 + exp2p5)/2
        d['expect2p5'].append(exp2p5)
        d['expect16'].append(exp16)
        d['expect50'].append(exp50)
        d['expect68'].append(exp68)
        d['expect84'].append(exp84)
        d['expect95'].append(exp95)
        d['expect97p5'].append(exp97p5)
        d['expect68lo'].append(exp68 - exp16)
        d['expect68hi'].append(exp84 - exp68)
        d['expect95lo'].append(exp95 - exp2p5)
        d['expect95hi'].append(exp97p5 - exp95)

def draw_1d_plot(d, name, title, y_range, xkey='mass'):
    if xkey == 'mass':
        xtitle = 'mass (GeV)'
    else:
        xtitle = 'lifetime (#mum)'

    g_observed = tgae(d[xkey], d['observed'], None, None, None, None, title, xtitle, 1)
    g_observed.SetMarkerStyle(20)
    g_observed.SetMarkerSize(1.2)
    g_observed.Draw('ALP')
    g_observed.GetYaxis().SetRangeUser(*y_range)

    g_expect95 = tgae(d[xkey], d['expect95'], None, None, d['expect95lo'], d['expect95hi'], title, xtitle, 5)
    g_expect95.Draw('3')

    g_expect68 = tgae(d[xkey], d['expect68'], None, None, d['expect68lo'], d['expect68hi'], title, xtitle, 3)
    g_expect68.Draw('3')

    g_expect50 = tgae(d[xkey], d['expect50'], None, None, None, None, title, xtitle, 1)
    g_expect50.SetLineStyle(2)
    g_expect50.Draw('L')

    g_observed.Draw('LP')

    draw_gluglu = xkey == 'mass'
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

def do_1d_plots():
    xxx = [
        (lambda s: 'neu' in sample.name and sample.mass == 800,  'multijetM800',   '', (0.01, 50), 'tau'),
        (lambda s: 'neu' in sample.name and sample.tau  == 1., 'multijettau1mm', '', (0.01, 50), 'mass'),
        (lambda s: 'ddbar' in sample.name and sample.mass == 800,  'ddbarM800',   '', (0.01, 50), 'tau'),
        (lambda s: 'ddbar' in sample.name and sample.tau  == 1., 'ddbartau1mm', '', (0.01, 50), 'mass'),
        ]
    
    f = ROOT.TFile('limits_input.root')
    for use, name, nice, y_range, xkey in xxx:
        d = defaultdict(list)
        for sample in sample_iterator(f):
            if use(sample):
                fn = 'combine_output/signal_%05i/results' % sample.isample
                parse(d, sample.tau, sample.mass, fn, fn)
        draw_1d_plot(d, name, nice, y_range, xkey)

def interpolate(h):
    # R + akima does a better job so don't use this
    hint = ROOT.TH2D(h.GetName() + '_interp', '', 2900, 300, 3200, 399, 0.1, 40)
    hint.SetStats(0)
    xax = hint.GetXaxis()
    yax = hint.GetYaxis()
    for ix in xrange(1, hint.GetNbinsX()+1):
        x = xax.GetBinLowEdge(ix)
        for iy in xrange(1, hint.GetNbinsY()+1):
            y = yax.GetBinLowEdge(iy)
            hint.SetBinContent(ix, iy, h.Interpolate(x,y))
    return hint

def save_2d_plots():
    in_f = ROOT.TFile('limits_input.root')
    out_f = ROOT.TFile('limits.root', 'recreate')

    for kind in 'mfv_ddbar', 'mfv_neu':
        d = defaultdict(list)
        for sample in sample_iterator(in_f):
            if sample.kind != kind:
                continue

            fn = 'combine_output/signal_%05i/results' % sample.isample
            try:
                parse(d, sample.tau, sample.mass, fn, fn)
            except ValueError:
                print "can't parse", sample.name, sample.isample

        def axisize(l):
            l = sorted(set(l))
            delta = l[-1] - l[-2]
            l.append(l[-1] + delta)
            return to_array(l)

        taus, masses = axisize(d['tau']), axisize(d['mass'])

        out_f.mkdir(kind).cd()

        for x in d:
            if x == 'tau' or x == 'mass':
                continue

            h = ROOT.TH2D(x, '', len(masses)-1, masses, len(taus)-1, taus)
            h.SetStats(0)
            for t,m,v in izip(d['tau'], d['mass'], d[x]):
                h.SetBinContent(h.FindBin(m,t), v)

            h.Write()

####

def gluglu_exclude(h, opt):
    gluglu, hgluglu = make_gluglu_hist()
    gluglu = dict((m, (s, es)) for m, s, es in gluglu)
    max_mass = max(gluglu.keys())

    hexc = h.Clone(h.GetName() +'_exc_%s' % opt)
    hexc.SetStats(0)

    for ix in xrange(1, h.GetNbinsX()+1):
        mass = h.GetXaxis().GetBinLowEdge(ix)
        if mass >= max_mass:
            for iy in xrange(1, h.GetNbinsY()+1):
                hexc.SetBinContent(ix,iy, 0)
            continue

        for iy in xrange(1, h.GetNbinsY()+1):
            tau = h.GetYaxis().GetBinLowEdge(iy)

            lim = h.GetBinContent(ix, iy)

            bin = hgluglu.FindBin(mass)
            assert bin < hgluglu.GetNbinsX()
            ma = hgluglu.GetBinLowEdge(bin)
            mb = hgluglu.GetBinLowEdge(bin+1)
            sa, esa = gluglu[ma]
            sb, esb = gluglu[mb]

            z = (mass - ma) / (mb - ma)
            s = sa + (sb - sa) * z
            es = (z**2 * esb**2 + (1 - z)**2 * esa**2)**0.5

            bin = hexc.FindBin(mass, tau)
            s2 = s
            if opt.lower() == 'up':
                s2 += es
            elif opt.lower() == 'dn':
                s2 -= es
            if lim < s2:
                hexc.SetBinContent(bin, 1)
            else:
                hexc.SetBinContent(bin, 0)
    return hexc

def simple_exclude():
    f = ROOT.TFile('limits.root')
    h = f.Get('observed')
    hi = gluglu_exclude(h, 'nm')
    c = ROOT.TCanvas('c', '', 800, 800)
    hi.SetMarkerStyle(20)
    hi.SetMarkerSize(1.5)
    hi.Draw('colz')
    c.SaveAs('$asdf/a.png')
    hi.GetYaxis().SetRangeUser(0.1,40)
    c.SaveAs('$asdf/asml.png')

def exc_graph(h, color, style):
    xax = h.GetXaxis()
    yax = h.GetYaxis()
    xs,ys = array('d'), array('d')
    for iy in xrange(1, h.GetNbinsY()+1):
        y = yax.GetBinLowEdge(iy)
        for ix in xrange(h.GetNbinsX(), 0, -1):
            x = xax.GetBinLowEdge(ix)
            l = h.GetBinContent(ix, iy)
            if l:
                xs.append(x)
                ys.append(y)
                #print x, y, l
                break
    g = ROOT.TGraph(len(xs), xs, ys)
    g.SetTitle(';neutralino mass (GeV);neutralino lifetime (mm)')
    g.SetLineWidth(2)
    g.SetLineColor(color)
    g.SetLineStyle(style)
    return g

def exc_graph_dumb(h, width, color, style, break_at):
    xax = h.GetXaxis()
    yax = h.GetYaxis()
    axes = [yax, xax]
    nbins = [h.GetNbinsY(), h.GetNbinsX()]
    
    gs = []

    def make_g(x0, x1, y0, y1):
        g = ROOT.TGraph(2, array('d', [x0, x1]), array('d', [y0, y1]))
        g.SetTitle(';neutralino mass (GeV);neutralino lifetime (mm)')
        g.SetLineWidth(width)
        g.SetLineColor(color)
        g.SetLineStyle(style)
        g.GetHistogram().SetMaximum(30)
        g.GetHistogram().SetMinimum(0.3)
        gs.append(g)

    for iy in xrange(1, h.GetNbinsY()+1):
        y0 = yax.GetBinLowEdge(iy)
        y1 = yax.GetBinLowEdge(iy+1)
        for ix in xrange(h.GetNbinsX()-1, 0, -1):
            l = h.GetBinContent(ix, iy)
            lm1 = h.GetBinContent(ix+1, iy)
            if l + lm1 == 1:
                x0 = x1 = xax.GetBinUpEdge(ix)
                make_g(x0, x1, y0, y1)

    for ix in xrange(1, h.GetNbinsX()+1):
        x0 = xax.GetBinLowEdge(ix)
        x1 = xax.GetBinLowEdge(ix+1)
        for iy in xrange(h.GetNbinsY()-1, 0, -1):
            l = h.GetBinContent(ix, iy)
            lm1 = h.GetBinContent(ix, iy+1)
            if l + lm1 == 1:
                y0 = y1 = yax.GetBinUpEdge(iy)
                if y0 > break_at:
                    make_g(x0, x1, y0, y1)

    return gs

def dbg_exclude():
    f = ROOT.TFile('limits.root')

    for interp in ('', '_interp'):
        c = ROOT.TCanvas('c', '', 1000, 800)

        hlim = f.Get('observed%s' % interp)

        for ix in xrange(0, hlim.GetNbinsX()+2):
            for iy in xrange(0, hlim.GetNbinsY()+2):
                hlim.SetBinContent(ix, iy, 0)
                hlim.SetBinError  (ix, iy, 0)
        hlim.Draw()

        #hexc = 
        #hexc.Draw('colz')

        gs = exc_graph_dumb(f.Get('observed%s_exc' % interp), 2, ROOT.kBlack, 1, -1) + \
             exc_graph_dumb(f.Get('expect50%s_exc' % interp), 2, ROOT.kBlue, 1, -1) + \
             exc_graph_dumb(f.Get('expect16%s_exc' % interp), 2, ROOT.kRed, 1, -1) + \
             exc_graph_dumb(f.Get('expect84%s_exc' % interp), 2, ROOT.kMagenta, 1, -1)

        for g in gs:
            g.Draw('L')

        c.SaveAs('/uscms/home/tucker/asdf/a%s.png' % interp)
        c.SaveAs('/uscms/home/tucker/asdf/a%s.root' % interp)

def to_r():
    f = ROOT.TFile('limits.root')
    print 'library(akima)'
    for x in 'observed', 'expect2p5', 'expect16', 'expect50', 'expect68', 'expect84', 'expect95', 'expect97p5':
        h = f.Get(x)
        to_ascii(h, open(h.GetName() + '.csv', 'wt'), sep=',')
        print 'h<-read.table("c:/users/tucker/desktop/%s.csv", header=TRUE, sep=",")' % x
        print 'i<-interp(x=h$x, y=h$y, z=h$z, xo=seq(300, 3000, by=1), yo=seq(0.1,40,by=0.1))'
        for a in 'xyz':
            print 'write.csv(i$%s, "c:/users/tucker/desktop/%s_%s.csv")' % (a,x,a)
        
def one_from_r(ex, name, csvs=True):
    if csvs:
        def read_csv(fn):
            lines = [x.strip() for x in open(fn).read().replace('"', '').split('\n') if x.strip()]
            lines.pop(0)
            vs = []
            for line in lines:
                ws = [float(x) for x in line.split(',')]
                ws.pop(0)
                if len(ws) == 1:
                    ws = ws[0]
                vs.append(ws)
            return vs

        x = read_csv('%s_x.csv' % ex)
        y = read_csv('%s_y.csv' % ex)
        z = read_csv('%s_z.csv' % ex)
    else:
        x,y,z = from_pickle('/uscms/home/tucker/afshome/%sxyz.gzpickle' % ex)

    assert sorted(x) == x
    assert sorted(y) == y
    nx = len(x)
    ny = len(y)
    x.append(x[-1] + (x[-1] - x[-2]))
    y.append(y[-1] + (y[-1] - y[-2]))
    #print ex, nx, ny
    x = array('d', x)
    y = array('d', y)
    h = ROOT.TH2F(name, '', len(x)-1, x, len(y)-1, y)
    h.SetStats(0)
    for ix in xrange(1, nx+1):
        for iy in xrange(1, ny+1):
            h.SetBinContent(ix, iy, z[ix-1][iy-1])
    return h

def from_r():
    f = ROOT.TFile('limits_fromr.root', 'create')
    for opt in ('nm', 'up', 'dn'):
        #for ex in 'observed expect2p5 expect16 expect50 expect68 expect84 expect95 expect97p5'.split():
        for ex in 'observed expect50'.split():
            n = '%s_fromrinterp' % ex
            h = one_from_r(ex, n)
            hexc = gluglu_exclude(h, opt)
            g = exc_graph(hexc, 1, 1, duh=True)
            g.SetName(n + '_%s_exc_g' % opt)
            h.Write()
            hexc.Write()
            g.Write()
    f.Close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'save_1d_plots':
            set_style()
            ps = plot_saver(plot_dir('o2t_limitplot_run2_tmp4'), size=(600,600))
            draw_gluglu()
            ps.save('gluglu')
            do_1d_plots()

        elif cmd == 'save_2d_plots':
            save_2d_plots()

        elif cmd == 'simple_exclude':
            simple_exclude()

        elif cmd == 'to_r':
            to_r()

        elif cmd == 'from_r':
            from_r()

        else:
            print 'huh?'

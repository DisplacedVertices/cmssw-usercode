#!/usr/bin/env python

import os, sys, re
from array import array
from collections import defaultdict
from itertools import izip
from pprint import pprint
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.general import from_pickle
from limits_input import sample_iterator, axisize

def fmt(t, title, xtitle, color):
    t.SetFillColor(color)
    t.SetTitle('%s;%s;#sigma #times BR^{2} (fb)' % (title, xtitle))
    return t

def tge(xye):
    x = array('f', [z[0] for z in xye])
    y = array('f', [z[1] for z in xye])
    ey = array('f', [z[2] for z in xye])
    ex = array('f', [0.001]*len(x))
    return ROOT.TGraphErrors(len(x), x, y, ex, ey)

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

def parse_gluglu(gluglu=[]):
    if not gluglu:
        gluglu = [eval(x.strip()) for x in open('gluglu.csv') if x.strip()]
        gluglu = [(z[0], z[1]*1000, z[2]/100*z[1]*1000) for z in gluglu] # convert pb to fb and percent to absolute
    return gluglu

def fmt_gluglu(g, xtitle):
    fmt(g, '', xtitle, 9)
    g.SetFillStyle(3001)

def make_gluglu():
    g = tge(parse_gluglu())
    fmt_gluglu(g, 'mass (GeV)')
    return g

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

class limits:
    class point:
        res = (
            ('observed'  , re.compile('Observed Limit: r < (.*)')),
            ('expect2p5' , re.compile('Expected  2.5%: r < (.*)')),
            ('expect16'  , re.compile('Expected 16.0%: r < (.*)')),
            ('expect50'  , re.compile('Expected 50.0%: r < (.*)')),
            ('expect84'  , re.compile('Expected 84.0%: r < (.*)')),
            ('expect97p5', re.compile('Expected 97.5%: r < (.*)')),
            )

        def __init__(self, sample):
            self.sample = sample
            self.observed = self.expect2p5 = self.expect16 = self.expect50 = self.expect84 = self.expect97p5 = None

        @property
        def valid(self):
            return all(x is not None for x in (self.observed,self.expect2p5,self.expect16,self.expect50,self.expect84,self.expect97p5))

        @property
        def expect_valid(self):
            return all(x is not None for x in (self.expect2p5,self.expect16,self.expect50,self.expect84,self.expect97p5))

        @property
        def expect68(self):
            return (self.expect16 + self.expect84) / 2
        @property
        def expect95(self):
            return (self.expect2p5 + self.expect97p5) / 2
        @property
        def expect68lo(self):
            return self.expect68 - self.expect16
        @property
        def expect68hi(self):
            return self.expect84 - self.expect68
        @property
        def expect95lo(self):
            return self.expect95 - self.expect2p5
        @property
        def expect95hi(self):
            return self.expect97p5 - self.expect95

        def tryset(self, line):
            for a,r in self.res:
                mo = r.search(line)
                if mo:
                    x = float(mo.group(1))
                    setattr(self, a, x)

    def __init__(self):
        self.points = []

    def parse(self, sample, fn):
        p = limits.point(sample)
        for line in open(fn):
            p.tryset(line)
        assert p.valid
        self.points.append(p)

    def __getitem__(self, key):
        if key == 'tau':
            return [p.sample.tau for p in self.points]
        elif key == 'mass':
            return [p.sample.mass for p in self.points]
        else:
            return [getattr(p,key) for p in self.points]

def make_1d_plot(d, name, xkey='mass'):
    if xkey == 'mass':
        which_mass = None
        xtitle = 'mass (GeV)'
    else:
        assert type(xkey) == tuple
        xkey, which_mass = xkey
        xtitle = 'lifetime (#mum)'

    class G: pass
    g = G()

    g.observed = tgae(d[xkey], d['observed'], None, None, None, None, '', xtitle, 1)
    g.expect95 = tgae(d[xkey], d['expect95'], None, None, d['expect95lo'], d['expect95hi'], '', xtitle, 5)
    g.expect68 = tgae(d[xkey], d['expect68'], None, None, d['expect68lo'], d['expect68hi'], '', xtitle, 3)
    g.expect50 = tgae(d[xkey], d['expect50'], None, None, None, None, '', xtitle, 1)

    g.observed.SetMarkerStyle(20)
    g.observed.SetMarkerSize(1.2)
    g.expect50.SetLineStyle(2)

    if xkey == 'mass':
        g.gluglu = make_gluglu()
    else:
        xsec, unc = [(xsec,unc) for mass, xsec, unc in parse_gluglu() if mass == which_mass][0]
        x = d[xkey]
        y = [xsec]*len(x)
        ey = [unc]*len(x)
        g.gluglu = tge(zip(x,y,ey))
        fmt_gluglu(g.gluglu, xtitle)
        
    return g

def save_1d_plots():
    xxx = [
        (lambda s: 'neu'   in sample.name and sample.mass == 800 and sample.tau <= 40.,  'multijetM800',   lambda s: s.sample.tau,  ('tau', 800.)),
        (lambda s: 'neu'   in sample.name and sample.tau  == 1.,                         'multijettau1mm', lambda s: s.sample.mass, 'mass'),
        (lambda s: 'ddbar' in sample.name and sample.mass == 800 and sample.tau <= 40.,  'ddbarM800',      lambda s: s.sample.tau,  ('tau', 800.)),
        (lambda s: 'ddbar' in sample.name and sample.tau  == 1.,                         'ddbartau1mm',    lambda s: s.sample.mass, 'mass'),
        ]
    
    in_f = ROOT.TFile('limits_input.root')
    out_f = ROOT.TFile('limits_1d.root', 'recreate')

    for use, name, sorter, xkey in xxx:
        d = limits()
        for sample in sample_iterator(in_f):
            if use(sample):
                d.parse(sample, 'combine_output/signal_%05i/results' % sample.isample)
        d.points.sort(key=sorter)

        out_f.mkdir(name).cd()
        g = make_1d_plot(d, name, xkey)
        for gg in 'observed expect50 expect68 expect95 gluglu'.split():
            getattr(g,gg).Write(gg)

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
        d = limits()
        for sample in sample_iterator(in_f):
            if sample.kind != kind:
                continue
            d.parse(sample, 'combine_output/signal_%05i/results' % sample.isample)

        taus, masses = axisize(d['tau']), axisize(d['mass'])

        out_f.mkdir(kind).cd()

        for x in 'observed expect2p5 expect16 expect50 expect68 expect84 expect95 expect97p5'.split():
            h = ROOT.TH2D(x, '', len(masses)-1, masses, len(taus)-1, taus)
            h.SetStats(0)
            for p in d.points:
                h.SetBinContent(h.FindBin(p.sample.mass, p.sample.tau), getattr(p, x))
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
    print '''
# if you didn't set up already, do this
. /cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt/setup.sh
mkdir ~/.R
R --no-save <<EOF
install.packages("akima", repos="http://cran.r-project.org", lib="~/.R/")
EOF

# cmds
env R_LIBS=~/.R R --no-save <<EOF
'''
    print 'library(akima)'
    for k in 'mfv_ddbar', 'mfv_neu':
        for y in 'observed', 'expect2p5', 'expect16', 'expect50', 'expect68', 'expect84', 'expect95', 'expect97p5':
            x = '%s_%s' % (k,y)
            h = f.Get('%s/%s' % (k,y))
            to_ascii(h, open('to_r_%s.csv' % x, 'wt'), sep=',')
            print 'h<-read.table("to_r_%s.csv", header=TRUE, sep=",")' % x
            print 'i<-interp(x=h\\$x, y=h\\$y, z=h\\$z, xo=seq(300, 3000, by=1), yo=seq(0.1,40,by=0.1))'
            for a in 'xyz':
                print 'write.csv(i\\$%s, "from_r_%s_%s.csv")' % (a,x,a)
    print 'EOF'
    os.system('rm -f to_r.zip')
    os.system('zip -m to_r.zip to_r_*.csv 2>&1 >/dev/null')

def one_from_r(ex, name):
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

    x = read_csv('from_r_%s_x.csv' % ex)
    y = read_csv('from_r_%s_y.csv' % ex)
    z = read_csv('from_r_%s_z.csv' % ex)

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
    f = ROOT.TFile('limits_fromr.root', 'recreate')
    for k in 'mfv_ddbar', 'mfv_neu':
        for opt in ('nm', 'up', 'dn'):
            #for ex in 'observed expect2p5 expect16 expect50 expect68 expect84 expect95 expect97p5'.split():
            for ex in 'observed expect50'.split():
                ex = k + '_' + ex
                n = '%s_fromrinterp' % ex
                h = one_from_r(ex, n)
                hexc = gluglu_exclude(h, opt)
                g = exc_graph(hexc, 1, 1)
                g.SetName(n + '_%s_exc_g' % opt)
                h.Write()
                hexc.Write()
                g.Write()
    f.Close()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'draw_gluglu':
            set_style()
            ps = plot_saver(plot_dir('limitplot_gluglu'), size=(600,600))
            draw_gluglu()
            ps.save('gluglu')

        if cmd == 'save_1d_plots':
            save_1d_plots()

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

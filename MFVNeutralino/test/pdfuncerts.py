import gzip
from functools import partial
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.Sample import norm_from_file
from DVCode.Tools.general import to_pickle, from_pickle
import DVCode.MFVNeutralino.AnalysisConstants as ac

class Sample(object):
    def __init__(self, name, fns):
        self.name = name
        self.fn = fns[0]

def scanpack():
    return eval(gzip.GzipFile('/uscms/home/tucker/public/mfv/scanpacks/2017p8/scanpackpdftest.merged.list.gz').read())

def samples():
    return [Sample(*x) for x in scanpack().iteritems()]

def avg(l):
    return sum(l)/len(l)
def rms(l):
    m = avg(l)
    return (sum((x-m)**2 for x in l)/(len(l)-1))**0.5

def analyze(plots=False):
    if plots:
        set_style()
        ps = plot_saver(plot_dir('pdfweights', temp=True), size=(600,600))

    fields = ('nominal','plus','minus','pdfunc','rel','relavg','n16','n84','ctl','ctlrel','ctlrelmd')
    fmt = '%-45s' + ' %10s'*len(fields)
    print fmt % (('sname',) + fields)

    ss = samples()
    for s in ss:
        f = ROOT.TFile.Open(s.fn)
        s.norm = norm_from_file(f)
        s.w = ac.int_lumi_2018 * 1e-3 / s.norm
        t = f.Get('mfvMiniTree/t')
        hr = draw_hist_register(t, True, True)
        if plots:
            for i in xrange(48,148):
                h = hr.draw('weights[%i]' % i, 'nvtx>=2', binning='100,0,2')
                ps.save(str(i))

        cut = '(nvtx>=2)'   # '(nvtx>=2 && (gen_x[0]**2 + gen_y[0]**2)**0.5<0.08 && (gen_x[1]**2+gen_y[1]**2)**0.5 < 0.08)'
        h = hr.draw('weight', cut, binning='1,0,1')
        s.nominal, _ = tuple(s.w*x for x in get_integral(h))

        s.pdfunc, s.family = [], []
        for i in xrange(46,148): # JMTBAD indices into misc_weights are fragile, need to put the pdf weights/info somewhere else than weights
            h = hr.draw('weight', '%s*misc_weights[%i]' % (cut,i), binning='1,0,1')
            v = tuple(s.w*x for x in get_integral(h))[0]
            (s.pdfunc if i < 48 else s.family).append(v)

        s.plus, s.minus = s.pdfunc
        s.pdfunc = abs(s.plus - s.minus)/2
        s.plus = abs(s.plus - s.nominal)
        s.minus = abs(s.nominal - s.minus)
        s.rel = s.pdfunc / s.nominal

        s.family.sort()
        s.n16, s.n84 = s.family[16], s.family[83]
        s.ctl = (s.n84 - s.n16)/2
        s.avg = avg(s.family)
        s.rms = rms(s.family)
        s.mdn = (s.family[49] + s.family[50])/2
        s.md = (s.n84 + s.n16)/2
        s.relavg = s.pdfunc / s.avg
        s.ctlrel = s.ctl / s.nominal
        s.ctlrelmd = s.ctl / s.md

        print fmt.replace('%10s','%10.4f') % ((s.name,) + tuple(getattr(s,fi) for fi in fields))

    to_pickle(ss, 'pdfuncerts.gzpickle')

def plot():
    set_style()
    ps = plot_saver(plot_dir('pdfuncerts'), size=(600,600), log=False)
    ps.c.SetLeftMargin(0.11)

    parabs = {
        300:  ((300,0.06), (585,0.02), (877,0.009)),
        1000: ((300,0.03), (550,0.01), (873,0.006)),
        10000:((300,0.04), (550,0.015), (877,0.005)),
    }

    lines = {
        300:  ((877,0.009), (3000,0.075)),
        1000: ((873,0.006), (3000,0.05)),
        10000:((877,0.005), (3000,0.035)),
    }

    def fparab(points,_n=[0]):
        (x1,y1),(x2,y2),(x3,y3) = sorted(points)
        c1 = y1/(x1-x2)/(x1-x3)
        c2 = y2/(x2-x1)/(x2-x3)
        c3 = y3/(x3-x1)/(x3-x2)
        a = c1+c2+c3
        b = -((c2+c3)*x1+(c1+c3)*x2+(c1+c2)*x3)
        c = c1*x2*x3 + c2*x1*x3 + c3*x1*x2
        fm = '%.4g*x**2 + %.4g*x + %.4g' % (a,b,c)
        fcn = ROOT.TF1('parab%i' % _n[0], fm,  x1, x3)
        _n[0] += 1
        return fcn, fm

    def fline(points,_n=[0]):
        (x1,y1),(x2,y2) = sorted(points)
        m = (y2-y1)/(x2-x1)
        b = y1-m*x1
        fm = '%.4g*x + %.4g' % (m,b)
        fcn = ROOT.TF1('line%i' % _n[0], fm, x1, x2)
        _n[0] += 1
        return fcn, fm

    samples = defaultdict(list)
    for s in from_pickle('pdfuncerts.gzpickle'):
        tau = int(s.name.split('tau')[1].split('um')[0])
        samples[tau].append(s)
    
    for tau in 300, 1000, 10000:
        gneu, gstop = [], []

        for s in sorted(samples[tau], key=lambda s: s.name):
            mass = float(s.name.split('_M')[1].split('_')[0])
            num, den = s.nominal/s.w, s.norm
            e, ee = wilson_score_vpme(num, den)
            st = num**-0.5
            print s.name, tau, mass, s.ctlrelmd, st, s.nominal, e, ee, num,den,clopper_pearson(num,den)
            (gneu if 'neu' in s.name else gstop).append((mass, s.ctlrelmd, ee))
        
        gneu, gstop = tgraph(gneu) if gneu else None, tgraph(gstop)
        for g,c in (gneu,4), (gstop,2):
            if not g: continue
            g.SetTitle(';mass (GeV);relative acc. unc.')
            g.SetMarkerColor(c)
            g.SetLineColor(c)
            g.SetMarkerStyle(20)
        gstop.Draw('AP')
        if gneu: gneu.Draw('P')
        gstop.GetYaxis().SetRangeUser(0,0.08)

        leg = ROOT.TLegend(0.249,0.742,0.599,0.852,'#tau = %s' % {300:'300 #mum',1000:'1 mm',10000:'10 mm'}[tau])
        leg.SetBorderSize(0)
        leg.AddEntry(gstop, 'dijet', 'LP')
        if gneu: leg.AddEntry(gneu, 'multijet', 'LP')
        leg.Draw()

        prb, pf = fparab(parabs[tau])
        prb.Draw('same')
        lin, lf = fline(lines[tau])
        lin.Draw('same')
        print tau, pf, lf

        ps.save('tau%06i' % tau)

def plot_vars():
    set_style()
    ps = plot_saver(plot_dir('pdfqetc', temp=True), size=(600,600), log=False)
    ps.c.SetLeftMargin(0.11)

    for sname, (fn,) in scanpack().iteritems():
        print sname
        f = ROOT.TFile.Open(fn)
        fout = ROOT.TFile(sname + '.root', 'recreate')
        t = f.Get('mfvMiniTree/t')
        hr = draw_hist_register(t, True)
        hrd = partial(hr.draw, cut='nvtx>=2', write=True)
        hrd('misc_weights[148]', binning='27,-5,22', rename='h_id1', title='two-vertex events;parton #1 id;events')
        hrd('misc_weights[149]', binning='27,-5,22', rename='h_id2', title='two-vertex events;parton #2 id;events')
        hrd('misc_weights[150]', binning='50,0,1', rename='h_x1', title='two-vertex events;x_{1};events/0.02')
        hrd('misc_weights[151]', binning='50,0,1', rename='h_x2', title='two-vertex events;x_{2};events/0.02')
        hrd('misc_weights[154]', binning='50,0,5000', rename='h_scale', title='two-vertex events;Q_{PDF} (GeV);events/100 GeV')


if __name__ == '__main__':
    if 'analyze' in sys.argv:
        analyze()
    plot()
    #plot_vars()

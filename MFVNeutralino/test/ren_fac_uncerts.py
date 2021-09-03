import gzip
from functools import partial
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.Sample import norm_from_file, norm_from_file_weight
from DVCode.Tools.general import to_pickle, from_pickle
import DVCode.MFVNeutralino.AnalysisConstants as ac

year = 2018

class Sample(object):
    def __init__(self, name, fns):
        self.name = name
        self.fn = fns[0]

def scanpack():
    return eval(gzip.GzipFile('/uscms/home/joeyr/public/mfv/scanpacks/2017p8/ren_fac.list.gz').read())

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
        ps = plot_saver(plot_dir('scaleweights', temp=True), size=(600,600))

    fields = ('nominal','n16','n84','ctl','ctlrel','ctlrelmd')
    fmt = '%-45s' + ' %10s'*len(fields)
    print fmt % (('sname',) + fields)

    ss = samples()
    for s in ss:
        f = ROOT.TFile.Open(s.fn)
        s.norm = norm_from_file(f)
        s.w = ac.int_lumi_2018 * 1e-3 / s.norm
        t = f.Get('mfvMiniTree/t')
        hr = draw_hist_register(t, True, True)

        weight_str_list = ["ren_weight_up", "ren_weight_dn", "fac_weight_up", "fac_weight_dn", "ren_weight_up*fac_weight_up", "ren_weight_dn*fac_weight_dn"]

        cut = '(nvtx>=2)'   # '(nvtx>=2 && (gen_x[0]**2 + gen_y[0]**2)**0.5<0.08 && (gen_x[1]**2+gen_y[1]**2)**0.5 < 0.08)'
        h = hr.draw('weight', cut, binning='1,0,1')
        s.nominal, _ = tuple(s.w*x for x in get_integral(h))

        s.scaleunc, s.family = [], []
        for weight_str in weight_str_list :

            # because I didn't pick better names...
            if "ren" in weight_str and "fac" in weight_str :
                weight_name_for_norm = "sum_weight_ren_fac"
            elif "ren" in weight_str :
                weight_name_for_norm = "sum_weight_ren"
            elif "fac" in weight_str :
                weight_name_for_norm = "sum_weight_fac"

            if "_up" in weight_str :
                weight_name_for_norm += "_up"
            elif "_dn" in weight_str :
                weight_name_for_norm += "_dn"

            s.norm = norm_from_file_weight(f, weight_name=weight_name_for_norm)
            s.w = ac.int_lumi_2018 * 1e-3 / s.norm

            h = hr.draw('weight', '%s*%s' % (cut,weight_str), binning='1,0,1')
            v = tuple(s.w*x for x in get_integral(h))[0]
            #print '%s*%s, weight*nvtx==2 = %s' % (cut,weight_str,v)
            s.family.append(v)

        if len(weight_str_list) == 6 :
            s.family.sort()
            s.n16, s.n84 = s.family[1], s.family[4] # since total is 6
            s.ctl = max( abs(s.family[0]-s.nominal), abs(s.family[5]-s.nominal) ) # i.e. maximum deviation ==> envelope
            #s.ctl = (s.n84 - s.n16)/2
            s.avg = avg(s.family)
            s.rms = rms(s.family)
            s.mdn = (s.family[2] + s.family[3])/2
            s.md = (s.n84 + s.n16)/2
            #s.relavg = s.scaleunc / s.avg
            if s.nominal == 0 : 
                print "s.nominal is 0!!!!!!!!!!!!"
                s.nominal = 0.00001
            if s.md == 0 : 
                print "s.md is 0!!!!!!!!!!!!"
                s.md = 0.00001
            s.ctlrel = s.ctl / s.nominal
            s.ctlrelmd = s.ctl / s.md

            print fmt.replace('%10s','%10.4f') % ((s.name,) + tuple(getattr(s,fi) for fi in fields))
        else :
            print "invalid weight_str_list!!!!!!!!!!!!!!!!!"


    to_pickle(ss, 'ren_fac.gzpickle')

def plot():
    set_style()
    ps = plot_saver(plot_dir('ren_fac_%s' % year), size=(600,600), log=False)
    ps.c.SetLeftMargin(0.11)

    samples = defaultdict(list)
    for s in from_pickle('ren_fac.gzpickle'):
        tau = int(s.name.split('tau')[1].split('um')[0])
        samples[tau].append(s)
    
    for tau in 300, 1000, 10000:
        gneu, gstop = [], []

        for s in sorted(samples[tau], key=lambda s: s.name):

            mass = float(s.name.split('_M')[1].split('_')[0])
            num, den = s.nominal/s.w, s.norm
            e, ee = wilson_score_vpme(num, den)
            st = num**-0.5
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
        gstop.GetYaxis().SetRangeUser(0,0.1)

        leg = ROOT.TLegend(0.249,0.742,0.599,0.852,'#tau = %s' % {300:'300 #mum',1000:'1 mm',10000:'10 mm'}[tau])
        leg.SetBorderSize(0)
        leg.AddEntry(gstop, 'dijet', 'LP')
        if gneu: leg.AddEntry(gneu, 'multijet', 'LP')
        leg.Draw()

        fitopt = "RSQ0"
        fitdict = { (300, 500)   : "pol1", 
                    (500, 1000)  : "pol1", 
                    (1000, 3000) : "pol0"}

        for key in fitdict :
            fitfunc = fitdict[key]
            fitrange = key
            gstop.Fit(fitfunc, fitopt, "", *fitrange)
        

        for kind in ["mfv_neu","mfv_stopdbardbar"] :
            if   kind == "mfv_neu"  :         g = gneu
            elif kind == "mfv_stopdbardbar" : g = gstop
            else : os.abort("invalid kind!")

            outstr = "('%s', %s, '%s') : lambda x: \n" % (kind, tau, year)
            fit_M_300_to_500 = g.Fit("pol1" ,fitopt, "", 300, 500)
            fit_M_500_to_1000 = g.Fit("pol1" ,fitopt, "", 500, 1000)
            fit_M_1000_to_3000 = g.Fit("pol0" ,fitopt, "", 1000, 3000)

            outstr += "%E + %E*x if x < 500 "       % (fit_M_300_to_500.Parameter(0),  fit_M_300_to_500.Parameter(1))
            outstr += "else %E + %E*x if x < 1000 " % (fit_M_500_to_1000.Parameter(0), fit_M_500_to_1000.Parameter(1))
            outstr += "else %E,"                    % (fit_M_1000_to_3000.Parameter(0))
            print outstr

        ps.save('tau%06i' % tau)


if __name__ == '__main__':
    if 'analyze' in sys.argv:
        analyze()
    plot()

import gzip, statmodel, JMTucker.MFVNeutralino.AnalysisConstants as ac
from JMTucker.MFVNeutralino.MiniTreeBase import *

bins = to_array(0., 0.04, 0.07, 4)
nbins = len(bins)-1

years = '2017', '2018'
nyears = len(years)

int_lumi = ac.scaled_int_lumi_2017, ac.scaled_int_lumi_2018
# next 3 lines of values override what's in the 2v_from_jets output
observed = (0,0,0), (0,0,0)
bkg_n1v = 1303, 908
bkg_n2v = 1, 1
bkg_c1v = (0.709, 0.257, 0.034), (0.650, 0.313, 0.037) # these do not and are checked

def sig_uncert(name): # JMTBAD implement different sig uncerts per trackmover study when done
    u = 0.24
    return (u,u,u)

bkg_uncert = [(0.14, 0.26, 0.42), (0.14, 0.26, 0.42)]
bkg_uncert_stat = [statmodel.ebins['data100pc_%s_5track' % year] for year in years]
for y in xrange(nyears):
    bkg_uncert[y] = [(a**2 + b**2)**0.5 for a,b in zip(bkg_uncert[y], bkg_uncert_stat[y])] # JMTBAD use proper gmN?

def bkg_fn(year, which='default'):
    if which == 'c':
        which = 'btag_corrected_nom'
    else:
        assert which == 'default'
    return '2v_from_jets_data_%s_5track_%s_V27m.root' % (year, which)

def bkg_f(year, which='default', _c={}):
    k = year, which
    if not _c.has_key(k):
        _c[k] = ROOT.TFile.Open(bkg_fn(*k))
    return _c[k]

def cbkg_f(year):
    return bkg_f(year, which='c')

in_trees, in_scanpack_list = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV27m/mfv*_%s.root' % years[0], None
#in_trees, in_scanpack_list = None, '/uscms/home/tucker/public/mfv/scanpacks/None'

limitsinput_fn = 'limitsinput.root'

####

def ndx2isample(ndx):
    return -(ndx+1)
def isample2ndx(isample):
    return -isample-1

def name_list(f):
    return f.Get('name_list')
def nsamples(f):
    return name_list(f).GetNbinsX()

def details2name(kind, tau, mass):
    # same convention as scanpack: tau float:mm, mass int:GeV
    return '%s_tau%06ium_M%04i' % (kind, int(tau*1000), mass)
def name2kind(name):
    return name.split('_tau')[0]
def name2tau(name):
    return int(name.split('tau')[1].split('um')[0]) / 1000.
def name2mass(name):
    return int(name.split('M')[1].split('_')[0])
def name2details(name):
    return name2kind(name), name2tau(name), name2mass(name)
def name2taumass(name):
    return name2tau(name), name2mass(name)

def name2isample(f, name):
    h = name_list(f)
    ax = h.GetXaxis()
    for ibin in xrange(1, h.GetNbinsX()+1):
        if name == ax.GetBinLabel(ibin):
            return -ibin
    raise ValueError('no name %s found in %r' % (name, f))

def isample2name(f, isample):
    h = name_list(f)
    nb = h.GetNbinsX()
    ibin = -isample
    if ibin < 1 or ibin > nb:
        raise ValueError('isample %i wrong for name list in %r (nb = %i)' % (isample, f, nb))
    return h.GetXaxis().GetBinLabel(ibin)

def isample_iterator(f):
    h = name_list(f)
    for ibin in xrange(1, h.GetNbinsX()+1):
        yield -ibin

def isamplename_iterator(f):
    h = name_list(f)
    ax = h.GetXaxis()
    for ibin in xrange(1, h.GetNbinsX()+1):
        yield -ibin, ax.GetBinLabel(ibin)

def name_iterator(f):
    for _, name in isamplename_iterator(f):
        yield name

class sample(object):
    pass

def sample_iterator(f):
    for isample, name in isamplename_iterator(f):
        s = sample()
        s.isample = isample
        s.name = name
        s.kind, s.tau, s.mass = name2details(name)
        yield s

def test_sample_iterator(f):
    kinds = 'mfv_neu', 'mfv_stopdbardbar'
    taus = [t/1000. for t in 100, 300, 1000, 10000, 30000]
    masses = [400, 600, 800, 1200, 1600, 3000]

    allowed = {name:isample for isample,name in isamplename_iterator(f)}
    for k in kinds:
        for t in taus:
            for m in masses:
                name = details2name(k,t,m)
                if name in allowed:
                    s = sample()
                    s.name = name
                    s.isample = allowed[name]
                    s.kind, s.tau, s.mass = k, t, m
                    yield s

def sample_iterator_1d_plots(f):
    for s in sample_iterator(f):
        if s.mass in (800., 1600., 2300.) or s.tau in (0.4, 1., 10.):
            yield s

####

def make():
    assert not os.path.exists(limitsinput_fn)
    ROOT.TH1.AddDirectory(1)

    f = ROOT.TFile(limitsinput_fn, 'recreate')
    hs = []

    # bkg: separate histograms by year
    for y, year in enumerate(years):
        bkg_f(year), cbkg_f(year); f.cd()

        h_int_lumi = ROOT.TH1D('h_int_lumi_%s' % year, '', 1, 0, 1)
        h_int_lumi.SetBinContent(1, int_lumi[y])

        h_observed = ROOT.TH1D('h_observed_%s' % year, '', nbins, bins)
        for i,v in enumerate(observed[y]):
            h_observed.SetBinContent(i+1, v)
    
        h_bkg_dbv = to_TH1D( bkg_f(year).Get('h_1v_dbv'),  'h_bkg_dbv_%s' % year)
        h_bkg_dvv = to_TH1D(cbkg_f(year).Get('h_c1v_dvv'), 'h_bkg_dvv_%s' % year)

        h_bkg_dbv.Scale(bkg_n1v[y]/get_integral(h_bkg_dbv)[0])
        h_bkg_dvv.Scale(bkg_n2v[y]/get_integral(h_bkg_dvv)[0])

        h = h_bkg_dvv_rebin = h_bkg_dvv.Rebin(nbins, 'h_bkg_dvv_rebin_%s' % year, bins)
        move_overflow_into_last_bin(h_bkg_dvv_rebin)
        for i in xrange(nbins):
            if abs(bkg_c1v[y][i] - h.GetBinContent(i+1)/bkg_n2v[y]) > 0.001:
                print y,i, bkg_c1v[y][i], h.GetBinContent(i+1)/bkg_n1v[y]
                assert 0

        h_bkg_uncert = ROOT.TH1D('h_bkg_uncert_%s' % year, '', nbins, bins)
        for i,v in enumerate(bkg_uncert[y]):
            h_bkg_uncert.SetBinContent(i+1, v)

        hs += [h_int_lumi, h_observed, h_bkg_dbv, h_bkg_dvv, h_bkg_dvv_rebin, h_bkg_uncert]

    # now signals.
    if in_trees:
        title = in_trees
        sigs = sorted(glob(in_trees))
        sigs = [(os.path.basename(fn).replace('.root', ''), [fn]) for fn in sigs]
    elif in_scanpack_list:
        title = in_scanpack_list
        f_scanpack_list = (gzip.GzipFile if in_scanpack_list.endswith('.gz') else open)(in_scanpack_list)
        sigs = sorted(eval(f_scanpack_list.read()).items())

    name_list = ROOT.TH1C('name_list', title, len(sigs), 0, len(sigs))

    for isig, (name, fns) in enumerate(sigs):
        isample = ndx2isample(isig)
        print isig, isample, name, fns, 

        name_list.GetXaxis().SetBinLabel(-isample, name.replace('_' + years[0], ''))

        for y, year in enumerate(years):
            name = name.replace(years[0], year)
            ngen = 0.
            sig_t = ROOT.TChain('mfvMiniTree/t')
            for fn in fns:
                fn = fn.replace(years[0], year)
                sig_f = ROOT.TFile.Open(fn)
                ngen += sig_f.Get('mfvWeight/h_sums').GetBinContent(1)
                sig_f.Close()
                sig_t.Add(fn)
            f.cd()

            h_dbv_name = 'h_signal_%i_dbv_%s' % (isample, year)
            h_dbv = ROOT.TH1D(h_dbv_name, name, 125, 0, 2.5)
            sig_t.Draw('dist0>>%s' % h_dbv_name, 'weight*(nvtx==1)')

            h_dvv_name = 'h_signal_%i_dvv_%s' % (isample, year)
            h_dvv = ROOT.TH1D(h_dvv_name, name, 400, 0, 4)
            sig_t.Draw('svdist>>%s' % h_dvv_name, 'weight*(nvtx>=2)')

            h_dphi_name = 'h_signal_%i_dphi_%s' % (isample, year)
            h_dphi = ROOT.TH1D(h_dphi_name, name, 10, -3.15, 3.15)
            sig_t.Draw('svdphi>>%s' % h_dphi_name, 'weight*(nvtx>=2)')

            h_norm = ROOT.TH1D('h_signal_%i_norm_%s' % (isample, year), name, 2, 0, 2)
            norm = 1e-3 / ngen  # 1 fb xsec in pb / number of events read, int lumi will be added later
            h_norm.SetBinContent(1, norm)
            h_norm.SetBinContent(2, norm)

            h_dvv_rebin = h_dvv.Rebin(nbins, 'h_signal_%i_dvv_rebin_%s' % (isample, year), bins)
            move_overflow_into_last_bin(h_dvv_rebin)
            for i in 1,2,3:
                print 1e-3 * int_lumi[y] * h_dvv_rebin.GetBinContent(i) / ngen,

            h_uncert = ROOT.TH1D('h_signal_%i_uncert_%s' % (isample, year), '', nbins, bins)
            for i,v in enumerate(sig_uncert(name)):
                h_uncert.SetBinContent(i+1, v)

            hs += [h_dbv, h_dvv, h_dphi, h_norm, h_dvv_rebin, h_uncert]
        print

    f.Write()
    f.Close()

def nevents(f, isample):
    h = f.Get('h_signal_%i_norm' % isample)
    return 1e-3 / h.GetBinContent(2)

def h_dbv(f, isample):
    return f.Get('h_signal_%i_dbv' % isample)
def h_dvv(f, isample):
    return f.Get('h_signal_%i_dvv_rebin' % isample)

def i1v(f, isample):
    return h_dbv(f, isample).GetEntries()
def i2v(f, isample):
    return h_dvv(f, isample).GetEntries()

def n1v(f, isample):
    h = h_dbv(f, isample)
    return h.Integral(0, h.GetNbinsX()+2)
def n2v(f, isample):
    h = h_dvv(f, isample)
    return h.Integral(0, h.GetNbinsX()+2)

def _eff(fcn, f, isample):
    i = fcn(f, isample)
    n = nevents(f, isample)
    e,l,u = wilson_score(i,n)
    return e, (u-l)/2
def eff1v(f, isample):
    return _eff(i1v, f, isample)
def eff2v(f, isample):
    return _eff(i2v, f, isample)


def draw():
    ps = plot_saver(plot_dir('o2t_templates_run2'), size=(600,600))
    f = ROOT.TFile(limitsinput_fn)

    whiches = [
        ('multijet', [
            (name2isample(f, 'mfv_neu_tau00100um_M0800'), ROOT.kRed,      'multijet M = 800 GeV, #tau = 100 #mum'),
            (name2isample(f, 'mfv_neu_tau00300um_M0800'), ROOT.kGreen+2,  'multijet M = 800 GeV, #tau = 300 #mum'),
            (name2isample(f, 'mfv_neu_tau01000um_M0800'), ROOT.kBlue,     'multijet M = 800 GeV, #tau = 1 mm'),
            (name2isample(f, 'mfv_neu_tau10000um_M0800'), ROOT.kMagenta,  'multijet M = 800 GeV, #tau = 10 mm'),
            (name2isample(f, 'mfv_neu_tau30000um_M0800'), ROOT.kOrange+2, 'multijet M = 800 GeV, #tau = 30 mm'),
            ]),
        ('dijet', [
            (name2isample(f, 'mfv_ddbar_tau00100um_M0800'), ROOT.kRed,      'dijet M = 800 GeV, #tau = 100 #mum'),
            (name2isample(f, 'mfv_ddbar_tau00300um_M0800'), ROOT.kGreen+2,  'dijet M = 800 GeV, #tau = 300 #mum'),
            (name2isample(f, 'mfv_ddbar_tau01000um_M0800'), ROOT.kBlue,     'dijet M = 800 GeV, #tau = 1 mm'),
            (name2isample(f, 'mfv_ddbar_tau10000um_M0800'), ROOT.kMagenta,  'dijet M = 800 GeV, #tau = 10 mm'),
            (name2isample(f, 'mfv_ddbar_tau30000um_M0800'), ROOT.kOrange+2, 'dijet M = 800 GeV, #tau = 30 mm'),
            ]),
        ]

    def fmt(h, name, color, save=[]):
        binning = to_array(0., 0.04, 0.07, 0.15)
        h = h.Rebin(len(binning)-1, name, binning)
        h.Sumw2()
        h.SetStats(0)
        h.SetLineWidth(3)
        h.SetLineColor(color)
        h.SetTitle(';d_{VV} (cm);event rate (unit norm.)')
        move_overflow_into_last_bin(h)
        h.Scale(1./h.Integral(0,h.GetNbinsX()+2))
        save.append(h)
        return h
    
    for which_name, which in whiches: 
        hbkg = fmt(f.Get('h_bkg_dvv'), 'bkg', ROOT.kBlack)
        hbkg.Draw('hist e')
        hbkg.GetYaxis().SetRangeUser(0,1.5)

        leg = ROOT.TLegend(0.142, 0.657, 0.702, 0.857)
        leg.SetBorderSize(0)
        leg.AddEntry(hbkg, 'Background template d_{VV}^{C}', 'LE')

        for isample, color, title in which:
            h = fmt(f.Get('h_signal_%i_dvv' % isample), title, color)
            h.Draw('hist e same')
            leg.AddEntry(h, title, 'LE')

        leg.Draw()

        ps.save(which_name, log=False)

def compare(fn1, fn2, outbase):
    f1, f2 = fs = ROOT.TFile.Open(fn1), ROOT.TFile.Open(fn2)
    samples_1 = dict((name, isample) for isample, name in isamplename_iterator(f1))
    samples_2 = dict((name, isample) for isample, name in isamplename_iterator(f2))
    names_1 = set(samples_1)
    names_2 = set(samples_2)

    names = sorted(names_1 & names_2)
    nnames = len(names)
    if not names:
        print 'no samples in common between %s and %s' % (fn1, fn2)
        return
    else:
        print '%i samples in common' % nnames

    if names_1 != names_2:
        print '# samples only in %s: %i' % (fn1, len(names_1 - names_2))
        #pprint(sorted(names_1 - names_2))
        print '# samples only in %s: %i' % (fn2, len(names_2 - names_1))
        #pprint(sorted(names_2 - names_1))

    h_fcns = []
    def make_h_fcn(nm, fcn):
        h = ROOT.TH1D(nm, '%s - %s' % (fn1, fn2), nnames, 0, nnames)
        h_fcns.append((h, fcn))
        return h

    h_eff1v = make_h_fcn('eff1v', eff1v)
    h_eff2v = make_h_fcn('eff2v', eff2v)
    h_dbvmean = make_h_fcn('dbvmean', lambda f,isample: (h_dbv(f,isample).GetMean(), h_dbv(f,isample).GetMeanError()))
    h_dbvrms  = make_h_fcn('dbvrms',  lambda f,isample: (h_dbv(f,isample).GetRMS(),  h_dbv(f,isample).GetRMSError() ))
    h_dvvmean = make_h_fcn('dvvmean', lambda f,isample: (h_dvv(f,isample).GetMean(), h_dvv(f,isample).GetMeanError()))
    h_dvvrms  = make_h_fcn('dvvrms',  lambda f,isample: (h_dvv(f,isample).GetRMS(),  h_dvv(f,isample).GetRMSError() ))

    all_stat_same, all_same = True, True

    for iname, name in enumerate(names):
        isamples = samples_1[name], samples_2[name]
        for h, fcn in h_fcns:
            (v1,e1), (v2, e2) = [fcn(f, isample) for f,isample in zip(fs, isamples)]
            h.GetXaxis().SetBinLabel(iname+1, name)
            d = v1 - v2
            e = (e1**2 + e2**2)**0.5
            h.SetBinContent(iname+1, d)
            h.SetBinError  (iname+1, e)
            if abs(d) > 1e-5:
                all_same = False
            if abs(d) > e:
                all_stat_same = False

    c = ROOT.TCanvas('c', '', 1000, 800)
    line = ROOT.TLine(0, 0, nnames, 0)
    line.SetLineStyle(2)
    line.SetLineWidth(2)

    for i,(h,_) in enumerate(h_fcns):
        h.SetStats(0)
        h.SetLineWidth(2)
        h.Draw('e')
        line.Draw()
        for ext in 'root', 'png':
            c.SaveAs(outbase + '/%i_%s.%s' % (i, h.GetName(), ext))

    print 'all same? %r statistically? %r' % (all_same, all_stat_same)

def points(f=None):
    if f is None:
        f = ROOT.TFile(limitsinput_fn)
    kinds  = sorted(set(s.kind for s in sample_iterator(f)))
    masses = sorted(set(s.mass for s in sample_iterator(f)))
    taus   = sorted(set(s.tau  for s in sample_iterator(f)))
    return kinds, masses, taus

def axisize(l):
    l = sorted(set(l))
    delta = l[-1] - l[-2]
    l.append(l[-1] + delta)
    return to_array(l)

def axes(f=None):
    kinds, masses, taus = points(f)
    masses = axisize(masses)
    taus   = axisize(taus)
    return kinds, masses, taus

def nevents_plot():
    in_f = ROOT.TFile(limitsinput_fn)
    out_f = ROOT.TFile('nevents.root', 'recreate')

    kinds, masses, taus = axes(in_f)
    nmasses = len(masses) - 1
    ntaus = len(taus) - 1

    for kind in kinds:
        h = ROOT.TH2D('nevents_%s' % kind, ';mass (GeV);#tau (mm)', nmasses, masses, ntaus, taus)

        for ibin in xrange(1, nmasses+1):
            mass = h.GetXaxis().GetBinLowEdge(ibin)
            for jbin in xrange(1, ntaus+1):
                tau = h.GetYaxis().GetBinLowEdge(jbin)

                try:
                    isample = name2isample(in_f, details2name(kind, tau, mass))
                except ValueError:
                    continue

                nev = nevents(in_f, isample)

                h.SetBinContent(ibin, jbin, nev)
                h.SetBinError  (ibin, jbin, nev**0.5)

        out_f.cd()
        h.Write()

    out_f.Write()
    out_f.Close()

def signal_efficiency():
    from signal_efficiency import SignalEfficiencyCombiner
    combiner = SignalEfficiencyCombiner() #simple=limitsinput_fn)
    in_f = combiner.inputs[0].f
    out_f = ROOT.TFile('signal_efficiency.root', 'recreate')

    kinds, masses, taus = axes(in_f)
    nmasses = len(masses) - 1
    ntaus = len(taus) - 1

    for kind in kinds:
        h = ROOT.TH2D('signal_efficiency_%s' % kind, ';mass (GeV);#tau (mm)', nmasses, masses, ntaus, taus)

        for ibin in xrange(1, nmasses+1):
            mass = h.GetXaxis().GetBinLowEdge(ibin)
            for jbin in xrange(1, ntaus+1):
                tau = h.GetYaxis().GetBinLowEdge(jbin)

                try:
                    isample = name2isample(in_f, details2name(kind, tau, mass))
                except ValueError:
                    continue

                r = combiner.combine(isample)
                bin_start = 1 # 1 for >=400 um, 2 for >=700um
                e  = sum(x for x in r.sig_rate       [bin_start:]) / combiner.int_lumi
                ee = sum(x for x in r.sig_stat_uncert[bin_start:]) / combiner.int_lumi # JMTBAD

                h.SetBinContent(ibin, jbin, e)
                h.SetBinError  (ibin, jbin, ee)

        out_f.cd()
        h.Write()

    out_f.Write()
    out_f.Close()

if __name__ == '__main__':
    if 'make' in sys.argv:
        make()
    elif 'draw' in sys.argv:
        draw()
    elif 'compare' in sys.argv:
        compare(*sys.argv[2:5])
    elif 'nevents' in sys.argv:
        f = ROOT.TFile(limitsinput_fn)
        for s in sample_iterator(f):
            print s.name.ljust(30), '%6i' % int(nevents(f, s.isample))
        nevents_plot()
    elif 'points' in sys.argv:
        print 'kinds = %r\nmasses = %r\ntaus = %r' % points()
    elif 'signal_efficiency' in sys.argv:
        signal_efficiency()
    else:
        print 'dunno'

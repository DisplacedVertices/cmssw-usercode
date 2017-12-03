from JMTucker.MFVNeutralino.MiniTreeBase import *

for i in xrange(10):
    print 'put in the 0.998 scale factor or whatever it is, and figure out how to do hip and 2015'

nbins = 3
bins = to_array(0., 0.04, 0.07, 4)

observed = [1,0,0]

int_lumi = ac.int_lumi_2015p6 * ac.scale_factor_2015p6

bkg_n1v = 1183.
bkg_n2v = 1.

bkg_frac_check = [0.51, 0.37, 0.12]
sig_uncert = [0.24, 0.24, 0.24]
bkg_uncert = [0.25, 0.25, 0.69]
bkg_uncert_stat = [0.02, 0.05, 0.18]
bkg_uncert = [(a**2 + b**2)**0.5 for a,b in zip(bkg_uncert, bkg_uncert_stat)] # JMTBAD use proper gmN?

in_fn = '/uscms/home/jchu/public/2v_from_jets_data_2015p6_5track_default_v15_v5.root'
#in_trees, in_scanpack_list = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15_v5/mfv*root', None
in_trees, in_scanpack_list = None, '/uscms/home/tucker/work/hip_8025/src/JMTucker/MFVNeutralino/test/MakeSamples/scanpacks/scanpack_merge_1_1p5_2.list'

limitsinput_fn = 'limitsinput.root'

####

assert nbins == len(bins) - 1
for l in observed, bkg_frac_check, sig_uncert, bkg_uncert, bkg_uncert_stat:
    assert len(l) == nbins

assert abs(sum(bkg_frac_check) - 1) < 0.01

if '_data_' in in_fn:
    assert abs(sum(observed) - bkg_n2v) < 0.01

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
    return '%s_tau%05ium_M%04i' % (kind, int(tau*1000), mass)
def name2kind(name):
    return name.split('_tau')[0]
def name2tau(name):
    return int(name.split('tau')[1].split('um')[0]) / 1000.
def name2mass(name):
    return int(name.split('M')[1])
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
    nbins = h.GetNbinsX()
    ibin = -isample
    if ibin < 1 or ibin > nbins:
        raise ValueError('isample %i wrong for name list in %r (nbins = %i)' % (isample, f, nbins))
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
    kinds = 'mfv_neu', 'mfv_ddbar'
    taus = [t/1000. for t in 100, 400, 1000, 10000, 31000]
    masses = [300, 400, 500, 600, 800, 1200, 1800, 3000]

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
        if (s.mass == 800 and s.tau <= 40.) or s.tau == 1.:
            yield s
    
def make():
    assert not os.path.exists(limitsinput_fn)
    ROOT.TH1.AddDirectory(1)
    in_f = ROOT.TFile(in_fn)
    f = ROOT.TFile(limitsinput_fn, 'recreate')

    h_int_lumi = ROOT.TH1D('h_int_lumi', '', 1, 0, 1)
    h_int_lumi.SetBinContent(1, int_lumi)

    h_observed = ROOT.TH1D('h_observed', '', nbins, bins)
    for i,v in enumerate(observed):
        h_observed.SetBinContent(i+1, v)
    
    # bkg comes from Jen's 2v_from_hists
    h_bkg_dbv  = to_TH1D(in_f.Get('h_1v_dbv') , 'h_bkg_dbv')
    h_bkg_dvv  = to_TH1D(in_f.Get('h_c1v_dvv'), 'h_bkg_dvv')

    h_bkg_dphi = ROOT.TH1D('h_bkg_dphi', '', 100, 0, pi)
    f_dphi = in_f.Get('f_dphi')
    for ibin in xrange(1, h_bkg_dphi.GetNbinsX()+1):
        a = h_bkg_dphi.GetXaxis().GetBinLowEdge(ibin)
        b = h_bkg_dphi.GetXaxis().GetBinLowEdge(ibin+1)
        h_bkg_dphi.SetBinContent(ibin, f_dphi.Integral(a,b)/(b-a))

    h_bkg_dbv.Scale(bkg_n1v/h_bkg_dbv.Integral())
    for h in h_bkg_dvv, h_bkg_dphi:
        h.Scale(bkg_n2v/h.Integral())

    h_bkg_dvv_rebin = h_bkg_dvv.Rebin(len(bins)-1, 'h_bkg_dvv_rebin', bins)
    move_overflow_into_last_bin(h_bkg_dvv_rebin)

    h_bkg_uncert = ROOT.TH1D('h_bkg_uncert', '', nbins, bins)
    for i,v in enumerate(bkg_uncert):
        h_bkg_uncert.SetBinContent(i+1, v)

    # now signals. grab the printout and put in signals.h for the fitting code to pick up
    if in_trees:
        title = in_trees
        sigs = glob(in_trees)
        sigs = [fn for fn in sigs if not fn.endswith('hip1p0.root')]
        sigs = \
            sorted(x for x in sigs if '_2015' not in x and '_hip' not in x) + \
            sorted(x for x in sigs if '_2015' not in x and '_hip' in x) + \
            sorted(x for x in sigs if '_2015' in x)
        sigs = [(os.path.basename(fn).replace('.root', ''), [fn]) for fn in sigs]
    elif in_scanpack_list:
        title = in_scanpack_list
        sigs = sorted(eval(open(in_scanpack_list).read()).items())

    nsigs = len(sigs)
    hs_sig = []
    name_list = ROOT.TH1C('name_list', title, nsigs, 0, nsigs) # I'm too stupid to get TList of TStrings to work in python

    for isig, (name, fns) in enumerate(sigs):
        isample = ndx2isample(isig)
        name_list.GetXaxis().SetBinLabel(-isample, name)

        sig_t = ROOT.TChain('mfvMiniTree/t')
        ngen = 0.
        for fn in fns:
            sig_f = ROOT.TFile.Open(fn)
            ngen += sig_f.Get('mfvWeight/h_sums').GetBinContent(1)
            sig_f.Close()
            sig_t.Add(fn)

        f.cd()

        h_dbv_name = 'h_signal_%i_dbv' % isample
        h_dbv = ROOT.TH1D(h_dbv_name, name, 1250, 0, 2.5)
        sig_t.Draw('dist0>>%s' % h_dbv_name, 'weight*(nvtx==1)')

        h_dvv_name = 'h_signal_%i_dvv' % isample
        h_dvv = ROOT.TH1D(h_dvv_name, name, 4000, 0, 4)
        sig_t.Draw('svdist>>%s' % h_dvv_name, 'weight*(nvtx>=2)')

        h_dphi_name = 'h_signal_%i_dphi' % isample
        h_dphi = ROOT.TH1D(h_dphi_name, name, 10, -3.15, 3.15)
        sig_t.Draw('svdphi>>%s' % h_dphi_name, 'weight*(nvtx>=2)')

        h_norm = ROOT.TH1D('h_signal_%i_norm' % isample, name, 2, 0, 2)
        norm = 1e-3 / ngen  # 1 fb xsec in pb / number of events read, int lumi will be added in ToyThrower
        h_norm.SetBinContent(1, norm)
        h_norm.SetBinContent(2, norm)

        h_dvv_rebin = h_dvv.Rebin(len(bins)-1, 'h_signal_%i_dvv_rebin' % isample, bins)
        move_overflow_into_last_bin(h_dvv_rebin)

        h_uncert = ROOT.TH1D('h_signal_%i_uncert' % isample, '', nbins, bins)
        for i,v in enumerate(sig_uncert):
            h_uncert.SetBinContent(i+1, v)

        hs_sig += [h_dbv, h_dvv, h_dphi, h_norm, h_dvv_rebin, h_uncert]

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


def signals_h():
    f = ROOT.TFile(limitsinput_fn)
    for isample, name in isamplename_iterator(f):
        print 'samples.push_back({%i, "%s", 0, 0});' % (isample, name)

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

def points():
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

def axes():
    kinds, masses, taus = points()
    masses = axisize(masses)
    taus   = axisize(taus)
    return kinds, masses, taus

def signal_efficiency():
    in_f = ROOT.TFile(limitsinput_fn)
    out_f = ROOT.TFile('signal_efficiency.root', 'recreate')

    kinds, masses, taus = axes()
    nmasses = len(masses) - 1
    ntaus = len(taus) - 1

    for kind in kinds:
        h = ROOT.TH2D('signal_efficiency_%s' % kind, ';mass (GeV);#tau (mm)', nmasses, masses, ntaus, taus)

        for ibin in xrange(1, nmasses+1):
            mass = h.GetXaxis().GetBinLowEdge(ibin)
            for jbin in xrange(1, ntaus+1):
                tau = h.GetYaxis().GetBinLowEdge(jbin)

                name = '%s_tau%05ium_M%04i' % (kind, int(tau*1000), mass)
                try:
                    isample = name2isample(in_f, name)
                except ValueError:
                    continue

                dvv = h_dvv(in_f, isample)

                n2v = int(dvv.Integral(2, 1000000)) # 2 for >=400 um, 3 for >=700um
                ngen = nevents(in_f, isample)

                e,l,u = wilson_score(n2v, ngen)
                ee = (u-l)/2

                h.SetBinContent(ibin, jbin, e)
                h.SetBinError  (ibin, jbin, ee)

        out_f.cd()
        h.Write()

    out_f.Write()
    out_f.Close()

if __name__ == '__main__':
    if 'make' in sys.argv:
        make()
    elif 'signals_h' in sys.argv:
        signals_h()
    elif 'draw' in sys.argv:
        draw()
    elif 'compare' in sys.argv:
        compare(*sys.argv[2:5])
    elif 'nevents' in sys.argv:
        for s in sample_iterator(ROOT.TFile(limitsinput_fn)):
            print s.name.ljust(30), '%6i' % int(nevents(f, s.isample))
    elif 'points' in sys.argv:
        print 'kinds = %r\nmasses = %r\ntaus = %r' % points()
    elif 'signal_efficiency' in sys.argv:
        signal_efficiency()
    else:
        print 'dunno'

import sys, os
from collections import defaultdict
from glob import glob
from gzip import GzipFile
from JMTucker.Tools import colors
from JMTucker.Tools.ROOTTools import ROOT, to_TH1D, to_array, get_integral, move_overflow_into_last_bin, set_style

set_style()

class Params(object):
    def __init__(self):
        self.bins = to_array(0., 0.04, 0.07, 4)
        self.nbins = len(self.bins)-1
        # 2015 is included in 2016. We scale/sum up 2015, 2016hip, 2016nonhip below, instead of that being done separately in
        # SignalEfficiencyCombiner--this simplifies the datacard and plot making downstream.
        self.years = '2016', '2017', '2018'
        self.nyears = len(self.years)
        import JMTucker.MFVNeutralino.AnalysisConstants as ac
        self.int_lumis = ac.scaled_int_lumi_2015p6, ac.scaled_int_lumi_2017, ac.scaled_int_lumi_2018
        self.fn = 'limitsinput.root'

gp = Params()

####

def name_list(f):
    return f.Get('name_list')
def nsamples(f):
    return name_list(f).GetNbinsX()
def available_code(f, isample):
    return int(name_list(f).GetBinContent(-isample))
def isample_available(f, isample, years):
    if not years: return True
    years = [str(year) for year in years]
    ac = available_code(f, isample)
    return all((ac & (1 << y)) for y, year in enumerate(gp.years) if year in years)
    
def details2name(kind, tau, mass):
    # same convention as scanpack: tau float:mm, mass int:GeV
    return '%s_tau%06ium_M%04i' % (kind, int(tau*1000), mass)
def _nameok(name):
    assert name.count('_tau') == 1 and name.count('um_') == 1 and name.count('_M') == 1
def name2kind(name):
    _nameok(name)
    return name.split('_tau')[0]
def name2tau(name):
    _nameok(name)
    return int(name.split('_tau')[1].split('um_')[0]) / 1000.
def name2mass(name):
    _nameok(name)
    return int(name.split('_M')[1].split('_')[0])
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

class sample_iterator(object):
    def __init__(self, f, require_years=[], test=False, slices_1d=False):
        self.f = f
        self.h = name_list(self.f)
        self.require_years = require_years
        self.test = test
        if test:
            raise NotImplementedError('test set')
        self.slices_1d = slices_1d
    def __iter__(self):
        for ibin in xrange(1, self.h.GetNbinsX()+1):
            if isample_available(self.f, -ibin, self.require_years):
                self.isample = -ibin
                self.name = self.h.GetXaxis().GetBinLabel(ibin)
                self.kind, self.tau, self.mass = name2details(self.name)

                if self.slices_1d:
                    if self.mass in (800, 1600, 2400, 3000) or self.tau in (0.3, 1., 10.):
                        yield self
                elif self.test:
                    pass
                else:
                    yield self

####

def make_bkg(f):
    # the first 3 sets of values override what's in 2v_from_jets
    observed = (1,0,0), (0,0,0), (0,0,0)
    bkg_n1v  = 1183, 1303, 908
    bkg_n2v  = 1, 1, 1 # this is not supposed to be the sum of observed, but could/should be set to the pre-fit expectation (predict2v.py)
    # but bkg_c1v is checked against what's in 2v_from_jets
    bkg_c1v = (0.509, 0.374, 0.117), (0.709, 0.257, 0.034), (0.650, 0.313, 0.037)

    bkg_uncert = [(1.25, 1.25, 1.69), (1.16, 1.29, 1.41), (1.19, 1.35, 1.53)] # combine lnN convention

    import statmodel
    bkg_uncert_stat = [statmodel.ebins['data100pc_%s_5track' % year] for year in gp.years]
    for y in xrange(gp.nyears):
        bkg_uncert[y] = [(a**2 + b**2)**0.5 for a,b in zip(bkg_uncert[y], bkg_uncert_stat[y])] # JMTBAD use proper gmN?

    def bkg_fn(year, which='default'):
        path = '/uscms/home/tucker/public/mfv/'
        if year == '2016':
            return path + '2v_from_jets_data_2015p6_5track_default_v15_v5.root'
        else:
            if which == 'c':
                which = 'btag_corrected_nom'
            else:
                assert which == 'default'
            return path + '2v_from_jets_data_%s_5track_%s_V27m.root' % (year, which)

    def bkg_f(year, which='default', _c={}):
        k = year, which
        if not _c.has_key(k):
            _c[k] = ROOT.TFile.Open(bkg_fn(*k))
        return _c[k]

    def cbkg_f(year):
        return bkg_f(year, which='c')

    ##

    print 'make_bkg:',
    for y, year in enumerate(gp.years):
        h_int_lumi = ROOT.TH1D('h_int_lumi_%s' % year, '', 1, 0, 1)
        h_int_lumi.SetBinContent(1, gp.int_lumis[y])

        h_observed = ROOT.TH1D('h_observed_%s' % year, '', gp.nbins, gp.bins)
        for i,v in enumerate(observed[y]):
            h_observed.SetBinContent(i+1, v)
    
        h_bkg_dbv = to_TH1D( bkg_f(year).Get('h_1v_dbv'),  'h_bkg_dbv_%s' % year)
        h_bkg_dvv = to_TH1D(cbkg_f(year).Get('h_c1v_dvv'), 'h_bkg_dvv_%s' % year)

        h_bkg_dbv.Scale(bkg_n1v[y]/get_integral(h_bkg_dbv)[0])
        h_bkg_dvv.Scale(bkg_n2v[y]/get_integral(h_bkg_dvv)[0])

        h = h_bkg_dvv_rebin = h_bkg_dvv.Rebin(gp.nbins, 'h_bkg_dvv_rebin_%s' % year, gp.bins)
        move_overflow_into_last_bin(h_bkg_dvv_rebin)
        for i in xrange(gp.nbins):
            if abs(bkg_c1v[y][i] - h.GetBinContent(i+1)/bkg_n2v[y]) > 0.001:
                print y,i, bkg_c1v[y][i], h.GetBinContent(i+1)/bkg_n1v[y]
                assert 0

        h_bkg_uncert = ROOT.TH1D('h_bkg_uncert_%s' % year, '', gp.nbins, gp.bins)
        for i,v in enumerate(bkg_uncert[y]):
            h_bkg_uncert.SetBinContent(i+1, v)

        f.cd()            
        for h in h_int_lumi, h_observed, h_bkg_dbv, h_bkg_dvv, h_bkg_dvv_rebin, h_bkg_uncert:
            h.SetTitle('')
            h.Write()

    print 'done'

class signalset(object):
    isamples = []
    def __init__(self, name, year, isample=None):
        self.name = name
        self.years = set()
        assert year in gp.years and year not in self.years
        self.years.add(year)

        if isample is None:
            isample = min(self.isamples) - 1 if self.isamples else -1
        self.isample = isample
        self.isamples.append(isample)

def make_signals_2015p6(f, name_list):
    # Pull 2015+6 values from previous limitsinput file.
    # (not all 2017+8 signal points exist there, will glue in later.)
    # Rescale+add how SignalEfficiencyCombiner did previously.  Go
    # ahead and store the rate already scaled by the integrated
    # luminosity. This makes the 2016 weighted sum situation easier
    # downstream.

    fn_2016_hip = '/uscms/home/tucker/public/mfv/limitsinput_data_v15v5_scanpack_merge_hip_1_2_2p6_3_3p6_removeddbar.root'
    fn_2016_nonhip = '/uscms/home/tucker/public/mfv/limitsinput_data_v15v5_scanpack_merge_1_1p5_2_2p5_2p7_3_3p5_removeddbar.root'
    name_list['title'] = name_list.get('title', '') + '+%s+%s' % (fn_2016_hip, fn_2016_nonhip)
    f_2015 = f_2016 = f_2016_nonhip = ROOT.TFile.Open(fn_2016_nonhip)
    f_2016_hip = ROOT.TFile.Open(fn_2016_hip)
    h_name_list_2016 = f_2016_nonhip.Get('name_list') # already checked that the two files are in sync
    def _hs(n):
        return [f_2015.Get(n), f_2016_hip.Get(n), f_2016_nonhip.Get(n)]
    def trigmult2016(x):
        return 1 # this was 0.99 in signal_efficiency, but now it's already in int_lumi at top
    def sf20156(x, pars=(0.9784, -1128., 1444.)):
        return trigmult2016(x) * (2. - pars[0] * ROOT.TMath.Erf((x-pars[1])/pars[2]))
    sfs = [sf20156, trigmult2016, trigmult2016]
    int_lumis = [2592.4, 19492., 16059.]

    nsigs = h_name_list_2016.GetNbinsX()
    for ibin in xrange(1, nsigs+1):
        if (ibin-1)%(nsigs/20) == 0:
            sys.stdout.write('\rmake_signals_2015p6: %i/%i' % (ibin-1, nsigs)); sys.stdout.flush()
        isample = -ibin
        bn = 'h_signal_%i_' % isample

        # convert sample name to new format--really only more digits in tau field
        old_name = f_2016.Get(bn + 'norm').GetTitle()
        mass = name2mass(old_name) # needed in scalefactor too
        new_name = details2name(name2kind(old_name), name2tau(old_name), mass)
        name_list[new_name] = signalset(new_name, '2016', isample)

        norms = _hs(bn + 'norm')
        ngens = [1e-3/h.GetBinContent(2) for h in norms]
        ngentot = sum(ngens[1:]) # hip/nonhip are the only independent samples, 2015 is just 2016 that we rescale

        for n in 'dbv', 'dphi', 'dvv', 'dvv_rebin':
            hs = _hs(bn + n)
            for h,ng,sf,il in zip(hs, ngens, sfs, int_lumis):
                if n != 'dvv_rebin':
                    h.Rebin(10) # did too many bins last time
                h.Scale(sf(mass) * 1e-3 * il / ng)
                    
            h = hs.pop(0)
            for h2 in hs:
                h.Add(h2)

            h.SetName(bn + n + '_2016')
            h.SetTitle(new_name + '_2016')
            f.cd(); h.Write()

        f.cd()

        h = ROOT.TH1D(bn + 'uncert_2016', new_name + '_2016', gp.nbins, gp.bins)
        for ib in xrange(1,gp.nbins+1): h.SetBinContent(ib, 1.24) # ignore old hist and just set by new convention
        h.Write()

        h = ROOT.TH1D(bn + 'ngen_2016', new_name + '_2016', 1,0,1)
        h.SetBinContent(1, ngentot)
        h.Write()

    print '\rmake_signals_2015p6: done       '

def make_signals_2017p8(f, name_list):
    # 2017,8 are from minitrees (the 100kevt official samples) and scanpack.
    scanpack_list = '/uscms/home/tucker/public/mfv/scanpacks/2017p8/scanpack1D.merged.list.gz'
    trees = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV27m/mfv*.root'
    title = []
    sigs = {}

    def sig_uncert(name): # JMTBAD implement different sig uncerts per trackmover study when done
        # must be in combine lnN convention
        u = 1.24 
        return (u,u,u)

    if scanpack_list:
        title.append(scanpack_list)
        sigs.update(eval(GzipFile(scanpack_list).read()))
    if trees:
        title.append(trees)
        sigs.update({os.path.basename(fn).replace('.root', '') : [fn] for fn in sorted(glob(trees))}) # overrides scanpack entries
    name_list['title'] = name_list.get('title', '') + '+' + '+'.join(title)

    nsigs = len(sigs)
    for isig, (name_year, fns) in enumerate(sigs.iteritems()):
        if isig%(nsigs/20) == 0:
            sys.stdout.write('\rmake_signals_2017p8: %i/%i' % (isig, nsigs)); sys.stdout.flush()

        name, year = name_year.rsplit('_',1)
        if name_list.has_key(name):
            s = name_list[name]
            s.years.add(year)
        else:
            s = name_list[name] = signalset(name, year)
        n = lambda x: 'h_signal_%i_%s_%s'  % (s.isample, x, year)

        ngen = 0.
        sig_t = ROOT.TChain('mfvMiniTree/t')
        for fn in fns:
            sig_f = ROOT.TFile.Open(fn)
            ngen += sig_f.Get('mfvWeight/h_sums').GetBinContent(1)
            sig_f.Close()
            sig_t.Add(fn)

        iyear = gp.years.index(year)
        scale = 1e-3 * gp.int_lumis[iyear] / ngen # JMTBAD * sf for L1 EE prefiring, hem15/16, etc.

        ROOT.TH1.AddDirectory(1) # the Draw>> output goes off into the ether without this stupid crap
        h_dbv  = ROOT.TH1D(n('dbv'),  '', 125, 0, 2.5)
        h_dvv  = ROOT.TH1D(n('dvv'),  '', 400, 0, 4)
        h_dphi = ROOT.TH1D(n('dphi'), '', 10, -3.15, 3.15)
        sig_t.Draw('dist0>>%s'  % n('dbv'),  'weight*(nvtx==1)')
        sig_t.Draw('svdist>>%s' % n('dvv'),  'weight*(nvtx>=2)')
        sig_t.Draw('svdphi>>%s' % n('dphi'), 'weight*(nvtx>=2)')
        ROOT.TH1.AddDirectory(0)
        for h in h_dbv, h_dvv, h_dphi:
            h.SetDirectory(0)
            h.Scale(scale)
        
        h_dvv_rebin = h_dvv.Rebin(gp.nbins, n('dvv_rebin'), gp.bins)
        move_overflow_into_last_bin(h_dvv_rebin)

        h_ngen = ROOT.TH1D(n('ngen'), '', 1,0,1)
        h_ngen.SetBinContent(1, ngen)
        
        h_uncert = ROOT.TH1D(n('uncert'), '', gp.nbins, gp.bins)
        for i,v in enumerate(sig_uncert(name_year)):
            h_uncert.SetBinContent(i+1, v)
        
        f.cd()
        for h in h_dbv, h_dphi, h_dvv, h_dvv_rebin, h_uncert, h_ngen:
            h.SetTitle(name_year)
            h.Write()

    print '\rmake_signals_2017p8: done       '

def make():
    for i in xrange(20):
        print colors.error("don't forget:    2015/6 pileup weights     sig uncert per year/point     pythia8240 rescaling/regen     PDFs     L1 EE prefiring     HEM15/16     anything else?")

    assert not os.path.exists(gp.fn)
    ROOT.TH1.AddDirectory(0)
    f = ROOT.TFile(gp.fn, 'recreate')

    make_bkg(f)

    name_list = {}
    make_signals_2015p6(f, name_list)
    make_signals_2017p8(f, name_list)

    title = name_list.pop('title')
    isamples = sorted([s.isample for s in name_list.itervalues()], reverse=True)
    assert isamples == range(-1,isamples[-1]-1,-1)

    nsigs = len(isamples)
    h = ROOT.TH1C('name_list', title, nsigs, 0, nsigs)
    missing = defaultdict(list)
    for s in name_list.itervalues():
        miss = tuple(sorted(set(gp.years) - s.years))
        missing[miss].append(s.name)
        c = sum((int(year in s.years) << y) for y, year in enumerate(gp.years))
        h.GetXaxis().SetBinLabel(-s.isample, s.name)
        h.SetBinContent(-s.isample, c)
    f.cd(); h.Write()
    f.Close()

    if missing:
        w = colors.warning
        print w('missing summary:')
        for k in sorted(missing):
            if not k:
                continue
            l = sorted(missing[k])
            n = len(l)
            print w(repr(tuple(int(y) for y in sorted(k))) + ': %i samples' % n)
            for i in xrange(0, n, 6):
                for j in xrange(i, min(i+6, n)):
                    print w('    ' + l[j]),
                print

def ngen(f, isample, year):
    h = f.Get('h_signal_%i_ngen_%s' % (isample, year))
    return int(h.GetBinContent(1)) if h else -1

'''
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
'''

def draw():
    ps = plot_saver(plot_dir('o2t_templates_run2'), size=(600,600))
    f = ROOT.TFile(gp.fn)

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
        f = ROOT.TFile(gp.fn)
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
    in_f = ROOT.TFile(gp.fn)
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
    raise ValueError('propagate change to use stored rate already normalized to int lumi')
    from signal_efficiency import SignalEfficiencyCombiner
    combiner = SignalEfficiencyCombiner() #simple=gp.fn)
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
    elif 'ngen' in sys.argv:
        f = ROOT.TFile(gp.fn)
        years = sys.argv[sys.argv.index('ngen'):]
        for s in sample_iterator(f, years, slices_1d=True):
            print '%6i' % s.isample, s.name.ljust(35), ' '.join(['%10s']*gp.nyears) % tuple(ngen(f, s.isample, year) for year in gp.years)
        #nevents_plot()
    elif 'points' in sys.argv:
        print 'kinds = %r\nmasses = %r\ntaus = %r' % points()
    elif 'signal_efficiency' in sys.argv:
        signal_efficiency()
    else:
        print 'dunno'

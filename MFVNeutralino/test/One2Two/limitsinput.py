import sys, os
from collections import defaultdict
from glob import glob
from gzip import GzipFile
from JMTucker.Tools import colors
from JMTucker.Tools.ROOTTools import ROOT, to_TH1D, to_array, get_integral, move_overflow_into_last_bin, set_style, lerp, bilerp, plot_saver, plot_dir

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
        self.l1eeprefiring_2017 = True # whether to simulate L1 EE prefiring in 2017
        self.hem1516_2018 = True # whether to simulate the HEM 15/16 failure in for part of 2018

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
    
# NOTE! Resonance mass is only needed for bookkeeping, since the resonance itself is prompt while its decay products are the LLPs
def details2name(kind, tau, mass, massResonance=None):
    # same convention as scanpack: tau float:mm, mass int:GeV
    if "splitSUSY" in kind :
        return '%s_tau%09ium_M%04i_100' % (kind, int(tau*1000), mass) # FIXME assumes the LSP is 100 GeV always
    elif "HtoLLP" in kind or "ZprimetoLLP" in kind :
        if tau < 1 :
            taustr = "0p%i" % int(tau*10)
        else :
            taustr = int(tau)
        return '%s_tau%smm_M%i_%i' % (kind, taustr, massResonance, mass)
    elif "Stealth" in kind :
        if tau < 0.1 :
            taustr = "0p0%i" % int(tau*100)
        elif tau >= 0.1 and tau < 1 :
            taustr = "0p%i" % int(tau*10)
        else :
            taustr = int(tau)
        #print "details2name: " + '%s_mStop_%i_mS_%i_ctau_%s' % (kind, massResonance, mass, taustr)
        return '%s_mStop_%i_mS_%i_ctau_%s' % (kind, massResonance, mass, taustr)
    else :
        return '%s_tau%06ium_M%04i' % (kind, int(tau*1000), mass)

def _nameok(name):
    assert (name.count('_tau') == 1 and (name.count('um_') == 1 or name.count('mm_') == 1) and name.count('_M') == 1) or (name.count('_ctau_') == 1 and name.count('_mStop_') == 1 and name.count('_mS_') == 1)

def name2kind(name):
    _nameok(name)
    if '_tau' in name :
        return name.split('_tau')[0]
    elif '_mStop_' in name :
        # for Stealth SUSY samples
        return name.split('_mStop_')[0]
    else :
        print "unsupported name, surprised _nameok didn't already fail: %s" % name
        return None

def name2tau(name):
    _nameok(name)
    if 'um_' in name :
        return int(name.split('_tau')[1].split('um_')[0]) / 1000.
    elif 'mm_' in name :
        return float((name.split('_tau')[1].split('mm_')[0]).replace('p','.'))
    else :
        return float((name.split('_ctau_')[1]).replace('p','.').split('_')[0])

def name2mass(name):
    _nameok(name)

    # for Stealth SUSY samples
    if '_mStop_' in name :
        listOfMasses = name.split('_mStop_')[1].split('_ctau_')[0].split('_mS_')
        mass = int(listOfMasses[1])
        massResonance = int(listOfMasses[0])
    else :
        listOfMasses = name.split('_M')[1].split('_')
        if len(listOfMasses) == 1 :
            mass = int(listOfMasses[0])
            massResonance = None
        else :
            mass = int(listOfMasses[1])
            massResonance = int(listOfMasses[0])
    return mass, massResonance

def name2details(name):
    mass, massResonance = name2mass(name) 
    return name2kind(name), name2tau(name), mass, massResonance

def name2taumass(name):
    mass, massResonance = name2mass(name) 
    return name2tau(name), mass, massResonance

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

    class Sample(object):
        def __init__(self, isample, name):
            self.isample = isample
            self.name = name
            self.kind, self.tau, self.mass, self.massResonance = name2details(self.name)
            #print self.name

    def __iter__(self):
        for ibin in xrange(1, self.h.GetNbinsX()+1):
            if isample_available(self.f, -ibin, self.require_years):
                s = self.Sample(-ibin, self.h.GetXaxis().GetBinLabel(ibin))
                if self.slices_1d:
                    if s.mass in (800, 1600, 2400, 3000) or s.tau in (0.3, 1., 10.):
                        yield s
                elif self.test:
                    pass
                else:
                    yield s

####

def make_bkg(f):
    # the first 3 sets of values override what's in 2v_from_jets
    observed = (1,0,0), (0,0,0), (0,0,0)
    bkg_n1v  = 1183, 1303, 908
    bkg_n2v  = 1, 0.241, 0.111 # this is not supposed to be the sum of observed, but could/should be set to the pre-fit expectation (predict2v.py)
    # but bkg_c1v is checked against what's in 2v_from_jets
    bkg_c1v = (0.509, 0.374, 0.117), (0.709, 0.257, 0.034), (0.650, 0.313, 0.037)

    bkg_uncert = [(1.25, 1.25, 1.69), (1.16, 1.30, 1.51), (1.19, 1.30, 1.91)] # combine lnN convention

    import statmodel
    bkg_uncert_stat = [statmodel.ebins['data100pc_%s_5track' % year] for year in gp.years]
    for y in xrange(gp.nyears):
        bkg_uncert[y] = [(a**2 + b**2)**0.5 for a,b in zip(bkg_uncert[y], bkg_uncert_stat[y])] # JMTBAD use proper gmN?

    bkg_stat_uncert = [(1.071, 1.128, 1.465), (1.173, 1.216, 1.454), (1.217, 1.238, 1.586)] # stat errors uncorrelated
    bkg_syst_uncert = [(0.758, 1.218, 1.542), (0.743, 1.338, 1.389), (0.766, 1.315, 1.760)] # syst error anti-correlated

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
        h_bkg_stat_uncert = ROOT.TH1D('h_bkg_uncert_stat_%s' % year, '', gp.nbins, gp.bins)
        h_bkg_syst_uncert = ROOT.TH1D('h_bkg_uncert_syst_%s' % year, '', gp.nbins, gp.bins)
        for i,v in enumerate(bkg_uncert[y]):
            h_bkg_uncert.SetBinContent(i+1, v)
        for i,v in enumerate(bkg_stat_uncert[y]):
            h_bkg_stat_uncert.SetBinContent(i+1, v)
        for i,v in enumerate(bkg_syst_uncert[y]):
            h_bkg_syst_uncert.SetBinContent(i+1, v)

        f.cd()            
        for h in h_int_lumi, h_observed, h_bkg_dbv, h_bkg_dvv, h_bkg_dvv_rebin, h_bkg_uncert, h_bkg_stat_uncert, h_bkg_syst_uncert:
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
        self.ipair = None

        if isample is None:
            isample = self.next_isample()
        self.isample = isample
        self.isamples.append(isample)

    @classmethod
    def next_isample(cls):
        return min(cls.isamples) - 1 if cls.isamples else -1

def sig_uncert_pdf(name_year):
    name, _ = name_year.rsplit('_',1)
    kind, tau, mass, massResonance = name2details(name)
    tau = int(tau*1000) # back to um

    fcns = {
          300: lambda x: 1.780e-07*x**2 + -0.0002978*x + 0.1333  if x < 877 else 3.109e-05*x + -0.01826,
         1000: lambda x: 1.180e-07*x**2 + -0.0001803*x + 0.07347 if x < 873 else 2.069e-05*x + -0.01206,
        10000: lambda x: 1.203e-07*x**2 + -0.0002023*x + 0.08985 if x < 877 else 1.413e-05*x + -0.007393,
          }

    ab = None
    if tau <= 300:
        p = fcns[300](mass)
    elif tau >= 10000:
        p = fcns[10000](mass)
    elif 300 < tau <= 1000:
        ab = 300,1000
    elif 1000 < tau <= 10000:
        ab = 1000,10000
    if ab is not None:
        a,b = ab
        fa = fcns[a](mass)
        fb = fcns[b](mass)
        p = lerp(tau, a, b, fa, fb)

    return p

def sig_uncert_alphas(name_year):
    name, year = name_year.rsplit('_',1)
    kind, tau, mass, massResonance = name2details(name)
    tau = int(tau*1000) # back to um

    fcns = {
            ('mfv_neu', 300, '2017') : lambda x: 8.412357E-02 + -1.492608E-04*x if x < 500 else 1.366428E-02 + -8.342191E-06*x if x < 1000 else 5.163025E-03,
            ('mfv_neu', 1000, '2017') : lambda x: 2.482616E-02 + -1.677113E-05*x if x < 500 else 2.930580E-02 + -2.573041E-05*x if x < 1000 else 3.386116E-03,
            ('mfv_neu', 10000, '2017') : lambda x: 7.566047E-02 + -1.147594E-04*x if x < 500 else 3.476814E-02 + -3.297473E-05*x if x < 1000 else 1.611145E-03,
            ('mfv_neu', 300, '2018') : lambda x: 3.826184E-02 + -3.562455E-05*x if x < 500 else 3.727006E-02 + -3.570847E-05*x if x < 1000 else 4.543582E-03,
            ('mfv_neu', 1000, '2018') : lambda x: 1.381364E-01 + -2.434682E-04*x if x < 500 else 3.364486E-02 + -3.615300E-05*x if x < 1000 else 2.315426E-03,
            ('mfv_neu', 10000, '2018') : lambda x: 1.395761E-01 + -2.494418E-04*x if x < 500 else 2.779135E-02 + -2.693736E-05*x if x < 1000 else 1.683538E-03,
            ('mfv_stopdbardbar', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_stopdbardbar', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_stopdbardbar', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_stopdbardbar', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_stopdbardbar', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_stopdbardbar', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
            ('mfv_HtoLLPto4b', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_HtoLLPto4b', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_HtoLLPto4b', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_HtoLLPto4b', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_HtoLLPto4b', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_HtoLLPto4b', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
            ('mfv_HtoLLPto4j', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_HtoLLPto4j', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_HtoLLPto4j', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_HtoLLPto4j', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_HtoLLPto4j', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_HtoLLPto4j', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
            ('mfv_ZprimetoLLPto4b', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_ZprimetoLLPto4b', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_ZprimetoLLPto4b', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_ZprimetoLLPto4b', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_ZprimetoLLPto4b', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_ZprimetoLLPto4b', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
            ('mfv_ZprimetoLLPto4j', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_ZprimetoLLPto4j', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_ZprimetoLLPto4j', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_ZprimetoLLPto4j', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_ZprimetoLLPto4j', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_ZprimetoLLPto4j', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
            ('mfv_StealthSHH', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_StealthSHH', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_StealthSHH', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_StealthSHH', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_StealthSHH', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_StealthSHH', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
            ('mfv_StealthSYY', 300, '2017') : lambda x: 4.162419E-02 + -6.643979E-05*x if x < 500 else 1.544804E-02 + -1.408750E-05*x if x < 1000 else 2.704658E-03,
            ('mfv_StealthSYY', 1000, '2017') : lambda x: 2.941164E-02 + -4.224396E-05*x if x < 500 else 1.485796E-02 + -1.313661E-05*x if x < 1000 else 1.379749E-03,
            ('mfv_StealthSYY', 10000, '2017') : lambda x: 3.286446E-02 + -4.490090E-05*x if x < 500 else 1.932494E-02 + -1.782184E-05*x if x < 1000 else 1.427578E-03,
            ('mfv_StealthSYY', 300, '2018') : lambda x: 5.826609E-02 + -9.844897E-05*x if x < 500 else 1.450902E-02 + -1.250891E-05*x if x < 1000 else 2.639510E-03,
            ('mfv_StealthSYY', 1000, '2018') : lambda x: 4.604910E-02 + -6.757893E-05*x if x < 500 else 2.369948E-02 + -2.466162E-05*x if x < 1000 else 1.553165E-03,
            ('mfv_StealthSYY', 10000, '2018') : lambda x: 6.065365E-02 + -1.067197E-04*x if x < 500 else 1.328695E-02 + -1.332486E-05*x if x < 1000 else 1.429334E-03,
          }

    ab = None
    if tau <= 300:
        p = fcns[(kind, 300, year)](mass)
    elif tau >= 10000:
        p = fcns[(kind, 10000, year)](mass)
    elif 300 < tau <= 1000:
        ab = 300,1000
    elif 1000 < tau <= 10000:
        ab = 1000,10000
    if ab is not None:
        a,b = ab
        fa = fcns[(kind, a, year)](mass)
        fb = fcns[(kind, b, year)](mass)
        p = lerp(tau, a, b, fa, fb)

    return p

def make_signals_2015p6(f, name_list):
    # Pull 2015+6 values from previous-format limitsinput file(s).
    # (Not all 2017+8 signal points exist in the final one for the
    # 2016 paper, but we make new ones now using the scanpack2017p8_2016 branch.)
    # Rescale+add how SignalEfficiencyCombiner did previously.  Go
    # ahead and store the rate already scaled by the integrated
    # luminosity. This makes the 2016 weighted sum situation easier
    # downstream.

    fnpairs = [ # (hip, nonhip)--the first pair are to be the final 2016 paper one, the rest define newly generated signal points
        #('/uscms/home/tucker/public/mfv/limitsinput_data_v15v5_scanpack_merge_hip_1_2_2p6_3_3p6_removeddbar.root', 
        # '/uscms/home/tucker/public/mfv/limitsinput_data_v15v5_scanpack_merge_1_1p5_2_2p5_2p7_3_3p5_removeddbar.root',),
        #('/uscms/home/tucker/public/mfv/limitsinput_scanpack1D2016missing_hip.root',
        # '/uscms/home/tucker/public/mfv/limitsinput_scanpack1D2016missing.root',),
        #('/uscms/home/tucker/public/mfv/limitsinput_scanpack4p6_hip.root',
        # '/uscms/home/tucker/public/mfv/limitsinput_scanpack4p6.root',),
        #('/uscms/home/joeyr/work/split_susy/mfv_946p1/src/JMTucker/MFVNeutralino/test/One2Two/limitsinput_2016.root',
        # '/uscms/home/joeyr/work/split_susy/mfv_946p1/src/JMTucker/MFVNeutralino/test/One2Two/limitsinput_2016.root',),
         ('/uscms/home/joeyr/dark_sector_review_paper/mfv_8035/src/JMTucker/MFVNeutralino/test/One2Two/limitsinput.root',), # modified code below to only use one 2016 file (since we don't have a HIP one for this study)
        ]

    def trigmult2016(x):
        return 1 # this was 0.99 in signal_efficiency, but now it's already in int_lumi at top
    def sf20156(x, pars=(0.9784, -1128., 1444.)):
        return trigmult2016(x) * (2. - pars[0] * ROOT.TMath.Erf((x-pars[1])/pars[2]))
    sfs = [sf20156, trigmult2016]
    int_lumis = [2592.4, 16059.+19492.]

    for ipair, (fn_2016,) in enumerate(fnpairs):
        name_list['title'] = name_list.get('title', '') + '+%s' % (fn_2016)
        f_2015 = f_2016 = ROOT.TFile.Open(fn_2016)
        h_name_list_2016 = f_2016.Get('name_list') # already checked that the two files are in sync
        def _hs(n):
            return [f_2015.Get(n), f_2016.Get(n)]

        nsigs = h_name_list_2016.GetNbinsX()
        for ibin in xrange(1, nsigs+1):
            #if nsigs > 20 and (ibin-1)%(nsigs/20) == 0:
            print('\rmake_signals_2015p6: pair %i/%i, %i/%i' % (ipair+1, len(fnpairs), ibin, nsigs)); sys.stdout.flush()

            old_isample = -ibin
            new_isample = old_isample if ipair == 0 else signalset.next_isample()
            old_bn = 'h_signal_%i_' % old_isample
            new_bn = 'h_signal_%i_' % new_isample

            # convert sample name to new format--really only more digits in tau field
            old_name = f_2016.Get(old_bn + 'norm').GetTitle()
            mass, massResonance = name2mass(old_name) # needed in scalefactor too
            new_name = details2name(name2kind(old_name), name2tau(old_name), mass, massResonance)

            if name_list.has_key(new_name):
                print colors.warning('\nwarning: %s found in ipair %i with isample %i was found in previous ipair %s with isample %i, skipping' % (new_name, ipair, old_isample, name_list[new_name].ipair, name_list[new_name].isample))
                continue

            name_list[new_name] = ss = signalset(new_name, '2016', new_isample)
            ss.ipair = ipair

            norms = _hs(old_bn + 'norm')
            ngens = [(1e-3/h.GetBinContent(2)) for h in norms]
            ngentot = sum(ngens[1:]) # hip/nonhip are the only independent samples, 2015 is just 2016 that we rescale

            for n in 'dbv', 'dphi', 'dvv', 'dvv_rebin':
                hs = _hs(old_bn + n)
                for h,ng,sf,il in zip(hs, ngens, sfs, int_lumis):
                    if n == 'dbv' or n == 'dvv':
                        h.Rebin(10) # did too many bins last time

                    h.Scale(sf(mass) * 1e-3 * il / ng)

                h = hs.pop(0)
                for h2 in hs:
                    h.Add(h2)

                h.SetName(new_bn + n + '_2016')
                h.SetTitle(new_name + '_2016')
                f.cd(); h.Write()

            f.cd()

            h = ROOT.TH1D(new_bn + 'uncert_2016', new_name + '_2016', gp.nbins, gp.bins)
            uncerts = [0.24, sig_uncert_pdf(new_name + '_2016')] # ignore old hist, just use the previous total 24%
            for ib in xrange(1,gp.nbins+1): h.SetBinContent(ib, 1+sum(x**2 for x in uncerts)**0.5)
            h.Write()

            h = ROOT.TH1D(new_bn + 'ngen_2016', new_name + '_2016', 1,0,1)
            h.SetBinContent(1, ngentot)
            h.Write()

        print '\rmake_signals_2015p6: done with pair %i             ' % (ipair+1)


def hlp(x,l):
    x = int(x)
    l,n = sorted(l), len(l)
    if x < l[0]:
        x = l[0]
        a = b = 0
    elif x >= l[-1]:
        x = l[-1]
        a = b = n-1
    else:
        for i,y in enumerate(l[:-1]):
            if y <= x < l[i+1]:
                a,b = i, i+1
                break
    return x, l, a, b, l[a], l[b]

def sig_trackmover_per_event_unc(name_year, debug=False, syst=''):
    name, year = name_year.rsplit('_',1)
    kind, tau, mass, massResonance = name2details(name)
    tau = int(tau*1000) # back to um

    masses = [400,600,800,1200,1600,3000]
    taus = [100,300,1000,10000,30000]
    kind = kind + syst

    trackmover = { # after kind and year indices, rows are masses, cols are taus, each in same order as above two lists
        'mfv_stopdbardbar': { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_splitSUSY':    { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_HtoLLPto4b':   { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_HtoLLPto4j':   { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_ZprimetoLLPto4b': { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_ZprimetoLLPto4j': { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_StealthSHH': { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_StealthSYY': { '2017': ( (0.2384, 0.1904, 0.1492, 0.1050, 0.1002),
                                        (0.2496, 0.2014, 0.1604, 0.1152, 0.1104),
                                        (0.2534, 0.2100, 0.1716, 0.1264, 0.1194),
                                        (0.2584, 0.2142, 0.1756, 0.1278, 0.1204),
                                        (0.2582, 0.2144, 0.1752, 0.1264, 0.1192),
                                        (0.2684, 0.2186, 0.1760, 0.1244, 0.1158), ),
                              '2018': ( (0.3068, 0.2600, 0.2344, 0.2010, 0.1968),
                                        (0.3084, 0.2616, 0.2396, 0.2044, 0.1886),
                                        (0.3084, 0.2654, 0.2438, 0.1900, 0.1910),
                                        (0.3120, 0.2690, 0.2274, 0.1940, 0.1926),
                                        (0.3140, 0.2594, 0.2320, 0.1974, 0.1940),
                                        (0.3104, 0.2634, 0.2364, 0.2004, 0.1950), ), },
        'mfv_neu':          { '2017': ( (0.276, 0.193, 0.11, 0.058, 0.059),
                                        (0.243, 0.166, 0.093, 0.043, 0.044),
                                        (0.22, 0.153, 0.088, 0.036, 0.037),
                                        (0.189, 0.138, 0.081, 0.029, 0.029),
                                        (0.163, 0.124, 0.075, 0.024, 0.024),
                                        (0.132, 0.101, 0.063, 0.019, 0.016), ),
                              '2018': ( (-0.054, -0.002, 0.015, 0.01, 0.008),
                                        (-0.012, 0.019, 0.018, 0.008, 0.01),
                                        (0.003, 0.022, 0.018, 0.009, 0.009),
                                        (0.017, 0.028, 0.022, 0.009, 0.01),
                                        (0.029, 0.034, 0.027, 0.01, 0.009),
                                        (0.042, 0.043, 0.032, 0.011, 0.009), ), }, 
        'mfv_neu_stat_unc': { '2017': ( (5.157, 2.619, 1.565, 1.108, 1.516),
                                        (2.543, 1.175, 0.667, 0.395, 0.48),
                                        (1.811, 0.766, 0.422, 0.218, 0.245),
                                        (1.522, 0.592, 0.323, 0.151, 0.16),
                                        (1.381, 0.536, 0.286, 0.128, 0.133),
                                        (1.471, 0.486, 0.253, 0.107, 0.098), ),
                              '2018': ( (8.097, 3.639, 2.159, 1.6, 2.058),
                                        (3.7, 1.563, 0.836, 0.511, 0.608),
                                        (2.675, 1.024, 0.522, 0.273, 0.31),
                                        (2.186, 0.784, 0.399, 0.189, 0.202),
                                        (2.036, 0.694, 0.358, 0.165, 0.166),
                                        (1.966, 0.622, 0.313, 0.133, 0.127), ), },
         'mfv_neu_toc_unc': { '2017': ( (4.769, 1.527, 1.973, 4.487, 4.841),
                                        (4.752, 1.456, 1.061, 2.644, 3.087),
                                        (2.92, 0.477, 0.324, 1.73, 2.078),
                                        (0.176, 1.229, 0.894, 0.64, 0.972),
                                        (1.346, 2.293, 1.784, 0.181, 0.423),
                                        (3.692, 3.568, 2.717, 0.492, 0.182), ),
                              '2018': ( (13.768, 8.186, 6.416, 8.13, 7.676),
                                        (13.729, 7.804, 4.942, 4.641, 5.165),
                                        (12.017, 6.554, 4.069, 3.446, 3.771),
                                        (8.099, 4.175, 2.24, 2.102, 2.355),
                                        (5.819, 2.845, 1.346, 1.337, 1.51),
                                        (1.54, 0.141, 0.598, 0.28, 0.511), ), },
'mfv_neu_closeseedtk_unc':  { '2017': ( (3.155, 1.88, 1.087, 0.666, 0.718),
                                        (2.656, 1.586, 0.875, 0.481, 0.502),
                                        (2.248, 1.424, 0.807, 0.389, 0.409),
                                        (1.767, 1.191, 0.687, 0.291, 0.307),
                                        (1.423, 1.003, 0.593, 0.229, 0.24),
                                        (0.97, 0.7, 0.43, 0.156, 0.145), ),
                              '2018': ( (4.168, 2.175, 1.178, 0.791, 0.799),
                                        (3.21, 1.829, 0.936, 0.484, 0.497),
                                        (2.838, 1.633, 0.858, 0.393, 0.394),
                                        (2.2, 1.386, 0.762, 0.304, 0.296),
                                        (1.835, 1.17, 0.667, 0.249, 0.23),
                                        (1.182, 0.838, 0.507, 0.174, 0.159), ), }, }
    vtm = trackmover[kind][year]

    # just do linear interpolation--could fit, but the final result in the limits won't depend strongly on this
    mass, ms, mia, mib, mxa, mxb = mmm = hlp(mass, masses)
    tau,  ts, tia, tib, txa, txb = ttt = hlp(tau,  taus)

    if mia == mib and tia == tib:
        vtm = vtm[mia][tia]
    elif mia == mib:
        vtm = lerp(tau,  txa, txb, vtm[mia][tia], vtm[mia][tib])
    elif tia == tib:
        vtm = lerp(mass, mxa, mxb, vtm[mia][tia], vtm[mib][tia])
    else:
        points = [(mxa, txa, vtm[mia][tia]), (mxa, txb, vtm[mia][tib]), (mxb, txa, vtm[mib][tia]), (mxb, txb, vtm[mib][tib])]
        vtm = bilerp(mass, tau, points)

    if debug:
        print name_year, 'mmm', mmm, 'ttt', ttt

    return vtm

def sig_datamcSF_2017p8(name_year, debug=False):
    vtm = sig_trackmover_per_event_unc(name_year, debug)
    return 1 - vtm / 2 # trackmover is in the form 2 * (1 - TM_data / TM_MC)

def sig_uncert_2017p8(name_year, debug=False):
    vtm = (1 / sig_datamcSF_2017p8(name_year, debug))**2 - 1
    uncerts = [vtm]
    uncerts += [sig_uncert_pdf(name_year)]
    uncerts += [sig_uncert_alphas(name_year)]

    if 'mfv_neu' in name_year:
        for unc in ('_stat_unc', '_toc_unc', '_closeseedtk_unc'):
            uncerts += [sig_trackmover_per_event_unc(name_year, debug, unc) / 100.]

    uncerts += [x/100. for x in (3,1,5,2,2,1)] # list from AN + the last '1' is for L1EE prefiring in 2017 and HEM15/16 in 2018

    u = 1 + sum(x**2 for x in uncerts)**0.5 # final number must be in combine lnN convention
    if debug:
        print name_year, '->', vtm, '    u = %.4f' % u
    return u,u,u

def make_signals_2017p8(f, name_list):
    # 2017,8 are from minitrees (the 100kevt official samples) and scanpack.
    #scanpack_list = '/uscms/home/tucker/public/mfv/scanpacks/2017p8/scanpack1D_4_4p7_4p8.merged.list.gz'
    scanpack_list = None
    #trees = '/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreview_withGenInfom/reweighted/mfv*.root'
    trees = '/eos/user/j/jreicher/dark_sector_review/StealthSUSY/reweighted/mfv*.root'
    title = []
    sigs = {}

    if scanpack_list:
        title.append(scanpack_list)
        sigs.update(eval(GzipFile(scanpack_list).read()))
    if trees:
        title.append(trees)
        sigs.update({os.path.basename(fn).replace('.root', '') : [fn] for fn in sorted(glob(trees)) if not "2016" in fn}) # overrides scanpack entries
    name_list['title'] = name_list.get('title', '') + '+' + '+'.join(title)

    nsigs = len(sigs)
    for isig, (name_year, fns) in enumerate(sigs.iteritems()):
        #if nsigs > 20 and isig%(nsigs/20) == 0:
        print('\rmake_signals_2017p8: %i/%i' % (isig, nsigs)); sys.stdout.flush()

        name, year = name_year.rsplit('_',1)
        if name_list.has_key(name):
            s = name_list[name]
            s.years.add(year)
        else:
            s = name_list[name] = signalset(name, year)
        n = lambda x: 'h_signal_%i_%s_%s'  % (s.isample, x, year)

        ngen = 0.
        t = ROOT.TChain('mfvMiniTree/t')
        for fn in fns:
            sig_f = ROOT.TFile.Open(fn)

            ngen += sig_f.Get('mfvWeight/h_sums').GetBinContent(1)
            sig_f.Close()
            t.Add(fn)

        if year == '2017' and gp.l1eeprefiring_2017:
            t.SetAlias('jet_l1ee', 'abs(jet_eta) > 2.25 && jet_pt > 100')
            t.SetAlias('njets_l1ee', 'Sum$(!jet_l1ee)')
            t.SetAlias('jetht_l1ee', 'Sum$(jet_pt * (jet_pt > 40 && !jet_l1ee))')
            t.SetAlias('limitsinput_pass', '(njets_l1ee >= 4 && jetht_l1ee >= 1200)')
        elif year == '2018' and gp.hem1516_2018:
            t.SetAlias('jet_hem1516', 'jet_eta < -1.3 && jet_phi < -0.87 && jet_phi > -1.57')
            t.SetAlias('njets_hem1516', 'Sum$(!jet_hem1516)')
            t.SetAlias('jetht_hem1516', 'Sum$(jet_pt * (jet_pt > 40 && !jet_hem1516))')
            t.SetAlias('limitsinput_pass', '(njets_hem1516 >= 4 && jetht_hem1516 >= 1200) || (rndm < 0.36)') # silly way to represent effect only on 64% of the data
        else:
            t.SetAlias('limitsinput_pass', '1==1')

        iyear = gp.years.index(year)
        scale = 1e-3 * gp.int_lumis[iyear] / ngen
        data_mc_scale = sig_datamcSF_2017p8(name_year)

        ROOT.TH1.AddDirectory(1) # the Draw>> output goes off into the ether without this stupid crap
        h_dbv  = ROOT.TH1D(n('dbv'),  '', 1250, 0, 2.5)
        h_dvv  = ROOT.TH1D(n('dvv'),  '', 400, 0, 4)
        h_dphi = ROOT.TH1D(n('dphi'), '', 10, -3.15, 3.15)
        t.Draw('dist0>>%s'  % n('dbv'),  'weight*(limitsinput_pass && nvtx==1)')
        t.Draw('svdist>>%s' % n('dvv'),  'weight*(limitsinput_pass && nvtx>=2)')
        t.Draw('svdphi>>%s' % n('dphi'), 'weight*(limitsinput_pass && nvtx>=2)')
        ROOT.TH1.AddDirectory(0)
        for h in h_dbv, h_dvv, h_dphi:
            h.SetDirectory(0)
            h.Scale(scale)
            if 'dbv' in h.GetTitle():
                h.Scale(data_mc_scale)
            else:
                h.Scale(data_mc_scale**2)
        
        h_dvv_rebin = h_dvv.Rebin(gp.nbins, n('dvv_rebin'), gp.bins)
        move_overflow_into_last_bin(h_dvv_rebin)

        h_ngen = ROOT.TH1D(n('ngen'), '', 1,0,1)
        h_ngen.SetBinContent(1, ngen)
        
        h_uncert = ROOT.TH1D(n('uncert'), '', gp.nbins, gp.bins)
        for i,v in enumerate(sig_uncert_2017p8(name_year)):
            h_uncert.SetBinContent(i+1, v)
        
        f.cd()
        for h in h_dbv, h_dphi, h_dvv, h_dvv_rebin, h_uncert, h_ngen:
            h.SetTitle(name_year)
            h.Write()

    print '\rmake_signals_2017p8: done       '

def make():
    def warning():
        return
        for i in xrange(20):
            print colors.error("don't forget: anything?")
    warning()

    assert not os.path.exists(gp.fn)
    ROOT.TH1.AddDirectory(0)
    f = ROOT.TFile(gp.fn, 'recreate')

    # FIXME!!! we should have the old 2017p8 bkgs to reuse here
    make_bkg(f)

    name_list = {}
    # FIXME!!! need to do the same for 2016 before this will properly work
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

    warning()

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

# FIXME probably need to do something here for the resonance mass
def points(f=None):
    if f is None:
        f = ROOT.TFile(gp.fn)
    kinds  = sorted(set(s.kind for s in sample_iterator(f)))
    #masses = sorted(set( (s.massResonance*1000 + s.mass if s.massResonance is not None else s.mass) for s in sample_iterator(f))) # FIXME not used anywhere yet, let's not overcomplicate
    masses = sorted(set(s.massResonance for s in sample_iterator(f)))
    taus   = sorted(set(s.tau  for s in sample_iterator(f)))
    return kinds, masses, taus

def axisize(l):
    l = sorted(set(l))
    print l
    delta = l[-1] - l[-2]
    l.append(l[-1] + delta)
    return to_array(l)

# FIXME probably need to do something here for the resonance mass
def axes(f=None):
    kinds, masses, taus = points(f)
    masses = axisize(masses)
    taus   = axisize(taus)
    return kinds, masses, taus, len(masses)-1, len(taus)-1

# FIXME probably need to do something here for the resonance mass
def nevents_plot():
    in_f = ROOT.TFile(gp.fn)
    out_f = ROOT.TFile('nevents.root', 'recreate')
    kinds, masses, taus, nmasses, ntaus = axes(in_f)

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

# FIXME probably need to do something here for the resonance mass
def signal_efficiency():
    from signal_efficiency import SignalEfficiencyCombiner
    for which, years in ('run2', [2016,2017,2018]), ('2017p8', [2017,2018]):
        combiner = SignalEfficiencyCombiner(years)
        in_f = combiner.inputs[0].f
        out_f = ROOT.TFile('signal_efficiency_%s.root' % which, 'recreate')

        kinds, masses, taus, nmasses, ntaus = axes(in_f)
        taus.remove(30.)
        ntaus -= 1

        for kind in kinds:
            h = ROOT.TH2D('signal_efficiency_%s' % kind, ';mass (GeV);#tau (mm)', nmasses, masses, ntaus, taus)

            for ibin in xrange(1, nmasses+1):
                mass = h.GetXaxis().GetBinLowEdge(ibin)
                for jbin in xrange(1, ntaus+1):
                    tau = h.GetYaxis().GetBinLowEdge(jbin)
                    pt = kind, tau, 100, mass

                    isample, r = None, None
                    try:
                        isample = name2isample(in_f, details2name(*pt))
                        r = combiner.combine(isample)
                    except ValueError as exc:
                        if tau < 100:
                            print colors.warning('problem getting %r : isample %r exc %s' % (pt, isample, exc))
                        continue # leave holes in the plot to know which samples are missing

                    h.SetBinContent(ibin, jbin, r.total_sig_eff)
                    h.SetBinError  (ibin, jbin, 0) # JMTBAD

            out_f.cd()
            h.Write()

        out_f.Write()
        out_f.Close()

# FIXME probably need to do something here for the resonance mass
def event_scale_factors():
    from signal_efficiency import SignalEfficiencyCombiner
    for which, years in ('2017p8', [2017,2018]), :
        combiner = SignalEfficiencyCombiner(years)
        in_f = combiner.inputs[0].f
        out_f = ROOT.TFile('event_TrackMover_scale_factors_%s.root' % which, 'recreate')

        kinds, masses, taus, nmasses, ntaus = axes(in_f)
        taus.remove(30.)
        ntaus -= 1

        for kind in kinds:
            h = ROOT.TH2D('event_TrackMover_scale_factors_%s' % kind, ';mass (GeV);#tau (mm)', nmasses, masses, ntaus, taus)

            for ibin in xrange(1, nmasses+1):
                mass = h.GetXaxis().GetBinLowEdge(ibin)
                for jbin in xrange(1, ntaus+1):
                    tau = h.GetYaxis().GetBinLowEdge(jbin)
                    pt = kind, tau, mass

                    try:
                        name = details2name(*pt)
                        isample = name2isample(in_f, name)
                    except ValueError as exc:
                        if tau < 100:
                            print colors.warning('problem getting %r : isample %r exc %s' % (pt, isample, exc))
                        continue # leave holes in the plot to know which samples are missing

                    event_SF = None
                    if which == '2017p8' :
                        vtx_SF_2017 = sig_datamcSF_2017p8(name+"_2017")
                        vtx_SF_2018 = sig_datamcSF_2017p8(name+"_2018")
                        event_SF_2017 = vtx_SF_2017**2
                        event_SF_2018 = vtx_SF_2018**2
                        lumi2017 = gp.int_lumis[gp.years.index("2017")]
                        lumi2018 = gp.int_lumis[gp.years.index("2018")]
                        event_SF = (event_SF_2017*lumi2017 + event_SF_2018*lumi2018) / (lumi2017+lumi2018)
                        
                        # for table of SFs, with bins 0.1--0.3\mm & 0.3--1\mm & 1--10\mm & 10--100\mm,
                        # take the ~midpoint of each bin and put its SF in the table (averaged where necessary)
                        if mass == 1600 :
                            if tau == 0.2 or tau == 0.6 or tau == 0.7 or tau == 4 or tau == 7 or tau == 55 :
                                print("for SF table:",name, round(event_SF, 4))

                    else : 
                        sys.exit('event_scale_factors not set up to handle %s! Exiting.' % which)

                    h.SetBinContent(ibin, jbin, event_SF)
                    h.SetBinError  (ibin, jbin, 0) # JMTBAD

            out_f.cd()
            h.Write()

        out_f.Write()
        out_f.Close()


if __name__ == '__main__':
    if 'make' in sys.argv:
        make()
    elif 'uncert' in sys.argv:
        sig_uncert_2017p8(sys.argv[sys.argv.index('uncert')+1], debug=True)
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
    elif 'iter' in sys.argv:
        include_2016 = 'include_2016' in sys.argv
        years = ('2016','2017','2018') if include_2016 else ('2017','2018')
        samples = sample_iterator(ROOT.TFile('limitsinput.root'),
                                  require_years=years,
                                  test='test_batch' in sys.argv,
                                  slices_1d='slices_1d' in sys.argv,
                                  )
        names = set(s.name for s in samples)
        allowed = [arg for arg in sys.argv if arg in names]
        for sample in samples:
            if allowed and sample.name not in allowed:
                continue
            print sample.isample, sample.name, 'signal_%05i' % sample.isample
    elif 'signal_efficiency' in sys.argv:
        signal_efficiency()
    elif 'event_scale_factors' in sys.argv:
        event_scale_factors()
    else:
        sys.exit('no cmd recognized from argv=%r' % sys.argv[1:])

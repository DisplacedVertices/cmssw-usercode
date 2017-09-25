from pprint import pprint
from JMTucker.MFVNeutralino.MiniTreeBase import *

bins = to_array(0., 0.04, 0.07, 4)
nbins = len(bins) - 1

observed = [1,0,0]

int_lumi = ac.int_lumi_2015p6 * ac.scale_factor_2015p6

bkg_n1v = 3637.
bkg_n2v = 1.

sig_uncert = [0.24, 0.24, 0.24]
bkg_uncert = [0.25, 0.25, 0.69]
bkg_uncert_stat = [0.02, 0.05, 0.17]
bkg_uncert = [(a**2 + b**2)**0.5 for a,b in zip(bkg_uncert, bkg_uncert_stat)] # JMTBAD use proper gmN?

in_fn = '2v_from_jets_2015p6_5track_default_v15.root'
#in_trees, in_scanpack_list = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV15_v3/mfv*root', None
in_trees, in_scanpack_list = None, '/uscms/home/tucker/work/hip_8025/src/JMTucker/MFVNeutralino/test/MakeSamples/scanpack1.list.temp'

limits_input_fn = 'limits_input.root'

assert len(observed) == nbins
assert len(sig_uncert) == nbins
assert len(bkg_uncert) == nbins

def ndx2isample(ndx):
    return -(ndx+1)
def isample2ndx(isample):
    return -isample-1

def name_list(f):
    return f.Get('name_list')

def nsamples(f):
    return name_list(f).GetNbinsX()

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

def sample_iterator(f):
    h = name_list(f)
    ax = h.GetXaxis()
    for ibin in xrange(1, h.GetNbinsX()+1):
        yield -ibin, ax.GetBinLabel(ibin)

def names(f):
    return sorted(name for _, name in sample_iterator(f))

def make():
    ROOT.TH1.AddDirectory(1)
    in_f = ROOT.TFile(in_fn)
    f = ROOT.TFile(limits_input_fn, 'recreate')

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
        print 'samples.push_back({%i, "%s", 0, 0});' % (isample, name)

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


def draw():
    ps = plot_saver(plot_dir('o2t_templates_run2'), size=(600,600))

    f = ROOT.TFile(limits_input_fn)

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
        leg.AddEntry(hbkg, 'Simulated d_{VV}^{C}', 'LE')

        for isample, color, title in which:
            h = fmt(f.Get('h_signal_%i_dvv' % isample), title, color)
            h.Draw('hist e same')
            leg.AddEntry(h, title, 'LE')

        leg.Draw()

        ps.save(which_name, log=False)

def compare(fn1, fn2, outbase):
    f1, f2 = fs = ROOT.TFile.Open(fn1), ROOT.TFile.Open(fn2)
    samples_1 = dict((name, isample) for isample, name in sample_iterator(f1))
    samples_2 = dict((name, isample) for isample, name in sample_iterator(f2))
    names_1 = set(samples_1)
    names_2 = set(samples_2)

    names = sorted(names_1 & names_2)
    nnames = len(names)
    if not names:
        print 'no samples in common between %s and %s' % (fn1, fn2)
        return

    if names_1 != names_2:
        print 'samples only in %s:' % fn1
        pprint(sorted(names_1 - names_2))
        print 'samples only in %s:' % fn2
        pprint(sorted(names_2 - names_1))

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

    for iname, name in enumerate(names):
        isamples = samples_1[name], samples_2[name]
        for h, fcn in h_fcns:
            (v1,e1), (v2, e2) = [fcn(f, isample) for f,isample in zip(fs, isamples)]
            h.GetXaxis().SetBinLabel(iname+1, name)
            h.SetBinContent(iname+1, v1-v2)
            h.SetBinError  (iname+1, (e1**2 + e2**2)**0.5)

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

if __name__ == '__main__':
    if 'make' in sys.argv:
        make()
    elif 'draw' in sys.argv:
        draw()
    elif 'compare' in sys.argv:
        compare(*sys.argv[2:5])
    else:
        print 'dunno'

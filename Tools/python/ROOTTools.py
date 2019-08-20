#!/usr/bin/env python

import math, sys, os, tempfile
from array import array
from glob import glob
from collections import defaultdict, namedtuple
from JMTucker.Tools.general import chunks

if os.environ.has_key('JMT_ROOTTOOLS_NOBATCHMODE'):
    import ROOT
else:
    # keep ROOT from parsing out -h/--help
    _saved = []
    for _x in '-h', '--help':
        _i = -1
        if _x in sys.argv:
            _i = sys.argv.index(_x)
        if _i >= 0:
            _saved.append((_i,_x))
            sys.argv.remove(_x)
    sys.argv.append('-b')     # Start ROOT in batch mode;
    import ROOT; ROOT.TCanvas # make sure libGui gets initialized while '-b' is specified;
    sys.argv.remove('-b')     # and don't mess up sys.argv.
    for _off, (_i, _x) in enumerate(_saved):
        sys.argv.insert(_i+_off, _x)

def apply_hist_commands(hist, hist_cmds=None):
    """With hist_cmds a list of n-tuples, where the first entry of the
    tuple is a function name, call the function name on the histogram
    passing the n-1 remaining arguments to the function.

    E.g. if hist_cmds is [('SetMarkerStyle', 5), ('SetStats', 0)],
    this is equivalent to calling

    hist.SetMarkerStyle(5)
    hist.SetStats(0)

    Default is a no-op (hist_cmds = None).
    """

    if hist_cmds is None: return
    for fn, args in hist_cmds:
        t = type(args)
        if t != type(()) or t != type([]):
            args = (args,)
        getattr(hist, fn)(*args)

def bin_iterator(hist, bin_values=False):
    """Loop over all bins of hist (which has whatever dimension) and
    yield the bin coordinates and the bin contents."""

    xax = hist.GetXaxis()
    yax = hist.GetYaxis()
    zax = hist.GetZaxis()
    if issubclass(type(hist), ROOT.TH3):
        axes = (xax, yax, zax)
        for ibin in xrange(0, hist.GetNbinsX()+2):
            for jbin in xrange(0, hist.GetNbinsY()+2):
                for kbin in xrange(0, hist.GetNbinsZ()+2):
                    bin = (ibin, jbin, kbin)
                    cnt = hist.GetBinContent(ibin, jbin, kbin)
                    if bin_values:
                        x = tuple(ax.GetBinLowEdge(b) for b,ax in zip(bin, axes))
                        yield bin, x, cnt
                    else:
                        yield bin, cnt
    elif issubclass(type(hist), ROOT.TH2):
        axes = (xax, yax)
        for ibin in xrange(0, hist.GetNbinsX()+2):
            for jbin in xrange(0, hist.GetNbinsY()+2):
                bin = (ibin, jbin)
                cnt = hist.GetBinContent(ibin, jbin)
                if bin_values:
                    x = tuple(ax.GetBinLowEdge(b) for b,ax in zip(bin, axes))
                    yield bin, x, cnt
                else:
                    yield bin, cnt
    elif issubclass(type(hist), ROOT.TH1):
        for ibin in xrange(0, hist.GetNbinsX()+2):
            cnt = hist.GetBinContent(ibin)
            if bin_values:
                yield (ibin,), xax.GetBinLowEdge(ibin), cnt
            else:
                yield (ibin,), cnt
    else:
        raise TypeError('input is not a histogram')

def check_consistency(h1, h2, log=True):
    def p(s):
        if not (log or log == ''):
            return
        if type(log) == str:
            print log, s
        else:
            print s
    t1 = type(h1)
    t2 = type(h2)
    assert issubclass(t1, ROOT.TH1) and issubclass(t2, ROOT.TH1)
    if t1 != t2:
        p('histograms have different types')
        return False

    for ax in 'XYZ':
        n = getattr(h1, 'GetNbins' + ax)()
        if n != getattr(h2, 'GetNbins' + ax)():
            p('histograms have different number of bins along %s' % ax)
            return False
        for i in xrange(0, n+2):
            if getattr(h1, 'Get%saxis' % ax)().GetBinLowEdge(i) != getattr(h2, 'Get%saxis' % ax)().GetBinLowEdge(i):
                p('histograms have different %s binning' % ax)
                return False

    return True

def poisson_interval(nobs, alpha=(1-0.6827)/2, beta=(1-0.6827)/2):
    if nobs > 0:
        lower = ROOT.Math.gamma_quantile(alpha, nobs, 1)
    else:
        lower = 0.
    upper = ROOT.Math.gamma_quantile_c(beta, nobs+1, 1)
    return lower, upper

def poisson_intervalize(h, zero_x=False, include_zero_bins=False, rescales=None):
    bins = []
    nbins = h.GetNbinsX()
    first, last = None, None
    if include_zero_bins == 'surrounded':
        for i in xrange(1, nbins+1):
            has = h.GetBinContent(i) > 0
            if first is None and has:
                first = i
            if has:
                last = i
    else:
        first, last = 1, nbins

    for i in xrange(1, nbins+1):
        y = h.GetBinContent(i)
        if y > 0 or (include_zero_bins == 'surrounded' and first <= i <= last) or include_zero_bins == True:
            bins.append(i)

    h2 = ROOT.TGraphAsymmErrors(len(bins))
    np = 0 # TGraphs count from 0
    for ibin in bins:
        xl = h.GetBinLowEdge(ibin)
        xh = h.GetBinLowEdge(ibin+1)
        x = (xl + xh)/2
        y = h.GetBinContent(ibin)
        if rescales:
            y *= rescales[ibin]
        yl, yh = poisson_interval(y)
        if rescales:
            y /= rescales[ibin]
            yl /= rescales[ibin]
            yh /= rescales[ibin]
        h2.SetPoint(np, x, y)

        if zero_x:
            h2.SetPointEXlow (np, 0)
            h2.SetPointEXhigh(np, 0)
        else:
            h2.SetPointEXlow (np, x - xl)
            h2.SetPointEXhigh(np, xh - x)
        h2.SetPointEYlow (np, y - yl)
        h2.SetPointEYhigh(np, yh - y)

        np += 1
    return h2

def wilson_score_vpme(n_on, n_tot, alpha=1-0.6827):
    z = ROOT.Math.normal_quantile(1-alpha/2, 1)
    phat = float(n_on) / n_tot
    dn = 1 + z**2 / n_tot
    c = (phat + z**2/2/n_tot) / dn
    e = z * (phat*(1-phat)/n_tot + z**2/4/n_tot**2)**0.5
    return c, e

def wilson_score(n_on, n_tot, alpha=1-0.6827):
    c,e = wilson_score_vpme(n_on, n_tot, alpha)
    return c, c-e, c+e

def effective_n(v, e):
    return (v/e)**2

def effective_wilson_score_vpme(n_on, e_n_on, n_tot, e_n_tot, alpha=1-0.6827):
    c = n_on / n_tot
    _, e = wilson_score_vpme(effective_n(n_on, e_n_on), effective_n(n_tot, e_n_tot))
    return c, e

def effective_wilson_score(n_on, e_n_on, n_tot, e_n_tot, alpha=1-0.6827):
    c, e = effective_wilson_score_vpme(n_on, e_n_on, n_tot, e_n_tot, alpha)
    return c, c-e, c+e
    _
def clopper_pearson(n_on, n_tot, alpha=1-0.6827, equal_tailed=True):
    if equal_tailed:
        alpha_min = alpha/2
    else:
        alpha_min = alpha

    lower = 0
    upper = 1

    if n_on > 0:
        lower = ROOT.Math.beta_quantile(alpha_min, n_on, n_tot - n_on + 1)
    if n_tot - n_on > 0:
        upper = ROOT.Math.beta_quantile_c(alpha_min, n_on + 1, n_tot - n_on)

    if n_on == 0 and n_tot == 0:
        return 0, lower, upper
    else:
        return float(n_on)/n_tot, lower, upper

def clopper_pearson_poisson_means(x, y, alpha=1-0.6827):
    r, rl, rh = clopper_pearson(x, x+y, alpha)
    pl = rl/(1-rl)
    if y == 0 or abs(rh - 1) < 1e-9:
        return None, pl, None
    return r/(1-r), pl, rh/(1 - rh)

def propagate_ratio(x, y, ex, ey):
    #print x, y, ex, ey
    r = x/y
    if x == 0.:
        e = ex/y
    else:
        e = r*((ex/x)**2 + (ey/y)**2)**0.5
    return r, r-e, r+e

def interval_to_vpme(v,l,h):
    return v, (h-l)/2

def cm2mm(h):
    name = h.GetName() + '_mm'
    xax = h.GetXaxis()
    xt = xax.GetTitle()
    if '(cm)' in xt:
        xt = xt.replace('(cm)', '(mm)')
    else:
        xt += ' (mm)'
    title = ';'.join((h.GetTitle(),xt,h.GetYaxis().GetTitle()))
    nbins = xax.GetNbins()
    mn = xax.GetXmin() * 10
    mx = xax.GetXmax() * 10
    h2 = getattr(ROOT, h.Class().GetName())(name, title, nbins, mn, mx)
    for ibin in xrange(0,nbins+2):
        h2.SetBinContent(ibin, h.GetBinContent(ibin))
        h2.SetBinError  (ibin, h.GetBinError  (ibin))
    h2.SetEntries(h.GetEntries())
    h2.SetLineColor(h.GetLineColor())
    h2.SetLineStyle(h.GetLineStyle())
    h2.SetLineWidth(h.GetLineWidth())
    h2.SetMarkerColor(h.GetMarkerColor())
    h2.SetMarkerStyle(h.GetMarkerStyle())
    h2.SetMarkerSize(h.GetMarkerSize())
    h2.SetFillColor(h.GetFillColor())
    h2.SetFillStyle(h.GetFillStyle())
    return h2

def cmssw_setup():
    ROOT.gSystem.Load('libFWCoreFWLite')
    ROOT.FWLiteEnabler.enable()
    ROOT.gSystem.Load('libDataFormatsFWLite.so')
    ROOT.gSystem.Load('libDataFormatsPatCandidates.so')

class HorGValues:
    def __init__(self, z):
        self.x, self.exl, self.exh, self.y, self.eyl, self.eyh = [], [], [], [], [], []

        zclass = z.Class().GetName()
        if zclass.startswith('TH1') or zclass == 'TProfile':
            self.n = z.GetNbinsX()
            xax = z.GetXaxis()
            for ibin in xrange(1, self.n+1):
                self.x.append(xax.GetBinCenter(ibin))
                _xw = xax.GetBinWidth(ibin)/2
                self.exl.append(_xw)
                self.exh.append(_xw)
                self.y.append(z.GetBinContent(ibin))
                ey = z.GetBinError(ibin)
                self.eyl.append(ey)
                self.eyh.append(ey)

        elif zclass.startswith('TGraph'):
            self.n = z.GetN()
            for i in xrange(self.n):
                x,y = ROOT.Double(), ROOT.Double()
                z.GetPoint(i,x,y)
                self.x.append(float(x))
                self.y.append(float(y))
                self.exl.append(z.GetErrorXlow(i))
                self.exh.append(z.GetErrorXhigh(i))
                self.eyl.append(z.GetErrorYlow(i))
                self.eyh.append(z.GetErrorYhigh(i))

        else:
            assert ValueError('only works with TProfile or TH1-, TGraph-descended objects')

        self.ey = [(l+h)/2 for l,h in zip(self.eyl, self.eyh)]

    @classmethod
    def check_compatible(_, a, b):
        if a.n != b.n or \
                a.x != b.x or \
                a.exl != b.exl or \
                a.exh != b.exh: # why did I not require equal abscissae before?
            raise ValueError('incompatible objects to divide')

    def filter(self, keep):
        keep = [i for i,x in enumerate(self.x) if x in keep]
        def _filter(l):
            return [z for i,z in enumerate(l) if i in keep]
        self.x   = _filter(self.x)
        self.exl = _filter(self.exl)
        self.exh = _filter(self.exh)
        self.y   = _filter(self.y)
        self.eyl = _filter(self.eyl)
        self.eyh = _filter(self.eyh)
        self.n = len(self.x)

    @classmethod
    def mutualize(_, a, b):
        keep = sorted(set(a.x) & set(b.x))
        a.filter(keep)
        b.filter(keep)

def histogram_divide_values(h1, h2, allow_subset):
    v1 = HorGValues(h1)
    v2 = HorGValues(h2)
    if allow_subset:
        HorGValues.mutualize(v1, v2)
    else:
        HorGValues.check_compatible(v1, v2)
    return v1, v2

def histogram_divide(h1, h2,
                     confint=clopper_pearson,
                     use_effective=False,
                     force_le_1=True,
                     no_zeroes=False,
                     confint_params=(),
                     allow_subset=False):
    '''TGraphAsymmErrors(TH1,TH1) exists, but this is kept for
    flexibility (different confidence intervals, using effective
    n=(content/error)**2, etc. Works with TGraph* inputs too.'''

    v1, v2 = histogram_divide_values(h1, h2, allow_subset)
    n = v2.n
    x, exl, exh, y, eyl, eyh = [], [], [], [], [], []

    for i in xrange(n):
        #print i,
        sold, told = s, t = v1.y[i], v2.y[i]
        es, et = v1.ey[i], v2.ey[i]

        if t == 0 or (s == 0 and no_zeroes):
            continue

        if use_effective:
            assert confint == clopper_pearson or confint == propagate_ratio
            effective_t = t**2 / et**2
            et = effective_t**0.5
            s = s/t * effective_t
            es = es/t * effective_t
            t = effective_t
            #print sold,told,s,t,

        if s > t and force_le_1:
            print 'warning: point %i has s > t, in interval forcing rat = 1' % i
            s = t

        if confint == propagate_ratio:
            r,a,b = confint(s,t,es,et, *confint_params)
        else:
            r,a,b = confint(s,t, *confint_params)
        #print x[i],exl[i],exh[i], s, t, a, b

        if b is None: # JMTBAD
            assert confint is not clopper_pearson
            b = 1e99

        x.append(v2.x[i])
        exl.append(v2.exl[i])
        exh.append(v2.exh[i])
        y.append(r)
        eyl.append(r - a)
        eyh.append(b - r)

    if x:
        return ROOT.TGraphAsymmErrors(len(x), *[to_array(z) for z in (x,y,exl,exh,eyl,eyh)])

graph_divide = histogram_divide

def core_gaussian(hist, factor, i=[0]):
    core_mean  = hist.GetMean()
    core_width = factor*hist.GetRMS()
    f = ROOT.TF1('core%i' % i[0], 'gaus', core_mean - core_width, core_mean + core_width)
    i[0] += 1
    return f

class _hist_list:
    def __init__(self, hists):
        self.hists = dict(hists)
        if self.hists.has_key('all'):
            raise NameError("name 'all' is reserved")

    def __getattr__(self, name):
        if name == 'all':
            return self.hists.values()
        elif self.hists.has_key(name):
            return self.hists[name]
        else:
            raise AttributeError("no histogram '%s' found" % name)

def compare_hists(ps, samples, **kwargs):
    """For the common subset of histograms found in dir1..N, draw them
    superimposed, normalized to unit area, with different
    colors. samples is a list of [(sample_name, dir_name, color), ...].

    Options (see the list below) are specified as keyword arguments in
    kwargs, and so far include
    - sort_names: True: process the histograms in alphabetical
    order. False (default): in the order found in the ROOT directory.
    - show_progress: if True (default), print how far along we are
    processing the histograms.
    - only_n_first: if supplied, only do that that many histograms. If
    -1 (default), do all.
    
    Various callbacks (see the other list below) can be specified as
    keyword arguments to modify the drawing depending on the
    histogram. The callback receives the arguments (histogram_name,
    hist_list, current_sample_name), where hist_list is an instance of
    _hist_list above, and current_sample_name is the particular sample
    in question, if applicable. The hist_list object serves as proxy
    for any of the histograms by name, or to return the whole
    list. Some examples:

    draw_commands = lambda name, hists, curr: [hist.GetXaxis().SetRangeUser(0,1) for hist in hists.all]
    apply_commands = lambda name, hists, curr: (hists.ttbar.SetFillStyle(3004), hists.signal.SetFillStyle(3005))
    no_stats = lambda name, hists, curr: name == 'h_costheta'
    scaling = lambda name, hists, curr: {'ttbar': 1, 'signal': 0.01}[curr]
    """

    # options
    recurse        = kwargs.get('recurse',        False)
    sort_names     = kwargs.get('sort_names',     False)
    show_progress  = kwargs.get('show_progress',  True)
    only_n_first   = kwargs.get('only_n_first',   -1)
    raise_on_incompatibility = kwargs.get('raise_on_incompatibility', False)

    def _get(arg, default):
        return kwargs.get(arg, lambda name, hists, curr: default)

    # callbacks
    no_stats       = _get('no_stats',       False)
    stat_size      = _get('stat_size',      (0.2, 0.2))
    skip           = _get('skip',           False)
    apply_commands = _get('apply_commands', None)
    legend         = _get('legend',         None)
    separate_plots = _get('separate_plots', False)
    draw_command   = _get('draw_command',   '')
    scaling        = _get('scaling',        1.)
    ratio          = _get('ratio',          True)
    x_range        = _get('x_range',        None)
    move_overflows = _get('move_overflows', 'under over')
    profile        = _get('profile',        None)

    ###

    proto_dir = samples[0][1]
    if recurse:
        names = flatten_directory(proto_dir)
    else:
        names = [k.GetName() for k in proto_dir.GetListOfKeys()]
    names = [name for name in names if issubclass(type(proto_dir.Get(name)), ROOT.TH1)]
    if not names:
        raise ValueError('no TH1-descended objects found')

    if sort_names:
        names.sort()
    if only_n_first > 0:
        names = names[:only_n_first]

    def all_same(l, msg):
        if len(set(l)) != 1:
            if raise_on_incompatibility:
                raise ValueError(msg)
            else:
                print msg + ', skipping'
        else:
            return l[0]

    nnames = len(names)
    for iname, name in enumerate(names):
        if show_progress and (nnames < 10 or iname % (nnames/10) == 0):
            print '%5i/%5i' % (iname, nnames), name

        name_clean = name.replace('/','_').replace('#','n')

        hists = [dir.Get(name) for _,dir,_ in samples]

        is3d = all_same([issubclass(type(hist), ROOT.TH3) for hist in hists], "for name %s, some samples' histograms are TH3, and some are not" % name)
        if is3d:
            print 'skipping TH3 %s' % name # JMTBAD projections?
            continue
        is2d = all_same([issubclass(type(hist), ROOT.TH2) for hist in hists], "for name %s, some samples' histograms are TH2, and some are not" % name)
        if not all_same([issubclass(type(hist), ROOT.TH1) for hist in hists], "for name %s, some samples' histograms are TH1, and some are not" % name):
            continue

        hist_list = _hist_list((sample_name, hist) for hist, (sample_name,_,_) in zip(hists, samples))
        if skip(name, hist_list, None):
            continue

        profiled = False
        if is2d:
            pf = profile(name, hist_list, None)
            if pf:
                if pf is True or pf == 1:
                    pf = 'x'
                assert pf in 'xXyY'
                profiled = True
                hists = [(hist.ProfileY if pf in 'yY' else hist.ProfileX)('%s_%s_pfx' % (hist.GetName(), sample_name)) for hist, (sample_name,_,_) in zip(hists, samples)]

        for hist, (sample_name, dir, color) in zip(hists, samples):
            # Store these data in the histogram object so we don't
            # have to cross-reference later. If we give them unique
            # names (prefix 'cah_') ROOT probably won't mind...
            hist.cah_sample_name = sample_name
            hist.cah_color = color

        for hist in hists:
            if hist.GetSumw2N() == 0:
                hist.Sumw2() # for correct error bars post scaling
            hist.cah_integral = hist.Integral(0, hist.GetNbinsX()+1) if not is2d else 0.
            hist.cah_scaling = scaling(name, hist_list, hist.cah_sample_name)

        nostat = no_stats(name, hist_list, None)
        for hist in hists:
            hist.SetLineWidth(2)

            if not is2d and hist.cah_scaling is not None:
                if hist.cah_scaling > 0 and hist.cah_integral > 0:
                    hist.Scale(hist.cah_scaling/hist.cah_integral)
                else:
                    hist.Scale(abs(hist.cah_scaling))
            if nostat:
                hist.SetStats(0)
            hist.SetLineColor(hist.cah_color)
            hist.SetMarkerColor(hist.cah_color)

            hist.SetName(hist.cah_sample_name)
            
        apply_commands(name, hist_list, None)

        draw_cmd = draw_command(name, hist_list, None)
        
        sep = separate_plots(name, hist_list, None)
        if sep == 'all' or (is2d and sep):
            for hist in hists:
                hist.Draw('colz' if is2d else draw_cmd)
                ps.save(name_clean + '_' + hist.cah_sample_name, logz=is2d)

        hists_sorted = hists[:]
        if not is2d or profiled:
            hists_sorted.sort(key=lambda hist: hist.GetMaximum(), reverse=True)

        x_r = x_range(name, hist_list, None)
        m_o = move_overflows(name, hist_list, None)

        if len(hists) > 1 and ratio(name, hist_list, None) and (not is2d or profiled):
            ratios_plot(name_clean,
                        hists,
                        plot_saver=ps,
                        res_fit=False,
                        res_divide_opt={'confint': propagate_ratio, 'force_le_1': False},
                        statbox_size=stat_size(name, hist_list, None),
                        res_y_range=0.15,
                        x_range = x_r,
                        move_overflows = m_o,
                        )
        else:
            for i,hist in enumerate(hists_sorted):
                if i == 0:
                    hist.Draw(draw_cmd)
                else:
                    hist.Draw((draw_cmd + ' sames').strip())
                if (not is2d or profiled) and x_r:
                    hist.GetXaxis().SetRangeUser(*x_r)
                move_overflows_into_visible_bins(hist, m_o)

            ps.c.Update()
            if not no_stats(name, hist_list, None):
                ss = stat_size(name, hist_list, None)
                for i, hist in enumerate(hists):
                    differentiate_stat_box(hist, i, hist.cah_color, ss)

            leg = legend(name, hist_list, None)
            if leg is not None:
                leg.Draw()

            ps.save(name_clean, logz=is2d)

def cumulative_histogram(h, type='ge'):
    """Construct the cumulative histogram in which the value of each
    bin is the tail integral of the given histogram.
    """
    
    nb = h.GetNbinsX()
    hc = ROOT.TH1F(h.GetName() + '_cumulative_' + type, '', nb, h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    hc.Sumw2()
    if type == 'ge':
        first, last, step = nb+1, 0, -1
    elif type == 'le':
        first, last, step = 0, nb+1, 1
    else:
        raise ValueError('type %s not recognized' % type)
    for i in xrange(first, last, step):
        if i == first:
            prev, eprev = 0., 0.
        else:
            prev  = hc.GetBinContent(i-step)
            eprev = hc.GetBinError(i-step)
        c = h.GetBinContent(i) + prev
        ce = (h.GetBinError(i)**2 + eprev**2)**0.5
        hc.SetBinContent(i, c)
        hc.SetBinError(i, ce)
    return hc

def cut(*cuts):
    """Take a sequence of cuts and join them with && (protecting with
    parentheses), suitable for use by TTree::Draw."""
    
    return ' && '.join('(%s)' % c.strip() for c in cuts if c.strip())

def data_mc_comparison(name,
                       background_samples,
                       signal_samples = [],
                       data_samples = [],
                       output_fn = None,
                       plot_saver = None,
                       histogram_path = None,
                       file_path = None,
                       fcn_for_nevents_check = None,
                       int_lumi = None,
                       int_lumi_bkg_scale = None,
                       int_lumi_nice = None,
                       normalize_to_data = None,
                       canvas_title = '',
                       canvas_size = (700, 840),
                       canvas_top_margin = 0.01,
                       canvas_bottom_margin = 0.3,
                       canvas_left_margin = 0.12,
                       canvas_right_margin = 0.08,
                       join_info_override = None,
                       stack_draw_cmd = 'hist',
                       move_overflows = 'under over',
                       rebin = None,
                       bin_width_to = None,
                       poisson_intervals = False,
                       x_title = '',
                       y_title = 'arb. units',
                       x_title_offset = 1.,
                       y_title_offset = 1.3,
                       x_title_size = 0.04,
                       y_title_size = 0.04,
                       y_label_size = 0.035,
                       x_range = None,
                       y_range = (None, None),
                       signal_color_override = None,
                       signal_line_width = 3,
                       signal_draw_cmd = 'hist',
                       data_marker_style = 20,
                       data_marker_size = 1.3,
                       data_draw_cmd = 'pe',
                       res_divide_opt = 'n pois',
                       res_line_width = 2,
                       res_line_color = ROOT.kBlue+3,
                       res_x_title_size = 0.04,
                       res_x_title_offset = 1.,
                       res_y_title = 'Data/MC',
                       res_y_title_offset = None,
                       res_y_title_size = None,
                       res_x_label_size = 0.035,
                       res_y_label_size = 0.035,
                       res_y_range = (0., 3.),
                       res_draw_cmd = 'apez',
                       res_fit = True,
                       legend_pos = None,
                       enable_legend = True,
                       verbose = False,
                       cut_line = None,
                       background_uncertainty = None,
                       preliminary = False,
                       simulation = False,
                       ):
    """
    Put the histograms for the background samples into a THStack, with
    normalization, color, legend, and other 'join information' (which
    samples are grouped with which) taken from the Sample objects.

    Optionally, draw the same histogram for signal examples (not
    stacked, but overlaid) and data samples. The signal normalization,
    style, and color info are also taken from their Sample objects.

    If multiple data samples are supplied, the hists are simply added
    together. If any data sample is supplied, a data/MC ratio plot is
    drawn in a sub pad at the bottom of the canvas. Some of the
    related parameters (e.g. canvas, margin sizes) are exposed, but
    some are hardcoded for now, so fiddling with them may screw things
    up, or not produce the expected behavior. JMTBAD
    
    If histogram_path, file_path, and int_lumi are not supplied, all
    of the Sample objects must have a member object named 'hist' that
    has the histogram preloaded. Otherwise:

    - file_path must be of the format
    'filesystem/path/to/root/files/filename_%(name)s.root', with name
    being taken from the Sample object.

    - histogram_path is the path to the histogram inside the ROOT
    files, e.g. 'histos/RecoJets/njets'.

    - int_lumi is the integrated luminosity to scale the MC to, in
    pb^-1. Then the overall scale factor is int_lumi *
    Sample.partial_weight, which already must include number of
    events, cross section, filter efficiencies, k-factors -- see the
    Sample object for how that works.

    - Any TFiles and hists constructed are cached in the Sample
    objects.

    The saving of output files is done by a plot_saver object (see
    that class definition for more info), or directly with
    canvas.SaveAs if output_fn is specified and plot_saver is
    not. (Exactly one may be specified.) The plot_saver object's
    canvas is replaced with one made internally here (to support the
    sub pad for the data/MC ratio plot).

    Other info for the rest of the parameters:

    - name: used to name the TCanvas/ratio TPad, THStack, auxiliary
    histogram for the ratio plot, and save name for the plot_saver.
    
    - background_samples, signal_samples, and data_samples must be
    lists of Sample objects. signal_samples and data_samples may be
    empty lists.

    JMTBAD finish documentation
    """

    all_samples = background_samples + signal_samples
    if data_samples:
         all_samples.extend(data_samples)

    # Sanity checks on the parameters.
    if output_fn is None and plot_saver is None:
        raise ValueError('at least one of output_fn, plot_saver must be supplied')
    elif output_fn is not None and plot_saver is not None:
        raise ValueError('only one of output_fn and plot_saver may be supplied')

    check_params = (file_path is None, histogram_path is None, int_lumi is None)
    if any(check_params) and not all(check_params):
        raise ValueError('must supply all of file_path, histogram_path, int_lumi or none of them')

    if file_path is None:
        # Sanity check that all the samples have the hist preloaded.
        for sample in all_samples:
            if not hasattr(sample, 'hist') or not issubclass(type(sample.hist), ROOT.TH1):
                raise ValueError('all sample objects must have hist preloaded if file_path is not supplied')
    else:
        # Sanity check needed for the TFile caching below.
        previous_file_paths = list(set(vars(sample).get('file_path', None) for sample in all_samples))
        previous_file_paths_ok = len(previous_file_paths) == 1 and previous_file_paths[0] is not None
        first_binning = None
        bin_width_to_scales = None
        for sample in all_samples:
            if not previous_file_paths_ok:
                # Cache the TFile and do basic check on the sample
                # that the number of events is correct (if
                # fcn_for_nevents_check specified).
                sample._datamccomp_file_path = file_path
                sample._datamccomp_filename = file_path % sample
                sample._datamccomp_file = ROOT.TFile(sample._datamccomp_filename)
                if sample not in data_samples and fcn_for_nevents_check is not None:
                    if fcn_for_nevents_check(sample, sample._datamccomp_file) != sample.nevents:
                        raise ValueError('wrong number of events for %s' % sample.name)

            # Get the histogram, normalize, rebin, and move the
            # overflow to the last bin.
            sample.hist = sample._datamccomp_file.Get(histogram_path)
            if not issubclass(type(sample.hist), ROOT.TH1):
                raise RuntimeError('histogram %s not found in %s' % (histogram_path, sample._datamccomp_filename))

            xax = sample.hist.GetXaxis()
            if not first_binning:
                first_binning = [None] # ibin starts at 1
                for ibin in xrange(1, xax.GetNbins()+2):
                    first_binning.append(xax.GetBinLowEdge(ibin))
            else:
                for ibin in xrange(1, xax.GetNbins()+2):
                    if abs(first_binning[ibin] - xax.GetBinLowEdge(ibin)) > 1e-6:
                        raise ValueError('inconsistent binning')
            xax = None

            if sample not in data_samples:
                sample.hist.Scale(sample.partial_weight(sample._datamccomp_file) * int_lumi)
                if int_lumi_bkg_scale is not None and sample not in signal_samples:
                    sample.hist.Scale(int_lumi_bkg_scale)

            move_overflows_into_visible_bins(sample.hist, move_overflows)

            if rebin is not None:
                sample.hist_before_rebin = sample.hist
                rebin_name = sample.hist.GetName() + '_rebinned'
                if type(rebin) in (list, tuple):
                    rebin = array('d', rebin)
                if type(rebin) == array:
                    if rebin[-1] > sample.hist.GetXaxis().GetXmax():
                        raise ValueError('rebin_last %f greater than axis max (ROOT will handle this arbitrarily)' % (rebin[-1], sample.hist.GetXaxis().GetXmax()))
                    sample.hist = sample.hist.Rebin(len(rebin)-1, rebin_name, rebin)
                else:
                    sample.hist = sample.hist.Rebin(rebin, rebin_name)
            
            if bin_width_to:
                if bin_width_to_scales is None:
                    bin_width_to_scales = [None]
                    for ibin in xrange(1, sample.hist.GetNbinsX()+1):
                        bin_width_to_scales.append(sample.hist.GetXaxis().GetBinWidth(ibin) / bin_width_to)

                for ibin in xrange(1, sample.hist.GetNbinsX()+1):
                    c = sample.hist.GetBinContent(ibin)
                    e = sample.hist.GetBinError(ibin)
                    sc = bin_width_to_scales[ibin]
                    sample.hist.SetBinContent(ibin, c / sc)
                    sample.hist.SetBinError  (ibin, e / sc)

    # Use the first data sample to cache the summed histogram for all
    # the data.
    data_sample = None
    if len(data_samples) >= 1:
        print 'len data samples', len(data_samples)
        data_sample = data_samples[0]
        print 'integ', get_integral(data_sample.hist)[0]
        for ds in data_samples[1:]:
            data_sample.hist.Add(ds.hist)
            print 'integ', get_integral(data_sample.hist)[0]

        if normalize_to_data:
            data_integ = get_integral(data_sample.hist)[0]
            if data_integ == 0:
                data_integ = 1
            bkg_integ = sum(get_integral(sample.hist)[0] for sample in background_samples)
            print 'normalize_to_data scaling to equal area: data %f bkg %f sf %f' % (data_integ, bkg_integ, data_integ / bkg_integ)
            for sample in background_samples:
                sample.hist.Scale(data_integ / bkg_integ)

    #####################

    no_data_no_adjust_margins = data_sample is None and canvas_size == (700,840) and canvas_bottom_margin == 0.3
    if no_data_no_adjust_margins:
        canvas_size = (700, 700)

    canvas = ROOT.TCanvas('c_datamc_' + name, canvas_title, *canvas_size)
    if not no_data_no_adjust_margins:
        canvas.SetTopMargin(canvas_top_margin)
        canvas.SetBottomMargin(canvas_bottom_margin)
        canvas.SetLeftMargin(canvas_left_margin)
        canvas.SetRightMargin(canvas_right_margin)

    if plot_saver is not None:
        plot_saver.old_c = plot_saver.c
        plot_saver.c = canvas

    if verbose:
        print name

    legend_entries = []
    stack = ROOT.THStack('s_datamc_' + name, '')
    sum_background = None
    for sample in background_samples:
        join, nice_name, color = sample.join_info if join_info_override is None else join_info_override(sample)
        sample.hist.SetLineColor(color)
        sample.hist.SetFillColor(color)
        if nice_name not in [l[1] for l in legend_entries] or not join:
            legend_entries.append((sample.hist, nice_name, 'F'))
        stack.Add(sample.hist)
        if sum_background is None:
            sum_background = sample.hist.Clone('sum_background_' + name)
        else:
            sum_background.Add(sample.hist)

        if verbose:
            integ = get_integral(sample.hist, 0)
            if integ[0] == 0:
                print sample.name, '<', 3 * sample.partial_weight(sample._datamccomp_file) * int_lumi, '@95%CL'
            else:
                print sample.name, integ
                for ibin in xrange(0, sample.hist.GetNbinsX()+2):
                    print '   %6i %15.6f +- %15.6f' % (ibin, sample.hist.GetBinContent(ibin), sample.hist.GetBinError(ibin))

    stack.Draw(stack_draw_cmd)
    stack.SetTitle(';%s;%s' % (x_title, y_title))

    if data_sample is not None:
        stack.GetXaxis().SetLabelSize(0) # the data/MC ratio part will show the labels
    stack.GetXaxis().SetTitleSize(x_title_size)
    stack.GetYaxis().SetTitleSize(y_title_size)
    stack.GetXaxis().SetTitleOffset(x_title_offset)
    stack.GetYaxis().SetTitleOffset(y_title_offset)
    stack.GetYaxis().SetLabelSize(y_label_size)

    if background_uncertainty is not None:
        bkg_uncert_label, extra_bkg_uncert_frac, bkg_uncert_color, bkg_uncert_style = background_uncertainty
        sum_background_uncert = sum_background.Clone('sum_background_uncert')
        if extra_bkg_uncert_frac is not None and extra_bkg_uncert_frac > 0:
            for i in xrange(1, sum_background_uncert.GetNbinsX()+1):
                v = sum_background_uncert.GetBinContent(i)
                e = sum_background_uncert.GetBinError(i)
                e = (e**2 + (extra_bkg_uncert_frac*v)**2)**0.5
                sum_background_uncert.SetBinError(i, e)
        sum_background_uncert.SetLineColor(0)
        sum_background_uncert.SetFillColor(bkg_uncert_color)
        sum_background_uncert.SetFillStyle(bkg_uncert_style)
        sum_background_uncert.Draw('E2 same')
        stack.SetMaximum(stack.GetMaximum() * (1.1 + extra_bkg_uncert_frac))

    if x_range is not None:
        stack.GetXaxis().SetLimits(*x_range)
    y_range_min, y_range_max = y_range
    if y_range_min is not None:
        stack.SetMinimum(y_range_min)
    if y_range_max is not None:
        stack.SetMaximum(y_range_max)

    for sample in signal_samples:
        sample.hist.SetLineColor(sample.color if signal_color_override is None else signal_color_override(sample))
        sample.hist.SetLineWidth(signal_line_width)
        sample.hist.Draw('same ' + signal_draw_cmd)
        if verbose:
            integ = get_integral(sample.hist, 0)
            if integ[0] == 0:
                print sample.name, '<', 3 * sample.partial_weight(sample._datamccomp_file) * int_lumi, '@95%CL'
            else:
                print sample.name, integ

    if data_sample is not None:
        data_sample.hist.SetMarkerStyle(data_marker_style)
        data_sample.hist.SetMarkerSize(data_marker_size)
        if poisson_intervals:
            data_sample.hist_poissoned = poisson_intervalize(data_sample.hist, rescales=bin_width_to_scales)
            data_sample.hist_poissoned.SetMarkerStyle(data_marker_style)
            data_sample.hist_poissoned.SetMarkerSize(data_marker_size)
            data_sample.hist_poissoned.Draw(data_draw_cmd)
        else:
            data_sample.hist.Draw('same ' + data_draw_cmd)

    if enable_legend and legend_pos is not None:
        legend_entries.reverse()
        legend = ROOT.TLegend(*legend_pos)
        legend.SetTextFont(42)
        legend.SetBorderSize(0)
        if data_sample is not None:
            legend.AddEntry(data_sample.hist, 'Data', 'LPE')
        for l in legend_entries:
            legend.AddEntry(*l)
        if background_uncertainty is not None:
            legend.AddEntry(sum_background_uncert, bkg_uncert_label, 'F')
        for sample in signal_samples:
            if '\\' in sample.nice_name:
                legend.AddEntry(sample.hist, sample.nice_name.split('\\')[0], 'L')
                legend.AddEntry(sample.hist, sample.nice_name.split('\\')[1], '')
            else:
                legend.AddEntry(sample.hist, sample.nice_name, 'L')
        legend.Draw()
    else:
        legend = None

    if cut_line is not None:
        cut_line_coords, cut_line_color, cut_line_width, cut_line_style = cut_line
        if type(cut_line_coords) in (float, int):
            cut_line_coords = (cut_line_coords, stack.GetMinimum(),
                               cut_line_coords, stack.GetMaximum())
        cut_line = ROOT.TLine(*cut_line_coords)
        cut_line.SetLineColor(cut_line_color)
        cut_line.SetLineWidth(cut_line_width)
        cut_line.SetLineStyle(cut_line_style)
        cut_line.Draw()

    if int_lumi_nice is not None:
        def write(font, size, x, y, text):
            w = ROOT.TLatex()
            w.SetNDC()
            w.SetTextFont(font)
            w.SetTextSize(size)
            w.DrawLatex(x, y, text)
            return w
        subtr = 0.02
        lum_pos = 0.625
        stupid = 0
        if data_sample is not None:
            subtr = 0
            lum_pos = 0.618
            stupid = 0.02
        lum = write(42, 0.04, lum_pos+stupid, 0.930-subtr, int_lumi_nice)
        cms = write(61, 0.04, 0.098+stupid, 0.930-subtr, 'CMS')
        if simulation and preliminary:
            exlab_str = 'Simulation Preliminary'
        elif preliminary:
            exlab_str = 'Preliminary'
        elif simulation:
            exlab_str = 'Simulation'
        if simulation or preliminary:
            exlab = write(52, 0.035, 0.185+stupid, 0.930-subtr, exlab_str)

    if verbose:
        if data_sample is not None:
            print 'data integral:', data_sample.hist.Integral(0, data_sample.hist.GetNbinsX()+1)
        print 'bkg  integral:', sum_background.Integral(0, sum_background.GetNbinsX()+1)
        print

    ratio_pad, res_g, old_opt_fit = None, None, None
    if data_sample is not None:
        ratio_pad = ROOT.TPad('ratio_pad_' + name, '', 0, 0, 1, 1)
        ratio_pad.SetTopMargin(1-canvas_bottom_margin + 0.015)
        ratio_pad.SetLeftMargin(canvas_left_margin)
        ratio_pad.SetRightMargin(canvas_right_margin)
        ratio_pad.SetFillColor(0)
        ratio_pad.SetFillStyle(0)
        ratio_pad.Draw()
        ratio_pad.cd(0)

        res_g = ROOT.TGraphAsymmErrors(data_sample.hist, sum_background, res_divide_opt)
        res_g.SetMarkerStyle(20)
        res_g.SetMarkerSize(0)
        res_g.SetLineWidth(res_line_width)
        res_g.SetLineColor(res_line_color)
        if x_range is None:
            x_range_dmc = sum_background.GetXaxis().GetXmin(), sum_background.GetXaxis().GetXmax()
        else:
            x_range_dmc = x_range[0], x_range[1]
        res_g.GetXaxis().SetLimits(*x_range_dmc)
        res_g.GetXaxis().SetTitleSize(res_x_title_size)
        res_g.GetXaxis().SetTitleOffset(res_x_title_offset)
        res_g.GetXaxis().SetLabelSize(res_x_label_size)
        res_g.GetYaxis().SetLabelSize(res_y_label_size)
        res_g.GetYaxis().SetTitleOffset(res_y_title_offset if res_y_title_offset is not None else y_title_offset)
        res_g.GetYaxis().SetTitleSize(res_y_title_size if res_y_title_size is not None else y_title_size)
        res_g.GetYaxis().SetRangeUser(*res_y_range)
        res_g.SetTitle(';%s;%s' % (x_title, res_y_title))
        res_g.Draw(res_draw_cmd)
        ln = ROOT.TLine(x_range_dmc[0], 1, x_range_dmc[1], 1)
        ln.SetLineStyle(4)
        ln.SetLineColor(ROOT.kBlue+3)
        ln.Draw()

        if res_fit:
            old_opt_fit = ROOT.gStyle.GetOptFit()
            ROOT.gStyle.SetOptFit(0)
            fit_opt = 's ex0'
            fit_opt += ' v' if type(verbose) == str and 'fit' in verbose else ' q'
            fit_res = res_g.Fit('pol0', fit_opt)
            ratio_pad.Update()
            fit_tpt = ROOT.TPaveText(0.12, 0.25, 0.4, 0.27, 'ndc')
            fit_tpt.SetBorderSize(0)
            fit_tpt.AddText('p0 = %.2f #pm %.2f  #chi^{2}/ndf = %.2f/%i  p = %.3f' % (fit_res.Parameter(0), fit_res.ParError(0), fit_res.Chi2(), fit_res.Ndf(), fit_res.Prob()))
            fit_tpt.Draw()
            #fit_stat_box = res_g.GetListOfFunctions().FindObject('stats')
            #fit_stat_box.SetX1NDC(0)
            #fit_stat_box.SetX2NDC(0)
            #fit_stat_box.SetY1NDC(0)
            #fit_stat_box.SetY2NDC(0)

    if plot_saver is not None:
        plot_saver.save(name)
        plot_saver.c = plot_saver.old_c
        plot_saver.c.cd()
    elif output_fn is not None:
        canvas.SaveAs(output_fn)

    if old_opt_fit is not None:
        ROOT.gStyle.SetOptFit(old_opt_fit)

    return canvas, stack, sum_background, legend, ratio_pad, res_g

def detree(t, branches='run:lumi:event', cut='', xform=lambda x: tuple(int(y) for y in x), delete_tmp=True, save_fn=None):
    """Dump specified branches from tree into a list of tuples, via an
    ascii file. By default all vars are converted into integers. The
    xform parameter specifies the function transforming the tuple of
    strings into the desired format; if xform is a type instance, it
    is used on every column uniformly."""

    if type(xform) == type(type):
        xf = xform
        xform = lambda x: tuple(xf(y) for y in x)

    dir = None
    if os.environ['HOSTNAME'].startswith('cmslpc'):
        dir = '/uscmst1b_scratch/lpc1/3DayLifetime/' + os.environ['USER']
    tmp_f, tmp_fn = tempfile.mkstemp(dir=dir)
    t.GetPlayer().SetScanRedirect(True)
    t.GetPlayer().SetScanFileName(tmp_fn)
    t.Scan(branches, cut, 'colsize=50')
    t.GetPlayer().SetScanRedirect(False)
    nvp2 = branches.replace('::','').count(':') + 1 + 2
    with os.fdopen(tmp_f) as file:
        for line in file:
            if ' * ' in line and 'Row' not in line:
                yield xform(line.split('*')[2:nvp2])
    if save_fn:
        os.system('cp %s %s' % (tmp_fn, save_fn))
    if delete_tmp:
        os.remove(tmp_fn)

def differentiate_stat_box(hist, movement=1, new_color=None, new_size=None, color_from_hist=True, offset=None):
    """Move hist's stat box and change its line/text color. If
    movement is just an int, that number specifies how many units to
    move the box downward. If it is a 2-tuple of ints (m,n), the stat
    box will be moved to the left m units and down n units. A unit is
    the width or height of the stat box.

    Call TCanvas::Update first (and use TH1::Draw('sames') if
    appropriate) or else the stat box will not exist."""

    s = hist.FindObject('stats')
    if not s:
        return

    if color_from_hist:
        new_color = hist.GetLineColor()

    if new_color is not None:
        s.SetTextColor(new_color)
        s.SetLineColor(new_color)

    if type(movement) == int:
        movement = (0,movement)
    m,n = movement
    
    x1,x2 = s.GetX1NDC(), s.GetX2NDC()
    y1,y2 = s.GetY1NDC(), s.GetY2NDC()

    if new_size is not None:
        x1 = x2 - new_size[0]
        y1 = y2 - new_size[1]

    if offset is None:
        ox, oy = 0, 0
    else:
        ox, oy = offset

    s.SetX1NDC(x1 - (x2-x1)*m + ox)
    s.SetX2NDC(x2 - (x2-x1)*m + ox)
    s.SetY1NDC(y1 - (y2-y1)*n + oy)
    s.SetY2NDC(y2 - (y2-y1)*n + oy)

    return s

def resize_stat_box(hist, new_size):
    differentiate_stat_box(hist, movement=0, new_size=new_size, color_from_hist=False)

def draw_in_order(hists_and_cmds, sames=False):
    if type(hists_and_cmds[1]) == str:
        cmd = hists_and_cmds[1]
        hists_and_cmds = [(h,cmd) for h in hists_and_cmds[0]]
    hists = [(h, h.GetMaximum(), cmd, i) for i,(h,cmd) in enumerate(hists_and_cmds)]
    hists.sort(key=lambda x: x[1], reverse=True)
    for i, (h, m, cmd, iorig) in enumerate(hists):
        if i > 0 and 'same' not in cmd:
            cmd += ' same'
            if sames:
                cmd += 's'
        h.Draw(cmd)
    order = dict((x[0], x[-1]) for x in hists)
    return order

def flatten_directory(dir, prefix=''):
    """Take an input TDirectory object (a TFile is a TDirectory) and
    flatten its structure. E.g. for an input File with structure

    File
    \A
     \a1
     \a2
     \B
      \b1
    \c
    \d

    where uppercase names are directories and lowercase names are
    objects e.g. histos, we return
    ['A/a1', 'A/a2', 'A/B/b1', 'c', 'd'].
    """
    
    result = []
    for key in dir.GetListOfKeys():
        name = key.GetName()
        obj = dir.Get(name)
        if issubclass(type(obj), ROOT.TDirectory):
            for sub_name in flatten_directory(obj, name):
                result.append(name + '/' + sub_name)
        else:
            result.append(name)
    return result

def fit_gaussian(hist, factor=None, draw=False, cache=[]):
    """Fit a Gaussian to the histogram, and return a dict with fitted
    parameters and errors. If factor is supplied, fit only to range in
    hist.mean +/- factor * hist.rms.
    """

    if draw:
        opt = 'qr'
    else:
        opt = 'qr0'

    if factor is not None:
        fcn = core_gaussian(hist, factor)
        cache.append(fcn)
        hist.Fit(fcn, opt)
    else:
        hist.Fit('gaus', opt)
        fcn = hist.GetFunction('gaus')
        
    return {
        'constant': (fcn.GetParameter(0), fcn.GetParError(0)),
        'mu':       (fcn.GetParameter(1), fcn.GetParError(1)),
        'sigma':    (fcn.GetParameter(2), fcn.GetParError(2))
        }
    
def get_bin_content_error(hist, value):
    """For the given histogram, find the bin corresponding to the
    value and return its contents and associated
    error. Multi-dimensional histograms are supported; value may be a
    tuple in those cases.
    """

    if type(value) != type(()):
        value = (value,)
    bin = hist.FindBin(*value)
    return (hist.GetBinContent(bin), hist.GetBinError(bin))

def get_integral(hist, xlo=None, xhi=None, integral_only=False, include_last_bin=True, x_are_bins=False):
    """For the given histogram, return the integral of the bins
    corresponding to the values xlo to xhi along with its error.
    """

    if xlo is None:
        binlo = 0
    elif x_are_bins:
        binlo = xlo
    else:
        binlo = hist.FindBin(xlo)

    if xhi is None:
        binhi = hist.GetNbinsX()+1
    elif x_are_bins:
        binhi = xhi
    else:
        binhi = hist.FindBin(xhi)
        if not include_last_bin:
            binhi -= 1

    integral = hist.Integral(binlo, binhi)
    if integral_only:
        return integral

    wsq = 0
    for i in xrange(binlo, binhi+1):
        wsq += hist.GetBinError(i)**2
    return integral, wsq**0.5

integral = get_integral

def get_hist_quantiles(hist, probs, options='list'):
    """Get the quantiles for the histogram corresponding to the listed
    probs (e.g. probs = [0.1, 0.5, 0.9] to find the first decile, the
    mean, and the last decile."""

    if type(probs) == int:
        n = probs
        probs = array('d', [float(i)/n for i in xrange(n+1)])
    elif type(probs) != array:
        probs = array('d', probs)
    quantiles = array('d', [0.]*len(probs))
    hist.GetQuantiles(len(probs), quantiles, probs)
    if 'list' in options:
        quantiles = list(quantiles)
    if 'error' in options:
        n = hist.GetEntries()
        unc = hist.GetMeanError() * (math.pi * (2*n + 1) / 4 / n)**0.5 # JMTBAD this is the formula for the median given normal distribution
        quantiles = [(q, unc) for q in quantiles]
    if 'probs' in options:
        return quantiles, probs
    return quantiles

def get_quantiles(l, binning, probs, options=''):
    if binning is None:
        mn = min(l)
        mx = max(l)
        n = 10000
        d = (mx-mn)/n
        binning = n+1, min(l), max(l)+d
    h = ROOT.TH1D('get_quantiles_temp', '', *binning)
    h.SetDirectory(0)
    for x in l:
        h.Fill(x)
    return get_hist_quantiles(h, probs, options)

def get_hist_stats(hist, factor=None, draw=False, fit=True):
    """For the given histogram, return a five-tuple of the number of
    entries, the underflow and overflow counts, the fitted sigma
    (using the function specified by fcnname, which must be an
    already-made ROOT.TF1 whose parameter(2) is the value used), and the
    RMS.
    """

    results = fit_gaussian(hist, factor, draw) if fit else {}
    results.update({
        'entries': hist.GetEntries(),
        'under':   hist.GetBinContent(0),
        'over':    hist.GetBinContent(hist.GetNbinsX()+1),
        'mean':    (hist.GetMean(), hist.GetMeanError()),
        'rms':     (hist.GetRMS(), hist.GetRMSError())
        })
    return results

class draw_hist_register:
    """Keep track of the otherwise-anonymous histograms produced by
    TTree::Draw. Can specify binning as well (same syntax as Draw
    expects). Use something like:

    hr = hist_register(tree)
    hist = hr.draw('ordinate:abscissa', '100,0,1,100,0,5')
    hist.SetTitle('ordinate vs. abscissa')
    """
    uniq = [0]
    
    def __init__(self, tree, use_weight=False):
        self.id = self.uniq[0]
        self.uniq[0] += 1
        self.tree = tree
        self.n = 0
        self.use_weight = use_weight
        self.clear()

    def clear(self):
        # don't reset self.n
        self.names = []
        self.hists = []
        
    def name_for_draw(self, draw_str, binning=''):
        name = 'h_%i_%i' % (self.id, self.n)
        self.names.append(name)
        self.n += 1
        if binning:
            binning = '(%s)' % binning
        return draw_str + '>>' + name + binning

    def draw(self, draw_str, cut='', binning='', get_n=False, tree=None, nice_name=None, goff=False):
        if self.use_weight:
            if cut:
                cut = 'weight*(%s)' % cut
            else:
                cut = 'weight'
        varexp = self.name_for_draw(draw_str, binning)
        option = 'e' if self.use_weight else ''
        if goff:
            option += ' goff'
        n = (tree if tree else self.tree).Draw(varexp, cut, option)
        try:
            h = getattr(ROOT, self.names[-1])
        except AttributeError:
            b = binning.split(',')
            if len(b) == 3:
                h = ROOT.TH1F(self.names[-1], '', int(b[0]), float(b[1]), float(b[2]))
            else:
                assert len(b) == 6
                h = ROOT.TH2F(self.names[-1], '', int(b[0]), float(b[1]), float(b[2]), int(b[3]), float(b[4]), float(b[5]))
        self.hists.append(h)
        h.is2d = ':' in draw_str
        if nice_name is None:
            nice_name = draw_str.replace(':', '_vs_')
        h.nice_name = nice_name
        return (h,n) if get_n else h

def make_rms_hist(prof, name='', bins=None, cache={}):
    """Takes an input TProfile and produces a histogram whose bin contents are
    the RMS of the bins of the profile. Caches the histogram so that it doesn't
    get deleted by python before it gets finalized onto a TCanvas.

    If bins is a list of bin lower edges + last bin high edge,
    rebinning is done before making the RMS histogram. Due to a bug in
    ROOT's TProfile in versions less than 5.22 (?), rebinning is done
    manually here.
    """
    
    nbins = prof.GetNbinsX()
    if name == '':
        name = 'RMS' + prof.GetName()
    title = 'RMS ' + prof.GetTitle()
    old_axis = prof.GetXaxis()

    # Play nice with same-name histograms that were OK because they
    # were originally in different directories.
    while cache.has_key(name):
        name += '1'

    # Format of contents list: [(new_bin, (new_bin_content, new_bin_error)), ...]
    contents = []
    
    if bins:
        if type(bins) == type([]):
            bins = array('f', bins)
        new_hist = ROOT.TH1F(name, title, len(bins)-1, bins)
        new_axis = new_hist.GetXaxis()
        new_bins = {}
        for old_bin in xrange(1, nbins+1):
            new_bin = new_axis.FindBin(old_axis.GetBinLowEdge(old_bin))
            if not new_bins.has_key(new_bin):
                new_bins[new_bin] = [0., 0.]
            N = prof.GetBinEntries(old_bin)
            new_bins[new_bin][0] += N*prof.GetBinContent(old_bin)
            new_bins[new_bin][1] += N
        for val in new_bins.values():
            if val[1] > 0:
                val[0] /= val[1]
        contents = new_bins.items()
    else:
        new_hist = ROOT.TH1F(name, title, nbins, old_axis.GetXmin(), old_axis.GetXmax())
        for old_bin in xrange(1, nbins+1):
            f_bin = float(prof.GetBinContent(old_bin))
            ent_bin = float(prof.GetBinEntries(old_bin))
            contents.append((old_bin, (f_bin, ent_bin)))

    for new_bin, (f_bin, ent_bin) in contents:
        if f_bin > 0:
            f_bin = f_bin**0.5
        else:
            f_bin = 0
            
        if ent_bin > 0:
            err_bin = f_bin/(2.*ent_bin)**0.5
        else:
            err_bin = 0

        new_hist.SetBinContent(new_bin, f_bin)
        new_hist.SetBinError(new_bin, err_bin)
        
    cache[name] = new_hist
    return new_hist

def move_below_into_bin(h,a):
    """Given the TH1 h, add the contents of the bins below the one
    corresponding to a into that bin, and zero the bins below."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(0, b):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_above_into_bin(h,a,minus_one=False):
    """Given the TH1 h, add the contents of the bins above the one
    corresponding to a into that bin, and zero the bins above."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    b = h.FindBin(a)
    if minus_one:
        b -= 1
    bc = h.GetBinContent(b)
    bcv = h.GetBinError(b)**2
    for nb in xrange(b+1, h.GetNbinsX()+2):
        bc += h.GetBinContent(nb)
        bcv += h.GetBinError(nb)**2
        h.SetBinContent(nb, 0)
        h.SetBinError(nb, 0)
    h.SetBinContent(b, bc)
    h.SetBinError(b, bcv**0.5)

def move_overflow_into_last_bin(h):
    """Given the TH1 h, Add the contents of the overflow bin into the
    last bin, and zero the overflow bin."""
    assert(h.Class().GetName().startswith('TH1')) # i bet there's a better way to do this...
    nb = h.GetNbinsX()
    h.SetBinContent(nb, h.GetBinContent(nb) + h.GetBinContent(nb+1))
    h.SetBinError(nb, (h.GetBinError(nb)**2 + h.GetBinError(nb+1)**2)**0.5)
    h.SetBinContent(nb+1, 0)
    h.SetBinError(nb+1, 0)

def move_overflows_into_visible_bins(h, opt='under over'):
    """Combination of move_above/below_into_bin and
    move_overflow_into_last_bin, except automatic in the range. Have
    to already have SetRangeUser."""
    if type(opt) != str:
        opt = 'under over' if opt else ''
    opt = opt.strip().lower()
    if 'under' in opt:
        move_below_into_bin(h, h.GetBinLowEdge(h.GetXaxis().GetFirst()))
    if 'over' in opt:
        move_above_into_bin(h, h.GetBinLowEdge(h.GetXaxis().GetLast()))

def move_stat_box(s, ndc_coords):
    """Move the stat box s (or if s is its hist, get s from it) to the
    NDC coords (x1, y1, x2, y2) specified. (Remember to call
    TCanvas::Update first.)"""

    if type(s) != ROOT.TPaveStats:
        s = s.FindObject('stats')

    if ndc_coords == 'inf':
        ndc_coords = (1e6,1e6,1e6,1e6)
    s.SetX1NDC(ndc_coords[0])
    s.SetY1NDC(ndc_coords[1])
    s.SetX2NDC(ndc_coords[2])
    s.SetY2NDC(ndc_coords[3])

    return s

def p4(pt,eta,phi,mass):
    v = ROOT.TLorentzVector()
    v.SetPtEtaPhiM(pt,eta,phi,mass)
    return v

def poisson_means_divide(h1, h2, no_zeroes=False):
    return histogram_divide(h1, h2, confint=clopper_pearson_poisson_means, force_lt_1=False, no_zeroes=no_zeroes)

def plot_dir(x='', make=False, temp=False):
    hostname = os.environ['HOSTNAME']
    username = os.environ['USER']
    d = None
    if 'fnal.gov' in hostname and username == 'tucker':
        if temp:
            d = '/publicweb/t/tucker/asdf/tempplots'
        else:
            d = '/publicweb/t/tucker/asdf/plots'
    elif 'fnal.gov' in hostname and username == 'jchu':
        d = '/publicweb/j/jchu/plots'
    elif 'fnal.gov' in hostname and username == 'dquach':
        d = '/publicweb/d/dquach/plots'
    elif 'fnal.gov' in hostname and username == 'shogan':
	d = '/publicweb/s/shogan/images'
    elif 'fnal.gov' in hostname and username == 'joeyr':
        d = '/publicweb/j/joeyr/plots'
    if d:
        x = os.path.join(d,x)
    else:
        raise NotImplementedError("can't handle host %s and user %s" % (hostname, username))
    if make:
        try:
            os.makedirs(x)
        except OSError:
            pass
    return x

class plot_saver:
    i = 0
    
    def __init__(self, plot_dir=None, html=True, log=True, root=True, root_log=False, pdf=False, pdf_log=False, C=False, C_log=False, size=(820,630), per_page=-1, canvas_margins=None):
        self.c = ROOT.TCanvas('c%i' % plot_saver.i, '', *size)
        if canvas_margins is not None:
            if type(canvas_margins) == int or type(canvas_margins) == float:
                top, bottom, left, right = tuple(canvas_margins for x in xrange(4))
            else:
                top, bottom, left, right = canvas_margins
            self.c.SetTopMargin(top)
            self.c.SetBottomMargin(bottom)
            self.c.SetLeftMargin(left)
            self.c.SetRightMargin(right)
        plot_saver.i += 1
        self.saved = []
        self.html = html
        self.set_plot_dir(plot_dir)
        self.log = log
        self.root = root
        self.root_log = root_log
        self.pdf = pdf
        self.pdf_log = pdf_log
        self.C = C
        self.C_log = C_log
        self.per_page = per_page

    def __del__(self):
        self.write_index()

    def update_canvas(self):
        self.c.Update()

    def anchor_name(self, fn):
        return os.path.splitext(os.path.basename(fn))[0].replace('.', '_').replace('/', '_')
    
    def write_index(self):
        if not self.saved or not self.html:
            return
        html = open(os.path.join(self.plot_dir, 'index.html'), 'wt')
        if self.per_page > 0:
            nsaved = len(self.saved)
            ndxs = range(0, nsaved, self.per_page)
            npages = len(ndxs)
            for page, ndx in enumerate(ndxs):
                self.write_index_page(self.saved[ndx:ndx+self.per_page], page, npages)
        else:
            self.write_index_page(self.saved, 0, 1)
            
    def write_index_page(self, saved, page, num_pages):
        def html_fn(page):
            if page == 0:
                return 'index.html'
            else:
                return 'index_%i.html' % page
            return 
        html = open(os.path.join(self.plot_dir, html_fn(page)), 'wt')
        html.write('<html><body><pre>\n')
        def write_pages_line():
            html.write('pages: ')
            for i in xrange(num_pages):
                if i == page:
                    html.write('<b>%i</b>  ' % i)
                else:
                    html.write('<a href="%s">%i</a>  ' % (html_fn(i), i))
            html.write('\n')
        if num_pages > 1:
            write_pages_line()
        html.write('<a href="..">.. (parent directory)</a>\n')
        for i, save in enumerate(saved):
            if type(save) == str:
                # this is just a directory link
                html.write('<a href="%s">%10i%32s%s</a>\n' % (save, i, 'change directory: ', save))
                continue

            fn, log, root, root_log, pdf, pdf_log, C, C_log = save

            bn = os.path.basename(fn)
            html.write('<a href="#%s">%10i</a> ' % (self.anchor_name(fn), i))
            if log:
                html.write(' <a href="%s">log</a>' % os.path.basename(log))
            else:
                html.write('    ')
            if root:
                html.write(' <a href="%s">root</a>' % os.path.basename(root))
            else:
                html.write('     ')
            if root_log:
                html.write(' <a href="%s">root_log</a>' % os.path.basename(root_log))
            else:
                html.write('     ')
            if pdf:
                html.write(' <a href="%s">pdf</a>' % os.path.basename(pdf))
            else:
                html.write('     ')
            if pdf_log:
                html.write(' <a href="%s">pdf_log</a>' % os.path.basename(pdf_log))
            else:
                html.write('     ')
            if C:
                html.write(' <a href="%s">C</a>' % os.path.basename(C))
            else:
                html.write('     ')
            if C_log:
                html.write(' <a href="%s">C_log</a>' % os.path.basename(C_log))
            else:
                html.write('     ')
            html.write('  <a href="%s">%s</a>' % (bn, bn))
            html.write('\n')
        html.write('<br><br>')
        for i, save in enumerate(saved):
            if type(save) == str:
                continue # skip dir entries
            fn, log, root, root_log, pdf, pdf_log, C, C_log = save
            bn = os.path.basename(fn)
            rootlink = ', <a href="%s">root</a>' % os.path.basename(root) if root else ''
            html.write('<h4 id="%s"><a href="#%s">%s</a>%s</h4><br>\n' % (self.anchor_name(fn), self.anchor_name(fn), bn.replace('.png', ''), rootlink))
            if log:
                html.write('<img src="%s"><img src="%s"><br><br>\n' % (bn, os.path.basename(log)))
            else:
                html.write('<img src="%s"><br><br>\n' % bn)
        if num_pages > 1:
            write_pages_line()
        html.write('</pre></body></html>\n')
        
    def set_plot_dir(self, plot_dir):
        self.write_index()
        self.saved = []
        if plot_dir is not None and '~' in plot_dir:
            plot_dir = os.path.expanduser(plot_dir)
        self.plot_dir = plot_dir
        if plot_dir is not None:
            os.system('mkdir -p %s' % self.plot_dir)

    def save_dir(self, n):
        if self.plot_dir is None:
            raise ValueError('save_dir called before plot_dir set!')
        self.saved.append(n)

    def save(self, n, log=None, root=None, root_log=None, pdf=None, pdf_log=None, C=None, C_log=None, logz=None, other_c=None):
        can = self.c if other_c is None else other_c

        if logz:
            logfcn = can.SetLogz
        else:
            logfcn = can.SetLogy

        log = self.log if log is None else log
        root = self.root if root is None else root
        root_log = self.root_log if root_log is None else root_log
        pdf = self.pdf if pdf is None else pdf
        pdf_log = self.pdf_log if pdf_log is None else pdf_log
        C = self.C if C is None else C
        C_log = self.C_log if C_log is None else C_log
        
        if self.plot_dir is None:
            raise ValueError('save called before plot_dir set!')
        can.SetLogy(0)
        fn = os.path.join(self.plot_dir, n + '.png')
        can.SaveAs(fn)
        if root:
            root = os.path.join(self.plot_dir, n + '.root')
            can.SaveAs(root)
        if root_log:
            logfcn(1)
            root_log = os.path.join(self.plot_dir, n + '_log.root')
            can.SaveAs(root_log)
            logfcn(0)
        if log:
            logfcn(1)
            log = os.path.join(self.plot_dir, n + '_log.png')
            can.SaveAs(log)
            logfcn(0)
        if pdf:
            pdf = os.path.join(self.plot_dir, n + '.pdf')
            can.SaveAs(pdf)
        if pdf_log:
            logfcn(1)
            pdf_log = os.path.join(self.plot_dir, n + '_log.pdf')
            can.SaveAs(pdf_log)
            logfcn(0)
        if C:
            C = os.path.join(self.plot_dir, n + '.C')
            can.SaveAs(C_fn)
        if C_log:
            logfcn(1)
            C_log = os.path.join(self.plot_dir, n + '_log.C')
            can.SaveAs(C_log)
            logfcn(0)
        self.saved.append((fn, log, root, root_log, pdf, pdf_log, C, C_log))

def rainbow_palette(num_colors=500):
    """Make a rainbow palette with the specified number of
    colors. Also call SetNumberContours so it actually gets used when
    drawing COLZ."""
    
    r = array('d', [0, 0, 0, 1, 1])
    g = array('d', [0, 1, 1, 1, 0])
    b = array('d', [1, 1, 0, 0, 0])
    stops = array('d', [float(i)/4 for i in xrange(5)])
    ROOT.TColor.CreateGradientColorTable(5, stops, r, g, b, num_colors)
    ROOT.gStyle.SetNumberContours(num_colors)

def ratios_plot(name,
                hists,
                plot_saver = None,
                output_fn = None,
                canvas_size = (600, 600),
                canvas_top_margin = 0.05,
                canvas_bottom_margin = 0.3,
                canvas_left_margin = 0.12,
                canvas_right_margin = 0.08,
                x_title_offset = 1.,
                y_title_offset = 1.5,
                x_title_size = 0.04,
                y_title_size = 0.04,
                y_label_size = 0.03,
                x_range = None,
                y_range = None,
                res_divide_opt = {},
                res_line_width = 2,
                res_x_title_size = 0.04,
                res_x_title_offset = 1.,
                res_y_title = 'ratio',
                res_y_title_offset = None,
                res_y_title_size = None,
                res_x_label_size = 0.03,
                res_y_label_size = 0.03,
                res_y_range = (0., 2.),
                res_draw_cmd = 'pez',
                res_fit = True,
                res_lines = None,
                res_fcns = [],
                legend = None,
                move_overflows = 'under over',
                draw_normalized = False,
                statbox_size = None,
                which_ratios = 'first', # 'first' or 'pairs'
                ):
    '''With n hists/graphs, draw them and the n-1 ratios to hists[0].
    hists can be a list of just the hists/graphs, or it can be a list
    of tuples (object, draw_cmd).

    NB: for some reason, hists without Sumw2 called on them don't play
    nice (aren't drawn? disappear?) with something in this...
    '''

    _hists, draw_cmds = [], []
    for x in hists:
        if type(x) in (tuple,list):
            h,dc = x
            assert type(dc) == str
            _hists.append(h)
            draw_cmds.append(dc)
        else:
            _hists.append(x)
            draw_cmds.append('')
    hists = _hists

    are_hists  = all(h.Class().GetName().startswith('TH1') or h.Class().GetName().startswith('TProfile') for h in hists)
    are_graphs = all(h.Class().GetName().startswith('TGraph') for h in hists)

    # Sanity checks on the parameters.
    if not are_hists and not are_graphs:
        raise ValueError('hists must be either all TH1-descended or TGraph-descended')
    if draw_normalized and are_graphs:
        raise ValueError('no draw_normalized for graphs')
    if output_fn is None and plot_saver is None:
        raise ValueError('at least one of output_fn, plot_saver must be supplied')
    elif output_fn is not None and plot_saver is not None:
        raise ValueError('only one of output_fn and plot_saver may be supplied')
    if 'a' in res_draw_cmd:
        raise ValueError('no "a" in res_draw_cmd')
    if which_ratios not in ('first','pairs'):
        raise ValueError('which_ratios must be either "first" or "pairs"')

    res_fcns = [(x + ('',) if type(x) != tuple else x) for x in res_fcns]

    canvas = ROOT.TCanvas('c_ratiosplot_' + name, '', *canvas_size)
    canvas.SetTopMargin(canvas_top_margin)
    canvas.SetBottomMargin(canvas_bottom_margin)
    canvas.SetLeftMargin(canvas_left_margin)
    canvas.SetRightMargin(canvas_right_margin)

    if plot_saver is not None:
        plot_saver.old_c = plot_saver.c
        plot_saver.c = canvas

    def zzz(h):
        h.GetXaxis().SetLabelSize(0) # the data/MC ratio part will show the labels
        h.GetXaxis().SetTitleSize(x_title_size)
        h.GetYaxis().SetTitleSize(y_title_size)
        h.GetXaxis().SetTitleOffset(x_title_offset)
        h.GetYaxis().SetTitleOffset(y_title_offset)
        h.GetYaxis().SetLabelSize(y_label_size)
        if x_range:
            h.GetXaxis().SetRangeUser(*x_range)
        if y_range:
            h.GetYaxis().SetRangeUser(*y_range)

    if are_graphs:
        gg = ROOT.TMultiGraph()

    for i,(h,dc) in enumerate(zip(hists, draw_cmds)):
        zzz(h)

        if are_graphs:
            if 'a' in dc:
                dc.replace('a', '')
            if not dc:
                dc = 'p'
            gg.Add(h, dc)
        elif are_hists:
            if move_overflows:
                move_overflows_into_visible_bins(h, move_overflows)
            if draw_normalized:
                h.v = h.GetMaximum() / h.Integral(0,h.GetNbinsX()+1)
            else:
                h.v = h.GetMaximum()

    if are_graphs:
        gg.Draw('a')
        zzz(gg)
        gg.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
        #canvas.Update()
    else:
        #for i,h in enumerate(sorted(hists, key=lambda h: h.v, reverse=True)): # this sorts by the integral
        for i,h in enumerate(hists) : # this keeps the initial order
            cmd = h.DrawNormalized if draw_normalized else h.Draw
            dc = draw_cmds[i]
            if i == 0:
                if dc: # Draw never liked Draw('')
                    cmd(dc)
                else:
                    cmd()
            else:
                cmd('sames ' + dc)

    if are_hists:
        canvas.Update()
        if statbox_size is None:
            for h in hists:
                h.SetStats(0)
        else:
            for i,h in enumerate(hists):
                differentiate_stat_box(h, i, new_size=statbox_size)

    if legend is not None:
        legend = ROOT.TLegend(*legend)
        legend.SetTextFont(42)
        legend.SetBorderSize(0)
        for h in hists:
            legend.AddEntry(h, h.nice, 'LPE')
        for res_fcn, res_fcn_title in res_fcns:
            if res_fcn_title:
                legend.AddEntry(res_fcn, res_fcn_title, 'L')
        legend.Draw()

    ratio_pad = ROOT.TPad('ratio_pad_' + name, '', 0, 0, 1, 1)
    ratio_pad.SetTopMargin(1-canvas_bottom_margin + 0.015)
    ratio_pad.SetLeftMargin(canvas_left_margin)
    ratio_pad.SetRightMargin(canvas_right_margin)
    ratio_pad.SetFillColor(0)
    ratio_pad.SetFillStyle(0)
    ratio_pad.Draw()
    ratio_pad.cd(0)

    ratios = []
    old_opt_fit = None
    fit_tpt = None

    if which_ratios == 'first':
        pairs_for_ratios = [(hists[0],h) for h in hists[1:]]
    elif which_ratios == 'pairs':
        pairs_for_ratios = list(chunks(hists, 2))

    if type(res_y_range) == float: # dynamic, the number is the fraction to add under/over min/max
        min_r, max_r = 1e99, -1e99
        for h0,h in pairs_for_ratios:
            v1, v2 = histogram_divide_values(h, h0, True)
            xa, xb = h.GetBinLowEdge(h.GetXaxis().GetFirst()), h.GetBinLowEdge(h.GetXaxis().GetLast())
            rs = [v1.y[i] / v2.y[i] for i in xrange(v2.n) if v2.y[i] != 0. and xa < v1.x[i] < xb]
            if rs:
                min_r = min(min_r, min(rs))
                max_r = max(max_r, max(rs))
        res_y_range = min_r*(1-res_y_range), max_r*(1+res_y_range)

    for i,(h0,h) in enumerate(pairs_for_ratios):
        r = histogram_divide(h, h0, **res_divide_opt)
        if not r:
            continue
        ratios.append(r)
        r.SetMarkerStyle(20)
        r.SetMarkerSize(0)
        r.SetLineWidth(h.GetLineWidth())
        r.SetLineColor(h.GetLineColor())
        if not x_range:
            if are_hists:
                x_range = h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax()
            elif are_graphs:
                x_range = gg.GetXaxis().GetXmin(), gg.GetXaxis().GetXmax()
        r.GetXaxis().SetLimits(*x_range)
        r.GetXaxis().SetTitleSize(res_x_title_size)
        r.GetXaxis().SetTitleOffset(res_x_title_offset)
        r.GetXaxis().SetLabelSize(res_x_label_size)
        r.GetYaxis().SetLabelSize(res_y_label_size)
        r.GetYaxis().SetTitleOffset(res_y_title_offset if res_y_title_offset is not None else y_title_offset)
        r.GetYaxis().SetTitleSize(res_y_title_size if res_y_title_size is not None else y_title_size)
        r.GetYaxis().SetRangeUser(*res_y_range)
        r.GetYaxis().SetNdivisions(505)
        r.SetTitle(';%s;%s' % (h.GetXaxis().GetTitle(), res_y_title))
        if i == 0:
            r.Draw('a' + res_draw_cmd)
        else:
            r.Draw(res_draw_cmd)

        if res_fit:
            old_opt_fit = ROOT.gStyle.GetOptFit()
            ROOT.gStyle.SetOptFit(0)
            fit_opt = 'sqe'
            fcn = ROOT.TF1('f_rat_' + h.GetName(), 'pol1' if res_fit == 'pol1' else 'pol0')
            fcn.SetLineColor(h.GetLineColor())
            fit_res = r.Fit(fcn, fit_opt)
            ratio_pad.Update()

            if fit_tpt is None:
                x_width = x_range[1] - x_range[0]
                res_y_width = res_y_range[1] - res_y_range[0]
                fit_tpt = ROOT.TPaveText(x_range[0] + x_width/100,
                                         res_y_range[1] - res_y_width/6 * len(hists),
                                         x_range[0] + x_width / 2,
                                         res_y_range[1] - res_y_width/10)
                fit_tpt.SetBorderSize(0)
                fit_tpt.SetFillColor(ROOT.kWhite)
                fit_tpt.SetTextFont(42)
            if res_fit == 'pol1':
                txt = fit_tpt.AddText('p0 = %.2f #pm %.2f  p1 = %.2f #pm %.2f  #chi^{2}/ndf = %.2f/%i  p = %.3f' % (fit_res.Parameter(0), fit_res.ParError(0), fit_res.Parameter(1), fit_res.ParError(1), fit_res.Chi2(), fit_res.Ndf(), fit_res.Prob()))
            else:
                txt = fit_tpt.AddText('p0 = %.2f #pm %.2f  #chi^{2}/ndf = %.2f/%i  p = %.3f' % (fit_res.Parameter(0), fit_res.ParError(0), fit_res.Chi2(), fit_res.Ndf(), fit_res.Prob()))
            txt.SetTextAlign(12)
            txt.SetTextColor(h.GetLineColor())

    if res_lines and ratios:
        if type(res_lines) in (int,float):
            res_lines = [res_lines]
        if all([type(x) in (int,float) for x in res_lines]):
            res_lines = [(x, 1, 1, 7) for x in res_lines]
        res_ls = []
        for res_line_y, res_line_color, res_line_width, res_line_style in res_lines:
            if res_y_range[0] < res_line_y < res_y_range[1]:
                res_l = ROOT.TLine(x_range[0], res_line_y, x_range[1], res_line_y)
                res_ls.append(res_l)
                res_l.SetLineColor(res_line_color)
                res_l.SetLineWidth(res_line_width)
                res_l.SetLineStyle(res_line_style)
                res_l.Draw()

    if ratios:
        for res_fcn, _ in res_fcns:
            res_fcn.Draw('same')

    if fit_tpt:
        fit_tpt.Draw()

    if plot_saver is not None:
        plot_saver.save(name)
        plot_saver.c = plot_saver.old_c
        plot_saver.c.cd()
    elif output_fn is not None:
        canvas.SaveAs(output_fn)

    if old_opt_fit is not None:
        ROOT.gStyle.SetOptFit(old_opt_fit)

    return namedtuple('ratios_plot_result', 'canvas legend ratio_pad ratios'.split())(canvas, legend, ratio_pad, ratios)

def real_hist_max(h, return_bin=False, user_range=None, use_error_bars=True):
    """Find the real maximum value of the histogram, taking into
    account the error bars and/or the specified range."""

    m_ibin = None
    m = 0

    if user_range is None:
        b1, b2 = 1, h.GetNbinsX() + 1
    else:
        b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])+1
    
    for ibin in xrange(b1, b2):
        if use_error_bars:
            v = h.GetBinContent(ibin) + h.GetBinError(ibin)
        else:
            v = h.GetBinContent(ibin)
        if v > m:
            m = v
            m_ibin = ibin
    if return_bin:
        return m_ibin, m
    else:
        return m

def real_hist_min(h, return_bin=False, user_range=None):
    """Find the real minimum value of the histogram, ignoring empty
    bins, and taking into account the specified range."""

    m_ibin = None
    m = 99e99

    if user_range is None:
        b1, b2 = 1, h.GetNbinsX() + 1
    else:
        b1, b2 = h.FindBin(user_range[0]), h.FindBin(user_range[1])+1
    
    for ibin in xrange(b1, b2):
        v = h.GetBinContent(ibin)
        if v > 0 and v < m:
            m = v
            m_ibin = ibin
    if return_bin:
        return m_ibin, m
    else:
        return m

def root_fns_from_argv():
    return [x for x in sys.argv[1:] if os.path.isfile(x) and x.endswith('.root')]

def set_style(date_pages=False):
    ROOT.TH1.SetDefaultSumw2() # when would we ever not want to?
    ROOT.gEnv.SetValue('Hist.Precision.1D', 'double') # use TH1D instead of TH1F with TTree::Draw--again, why not do it always
    ROOT.gStyle.SetHistMinimumZero(1)
    ROOT.gStyle.SetPadTickX(1)
    ROOT.gStyle.SetPadTickY(1)
    ROOT.gStyle.SetOptStat(1222222)
    ROOT.gStyle.SetOptFit(2222)
    ROOT.gErrorIgnoreLevel = 1001 # Suppress TCanvas::SaveAs messages.
    return
    ROOT.gStyle.SetFillColor(0)
    if date_pages:
        ROOT.gStyle.SetOptDate()
    ROOT.gStyle.SetGridStyle(3)
    ROOT.gStyle.SetStatFormat('6.4g')
    ROOT.gStyle.SetPalette(1)
    ROOT.gStyle.SetTitleFont(42, 'XYZ')
    ROOT.gStyle.SetLabelFont(42, 'XYZ')
    ROOT.gStyle.SetStatFont(42)
    ROOT.gStyle.SetLegendFont(42)

def sort_histogram_pair(h1, h2, by=real_hist_max):
    """Return the pair ordered by e.g. real_hist_max to know which to
    draw first."""
    
    if real_hist_max(h1) > real_hist_max(h2):
        return h1,h2
    else:
        return h2,h1

def tdirectory_walk(root):
    keys = [k.ReadObj() for k in root.GetListOfKeys()]
    dirs, files = [], []
    for k in keys:
        if type(k) == ROOT.TDirectoryFile:
            dirs.append(k)
        else:
            files.append(k)
    yield root, dirs, files
    for d in dirs:
        for x in tdirectory_walk(d):
            yield x

def tdr_style():
    s =  ROOT.TStyle("s","Style for P-TDR")
    s.SetCanvasBorderMode(0)
    s.SetCanvasColor(ROOT.kWhite)
    s.SetCanvasDefH(600)
    s.SetCanvasDefW(600)
    s.SetCanvasDefX(0)
    s.SetCanvasDefY(0)

    s.SetPadBorderMode(0)
    s.SetPadColor(ROOT.kWhite)
    s.SetPadGridX(False)
    s.SetPadGridY(False)
    s.SetGridColor(0)
    s.SetGridStyle(3)
    s.SetGridWidth(1)

    s.SetFrameBorderMode(0)
    s.SetFrameBorderSize(1)
    s.SetFrameFillColor(0)
    s.SetFrameFillStyle(0)
    s.SetFrameLineColor(1)
    s.SetFrameLineStyle(1)
    s.SetFrameLineWidth(1)
  
    s.SetHistLineColor(1)
    s.SetHistLineStyle(0)
    s.SetHistLineWidth(1)

    s.SetEndErrorSize(2)
  
    s.SetMarkerStyle(20)
  
    s.SetOptFit(1)
    s.SetFitFormat("5.4g")
    s.SetFuncColor(2)
    s.SetFuncStyle(1)
    s.SetFuncWidth(1)

    s.SetOptDate(0)

    s.SetOptFile(0)
    s.SetOptStat(0)
    s.SetStatColor(ROOT.kWhite)
    s.SetStatFont(42)
    s.SetStatFontSize(0.025)
    s.SetStatTextColor(1)
    s.SetStatFormat("6.4g")
    s.SetStatBorderSize(1)
    s.SetStatH(0.1)
    s.SetStatW(0.15)

    s.SetPadTopMargin(0.05)
    s.SetPadBottomMargin(0.13)
    s.SetPadLeftMargin(0.16)
    s.SetPadRightMargin(0.02)

    s.SetOptTitle(0)
    s.SetTitleFont(42)
    s.SetTitleColor(1)
    s.SetTitleTextColor(1)
    s.SetTitleFillColor(10)
    s.SetTitleFontSize(0.05)

    s.SetTitleColor(1, "XYZ")
    s.SetTitleFont(42, "XYZ")
    s.SetTitleSize(0.06, "XYZ")
    s.SetTitleXOffset(0.9)
    s.SetTitleYOffset(1.25)

    s.SetLabelColor(1, "XYZ")
    s.SetLabelFont(42, "XYZ")
    s.SetLabelOffset(0.007, "XYZ")
    s.SetLabelSize(0.05, "XYZ")

    s.SetAxisColor(1, "XYZ")
    s.SetStripDecimals(True)
    s.SetTickLength(0.03, "XYZ")
    s.SetNdivisions(510, "XYZ")
    s.SetPadTickX(1)
    s.SetPadTickY(1)

    s.SetOptLogx(0)
    s.SetOptLogy(0)
    s.SetOptLogz(0)

    s.SetPaperSize(20.,20.)

    s.SetHatchesLineWidth(5)
    s.SetHatchesSpacing(0.05)

    s.cd()
    return s
    
def tgraph(vals):
    '''Make a TGraphAsymmErrors with the appropriate sets of numbers
    from vals according to their dimension. (All elements of vals must
    have the same dimension.)
    dimension = 1: vals are the y-coordinates, and the x-coordinates are range(n).
    dimension = 2: vals are (x,y).
    dimension = 3: vals are (x,y,ey).
    dimension = 4: vals are (x,ex,y,ey).
    dimension = 6: vals are (x,exl,exh,y,eyl,eyh).
    Other dimensions are not allowed.
    '''

    n = len(vals)
    vals2 = []
    for v in vals:
        try:
            iter(v)
        except TypeError:
            v = [v]
        vals2.append(v)
    vals = vals2
    dim = set(len(v) for v in vals)
    if len(dim) != 1:
        raise ValueError('everything in vals passed to tgraph* must be same dimension')
    dim = dim.pop()
    
    def _t(x,y, **kwargs):
        if kwargs.has_key('ex'):
            exl = exh = kwargs['ex']
        else:
            exl = kwargs.get('exl', [])
            exh = kwargs.get('exh', [])
            assert all((exl,exh)) or not any((exl,exh))
        if kwargs.has_key('ey'):
            eyl = eyh = kwargs['ey']
        else:
            eyl = kwargs.get('eyl', [])
            eyh = kwargs.get('eyh', [])
            assert all((eyl,eyh)) or not any((eyl,eyh))
        if not exl: exl = [0.]*n
        if not exh: exh = [0.]*n
        if not eyl: eyl = [0.]*n
        if not eyh: eyh = [0.]*n
        x = to_array(x)
        y = to_array(y)
        exl = to_array(exl)
        exh = to_array(exh)
        eyl = to_array(eyl)
        eyh = to_array(eyh)
        return ROOT.TGraphAsymmErrors(n, x, y, exl, exh, eyl, eyh)

    if dim == 1:
        x = range(n)
        return _t([float(i) for i in xrange(n)], [v[0] for v in vals])
    elif dim == 2:
        x,y = zip(*vals)
        return _t(x,y)
    elif dim == 3:
        x,y,ey = zip(*vals)
        return _t(x,y, ey=ey)
    elif dim == 4:
        x,ex,y,ey = zip(*vals)
        return _t(x,y, ex=ex, ey=ey)
    elif dim == 6:
        x,exl,exh,y,eyl,eyh = zip(*vals)
        return _t(x,y, exl=exl, exh=exh, eyl=eyl, eyh=eyh)
    else:
        raise ValueError('dimension %i not supported' % dim)

def tgraph_getpoint(g, i):
    x,y = ROOT.Double(), ROOT.Double()
    if i < 0:
        i += g.GetN()
    g.GetPoint(i,x,y)
    return x,y

def tgraph_points(g):
    return [tgraph_getpoint(g, i) for i in xrange(g.GetN())]

def to_array(*l):
    if type(l[0]) in (tuple, list):
        return array('d', l[0])
    else:
        return array('d', l)

def to_ascii(o, fn_or_f, fmt='%.6g', sep='\t'):
    '''Dump object o to file. Supported right now are TH1 and TH2, but
    TH3, TGraph and TTree are easy.
    Gotchas:
    TH[12]: currently we don't write overflow.'''
    if type(fn_or_f) == str:
        fn = fn_or_f
        if os.path.exists(fn):
            raise OSError('refusing to clobber %s' % fn)
        f = open(fn)
    else:
        f = fn_or_f

    def write(*l, **d):
        f.write(sep.join([d.get('fmt', fmt)] * len(l)) % l)
        f.write('\n')

    if isinstance(o, ROOT.TH2):
        write('x','y','z','ez', fmt='%s')
        for ix in xrange(1, o.GetNbinsX()+1):
            for iy in xrange(1, o.GetNbinsY()+1):
                write(o.GetXaxis().GetBinLowEdge(ix),
                      o.GetYaxis().GetBinLowEdge(iy),
                      o.GetBinContent(ix, iy),
                      o.GetBinError  (ix, iy),
                      )

    elif isinstance(o, ROOT.TH1):
        write('x','y','ey', fmt='%s')
        for ix in xrange(1, o.GetNbinsX()+1):
            write(o.GetXaxis().GetBinLowEdge(ix),
                  o.GetBinContent(ix),
                  o.GetBinError  (ix))

def to_TH1D(h, name):
    hh = ROOT.TH1D(name, h.GetTitle(), h.GetNbinsX(), h.GetXaxis().GetXmin(), h.GetXaxis().GetXmax())
    hh.Sumw2()
    for ibin in xrange(h.GetNbinsX()+2):
        hh.SetBinContent(ibin, h.GetBinContent(ibin))
        hh.SetBinError  (ibin, h.GetBinError  (ibin))
        hh.SetEntries(h.GetEntries())
    return hh

def ttree_iterator(tree, return_tree=False):
    for jentry in xrange(tree.GetEntriesFast()):
        if tree.LoadTree(jentry) < 0: break
        if tree.GetEntry(jentry) <= 0: continue
        if return_tree:
            yield jentry, tree
        else:
            yield jentry

zbi = ROOT.RooStats.NumberCountingUtils.BinomialWithTauObsZ

def zgammatau(x,y,tau,tau_uncert,_l=[0]):
    '''For the on-off problem [arXiv:physics/0702156] when the
    uncertainty in tau is not negligible. Assume a Gaussian prior for
    tau with some sigma given by tau_uncert. The x,y,tau are as in zbi
    above: x is the observation in the signal ("on") region, y is the
    observation in the sideband region ("off"), and tau is the ratio
    of the sizes of the regions off / on.

    JMTBAD this should be optimized. The _l crap is so you don't run
    into having the same symbols in the same namespace with repeated
    calls. Probably should just do without workspace/factory. And it
    doesn't seem to work for too-small values of tau_uncert...
    '''

    ROOT.RooMsgService.instance().setGlobalKillBelow(ROOT.RooFit.WARNING)
    w = ROOT.RooWorkspace('w' + str(_l[0]), True)
    def factory(w,s):
        #print s
        w.factory(s)
    _l[0] += 1
    factory(w, "Poisson::px(x[%f,0,500],sum::splusb(s[0,0,100],b[%f,0,300]))" % (x, y/tau))
    factory(w, "Poisson::py(y[%f,0,500],prod::taub(tau[%f,0,1.5],b))" % (y,tau))
    factory(w, "Uniform::prior_b(b)")
    factory(w, "Gaussian::prior_tau(tau,%f,%f)" % (tau,tau_uncert))
    factory(w, "PROJ::avgModel2(PROJ::averagedModel(PROD::foo(px|b,py,prior_b,prior_tau),b),tau)") 
    w.var("x").setVal(x)
    w.var("y").setVal(y)
    cdf = w.pdf("avgModel2").createCdf(ROOT.RooArgSet(w.var("x")))
    #print "Hybrid p-value = ", cdf.getVal(), "Z_Gamma Significance  = ", ROOT.RooStats.PValueToSignificance(1-cdf.getVal())
    return ROOT.RooStats.PValueToSignificance(1-cdf.getVal())

def zgammatauwrong(x,y,tau,tau_uncert):
    '''See zgammatau for the model, but here do the wrong thing and
    average over some range of taus given by tau +- 2*tau_uncert.
    '''

    n = 100
    a = max(tau - 2*tau_uncert, 0.)
    b = tau + 2*tau_uncert
    dt = (b-a)/n
    z, nz = 0., 0.
    for i in xrange(n):
        t = a + i*dt
        p = ROOT.Math.normal_pdf(t, tau_uncert, tau) * dt
        nz += p
        z += zbi(x,y,t) * p
    return z / nz

__all__ = [
    'apply_hist_commands',
    'array',
    'bin_iterator',
    'check_consistency',
    'histogram_divide',
    'wilson_score_vpme',
    'wilson_score',
    'effective_wilson_score_vpme',
    'effective_wilson_score',
    'clopper_pearson',
    'clopper_pearson_poisson_means',
    'propagate_ratio',
    'effective_n',
    'interval_to_vpme',
    'cm2mm',
    'cmssw_setup',
    'compare_hists',
    'core_gaussian',
    'cumulative_histogram',
    'cut',
    'data_mc_comparison',
    'detree',
    'differentiate_stat_box',
    'draw_in_order',
    'flatten_directory',
    'fit_gaussian',
    'get_bin_content_error',
    'get_integral',
    'integral',
    'get_hist_quantiles',
    'get_quantiles',
    'get_hist_stats',
    'graph_divide',
    'draw_hist_register',
    'make_rms_hist',
    'move_below_into_bin',
    'move_above_into_bin',
    'move_overflows_into_visible_bins',
    'move_overflow_into_last_bin',
    'move_stat_box',
    'p4',
    'plot_dir',
    'plot_saver',
    'poisson_interval',
    'poisson_intervalize',
    'poisson_means_divide',
    'rainbow_palette',
    'ratios_plot',
    'real_hist_max',
    'real_hist_min',
    'resize_stat_box',
    'root_fns_from_argv',
    'set_style',
    'sort_histogram_pair',
    'tdirectory_walk',
    'tdr_style',
    'tgraph',
    'tgraph_getpoint',
    'tgraph_points',
    'to_array',
    'to_ascii',
    'to_TH1D',
    'ttree_iterator',
    'zbi',
    'zgammatau',
    'zgammatauwrong',
    'ROOT',
    'math', 'sys', 'os', 'glob', 'array', 'defaultdict', 'namedtuple'
    ]

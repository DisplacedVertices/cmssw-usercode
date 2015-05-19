#from base_draw_fit import *

from array import array
from copy import copy
from math import log
from itertools import izip
from JMTucker.Tools.ROOTTools import *
set_style()
ROOT.gStyle.SetOptFit(0)
ps = plot_saver('plots/xxxlimits', size=(600,600), log=False, root=False)

def make_tge(x, y, ey):
    n = len(x)
    return ROOT.TGraphErrors(n, x, y, array('d', [0.]*n), ey)

def make_fcn(name, color, fit_range, pars):
    fcn = ROOT.TF1(name, '[0]+[1]*x', *fit_range)
    fcn.SetLineColor(color)
    fcn.SetLineWidth(2)
    fcn.SetParameters(*pars)
    return fcn

def find_x(fcn):
    val = log(0.05)
    a = fcn.GetParameter(0)
    b = fcn.GetParameter(1)
    return (val - a)/b

def find_limit(name, tree):
    limits = []

    for j in ttree_iterator(tree):
        for v in 'sig_limits pval_limits pval_limit_errs'.split():
            exec '%s = array("d", list(t.%s))' % (v,v)

        log_pval_limits = array('d')
        log_pval_limit_errs = array('d')
        for p, pe in izip(pval_limits, pval_limit_errs):
            lp = log(p)
            lpe = pe/p
            log_pval_limits.append(lp)
            log_pval_limit_errs.append(lpe)

        g_all = make_tge(sig_limits, log_pval_limits, log_pval_limit_errs)

        # find range for overall fit
        i = len(sig_limits)-2
        ever_above = False
        while i >= 0:
            pi   = pval_limits[i]
            pip1 = pval_limits[i+1]
            pe = (pval_limit_errs[i]**2 + pval_limit_errs[i+1]**2)**0.5
            #print i, pi, pip1, pe, abs(pi-pip1), 2*pe, abs(pi - pip1) < 3*pe, pi >= 0.15
            if pi >= 0.15:
                ever_above = True
                if abs(pi - pip1) < 3*pe:
                    break
            i -= 1
        if i == -1:
            i = 0

        print 'skip to', i
        sig_limits = sig_limits[i:]
        pval_limits = pval_limits[i:]
        pval_limit_errs = pval_limit_errs[i:]
        log_pval_limits = log_pval_limits[i:]
        log_pval_limit_errs = log_pval_limit_errs[i:]

        skip = []
        delta = 0
        for i, (s, p, pe) in enumerate(izip(sig_limits, pval_limits, pval_limit_errs)):
            if p > 0.8:
                skip.append(i-delta)
                delta += 1

        g_range = make_tge(sig_limits, log_pval_limits, log_pval_limit_errs)
        fit_range = sig_limits[0], sig_limits[-1]

        lf = ROOT.TLinearFitter(1, 'pol1')
        for s, lp, lpe in izip(sig_limits, log_pval_limits, log_pval_limit_errs):
            lf.AddPoint(array('d', [s]), lp, lpe)
        lf_ret = lf.EvalRobust()
        fcn_lf = make_fcn('fcn_lf', ROOT.kMagenta, fit_range, (lf.GetParameter(0), lf.GetParameter(1)))
        bits = ROOT.TBits()
        lf.GetFitSample(bits)
        nused = bits.CountBits()
        print 'lf.EvalRobust() returns', lf_ret, 'used # points:', bits.CountBits()
        print lf.PrintResults(3)
        print

        print 'just fit normal'
        fcn_range = make_fcn('fcn_range', ROOT.kBlue, fit_range, (-8e-3, -0.4))
        res = g_range.Fit(fcn_range, 'RVS')
        res.Print()
        print

        for s in skip:
            for l in (sig_limits, log_pval_limits, log_pval_limit_errs):
                l.pop(s) # second or later skips already calibrated for offset after popping previous

        g_skip = make_tge(sig_limits, log_pval_limits, log_pval_limit_errs)

        print 'now fit skipping p > 0.8'
        fcn_skip = make_fcn('fcn_skip', ROOT.kGreen+2, fit_range, (-8e-3, -0.4))
        res = g_skip.Fit(fcn_skip, 'RVS')
        res.Print()

        g_all.SetLineColor(28)
        g_all.SetMarkerColor(28)
        g_all.SetMarkerStyle(20)

        g_skip.SetLineColor(46)
        g_skip.SetMarkerColor(46)

        gg = ROOT.TMultiGraph()
        for g,c in ((g_all, 1), (g_range, ROOT.kBlue), (g_skip, ROOT.kRed)):
            g.SetLineColor(c)
            g.SetMarkerColor(c)
            g.SetMarkerStyle(20)
            g.SetMarkerSize(1)
            gg.Add(g, 'LP')
        gg.Draw('A')

        fcn_lf.Draw('same')

        x_lf = find_x(fcn_lf)
        x_skip = find_x(fcn_skip)
        print x_lf, x_skip
        zzz = ''
        if x_lf < 0:
            zzz += '_NEG'
        if abs(x_lf - x_skip) > 0.3:
            zzz += '_BIGDIFF'
        if nused < 5:
            zzz += '_FEWPTS'
        
        limits.append(x_lf)
        ps.save('%s_%i%s' % (name, j, zzz))

    return limits

def stats(l, header='', save_plot=True):
    if save_plot:
        h = ROOT.TH1F(header, '', 100, min(l) - 0.5, max(l) + 0.5)
        for x in l:
            h.Fill(x)
        h.Draw()
        ps.save(header)
        hc = cumulative_histogram(h)
        hc.Draw()
        ps.save(header + '_cumu')
    l.sort()
    n = len(l)
    if n % 2 == 0:
        median = (l[n/2] + l[n/2-1])/2.
    else:
        median = l[n/2]
    lo68 = l[int(n/2 - 0.34*n)]
    hi68 = l[int(n/2 + 0.34*n)]
    lo95 = l[int(n/2 - 0.475*n)]
    hi95 = l[int(n/2 + 0.475*n)]
    print '\n'
    print header
    print header + ':Expected  2.5%: r <', lo95
    print header + ':Expected 16.0%: r <', lo68
    print header + ':Expected 50.0%: r <', median
    print header + ':Expected 84.0%: r <', hi68
    print header + ':Expected 97.5%: r <', hi95
    print header + ':Observed Limit: r <', median
    return median, lo68, hi68, lo95, hi95

if 0:
    f = ROOT.TFile('mfvo2t_tmp-10.root')
    t = f.Get('Fitter/t_fit_info')
    find_limit('hello', t)
    f = ROOT.TFile('mfvo2t_normal.root')
    t = f.Get('Fitter/t_fit_info')
    find_limit('hello2', t)

if 0:
    from base_draw_fit import *
    ROOT.gStyle.SetOptFit(0)

    limits = find_limit('find', t)
    scale = sig_eff * ac.int_lumi / 1000. * ac.scale_factor
    limits_scaled = [limit / scale for limit in limits]

    stats(limits, 'mu_sig_limit')
    stats(limits_scaled, 'sigma_sig_limit')

if 1:
    f = ROOT.TFile('mfvo2t_mfv_neutralino_tau0300um_M0300.root')
    t = f.Get('Fitter/t_fit_info')
    limits = find_limit('hello', t)
    import JMTucker.MFVNeutralino.AnalysisConstants as ac
    sig_true = 1.4223
    sig_eff = sig_true / (ac.int_lumi / 1000. * ac.scale_factor)
    scale = sig_eff * ac.int_lumi / 1000. * ac.scale_factor
    limits_scaled = [limit / scale for limit in limits]
    print limits, limits_scaled


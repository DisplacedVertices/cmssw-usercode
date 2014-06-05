#!/usr/bin/env python

from base import *

sample = Samples.qcdht1000
svdist_cut = 0.048
svdist_cut_name = ('%.3f'% svdist_cut).replace('.', 'p')
min_ntracks = 5
plot_dir = 'plots/one2two/ntracks%i_%s_%s' % (min_ntracks, sample.name, svdist_cut_name)

################################################################################

ps = plot_saver(plot_dir, size=(600,600))
f, t = get_f_t(sample, min_ntracks)

########################################

# Fit delta phi = "dphi" in the sideband, and compare result to fit
# for all 2v events.

n2v = t.Draw('svdphi', 'nvtx == 2 && min_ntracks_ok')
nbins = int(round(1 + log(n2v, 2)))
print 'Sample: %s  n2v: %f  nbins: %i' % (sample.name, n2v, nbins)

t.Draw('svdphi >> h_2v_dphi(%i, %f, %f)' % (nbins, -pi, pi), 'nvtx == 2 && min_ntracks_ok')
h_2v_dphi = ROOT.h_2v_dphi.Clone('h_2v_dphi')

t.Draw('abs(svdphi) >> h_2v_absdphi(%i, 0, %f)' % (nbins, pi), 'nvtx == 2 && min_ntracks_ok')
h_2v_absdphi = ROOT.h_2v_absdphi.Clone('h_2v_absdphi')

t.Draw('svdphi >> h_2v_sideband_dphi(%i, %f, %f)' % (nbins, -pi, pi), 'nvtx == 2 && min_ntracks_ok && svdist < %f' % svdist_cut)
h_2v_sideband_dphi = ROOT.h_2v_sideband_dphi.Clone('h_2v_sideband_dphi')

t.Draw('abs(svdphi) >> h_2v_sideband_absdphi(%i, 0, %f)' % (nbins, pi), 'nvtx == 2 && min_ntracks_ok && svdist < %f' % svdist_cut)
h_2v_sideband_absdphi = ROOT.h_2v_sideband_absdphi.Clone('h_2v_sideband_absdphi')

def fit_dphi(h, is_abs, plot_name=None):
    class Result:
        def __init__(self, *args):
            self.exp, self.fcn, self.fit = args

    # Fitting to [0]*x**[1] doesn't work so well. Fit in steps of the
    # exponent and find the best chi2 ourselves.
    nsteps = 130
    steps = range(nsteps)
    results = []
    for step in steps:
        exp = 0.5 + 0.05*step
        integ = pi**(exp+1)/(exp+1)
        formula = '[0]*abs(x)**%.2f/%.9f' % (exp, integ)
        fcn = ROOT.TF1('f_absdphi_%s' % ('%.2f' % exp).replace('.', 'p'), formula, 0 if is_abs else -pi, pi)
        fit = h.Fit(fcn, 'ILRQS')
        results.append(Result(exp, fcn, fit))
    best = min(results, key=lambda result: result.fit.Chi2())

    # Go up by chi2 = 1 on either side to calculate rough 68% CL on exp.
    min_chi2 = best.fit.Chi2()
    target_chi2 = min_chi2 + 1
    i_min = results.index(best)
    for idelta, delta in enumerate((-1, 1)):
        i, chi2 = i_min, min_chi2
        while chi2 < min_chi2 + 1:
            i += delta
            chi2 = results[i].fit.Chi2()
        if delta < 0:
            best.exp_lo = results[i].exp
            best.chi2_lo = chi2
        else:
            best.exp_hi = results[i].exp
            best.chi2_hi = chi2
        
    if plot_name is not None:
        # Draw the chi2 well, and draw little lines indicating our
        # delta chi2 = 1 interval finding.
        exps = arrit(result.exp for result in results)
        chi2s = arrit(result.fit.Chi2() for result in results)
        g = ROOT.TGraph(nsteps, exps, chi2s)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.4)
        g.SetTitle('fit ndof = %i;#phi exponent;#chi^{2}' % results[0].fit.Ndf())
        g.Draw('ALP')

        l1 = ROOT.TLine(best.exp_lo, target_chi2, best.exp_hi, target_chi2)
        ll = ROOT.TLine(best.exp_lo, 0, best.exp_lo, target_chi2)
        lh = ROOT.TLine(best.exp_hi, 0, best.exp_hi, target_chi2)
        for l in (l1, ll, lh):
            l.Draw()
        ps.save(plot_name + '_chi2s')

        # Draw the best fit.
        hh = h.Clone('hh')
        hh.Fit(best.fcn, 'ILRQ')
        xtitle = '#Delta #phi'
        if is_abs:
            xtitle = '|%s|' % xtitle
        bin_width = hh.GetBinLowEdge(2) - hh.GetBinLowEdge(1)
        hh.SetTitle('best exp: %.2f (%.2f-%.2f @68%%CL);%s;events/%.3f' % (best.exp, best.exp_lo, best.exp_hi, xtitle, bin_width))
        ps.c.Update()
        s = move_stat_box(hh, (0.143, 0.497, 0.555, 0.862) if is_abs else (0.299, 0.5, 0.713, 0.864))
        s.SetOptStat(2222220)
        ps.save(plot_name + '_bestfit')

    return best, results

# Do the fits comparing dphi, |dphi| and sideband, all, and keep
# |dphi| sideband as f_dphi to use in the rest of the analysis.
f_dphi = None
for h in (h_2v_dphi, h_2v_absdphi, h_2v_sideband_dphi, h_2v_sideband_absdphi):
    hn = h.GetName().replace('h_','')
    is_abs = 'abs' in hn
    best, results = fit_dphi(h, is_abs, hn)
    if h is h_2v_sideband_absdphi:
        f_dphi = best
    
    print 'Best fit to %s%s: exp %.2f (%.2f-%.2f @68%%CL)  chi2: %.3f/%.1f  prob: %.4f' % ('|dphi|' if is_abs else ' dphi ',
                                                                                           ' in sideband' if 'sideband' in hn else '            ',
                                                                                           best.exp,
                                                                                           best.exp_lo,
                                                                                           best.exp_hi,
                                                                                           best.fit.Chi2(), best.fit.Ndf(), best.fit.Prob())

########################################

# Assemble h_dz. When run on MC, derive f_dz from this. When on data
# (and opening the box), check that h_dz is similar to MC.

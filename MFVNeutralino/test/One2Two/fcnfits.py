#!/usr/bin/env python

from base import *

samples = [Samples.qcdht1000]
use_weights = len(samples) > 1
for s in samples:
    s.weight = s.partial_weight * 20000 if use_weights else None
if use_weights:
    ROOT.TH1.SetDefaultSumw2()
sample_name = 'toy' if len(samples) > 1 else samples[0].name

svdist_cut = 0.048
svdist_cut_name = ('%.3f'% svdist_cut).replace('.', 'p')
min_ntracks = 5
plot_dir = 'plots/one2two/phifit_ntracks%i_svdist%s_%s' % (min_ntracks, svdist_cut_name, sample_name)

################################################################################

ps = plot_saver(plot_dir, size=(600,600))

################################################################################

# Fit delta phi = "dphi" in the sideband, and compare result to fit
# for all 2v events. Also construct the 1v_dphi distribution, to be
# used when doing the 1v sampling.

nbins = 8

h_2v_dphi             = ROOT.TH1F('h_2v_dphi'             , '', nbins, -pi, pi)
h_2v_absdphi          = ROOT.TH1F('h_2v_absdphi'          , '', nbins,   0, pi)
h_2v_sideband_dphi    = ROOT.TH1F('h_2v_sideband_dphi'    , '', nbins, -pi, pi)
h_2v_sideband_absdphi = ROOT.TH1F('h_2v_sideband_absdphi' , '', nbins,   0, pi)

for sample in samples:
    f, t = get_f_t(sample, min_ntracks)
    weight_str = '%s' if sample.weight is None else '%f*(%%s)' % sample.weight

    n2v = t.Draw('svdphi', weight_str % ('nvtx == 2 && min_ntracks_ok'))
    print 'Sample: %s  n2v: %f' % (sample.name, n2v)

    for svdphi, is_sideband in detree(t, 'svdphi:svdist < %f' % svdist_cut, 'nvtx == 2 && min_ntracks_ok', lambda x: (float(x[0]), bool(x[1]))):
        if sample.weight is None:
            h_2v_dphi.Fill(svdphi)
            h_2v_absdphi.Fill(abs(svdphi))
            if is_sideband:
                h_2v_sideband_dphi.Fill(svdphi)
                h_2v_sideband_absdphi.Fill(abs(svdphi))
        else:
            h_2v_dphi.Fill(svdphi, sample.weight)
            h_2v_absdphi.Fill(abs(svdphi), sample.weight)
            if is_sideband:
                h_2v_sideband_dphi.Fill(svdphi, sample.weight)
                h_2v_sideband_absdphi.Fill(abs(svdphi), sample.weight)

def fit_dphi(h, is_abs, plot_name=None):
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
        results.append(FitResult(fcn, fit))
        results[-1].exp = exp
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
        ps.update_canvas()
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

################################################################################

# Assemble h_dz. When run on MC, derive f_dz from this. When on data
# (and opening the box), check that h_dz is similar to MC.

for sideband in (False, True):
    cut = 'nvtx == 2 && min_ntracks_ok'
    if sideband:
        cut += ' && svdist < %f' % svdist_cut

    t.Draw('svdz >> h_2v_dz_all(400, -20, 20)', cut)
    h_2v_dz_all = ROOT.h_2v_dz_all.Clone('h_2v_dz_all')
    h_2v_dz_all.SetTitle('2v events;z0 - z1 (cm);events/1 mm')
    h_2v_dz_all.Draw()
    ps.update_canvas()
    s = move_stat_box(h_2v_dz_all, (0.673, 0.736, 0.980, 0.997))
    s.SetOptStat(2222220)
    ps.save('2v_%sdz_all' % ('sideband_' if sideband else ''))

    z_range = (-0.1, 0.1)
    t.Draw('svdz >> h_2v_dz(20, %f, %f)' % z_range, cut)
    h_2v_dz = ROOT.h_2v_dz.Clone('h_2v_dz')
    h_2v_dz.SetTitle('2v events;z0 - z1 (cm);events/100 #mum')
    fcn_dz = ROOT.TF1('f_dz', 'gaus', *z_range)
    f_dz = FitResult(fcn_dz, h_2v_dz.Fit(fcn_dz, 'RLQS'))
    ps.update_canvas()
    s = move_stat_box(h_2v_dz, (0.673, 0.686, 0.980, 0.997))
    s.SetOptStat(2222220)
    ps.save('2v_%sdz' % ('sideband_' if sideband else ''))

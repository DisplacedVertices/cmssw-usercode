#!/usr/bin/env python

'''
foreach ntk ( 5 6 7 8 )
  foreach sam (qcdht0500 qcdht1000 ttbarhadronic ttbarsemilep ttbardilep)
    py fcnfits.py $ntk $sam >&! out.fcnfits.ntk$ntk.$sam
  end
end
'''

from JMTucker.MFVNeutralino.MiniTreeBase import *

sample_name = None
samples = Samples.from_argv([Samples.qcdht1000])
#sample_name = 'qcdht1000andttbar'; samples = [Samples.qcdht1000] + Samples.ttbar_samples
#sample_name = 'qcdht5001000andttbar'; samples = [Samples.qcdht0500, Samples.qcdht1000] + Samples.ttbar_samples

use_weights = len(samples) > 1
for s in samples:
    s.weight = s.partial_weight * 20000 if use_weights else 1
if use_weights:
    ROOT.TH1.SetDefaultSumw2()
if sample_name is None:
    sample_name = 'toy' if len(samples) > 1 else samples[0].name

svdist_cut = 0.048
svdist_cut_name = ('%.3f'% svdist_cut).replace('.', 'p')
min_ntracks = typed_from_argv(int, 5)
plot_dir = 'plots/one2twoNew/fcnfit_ntracks%i_svdist%s_%s' % (min_ntracks, svdist_cut_name, sample_name)

################################################################################

ps = plot_saver(plot_dir, size=(600,600))

################################################################################

# Fit delta phi = "dphi" in the sideband, and compare result to fit
# for all 2v events. Do the same with delta z.

nbins = 8

h_2v_dphi             = ROOT.TH1F('h_2v_dphi'             , '', nbins, -pi, pi)
h_2v_absdphi          = ROOT.TH1F('h_2v_absdphi'          , '', nbins,   0, pi)
h_2v_sideband_dphi    = ROOT.TH1F('h_2v_sideband_dphi'    , '', nbins, -pi, pi)
h_2v_sideband_absdphi = ROOT.TH1F('h_2v_sideband_absdphi' , '', nbins,   0, pi)

h_2v_dz_all          = ROOT.TH1F('h_2v_dz_all',      '2v events;z0 - z1 (cm);events/1 mm',                 400, -20, 20)
h_2v_dz              = ROOT.TH1F('h_2v_dz',          '2v events;z0 - z1 (cm);events/100 #mum',              20, -0.1, 0.1)
h_2v_sideband_dz_all = ROOT.TH1F('h_2v_dz_all',      '2v events in sideband;z0 - z1 (cm);events/1 mm',     400, -20, 20)
h_2v_sideband_dz     = ROOT.TH1F('h_2v_sideband_dz', '2v events in sideband;z0 - z1 (cm);events/100 #mum',  20, -0.1, 0.1)

for sample in samples:
    f, t = get_f_t(sample, min_ntracks)
    weight_str = '%s' if sample.weight is None else '%f*(%%s)' % sample.weight
    n2v = t.Draw('svdphi', weight_str % ('nvtx == 2 && min_ntracks_ok'))
    print 'Sample: %s  n2v: %f' % (sample.name, n2v)

    v2v = detree(t,
                 'svdphi:svdz:svdist < %f' % svdist_cut,
                 'nvtx == 2 && min_ntracks_ok',
                 lambda x: (float(x[0]), float(x[1]), bool(int(x[2]))))

    for svdphi, svdz, is_sideband in v2v:
        h_2v_dphi.Fill(svdphi, sample.weight)
        h_2v_absdphi.Fill(abs(svdphi), sample.weight)
        h_2v_dz_all.Fill(svdz, sample.weight)
        h_2v_dz.Fill(svdz, sample.weight)
        if is_sideband:
            h_2v_sideband_dphi.Fill(svdphi, sample.weight)
            h_2v_sideband_absdphi.Fill(abs(svdphi), sample.weight)
            h_2v_sideband_dz.Fill(svdz, sample.weight)

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
        fit_options = 'ILRQS'
        if use_weights:
            fit_options = fit_options.replace('L', 'WL')
        fit = h.Fit(fcn, fit_options)
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
            if i < 0 or i >= len(results):
                break
            chi2 = results[i].fit.Chi2()
        if chi2 - min_chi2 < 1:
            print 'WARNING COULD NOT FIND INTERVAL'
        if delta < 0:
            best.exp_lo = results[i].exp
            best.chi2_lo = chi2
        else:
            best.exp_hi = results[i].exp
            best.chi2_hi = chi2
        
    if plot_name is not None:
        # Draw the chi2 well, and draw little lines indicating our
        # delta chi2 = 1 interval finding.
        exps = to_array(result.exp for result in results)
        chi2s = to_array(result.fit.Chi2() for result in results)
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

# Do the fits comparing dphi, |dphi| and sideband, all.
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

# Do the dz fits.
for sideband in (False, True):
    sideband_str = 'sideband_' if sideband else ''

    name = '2v_%sdz_all' % sideband_str
    h = eval('h_' + name)
    h.Draw()
    ps.update_canvas()
    s = move_stat_box(h, (0.673, 0.736, 0.980, 0.997))
    s.SetOptStat(2222220)
    ps.save(name)

    name = '2v_%sdz' % sideband_str
    h = eval('h_' + name)
    fcn_name = 'f_%sdz' % sideband_str
    fcn_dz = ROOT.TF1(fcn_name, 'gaus', -0.1, 0.1)
    exec '%s = fcn_dz' % fcn_name
    f_dz = FitResult(fcn_dz, h.Fit(fcn_dz, 'RLQS'))
    ps.update_canvas()
    s = move_stat_box(h, (0.673, 0.686, 0.980, 0.997))
    s.SetOptStat(2222220)
    ps.save(name)

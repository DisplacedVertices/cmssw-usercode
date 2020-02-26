from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
ROOT.TH1.AddDirectory(0)

do_bquark = False
is_mc = False
only_10pc = False
year = '2018'
version = 'V27m'
set_style()
ps = plot_saver(plot_dir('closure_%s%s%s_%s' % (version.capitalize(), '' if is_mc else '_data', '_10pc' if only_10pc else '', year)), size=(700,700), root=True, log=False)

fns = ['2v_from_jets%s_%s_3track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '2v_from_jets%s_%s_7track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '2v_from_jets%s_%s_4track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '2v_from_jets%s_%s_5track_default_%s.root' % ('' if is_mc else '_data', year, version)
       ]

# for overlaying the btag-based template
fns_btag = ['2v_from_jets%s_%s_3track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version), 
            '2v_from_jets%s_%s_7track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version), 
            '2v_from_jets%s_%s_4track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version), 
            '2v_from_jets%s_%s_5track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version)
            ]

ntk = []
for fn in fns:
    for x in fn.split('_'):
        if 'track' in x:
            ntk.append(int(x[:1]))

def errprop(val0, val1, err0, err1):
    if val0 == 0 and val1 == 0:
        return 0
    elif val1 == 0:
        return err0 / val0
    elif val0 == 0:
        return err1 / val1
    else:
        return ((err0 / val0)**2 + (err1 / val1)**2)**0.5

def scale_and_draw_template(template, twovtxhist, dvvc, color) :
    template.SetStats(0)
    template.SetLineColor(color)
    template.SetLineWidth(2)

    twovtxerr = ROOT.Double(0)
    twovtx = twovtxhist.IntegralAndError(0, twovtxhist.GetNbinsX(), twovtxerr)

    if twovtx > 0:
        template.Scale(twovtx/template.Integral())
    else:
        template.Scale(1./template.Integral())
        twovtxerr = 1.

    template_bins = get_bin_integral_and_stat_uncert(dvvc)

    if 'dphi' not in template.GetName():
        for bin in range(1, template.GetNbinsX() + 1):
            stat = 0.
            if bin <= 4:
                stat = template_bins[0][1] * (template.GetBinContent(bin) / template_bins[0][0])**0.5
            elif bin <= 7:
                stat = template_bins[1][1] * (template.GetBinContent(bin) / template_bins[1][0])**0.5
            else:
                stat = template_bins[2][1] * (template.GetBinContent(bin) / template_bins[2][0])**0.5

            newerr = (stat**2. + (twovtxerr * template.GetBinContent(bin) / template.Integral())**2.)**0.5
            template.SetBinError(bin, newerr)
    else:
        binerr_comb = ((template_bins[0][1])**2. + (template_bins[1][1])**2 + (template_bins[2][1])**2)**0.5
        for bin in range(template.GetNbinsX() + 1):
            newerr = (binerr_comb**2. / 5. + (twovtxerr * template.GetBinContent(bin) / template.Integral())**2)**0.5
            template.SetBinError(bin, newerr)
    template.Draw('hist sames')

def make_closure_plots(i):
    dvv_closure = ('h_2v_dvv', 'h_c1v_dvv')
    dphi_closure = ('h_2v_absdphivv', 'h_c1v_absdphivv')

    for closure in (dvv_closure, dphi_closure):
        twovtxhist = ROOT.TFile(fns[i]).Get(closure[0])
        twovtxhist.SetTitle(';|#Delta#phi_{VV}|;Events' if 'phi' in closure[0] else ';d_{VV} (cm);Events')
        twovtxhist.SetStats(0)
        twovtxhist.SetLineColor(ROOT.kBlue)
        twovtxhist.SetLineWidth(2)
        twovtxhist.SetMinimum(0)
        twovtxhist.Draw()

        template_btag = ROOT.TFile(fns_btag[i]).Get(closure[1])
        dvvc = ROOT.TFile(fns_btag[i]).Get('h_c1v_dvv')
        scale_and_draw_template(template_btag, twovtxhist, dvvc, ROOT.kRed)

        uncertband_btag = template_btag.Clone('uncertband_btag')
        uncertband_btag.SetFillColor(ROOT.kRed-3)
        uncertband_btag.SetFillStyle(3004)
        uncertband_btag.Draw('E2 sames')

        l1 = ROOT.TLegend(0.35, 0.75, 0.85, 0.85)
        l1.AddEntry(twovtxhist, 'Simulated events' if is_mc else 'Data')
        l1.AddEntry(template_btag, 'Background template' + (' (btag method)' if do_bquark else ''))

        if do_bquark:
            template = ROOT.TFile(fns[i]).Get(closure[1])
            scale_and_draw_template(template, twovtxhist, dvvc, ROOT.kGreen+2)

            uncertband = template.Clone('uncertband')
            uncertband.SetFillColor(ROOT.kGreen-3)
            uncertband.SetFillStyle(3005)
            uncertband.Draw('E2 sames')
            l1.AddEntry(template, 'Background template (bquark method)')


        l1.SetFillColor(0)
        l1.Draw()
        ps.save('%s-track' % ntk[i] if 'phi' not in closure[0] else '%s_dphi' % ntk[i])

def calculate_ratio(x, y, xerr, yerr):
    y_ = y
    yerr_ = yerr

    if y == 0: 
        y_ = 1.
        yerr_ = 1.

    r = x/y_
    e = r * errprop(x, y_, xerr, yerr_)
    return r, e

def get_bin_integral_and_stat_uncert(hist):
    sample = 'MCeffective' if is_mc else 'data100pc'
    if not is_mc and only_10pc:
        sample = 'data10pc'
    ebin = ebins['%s_%s_%dtrack' % (sample, year, 4 if ntracks==7 else ntracks)]

    bin1 = bin1_err = bin2 = bin2_err = bin3 = bin3_err = 0.

    if 'c1v' not in hist.GetName():
        bin1, bin1_err = get_integral(hist, xhi=0.04, include_last_bin=False)
        bin2, bin2_err = get_integral(hist, xlo=0.04, xhi=0.07, include_last_bin=False)
        bin3, bin3_err = get_integral(hist, xlo=0.07, xhi=0.4, include_last_bin=False)
    else:
        bin1 = get_integral(hist, 0., 0.04, integral_only=True, include_last_bin=False)
        bin1_err = bin1 * ebin[0]
        bin2 = get_integral(hist, 0.04, 0.07, integral_only=True, include_last_bin=False)
        bin2_err = bin2 * ebin[1]
        bin3 = get_integral(hist, 0.07, 0.4, integral_only=True, include_last_bin=False)
        bin3_err = bin3 * ebin[2]
    return [(bin1, bin1_err), (bin2, bin2_err), (bin3, bin3_err)]

def get_norm_frac_uncert(bins, total):
    allbins = []
    norm_sum = 0.

    if total == 0:
        allbins = bins
    else:
        for bin in bins:
            norm_sum += (bin[1] / total)**2

        for bin in bins:
            frac_uncert = ((1 - bin[0] / total) * (bin[1] / total)**2 + (bin[0] / total)**2 * norm_sum)**0.5
            allbins.append((bin[0] / total, frac_uncert))
    return allbins

def get_ratios(nums, dens):
    ratios = []
    for num, den in zip(nums, dens):
        r_bin, r_bin_err = calculate_ratio(num[0], den[0], num[1], den[1])
        ratios.append((r_bin, r_bin_err))
    return ratios

for i, ntracks in enumerate(ntk):
    make_closure_plots(i)

    twovtx = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    constructed = ROOT.TFile(fns_btag[i]).Get('h_c1v_dvv')

    if twovtx.Integral() > 0:
        constructed.Scale(twovtx.Integral()/constructed.Integral())
    else:
        constructed.Scale(1./constructed.Integral())

    twovtx_total, twovtx_total_err = get_integral(twovtx)
    twovtx_bins = get_bin_integral_and_stat_uncert(twovtx)

    con_total, con_total_err = get_integral(constructed)
    con_bins = get_bin_integral_and_stat_uncert(constructed)

    twovtx_bin_norm = get_norm_frac_uncert(twovtx_bins, twovtx_total)
    con_bin_norm = get_norm_frac_uncert(con_bins, con_total)
    ratios = get_ratios(twovtx_bin_norm, con_bin_norm)
    twovtx = (twovtx_total, twovtx_total_err) + tuple(x for bin in twovtx_bins for x in bin)
    con = (con_total, con_total_err) + tuple(x for bin in con_bins for x in bin)
    twovtx_norm = tuple(x for bin in twovtx_bin_norm for x in bin)
    con_norm = tuple(x for bin in con_bin_norm for x in bin)
    rat = tuple(x for bin in ratios for x in bin)
    try:
        pval = 1 - ROOT.Math.poisson_cdf(int(twovtx_bins[2][0]) - 1, con_bins[2][0])
    except:
        pval = 1
    

    print '%s-track' % ntk[i]
    print '  two-vertex events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % twovtx
    print ' constructed events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % con
    print '     dVV normalized:                    0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % twovtx_norm
    print '    dVVC normalized:                    0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % con_norm
    print '   ratio dVV / dVVC:                    0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % rat
    print '            p-value:                                                                               700-40000 um: %6.4f' % pval

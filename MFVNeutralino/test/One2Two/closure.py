from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
ROOT.TH1.AddDirectory(0)

do_btag = False
is_mc = True
only_10pc = False
year = '2017'
version = 'V25m'
set_style()
ps = plot_saver(plot_dir('closure_%s%s%s_%s' % (version.capitalize(), '' if is_mc else '_data', '_10pc' if only_10pc else '', year)), size=(700,700), root=False, log=False)

fns = ['2v_from_jets%s_%s_3track_default_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_7track_default_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_4track_default_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_5track_default_%s.root' % ('' if is_mc else '_data', year, version)]

# for overlaying the btag-based template
fns_btag = ['2v_from_jets%s_%s_3track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_7track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_4track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_5track_btag_corrected_%s.root' % ('' if is_mc else '_data', year, version)]

ntk = ['3-track', '4-track-3-track', '4-track', '5-track']
names = ['3-track x 3-track', '4-track x 3-track', '4-track x 4-track', '#geq 5-track x #geq 5-track']

n2v_year = {'2017': [651., 136., 2.22, 1.],
            '2018': [426., 79., 4.85, 1.],
            '2017p8': [1077., 215., 7.06, 1.]}
n2verr_year = {'2017': [53., 24., 1.14, 0.6],
               '2018': [50., 21., 2.35, 0.6],
               '2017p8': [72., 31., 2.61, 0.6]}

n2v = n2v_year[year]
n2verr = n2verr_year[year]

def errprop(val0, val1, err0, err1):
    if val0 == 0 and val1 == 0:
        return 0
    elif val1 == 0:
        return err0 / val0
    elif val0 == 0:
        return err1 / val1
    else:
        return ((err0 / val0)**2 + (err1 / val1)**2)**0.5

def scale_and_draw_template(template, n2v, i, simulated, color) :
    template.SetStats(0)
    template.SetLineColor(color)
    template.SetLineWidth(2)
    if is_mc:
        ratio = n2v[i] / template.Integral()

        newerrarray = []
        for bin in range(template.GetNbinsX() + 1):
            newerr = template.GetBinContent(bin) / template.Integral() * n2verr[i]
            newerrarray.append(newerr)
        template.Scale(ratio)
        for bin, err in enumerate(newerrarray):
            template.SetBinError(bin, err)
    else:
        if simulated.Integral() > 0:
            template.Scale(simulated.Integral()/template.Integral())
        else:
            template.Scale(1./template.Integral())
    template.Draw('hist sames')


def make_closure_plots(i):
    dvv_closure = ('h_2v_dvv', 'h_c1v_dvv')
    dphi_closure = ('h_2v_absdphivv', 'h_c1v_absdphivv')

    for closure in (dvv_closure, dphi_closure):
        simulated = ROOT.TFile(fns[i]).Get(closure[0])
        simulated.SetStats(0)
        simulated.SetLineColor(ROOT.kBlue)
        simulated.SetLineWidth(2)
        if is_mc:
            if simulated.Integral() > 0:
                simulated.Scale(n2v[i]/simulated.Integral())
        else:
            simulated.SetMaximum(0.4)
        simulated.SetMinimum(0)
        simulated.Draw()

        template = ROOT.TFile(fns[i]).Get(closure[1])
        scale_and_draw_template(template, n2v, i, simulated, ROOT.kRed)

        uncertband = template.Clone('uncertband')
        uncertband.SetFillColor(ROOT.kRed-3)
        uncertband.SetFillStyle(3004)
        uncertband.Draw('E2 sames')


        l1 = ROOT.TLegend(0.35, 0.75, 0.85, 0.85)
        l1.AddEntry(simulated, 'Simulated events' if is_mc else 'Data')
        l1.AddEntry(template, 'Background template' + (' (bquark method)' if do_btag else '') )

        if do_btag :
            template_btag = ROOT.TFile(fns_btag[i]).Get(closure[1])
            scale_and_draw_template(template_btag, n2v, i, simulated, ROOT.kGreen+2)

            uncertband_btag = template_btag.Clone('uncertband_btag')
            uncertband_btag.SetFillColor(ROOT.kGreen-3)
            uncertband_btag.SetFillStyle(3005)
            uncertband_btag.Draw('E2 sames')
            l1.AddEntry(template_btag, 'Background template (btag method)')

        l1.SetFillColor(0)
        l1.Draw()
        ps.save(ntk[i] if 'phi' not in closure[0] else '%s_dphi' % ntk[i])

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
    for bin in bins:
        norm_sum += (bin[1] / total)**2
    
    for bin in bins:
        frac_uncert = ((1 - 2 * bin[0] / total) * (bin[1] / total)**2 + (bin[0] / total)**2 * norm_sum)**0.5
        allbins.append((bin[0] / total, frac_uncert))
    return allbins

def get_ratios(nums, dens):
    ratios = []
    for num, den in zip(nums, dens):
        r_bin, r_bin_err = calculate_ratio(num[0], den[0], num[1], den[1])
        ratios.append((r_bin, r_bin_err))
    return ratios

for i, ntracks in enumerate([3,7,4,5]):
    make_closure_plots(i)

    simulated = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    constructed = ROOT.TFile(fns[i]).Get('h_c1v_dvv')

    if is_mc:
        if simulated.Integral() > 0:
            simulated.Scale(n2v[i] / simulated.Integral())
        constructed.Scale(n2v[i] / constructed.Integral())

    sim_total, sim_total_err = get_integral(simulated)
    sim_bins = get_bin_integral_and_stat_uncert(simulated)

    con_total, con_total_err = get_integral(constructed)
    con_bins = get_bin_integral_and_stat_uncert(constructed)

    sim_bin_norm = get_norm_frac_uncert(sim_bins, sim_total)
    con_bin_norm = get_norm_frac_uncert(con_bins, con_total)

    ratios = get_ratios(con_bin_norm, sim_bin_norm)

    sim = (sim_total, sim_total_err) + tuple(x for bin in sim_bins for x in bin)
    con = (con_total, con_total_err) + tuple(x for bin in con_bins for x in bin)
    sim_norm = tuple(x for bin in sim_bin_norm for x in bin)
    con_norm = tuple(x for bin in con_bin_norm for x in bin)
    rat = tuple(x for bin in ratios for x in bin)
    
    print ntk[i]
    print '   simulated events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % sim
    print ' constructed events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % con
    print '     dVV normalized:                    0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % sim_norm
    print '    dVVC normalized:                    0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % con_norm
    print '   ratio dVVC / dVV:                    0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % rat

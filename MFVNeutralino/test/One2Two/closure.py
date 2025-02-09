from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
ROOT.TH1.AddDirectory(0)

do_bquark = False
is_mc = True
only_10pc = False
year = '2017p8'
#version = 'ULV11'
version = 'ULV30Lepm'
set_style()
ps = plot_saver(plot_dir('closure_mc_%s%s%s_%s' % (version.capitalize(), '' if is_mc else '_data', '_10pc' if only_10pc else '', year)), size=(900,700), root=True, log=False)

#predictnorms = [1867.0+2451.0, 130.0+144.0, 9.0+1.5] #bjet
#predictnormerrs = [841.0, 55.0,2.9] #bjet


predictnorms = [726.9+251.1, 68.8+21.6, 1.6+0.5] #lepton
predictnormerrs = [603.9, 58.4,1.4] #lepton


fns = ['~/crabdirs/2v_from_jets_lep/2v_from_jets%s_%s_3track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '~/crabdirs/2v_from_jets_lep/2v_from_jets%s_%s_7track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       '~/crabdirs/2v_from_jets_lep/2v_from_jets%s_%s_4track_default_%s.root' % ('' if is_mc else '_data', year, version), 
       #'~/crabdirs/2v_from_jets_lep/2v_from_jets%s_%s_5track_default_%s.root' % ('' if is_mc else '_data', year, version)
       ]

# for overlaying the btag-based template
fns_btag = ['~/crabdirs/2v_from_jets/2v_from_jets%s_%s_3track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version), 
            '~/crabdirs/2v_from_jets/2v_from_jets%s_%s_7track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version), 
            '~/crabdirs/2v_from_jets/2v_from_jets%s_%s_4track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version), 
            #'~/crabdirs/2v_from_jets/2v_from_jets%s_%s_5track_btag_corrected_nom_%s.root' % ('' if is_mc else '_data', year, version)
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

def scale_and_draw_template(closure, template, twovtxhist, sumdbvc, color) :
    #######################
    # scale "template" bin by bin so that the total yield is the yield of "twovtxhist"
    # T[i] = C1V[i] * (I2V/I1V) where i is fine-binning
    # OBSOLETE stat. uncertainty of the template is corrected by get_bin_integral_and_stat_uncert() based on statmodel.py via ebins 
    # sts. uncertainty is derived directly from dC1V[i]
    # sys. uncertianty is asscoiated with the uncertainty of "twovtxhist" integral and of "sumdbv" integral  
    # dT[i]**2 = (T[i]**2) * ( (corrected_dC1V[i]/C1V[i])**2 + (dI2V/I2V)**2 + (dI1V/I1V)**2 ) where i is fine-binning though corrected_dC1V has coarse binning 
    #######################
    
    # Note that "template" and "sumdbvc" have the same input

    global predictnorm
    global predictnormerr 

    print(" predicted norm  ", predictnorm)
    print(" predicted norm err ", predictnormerr)
    
    template.SetStats(0)
    template.SetLineColor(color)
    template.SetLineWidth(2)

    twovtxerr = ROOT.Double(0.0) #dI2V
    twovtx = twovtxhist.IntegralAndError(0, twovtxhist.GetNbinsX(), twovtxerr) +1e-16#I2V
    rawtemperr = ROOT.Double( .0) #dI1V
    rawtemp = template.IntegralAndError(0, template.GetNbinsX(), rawtemperr) +1e-16#I1V
    if predictnorm > 0:
        twovtxhist.Scale(predictnorm/(twovtxhist.Integral()+1e-16))
        template.Scale(predictnorm/(template.Integral()+1e-16))
    else:
        twovtxhist.Scale(1./(twovtxhist.Integral()+1e-16))
        template.Scale(1./(template.Integral()+1e-16))
        predictnormerr = 1.
    #template_bins = get_bin_integral_and_stat_uncert(sumdbvc)
  
    twovtxhist.SetTitle(';|#Delta#phi_{VV}|;Events' if 'phi' in closure[0] else ';#Sigmad_{BV} (cm);Events')
    twovtxhist.SetStats(0)
    twovtxhist.SetLineColor(ROOT.kBlue)
    twovtxhist.SetLineWidth(2)
    twovtxhist.SetMinimum(0)
    twovtxhist.Draw()
 
    if 'dphi' not in template.GetName():
        for bin in range(1, template.GetNbinsX() + 1):
            stat = 0. # corrected_dC1V[i]
            
            """
            if template.FindBin(0.08):
                try:
                    stat = template_bins[0][1] * (template.GetBinContent(bin) / template_bins[0][0])**0.5
                except:
                    stat = 0.0
            elif template.FindBin(0.16):
                stat = template_bins[1][1] * (template.GetBinContent(bin) / template_bins[1][0])**0.5
            else:
                stat = template_bins[2][1] * (template.GetBinContent(bin) / template_bins[2][0])**0.5
            """
            #newerr = (stat**2. + (twovtxerr * template.GetBinContent(bin) / template.Integral())**2.)**0.5 #Old method
            newerr = template.GetBinContent(bin)*((( sumdbvc.GetBinError(bin)/ sumdbvc.GetBinContent(bin))**2 + (rawtemperr/rawtemp)**2 + (predictnormerr/predictnorm)**2)**0.5) # error propgation and corrected the first  
            template.SetBinError(bin, newerr)
    else:
        #binerr_comb = ((template_bins[0][1])**2. + (template_bins[1][1])**2 + (template_bins[2][1])**2)**0.5
        #bin_comb = ((template_bins[0][0]) + (template_bins[1][0]) + (template_bins[2][0])) 
        for bin in range(template.GetNbinsX() + 1):
            #newerr = (binerr_comb**2. / 5. + (twovtxerr * template.GetBinContent(bin) / template.Integral())**2)**0.5 #Old method
            #stat = binerr_comb * (template.GetBinContent(bin) / bin_comb)**0.5 # corrected_dC1V[i] 
            sumdbv_i = sumdbvc.GetBinContent(bin) 
            if (sumdbv_i == 0):
                sumdbv_i += 10**-16
                     
            newerr = template.GetBinContent(bin)*((( sumdbvc.GetBinError(bin)/sumdbv_i)**2 + (rawtemperr/rawtemp)**2 + (predictnormerr/predictnorm)**2)**0.5) 
            template.SetBinError(bin, newerr)
    template.GetYaxis().SetRangeUser(0.0, twovtxhist.GetMaximum()*1.05)
    template.Draw('hist sames')

def make_closure_plots(i):
    
    global predictnorm
    global predictnormerr 
    
    sumdbv_closure = ('h_2v_sumdbv', 'h_c1v_sumdbv')
    dphi_closure = ('h_2v_absdphivv', 'h_c1v_absdphivv')

    for closure in (sumdbv_closure, dphi_closure):
        twovtxhist = ROOT.TFile(fns[i]).Get(closure[0])
        template_btag = ROOT.TFile(fns[i]).Get(closure[1])
        sumdbvc = ROOT.TFile(fns[i]).Get('h_c1v_sumdbv')
        
        scale_and_draw_template(closure, template_btag, twovtxhist, sumdbvc, ROOT.kRed)

        uncertband_btag = template_btag.Clone('uncertband_btag')
        uncertband_btag.SetFillColor(ROOT.kRed-3)
        uncertband_btag.SetFillStyle(3004)
        uncertband_btag.Draw('E2 sames')

        l1 = ROOT.TLegend(0.35, 0.75, 0.85, 0.85)
        l1.AddEntry(twovtxhist, 'Simulated events' if is_mc else 'Data')
        l1.AddEntry(template_btag, 'Background template' + (' (btag method)' if do_bquark else ''))

        if do_bquark:
            template = ROOT.TFile(fns[i]).Get(closure[1])
            scale_and_draw_template(closure, template, twovtxhist, sumdbvc, ROOT.kGreen+2)

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


def get_bin_integral_and_stat_uncert(hist, rawhist):

    # input : normalized hist to predicted yield 
    bin1 = bin1_err = bin2 = bin2_err = bin3 = bin3_err = 0.

    intl_rawhist, intl_rawhisterr = get_integral(rawhist)

    intl_rawhist += 1e-16
    
    rawbin1, rawbin1_err = get_integral(rawhist, xhi=0.08, include_last_bin=False) 
    rawbin2, rawbin2_err = get_integral(rawhist, xlo=0.08, xhi=0.16, include_last_bin=False)  
    rawbin3, rawbin3_err = get_integral(rawhist, xlo=0.16, xhi=1.0, include_last_bin=False) 

    rawbin1 += 1e-16    
    rawbin2 += 1e-16    
    rawbin3 += 1e-16    

    bin1 = get_integral(hist, 0., 0.08, integral_only=True, include_last_bin=False) 
    bin1_err = bin1*((( rawbin1_err/rawbin1)**2 + (intl_rawhisterr/intl_rawhist)**2 + (predictnormerr/predictnorm)**2)**0.5)  
    bin2 = get_integral(hist, 0.08, 0.16, integral_only=True, include_last_bin=False) 
    bin2_err = bin2*((( rawbin2_err/rawbin2)**2 + (intl_rawhisterr/intl_rawhist)**2 + (predictnormerr/predictnorm)**2)**0.5)  
    bin3 = get_integral(hist, 0.16, 1.0, integral_only=True, include_last_bin=False)
    bin3_err = bin3*((( rawbin3_err/rawbin3)**2 + (intl_rawhisterr/intl_rawhist)**2 + (predictnormerr/predictnorm)**2)**0.5)  

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
   
    global predictnorm
    predictnorm = predictnorms[i]
    global predictnormerr 
    predictnormerr = predictnormerrs[i]

    make_closure_plots(i)
    
    twovtx = ROOT.TFile(fns[i]).Get('h_2v_sumdbv')
    constructed = ROOT.TFile(fns[i]).Get('h_c1v_sumdbv')

    if predictnorm > 0:
        twovtx.Scale(predictnorm/(twovtx.Integral()+1e-16))
        constructed.Scale(predictnorm/(constructed.Integral()+1e-16))
    else:
        twovtx.Scale(1./(twovtx.Integral()+1e-16))
        constructed.Scale(1./(constructed.Integral()+1e-16))

    twovtx_total, twovtx_total_err = get_integral(twovtx)
    twovtx_bins = get_bin_integral_and_stat_uncert(twovtx, ROOT.TFile(fns[i]).Get('h_2v_sumdbv')) #FIXME this function is obsolete
    con_total, con_total_err = get_integral(constructed)
    con_bins = get_bin_integral_and_stat_uncert(constructed, ROOT.TFile(fns[i]).Get('h_c1v_sumdbv')) #FIXME this function is obsolete

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
    print '  two-vertex events: %7.2f +/- %5.2f, 0-800 um: %7.2f +/- %5.2f, 800-1600 um: %6.2f +/- %5.2f, 1600-100000 um: %6.2f +/- %5.2f' % twovtx
    print ' constructed events: %7.2f +/- %5.2f, 0-800 um: %7.2f +/- %5.2f, 800-1600 um: %6.2f +/- %5.2f, 1600-100000 um: %6.2f +/- %5.2f' % con
    print '  sumdBV normalized:                    0-800 um: %7.3f +/- %5.3f, 800-1600 um: %6.3f +/- %5.3f, 1600-100000 um: %6.3f +/- %5.3f' % twovtx_norm
    print ' sumdBVC normalized:                    0-800 um: %7.3f +/- %5.3f, 800-1600 um: %6.3f +/- %5.3f, 1600-100000 um: %6.3f +/- %5.3f' % con_norm
    print ' . sumdBV / sumdBVC:                    0-800 um: %7.2f +/- %5.2f, 800-1600 um: %6.2f +/- %5.2f, 1600-100000 um: %6.2f +/- %5.2f' % rat
    print '            p-value:                                                                               1600-100000 um: %6.4f' % pval

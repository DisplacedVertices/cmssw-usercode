import os
from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
ROOT.TH1.AddDirectory(0)

set_style()
ps = plot_saver(plot_dir('pretty_closure_dphi_supplementary'), size=(700,700), log=False, pdf=True)

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)

# "default" is used to get the data observation, which doesn't care about template construction,
# while the "btag_corr" has our corrected template, and needs to be added properly
default_names_2017 = ['2v_from_jets_data_2017_3track_default_V27m.root', '2v_from_jets_data_2017_7track_default_V27m.root', '2v_from_jets_data_2017_4track_default_V27m.root', '2v_from_jets_data_2017_5track_default_V27m.root']
default_names_2018 = ['2v_from_jets_data_2018_3track_default_V27m.root', '2v_from_jets_data_2018_7track_default_V27m.root', '2v_from_jets_data_2018_4track_default_V27m.root', '2v_from_jets_data_2018_5track_default_V27m.root']
btag_corr_names_2017 = ['2v_from_jets_data_2017_3track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2017_7track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2017_4track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2017_5track_btag_corrected_nom_V27m.root']
btag_corr_names_2018 = ['2v_from_jets_data_2018_3track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2018_7track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2018_4track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2018_5track_btag_corrected_nom_V27m.root']

fns_2017 = [os.path.join('/uscms/home/dquach/public', fn) for fn in default_names_2017]
fns_2018 = [os.path.join('/uscms/home/dquach/public', fn) for fn in default_names_2018]
btag_fns_2017 = [os.path.join('/uscms/home/dquach/public', fn) for fn in btag_corr_names_2017]
btag_fns_2018 = [os.path.join('/uscms/home/dquach/public', fn) for fn in btag_corr_names_2018]
ntk = ['3track3track', '4track3track', '4track4track', '5track5track']
names = ['3-track + 3-track', '4-track + 3-track', '4-track + 4-track', '#geq5-track + #geq5-track']
#ymax = [75, 45, 10, 0.4]

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

def get_bin_integral_and_stat_uncert(hist, i, year):
    sample = 'data100pc'
    if "5" in ntk[i] :
        ntracks = 5
    elif "4" in ntk[i] :
        ntracks = 4 # including for 4x3
    elif "3" in ntk[i] :
        ntracks = 3
    ebin = ebins['%s_%s_%dtrack' % (sample, year, ntracks)]

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

def set_bin_errors(template, twovtxerr, i, year) :
    template_bins = get_bin_integral_and_stat_uncert(template, i, year)
    binerr_comb = ((template_bins[0][1])**2. + (template_bins[1][1])**2 + (template_bins[2][1])**2)**0.5
    for bin in range(template.GetNbinsX() + 1):
        newerr = (binerr_comb**2. / 5. + (twovtxerr * template.GetBinContent(bin) / template.Integral())**2)**0.5
        template.SetBinError(bin, newerr)
    return template

for i in range(4):
    hh_2017 = ROOT.TFile(fns_2017[i]).Get('h_2v_absdphivv')
    hh_2018 = ROOT.TFile(fns_2018[i]).Get('h_2v_absdphivv')
    h_2017 = ROOT.TFile(btag_fns_2017[i]).Get('h_c1v_absdphivv')
    h_2018 = ROOT.TFile(btag_fns_2018[i]).Get('h_c1v_absdphivv')

    if hh_2017.Integral() > 0:
        h_2017.Scale(hh_2017.Integral()/h_2017.Integral())
    else:
        h_2017.Scale(0.241/h_2017.Integral()) # predicted 5x5 value for 2017

    if hh_2018.Integral() > 0:
        h_2018.Scale(hh_2018.Integral()/h_2018.Integral())
    else:
        h_2018.Scale(0.111/h_2018.Integral()) # predicted 5x5 value for 2018

    # now add the 2017 and 2018 components together
    h = h_2017
    h.Add(h_2018)
    hh = hh_2017
    hh.Add(hh_2018)

    # note that all of the twovtxerr and set_bin_errors are strictly for HEPData!
    twovtxerr = ROOT.Double(0)
    twovtx = hh.IntegralAndError(0, hh.GetNbinsX(), twovtxerr)

    if hh.Integral() == 0 :
        twovtxerr = 0.352

    h = set_bin_errors(h, twovtxerr, i, "2017p8")

    h.SetTitle(';|#Delta#phi_{VV}|;Events/0.63 radians')
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetXaxis().SetLabelOffset(0.008)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetLabelOffset(0.008)
    h.GetYaxis().SetTitleOffset(1.38)
    h.GetYaxis().SetRangeUser(0, h.GetBinContent(h.GetNbinsX())*2.6)
    h.SetStats(0)
    h.SetLineColor(ROOT.kBlue)
    h.SetLineWidth(3)
    h.Draw('hist')

    hh = poisson_intervalize(hh, zero_x=True, include_zero_bins='surrounded')
    hh.SetLineWidth(3)
    hh.SetMarkerStyle(20)
    hh.SetMarkerSize(1.3)
    hh.Draw('PE')

    write(42, 0.040, 0.16, 0.750, names[i])

    xoffset = -0.06
    l1 = ROOT.TLegend(0.60+xoffset, 0.725, 1.04+xoffset, 0.865)
    l1.AddEntry(hh, 'Data', 'PE')
    l1.AddEntry(h, 'Background')
    l1.SetTextSize(0.040)
    l1.SetBorderSize(0)
    l1.SetFillStyle(0)
    l1.Draw()

    l2 = ROOT.TLegend(0.60+xoffset, 0.695, 1.04+xoffset, 0.725)
    l2.AddEntry(0,'template','')
    l2.SetTextSize(0.040)
    l2.SetBorderSize(0)
    l2.SetFillStyle(0)
    l2.Draw()

    write(61, 0.050, 0.16, 0.81, 'CMS')
    write(52, 0.047, 0.27, 0.81, 'Supplementary')
    write(42, 0.050, 0.595, 0.913, '101 fb^{-1} (13 TeV)')

    outfn = 'closure_dphi_%s' % ntk[i]
    ps.save(outfn)

    write(52, 0.047, 0.32, 0.81, 'Preliminary')
    ps.save(outfn + '_prelim')

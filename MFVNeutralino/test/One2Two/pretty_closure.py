import os
from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

set_style()
ps = plot_saver(plot_dir('pretty_closure_fixed'), size=(700,700), log=False, pdf=True)

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
names = ['3-track x 3-track', '4-track x 3-track', '4-track x 4-track', '#geq5-track x #geq5-track']
ymax = [70, 35, 9, 0.3]

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

for i in range(4):
    hh_2017 = ROOT.TFile(fns_2017[i]).Get('h_2v_dvv')
    hh_2018 = ROOT.TFile(fns_2018[i]).Get('h_2v_dvv')
    h_2017 = ROOT.TFile(btag_fns_2017[i]).Get('h_c1v_dvv')
    h_2018 = ROOT.TFile(btag_fns_2018[i]).Get('h_c1v_dvv')

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

    hh = cm2mm(hh)
    h = cm2mm(h)

    h.SetTitle(';d_{VV} (mm);Events/0.1 mm')
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.2)
    h.GetYaxis().SetRangeUser(0,ymax[i])
    h.SetStats(0)
    h.SetLineColor(ROOT.kBlue)
    h.SetLineWidth(3)
    h.Draw('hist')
    print h.Integral()
    print h.Integral(0,h.FindBin(0.4)-1)
    print h.Integral(h.FindBin(0.4),h.FindBin(0.7)-1)
    print h.Integral(h.FindBin(0.7),99999999)

    hh = poisson_intervalize(hh, zero_x=True, include_zero_bins='surrounded')
    hh.SetLineWidth(3)
    hh.SetMarkerStyle(20)
    hh.SetMarkerSize(1.3)
    hh.Draw('PE')

    write(42, 0.040, 0.370, 0.750, names[i])

    l1 = ROOT.TLegend(0.35, 0.60, 0.85, 0.73)
    l1.AddEntry(hh, 'Data', 'PE')
    l1.AddEntry(h, 'Background template')
    l1.SetBorderSize(0)
    l1.Draw()

    write(61, 0.050, 0.37, 0.81, 'CMS')
    write(42, 0.050, 0.595, 0.913, '101 fb^{-1} (13 TeV)')


    lines = [
        ROOT.TLine(0.4, 0, 0.4, ymax[i]),
        ROOT.TLine(0.7, 0, 0.7, ymax[i]),
        ]

    for ll in lines:
        ll.SetLineColor(ROOT.kRed)
        ll.SetLineWidth(2)
        ll.SetLineStyle(2)
        ll.Draw()

    outfn = 'closure_%s' % ntk[i]
    ps.save(outfn)

    write(52, 0.047, 0.48, 0.81, 'Preliminary')
    ps.save(outfn + '_prelim')

import os
from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

set_style()
ps = plot_saver(plot_dir('pretty_closure'), size=(700,700), log=False, pdf=True)

ps.c.SetBottomMargin(0.11)
ps.c.SetLeftMargin(0.13)
ps.c.SetRightMargin(0.06)

default_names = ['2v_from_jets_data_2017p8_3track_default_V27m.root', '2v_from_jets_data_2017p8_7track_default_V27m.root', '2v_from_jets_data_2017p8_4track_default_V27m.root', '2v_from_jets_data_2017p8_5track_default_V27m.root']
btag_corr_names = ['2v_from_jets_data_2017p8_3track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2017p8_7track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2017p8_4track_btag_corrected_nom_V27m.root', '2v_from_jets_data_2017p8_5track_btag_corrected_nom_V27m.root']
fns = [os.path.join('/uscms/home/dquach/public', fn) for fn in default_names]
btag_fns = [os.path.join('/uscms/home/dquach/public', fn) for fn in btag_corr_names]
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
    hh = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    h = ROOT.TFile(btag_fns[i]).Get('h_c1v_dvv')
    if hh.Integral() > 0:
        h.Scale(hh.Integral()/h.Integral())
    else:
        h.Scale(0.34/h.Integral())

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

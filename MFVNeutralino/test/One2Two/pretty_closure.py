import os
from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

set_style()
ps = plot_saver(plot_dir('pretty_closure'), size=(700,700), log=False, pdf=True)

fns = [os.path.join('/uscms/home/jchu/public/EXO-17-018', fn) for fn in ['2v_from_jets_data_2015p6_3track_default_v15_v5.root', '2v_from_jets_data_2015p6_7track_default_v15_v5.root', '2v_from_jets_data_2015p6_4track_default_v15_v5.root', '2v_from_jets_data_2015p6_5track_default_v15_v5.root']]
ntk = ['3track3track', '4track3track', '4track4track', '5track5track']
names = ['3-track x 3-track', '4-track x 3-track', '4-track x 4-track', '#geq5-track x #geq5-track']
ymax = [140, 40, 5, 4]

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

for i in range(4):
    hh = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    h = ROOT.TFile(fns[i]).Get('h_c1v_dvv')
    h.Scale(hh.Integral()/h.Integral())

    hh = cm2mm(hh)
    h = cm2mm(h)

    h.SetTitle(';d_{VV} (mm);Events/0.1 mm')
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetLabelSize(0.045)
    h.GetYaxis().SetTitleOffset(1.15)
    h.GetYaxis().SetRangeUser(0,ymax[i])
    h.SetStats(0)
    h.SetLineColor(ROOT.kBlue)
    h.SetLineWidth(3)
    h.Draw('hist')

    hh = poisson_intervalize(hh, zero_x=True)
    hh.SetLineWidth(3)
    hh.SetMarkerStyle(20)
    hh.SetMarkerSize(1.3)
    hh.Draw('PE')

    l1 = ROOT.TLegend(0.35, 0.65, 0.85, 0.78)
    l1.AddEntry(hh, 'Data', 'LPE')
    l1.AddEntry(h, 'Background template')
    l1.SetBorderSize(0)
    l1.Draw()

    write(42, 0.040, 0.370 , 0.80, names[i])
    write(61, 0.050, 0.109, 0.913, 'CMS')
    write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')

    ps.c.SetBottomMargin(0.11)
    ps.c.SetLeftMargin(0.11)

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

    write(52, 0.047, 0.219, 0.913, 'Preliminary')
    ps.save(outfn + '_prelim')

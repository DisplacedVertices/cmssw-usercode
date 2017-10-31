from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

set_style()
ps = plot_saver('../plots/EXO-17-018/closure', size=(700,700), log=False, pdf=True)

fns = ['2v_from_jets_data_2015p6_3track_default_v15_v5.root', '2v_from_jets_data_2015p6_7track_default_v15_v5.root', '2v_from_jets_data_2015p6_4track_default_v15_v5.root', '2v_from_jets_data_2015p6_5track_default_v15_v5.root']
ntk = ['3track3track', '4track3track', '4track4track', '5track5track']
names = ['3-track x 3-track', '4-track x 3-track', '4-track x 4-track', '#geq 5-track x #geq 5-track']
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

    h.SetTitle(';d_{VV} (cm);Events/100 #mum')
    h.GetXaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleSize(0.04)
    h.GetYaxis().SetTitleOffset(1.3)
    h.GetYaxis().SetRangeUser(0,ymax[i])
    h.SetStats(0)
    h.SetLineColor(ROOT.kBlue)
    h.SetLineWidth(3)
    h.Draw('hist')

    hh = poisson_intervalize(hh)
    hh.SetLineWidth(3)
    hh.SetMarkerStyle(20)
    hh.SetMarkerSize(1.3)
    hh.Draw('PE')

    l1 = ROOT.TLegend(0.50, 0.65, 0.85, 0.78)
    l1.AddEntry(hh, 'Data', 'LPE')
    l1.AddEntry(h, 'Construction')
    l1.SetBorderSize(0)
    l1.Draw()

    write(42, 0.040, 0.500, 0.80, names[i])
    write(61, 0.040, 0.098, 0.91, 'CMS')
    write(52, 0.035, 0.185, 0.91, 'Preliminary')
    write(42, 0.040, 0.625, 0.91, '38.5 fb^{-1} (13 TeV)')

    lines = [
        ROOT.TLine(0.04, 0, 0.04, ymax[i]),
        ROOT.TLine(0.07, 0, 0.07, ymax[i]),
        ]

    for ll in lines:
        ll.SetLineColor(ROOT.kRed)
        ll.SetLineWidth(2)
        ll.SetLineStyle(2)
        ll.Draw()

    ps.save('closure_%s' % ntk[i])

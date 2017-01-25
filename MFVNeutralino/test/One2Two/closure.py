from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

set_style()
ps = plot_saver('../plots/bkgest/closure', size=(700,700), root=False, log=False)

fns = ['2v_from_jets_3track_average3_c1p35_e2_a3p66.root', '2v_from_jets_4track3track_average3_c1p35_e2_a3p66.root', '2v_from_jets_4track_average4_c1p35_e2_a3p66.root', '2v_from_jets_5track_average5_c1p35_e2_a3p66.root']
ntk = ['3-track', '4-track-3-track', '4-track', '5-track']
n2v = [1323., 335., 22., 1.]

for i in range(4):
    hh = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    hh.SetTitle(';d_{VV} (cm);Events')
    hh.SetStats(0)
    hh.SetLineColor(ROOT.kBlue)
    hh.SetLineWidth(2)
    if hh.Integral() > 0:
        hh.Scale(n2v[i]/hh.Integral())
    else:
        hh.SetMaximum(0.4)
    hh.SetMinimum(0)
    hh.Draw()

    h = ROOT.TFile(fns[i]).Get('h_c1v_dvv')
    h.SetStats(0)
    h.SetLineColor(ROOT.kRed)
    h.SetLineWidth(2)
    h.Scale(n2v[i]/h.Integral())
    h.Draw('hist e sames')

    l1 = ROOT.TLegend(0.35, 0.75, 0.85, 0.85)
    l1.AddEntry(hh, 'Simulated events')
    l1.AddEntry(h, 'd_{VV}^{C}')
    l1.SetFillColor(0)
    l1.Draw()
    ps.save(ntk[i])

    err = ROOT.Double(0)
    sim = hh.IntegralAndError(5,40,err)
    if sim == 0:
        sim = 1
    print '%s: simulated events = %4.2f +/- %4.2f' % (ntk[i], sim, err)

    e = ROOT.Double(0)
    c = h.IntegralAndError(5,40,e)
    r = c/sim
    er = (c/sim) * ((e/c)**2 + (err/sim)**2)**0.5
    print '%s: dVVC1 events = %4.2f +/- %4.2f (%4.2f +/- %4.2f x)' % (ntk[i], c, e, r, er)

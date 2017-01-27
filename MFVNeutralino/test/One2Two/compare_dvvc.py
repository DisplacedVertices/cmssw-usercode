from JMTucker.Tools.ROOTTools import *
from array import array
ROOT.TH1.AddDirectory(0)

mode = 'vary_eff'
#mode = 'vary_dphi'
#mode = 'vary_dbv'

set_style()
ps = plot_saver('../plots/bkgest/compare_dvvc_%s' % mode, size=(700,700), root=False, log=False)

if mode == 'vary_eff':
    fn1 = '''2v_from_jets_3track_average3_c1p35_e2_a3p66.root
2v_from_jets_3track_maxtk3_c1p35_e2_a3p66.root
2v_from_jets_3track_ntk3_deltasvgaus_wevent_c1p35_e2_a3p66.root'''.split('\n')

    fn2 = '''2v_from_jets_4track_average4_c1p35_e2_a3p66.root
2v_from_jets_4track_maxtk4_c1p35_e2_a3p66.root
2v_from_jets_4track_ntk4_deltasvgaus_wevent_c1p35_e2_a3p66.root'''.split('\n')

    fn3 = '''2v_from_jets_5track_average5_c1p35_e2_a3p66.root
2v_from_jets_5track_maxtk5_c1p35_e2_a3p66.root
2v_from_jets_5track_ntk5_deltasvgaus_wevent_c1p35_e2_a3p66.root'''.split('\n')

    ls = '''average efficiency
maxtk efficiency
ntk_deltasvgaus_wevent efficiency'''.split('\n')

if mode == 'vary_dphi':
    fn1 = '''2v_from_jets_3track_average3_c1p35_e2_a3p66.root
2v_from_jets_3track_average3_c0p00_e0_a0p00.root'''.split('\n')

    fn2 = '''2v_from_jets_4track_average4_c1p35_e2_a3p66.root
2v_from_jets_4track_average4_c0p00_e0_a0p00.root'''.split('\n')

    fn3 = '''2v_from_jets_5track_average5_c1p35_e2_a3p66.root
2v_from_jets_5track_average5_c0p00_e0_a0p00.root'''.split('\n')

    ls = '''|#Delta#phi| from jets
|#Delta#phi| flat'''.split('\n')

if mode == 'vary_dbv':
    fn1 = '''2v_from_jets_3track_average3_c1p35_e2_a3p66.root
2v_from_jets_3track_average3_c1p35_e2_a3p66_sum.root'''.split('\n')

    fn2 = '''2v_from_jets_4track_average4_c1p35_e2_a3p66.root
2v_from_jets_4track_average4_c1p35_e2_a3p66_sum.root'''.split('\n')

    fn3 = '''2v_from_jets_5track_average5_c1p35_e2_a3p66.root
2v_from_jets_5track_average5_c1p35_e2_a3p66_sum.root'''.split('\n')

    ls = '''default
sort by b quarks'''.split('\n')

fns = [fn1, fn2, fn3]
ntk = ['3-track', '4-track', '5-track']
n2v = [1323., 22., 1.]

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet, ROOT.kPink+1]

g2s = []
for i in range(3):
    l1 = ROOT.TLegend(0.50,0.70,0.85,0.85)
    hh = ROOT.TFile(fns[i][0]).Get('h_2v_dvv')
    hh.SetTitle('%s;d_{VV} (cm);events' % ntk[i])
    hh.SetStats(0)
    hh.SetLineColor(ROOT.kBlack)
    hh.SetLineWidth(5)
    if hh.Integral() > 0:
        hh.Scale(n2v[i]/hh.Integral())
    hh.Draw()
    l1.AddEntry(hh, 'simulated events')

    hs = []
    for j in range(len(ls)):
        h = ROOT.TFile(fns[i][j]).Get('h_c1v_dvv')
        h.SetStats(0)
        h.SetLineColor(colors[j])
        h.SetLineWidth(2)
        h.Scale(n2v[i]/h.Integral())
        h.Draw('hist e sames')
        hs.append(h)
        l1.AddEntry(h, ls[j])

    l1.SetFillColor(0)
    l1.Draw()
    ps.save(ntk[i])

    if i == 2:
        hs = []
        l1 = ROOT.TLegend(0.50,0.75,0.85,0.85)
        for j in range(len(ls)):
            h = ROOT.TFile(fns[i][j]).Get('h_c1v_dvv')
            h.SetStats(0)
            h.SetLineColor(colors[j])
            h.SetLineWidth(2)
            h.Scale(n2v[i]/h.Integral())
            if j == 0:
                h.SetTitle(';d_{VV}^{C} (cm);Events')
                h.GetYaxis().SetRangeUser(0,0.4)
                h.Draw('hist e')
            elif j == 1:
                h.Draw('hist e sames')
            hs.append(h)
            if j > 1:
                continue
            l1.AddEntry(h, ls[j])
        l1.SetFillColor(0)
        l1.Draw()
        ps.save('compare_dvvc_%s' % mode)

    l2 = ROOT.TLegend(0.15,0.70,0.50,0.85)
    h2 = ROOT.TFile(fns[i][0]).Get('h_2v_absdphivv')
    h2.SetTitle('%s;|#Delta#phi_{VV}|;events' % ntk[i])
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kBlack)
    h2.SetLineWidth(5)
    if h2.Integral() > 0:
        h2.Scale(n2v[i]/h2.Integral())
    h2.SetMinimum(0)
    h2.Draw()
    l2.AddEntry(hh, 'simulated events')

    h2s = []
    for j in range(len(ls)):
        h = ROOT.TFile(fns[i][j]).Get('h_c1v_absdphivv')
        h.SetStats(0)
        h.SetLineColor(colors[j])
        h.SetLineWidth(2)
        h.Scale(n2v[i]/h.Integral())
        h.Draw('hist e sames')
        h2s.append(h)
        l2.AddEntry(h, ls[j])

    l2.SetFillColor(0)
    l2.Draw()
    ps.save('%s_dphi'%ntk[i])

    err = ROOT.Double(0)
    sim = hh.IntegralAndError(5,40,err)
    if sim == 0:
        sim = 1

    err_tot = ROOT.Double(0)
    sim_tot = hh.IntegralAndError(1,40,err_tot)
    if sim_tot == 0:
        sim_tot = 1
    r_tot = sim/sim_tot
    er_tot = sim/sim_tot * ((err/sim)**2 + (err_tot/sim_tot)**2)**0.5
    print '%s: simulated events = %4.2f +/- %4.2f (%4.2f +/- %4.2f x dVV)' % (ntk[i], sim, err, r_tot, er_tot)

    e1 = ROOT.Double(0)
    c1 = hs[0].IntegralAndError(5,40,e1)
    print '%s: dVVC1 events = %4.2f +/- %4.2f' % (ntk[i], c1, e1)

    x2 = []
    y2 = []
    ex2 = []
    ey2 = []
    for j,h in enumerate(hs):
        e = ROOT.Double(0)
        c = h.IntegralAndError(5,40,e)
        r = c/sim
        er = (c/sim) * ((e/c)**2 + (err/sim)**2)**0.5
        r1 = c/c1
        er1 = (c/c1) * ((e/c)**2 + (e1/c1)**2)**0.5

        e2 = ROOT.Double(0)
        c2 = h.IntegralAndError(1,40,e2)
        r2 = c/c2
        er2 = (c/c2) * ((e/c)**2 + (e2/c2)**2)**0.5

        print '%33s = %6.2f +/- %4.2f (%4.2f +/- %4.2f x simulated) (%4.2f +/- %4.2f x dVVC1) (%4.2f +/- %4.2f x dVVC)' % (ls[j], c, e, r, er, r1, er1, r2, er2)
        if j == 0:
            continue
        if j > 1:
            continue
        x2.append(i+1)
        ex2.append(0)
        y2.append(r1)
        ey2.append(er1)
    g2 = ROOT.TGraphErrors(len(x2), array('d',x2), array('d',y2), array('d',ex2), array('d',ey2))
    g2s.append(g2)

for i,g in enumerate(g2s):
    g.SetMarkerStyle(21)
    if i == 0:
        g.SetTitle('variation / default (d_{VV}^{C} > 400 #mum);3-track%12s4-track%12s5-or-more-track%2s' % ('','',''))
        g.GetXaxis().SetLimits(0,4)
        g.GetXaxis().SetLabelSize(0)
        g.GetXaxis().SetTitleOffset(0.5)
        g.GetYaxis().SetRangeUser(0.6,1.4)
        g.Draw('AP')
    else:
        g.Draw('P')
line = ROOT.TLine(0,1,4,1)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw()
ps.save('ratio_%s' % mode)

from JMTucker.Tools.ROOTTools import *
from array import array
ROOT.TH1.AddDirectory(0)

mode = 'vary_eff'
#mode = 'vary_dphi'
#mode = 'vary_dbv'

set_style()
ps = plot_saver('../plots/bkgest/compare_dvvc_%s' % mode, size=(600,600), root=False, log=False)

if mode == 'vary_eff':
    fn1 = '''2v_from_jets_3track_average3_c0p0_e0p0_a0p0.root
2v_from_jets_3track_maxtk3_c0p0_e0p0_a0p0.root
2v_from_jets_3track_maxtk3_merge_c0p0_e0p0_a0p0.root
2v_from_jets_3track_ntk3_c0p0_e0p0_a0p0.root
2v_from_jets_3track_ntk3_wevent_c0p0_e0p0_a0p0.root
2v_from_jets_3track_ntk3_deltasvgaus_c0p0_e0p0_a0p0.root
2v_from_jets_3track_ntk3_deltasvgaus_wevent_c0p0_e0p0_a0p0.root'''.split('\n')

    fn2 = '''2v_from_jets_4track_average4_c0p0_e0p0_a0p0.root
2v_from_jets_4track_maxtk4_c0p0_e0p0_a0p0.root
2v_from_jets_4track_maxtk4_merge_c0p0_e0p0_a0p0.root
2v_from_jets_4track_ntk4_c0p0_e0p0_a0p0.root
2v_from_jets_4track_ntk4_wevent_c0p0_e0p0_a0p0.root
2v_from_jets_4track_ntk4_deltasvgaus_c0p0_e0p0_a0p0.root
2v_from_jets_4track_ntk4_deltasvgaus_wevent_c0p0_e0p0_a0p0.root'''.split('\n')

    fn3 = '''2v_from_jets_5track_average5_c0p0_e0p0_a0p0.root
2v_from_jets_5track_maxtk5_c0p0_e0p0_a0p0.root
2v_from_jets_5track_maxtk5_merge_c0p0_e0p0_a0p0.root
2v_from_jets_5track_ntk5_c0p0_e0p0_a0p0.root
2v_from_jets_5track_ntk5_wevent_c0p0_e0p0_a0p0.root
2v_from_jets_5track_ntk5_deltasvgaus_c0p0_e0p0_a0p0.root
2v_from_jets_5track_ntk5_deltasvgaus_wevent_c0p0_e0p0_a0p0.root'''.split('\n')

    ls = '''average efficiency
maxtk efficiency
maxtk_merge efficiency
ntk efficiency
ntk_wevent efficiency
ntk_deltasvgaus efficiency
ntk_deltasvgaus_wevent efficiency'''.split('\n')

    lsh = 'avg    maxtk    merge    ntk    wevent    dzgaus    both  '

if mode == 'vary_dphi':
    fn1 = '''2v_from_jets_3track_average3_c0p0_e0p0_a0p0.root
2v_from_jets_3track_average3_c1p3_e2p0_a2p6.root
2v_from_jets_3track_average3_c1p1_e2p0_a2p6.root
2v_from_jets_3track_average3_c1p5_e2p0_a2p6.root
2v_from_jets_3track_average3_c1p3_e2p0_a1p2.root
2v_from_jets_3track_average3_c1p3_e2p0_a4p0.root'''.split('\n')

    fn2 = '''2v_from_jets_4track_average4_c0p0_e0p0_a0p0.root
2v_from_jets_4track_average4_c1p3_e2p0_a2p6.root
2v_from_jets_4track_average4_c1p1_e2p0_a2p6.root
2v_from_jets_4track_average4_c1p5_e2p0_a2p6.root
2v_from_jets_4track_average4_c1p3_e2p0_a1p2.root
2v_from_jets_4track_average4_c1p3_e2p0_a4p0.root'''.split('\n')

    fn3 = '''2v_from_jets_5track_average5_c0p0_e0p0_a0p0.root
2v_from_jets_5track_average5_c1p3_e2p0_a2p6.root
2v_from_jets_5track_average5_c1p1_e2p0_a2p6.root
2v_from_jets_5track_average5_c1p5_e2p0_a2p6.root
2v_from_jets_5track_average5_c1p3_e2p0_a1p2.root
2v_from_jets_5track_average5_c1p3_e2p0_a4p0.root'''.split('\n')

    ls = '''|#Delta#phi| flat
|#Delta#phi - 1.3|^{2} + 2.6
|#Delta#phi - 1.1|^{2} + 2.6
|#Delta#phi - 1.5|^{2} + 2.6
|#Delta#phi - 1.3|^{2} + 1.2
|#Delta#phi - 1.3|^{2} + 4.0'''.split('\n')

    lsh = 'flat       |#Delta#phi-c|^{2}+a       c-1#sigma       c+1#sigma       a-1#sigma       a+1#sigma     '

if mode == 'vary_dbv':
    fn1 = '''2v_from_jets_3track_average3_c0p0_e0p0_a0p0_noqcdht1000.root
2v_from_jets_3track_average3_c0p0_e0p0_a0p0_noqcdht1000_b.root
2v_from_jets_3track_average3_c0p0_e0p0_a0p0_noqcdht1000_nob.root
2v_from_jets_3track_average3_c0p0_e0p0_a0p0_noqcdht1000_sum.root'''.split('\n')

    fn2 = '''2v_from_jets_4track_average4_c0p0_e0p0_a0p0_noqcdht1000.root
2v_from_jets_4track_average4_c0p0_e0p0_a0p0_noqcdht1000_b.root
2v_from_jets_4track_average4_c0p0_e0p0_a0p0_noqcdht1000_nob.root
2v_from_jets_4track_average4_c0p0_e0p0_a0p0_noqcdht1000_sum.root'''.split('\n')

    fn3 = '''2v_from_jets_5track_average5_c0p0_e0p0_a0p0_noqcdht1000.root
2v_from_jets_5track_average5_c0p0_e0p0_a0p0_noqcdht1000_b.root
2v_from_jets_5track_average5_c0p0_e0p0_a0p0_noqcdht1000_nob.root
2v_from_jets_5track_average5_c0p0_e0p0_a0p0_noqcdht1000_sum.root'''.split('\n')

    ls = '''default
b quarks
no b quarks
sum'''.split('\n')

    lsh = 'default            b quarks            no b quarks            sum  '

fns = [fn1, fn2, fn3]
ntk = ['3-track', '4-track', '5-track']
n2v = [832., 17., 1.]

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet, ROOT.kPink+1]

gs = []
g1s = []
for i in range(3):
    l1 = ROOT.TLegend(0.35,0.60,0.85,0.85)
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

    l2 = ROOT.TLegend(0.15,0.60,0.65,0.85)
    h2 = ROOT.TFile(fns[i][0]).Get('h_2v_absdphivv')
    h2.SetTitle('%s;|#Delta#phi_{VV}|;events' % ntk[i])
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kBlack)
    h2.SetLineWidth(5)
    if h2.Integral() > 0:
        h2.Scale(n2v[i]/h2.Integral())
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
    print '%s: simulated events = %4.2f +/- %4.2f' % (ntk[i], sim, err)

    e1 = ROOT.Double(0)
    c1 = hs[0].IntegralAndError(5,40,e1)
    print '%s: dVVC1 events = %4.2f +/- %4.2f' % (ntk[i], c1, e1)

    x = []
    y = []
    y1 = []
    ex = []
    ey = []
    ey1 = []
    for j,h in enumerate(hs):
        e = ROOT.Double(0)
        c = h.IntegralAndError(5,40,e)
        r = c/sim
        er = (c/sim) * ((e/c)**2 + (err/sim)**2)**0.5
        r1 = c/c1
        er1 = (c/c1) * ((e/c)**2 + (e1/c1)**2)**0.5
        print '%33s = %4.2f +/- %4.2f (%4.2f +/- %4.2f x)' % (ls[j], c, e, r, er)
        x.append(j+1+0.1*i)
        y.append(r)
        y1.append(r1)
        ex.append(0)
        ey.append(er)
        ey1.append(er1)
    g = ROOT.TGraphErrors(len(x), array('d',x), array('d',y), array('d',ex), array('d',ey))
    gs.append(g)
    g1 = ROOT.TGraphErrors(len(x), array('d',x), array('d',y1), array('d',ex), array('d',ey1))
    g1s.append(g1)

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta]
l = ROOT.TLegend(0.67,0.72,0.87,0.87)
for i,g in enumerate(gs):
    g.SetMarkerStyle(21)
    g.SetMarkerColor(colors[i])
    g.SetLineColor(colors[i])
    if i == 0:
        g.SetTitle('d_{VV}^{C} / d_{VV} (>400 #mum);input distributions;')
        g.GetYaxis().SetRangeUser(0,4)
        g.Draw('AP')
    else:
        g.Draw('P')
    l.AddEntry(g, ntk[i], 'lep')
l.SetFillColor(0)
l.Draw()
line = ROOT.TLine(0,1,8,1)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw()
ps.save('ratio_simulated')

l = ROOT.TLegend(0.67,0.72,0.87,0.87)
for i,g in enumerate(g1s):
    g.SetMarkerStyle(21)
    g.SetMarkerColor(colors[i])
    g.SetLineColor(colors[i])
    if i == 0:
        g.SetTitle('d_{VV}^{C}(n) / d_{VV}^{C}(1) (>400 #mum);%s;' % lsh)
        g.GetYaxis().SetRangeUser(0.6,1.4)
        g.Draw('AP')
    else:
        g.Draw('P')
    l.AddEntry(g, ntk[i], 'lep')
l.SetFillColor(0)
l.Draw()
line = ROOT.TLine(0,1,8,1)
line.SetLineStyle(2)
line.SetLineWidth(2)
line.Draw()
ps.save('ratio_dvvc1')

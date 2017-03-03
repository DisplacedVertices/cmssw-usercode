from JMTucker.Tools.ROOTTools import *
from array import array
ROOT.TH1.AddDirectory(0)

mode = 'vary_eff'
#mode = 'vary_dphi'
#mode = 'vary_dbv'

set_style()
ROOT.gStyle.SetOptFit(0)
ps = plot_saver('../plots/bkgest/compare_dvvc_%s' % mode, size=(700,700), root=False, log=False)

fn1 = ['2v_from_jets_3track_average3_c1p35_e2_a3p66_v11.root']
fn2 = ['2v_from_jets_4track_average4_c1p35_e2_a3p66_v11.root']
fn3 = ['2v_from_jets_5track_average5_c1p35_e2_a3p66_v11.root']

if mode == 'vary_eff':
    fn1.append('2v_from_jets_3track_maxtk3_c1p35_e2_a3p66_v11.root')
    fn2.append('2v_from_jets_4track_maxtk4_c1p35_e2_a3p66_v11.root')
    fn3.append('2v_from_jets_5track_maxtk5_c1p35_e2_a3p66_v11.root')
    ls = ['average efficiency', 'maxtk efficiency']

if mode == 'vary_dphi':
    fn1.append('2v_from_jets_3track_average3_dphijvmin_v11.root')
    fn2.append('2v_from_jets_4track_average4_dphijvmin_v11.root')
    fn3.append('2v_from_jets_5track_average5_dphijvmin_v11.root')
    ls = ['|#Delta#phi| from 3-track #Delta#phi_{JJ}', '|#Delta#phi| from #Delta#phi_{JV}^{min}']

if mode == 'vary_dbv':
    fn1.append('2v_from_jets_3track_average3_c1p35_e2_a3p66_v11_sum.root')
    fn2.append('2v_from_jets_4track_average4_c1p35_e2_a3p66_v11_sum.root')
    fn3.append('2v_from_jets_5track_average5_c1p35_e2_a3p66_v11_sum.root')
    ls = ['default', 'sort by b quarks']

fns = [fn1, fn2, fn3]
ntk = ['3-track', '4-track', '5-track']
n2v = [1323., 22., 1.]

ebin1 = [0.0025, 0.0063, 0.0110]
ebin2 = [0.0021, 0.0068, 0.0280]
ebin3 = [0.0056, 0.0200, 0.0910]

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet, ROOT.kPink+1]

x = []
ex = []
y2 = []
ey2 = []
y3 = []
ey3 = []
for i in range(3):
    print ntk[i]
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
    l2.AddEntry(h2, 'simulated events')

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

        chi2 = 0
        for k in range(1,h.GetNbinsX()+1):
            if (h2.GetBinError(k) > 0):
                chi2 += (h.GetBinContent(k)-h2.GetBinContent(k))**2 / h2.GetBinError(k)**2
        print '%35s: deltaphi chi2/ndf = %f' % (ls[j], chi2/(h.GetNbinsX()-1))

    l2.SetFillColor(0)
    l2.Draw()
    ps.save('%s_dphi'%ntk[i])

    es1 = ROOT.Double(0)
    s1 = hh.IntegralAndError(1,4,es1)
    es2 = ROOT.Double(0)
    s2 = hh.IntegralAndError(5,7,es2)
    es3 = ROOT.Double(0)
    s3 = hh.IntegralAndError(8,40,es3)

    c1 = hs[0].Integral(1,4)
    ec1 = ebin1[i] * c1
    c2 = hs[0].Integral(5,7)
    ec2 = ebin2[i] * c2
    c3 = hs[0].Integral(8,40)
    ec3 = ebin3[i] * c3

    v1 = hs[1].Integral(1,4)
    ev1 = ebin1[i] * v1
    v2 = hs[1].Integral(5,7)
    ev2 = ebin2[i] * v2
    v3 = hs[1].Integral(8,40)
    ev3 = ebin3[i] * v3

    r1 = v1/c1
    er1 = (v1/c1) * ((ev1/v1)**2 + (ec1/c1)**2)**0.5
    r2 = v2/c2
    er2 = (v2/c2) * ((ev2/v2)**2 + (ec2/c2)**2)**0.5
    r3 = v3/c3
    er3 = (v3/c3) * ((ev3/v3)**2 + (ec3/c3)**2)**0.5

    print
    print '    simulated events: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (s1, es1, s2, es2, s3, es3)
    print 'default construction: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (c1, ec1, c2, ec2, c3, ec3)
    print '           variation: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (v1, ev1, v2, ev2, v3, ev3)
    print ' variation / default: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (r1, er1, r2, er2, r3, er3)
    print
    print

    if mode == 'vary_dphi':
        if i == 0:
            er2 *= 0.203370
            er3 *= 0.154157
        if i == 1:
            er2 *= 0.200499
            er3 *= 0.161360
        if i == 2:
            er2 *= 0.187591
            er3 *= 0.130377
    if mode == 'vary_eff':
        er2 *= (abs(r2-1))**0.5 / (1+r2)**0.5
        er3 *= (abs(r3-1))**0.5 / (1+r3)**0.5

    x.append(i-2)
    ex.append(0)
    y2.append(r2)
    ey2.append(er2)
    y3.append(r3)
    ey3.append(er3)

bins = ['bin2', 'bin3']
dvvc = ['400 #mum < d_{VV}^{C} < 700 #mum', 'd_{VV}^{C} > 700 #mum']
ys = [y2, y3]
eys = [ey2, ey3]
for i in range(2):
    g = ROOT.TGraphErrors(len(x), array('d',x), array('d',ys[i]), array('d',ex), array('d',eys[i]))
    g.SetMarkerStyle(21)
    g.SetTitle('variation / default (%s);3-track%12s4-track%12s5-or-more-track%2s' % (dvvc[i], '','',''))
    g.GetXaxis().SetLimits(-3,1)
    g.GetXaxis().SetLabelSize(0)
    g.GetXaxis().SetTitleOffset(0.5)
    g.GetYaxis().SetRangeUser(0.6,1.4)
    g.Draw('AP')

    line = ROOT.TLine(-3,1,1,1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()

    r = g.Fit('pol1','S','',-2,-1)
    g5 = ROOT.TGraphErrors(1, array('d',[-0.1]), array('d',[r.Value(0)]), array('d',[0]), array('d',[r.ParError(0)]))
    g5.SetLineColor(ROOT.kRed)
    g5.SetMarkerColor(ROOT.kRed)
    g5.SetMarkerStyle(21)
    g5.Draw('P')

    t5 = ROOT.TLatex()
    t5.SetTextFont(42)
    t5.SetTextSize(0.04)
    t5.SetTextColor(ROOT.kRed)
    t5.DrawLatex(-0.1, r.Value(0) - r.ParError(0) - t5.GetTextSize(), '%.2f #pm %.2f' % (r.Value(0), r.ParError(0)))

    t3 = ROOT.TLatex()
    t3.SetTextFont(42)
    t3.SetTextSize(0.04)
    t3.DrawLatex(-2, ys[i][0] - eys[i][0] - t3.GetTextSize(), '%.2f #pm %.2f' % (ys[i][0], eys[i][0]))

    t = ROOT.TLatex()
    t.SetTextFont(42)
    t.SetTextSize(0.04)
    t.DrawLatex(-2.5, 0.7, '#splitline{difference from 3-track to 5-or-more-track:}{%.2f #pm %.2f}' % (abs(r.Value(0) - ys[i][0]), (r.ParError(0)**2 + eys[i][0]**2)**0.5))

    ps.save('ratio_%s_%s' % (bins[i], mode))

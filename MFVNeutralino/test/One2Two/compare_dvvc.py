from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
from array import array
ROOT.TH1.AddDirectory(0)

is_mc = True
only_10pc = False
year = '2017p8'
version = 'V27m'

#mode = 'vary_eff'
#mode = 'vary_dphi'
mode = 'vary_bquarks'

set_style()
ROOT.gStyle.SetOptFit(0)
ps = plot_saver(plot_dir('compare_dvvc_%s_%s%s%s_%s' % (version.capitalize(), mode, '' if is_mc else '_data', '_10pc' if only_10pc else '', year)), size=(700,700), root=False, log=False)

fn1 = ['2v_from_jets%s_%s_3track_default_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_3track_%s_%s.root' % ('' if is_mc else '_data', year, mode, version)]
fn2 = ['2v_from_jets%s_%s_4track_default_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_4track_%s_%s.root' % ('' if is_mc else '_data', year, mode, version)]
fn3 = ['2v_from_jets%s_%s_5track_default_%s.root' % ('' if is_mc else '_data', year, version), '2v_from_jets%s_%s_5track_%s_%s.root' % ('' if is_mc else '_data', year, mode, version)]

if mode == 'vary_eff':
    ls = ['vertexer efficiency', 'ntkseeds efficiency']

if mode == 'vary_dphi':
    ls = ['|#Delta#phi| from 3-track #Delta#phi_{JJ}', 'uniform |#Delta#phi|']

# Note in 2015--2016, the 5-trk, two-vertex ratio was equal to 1 (hence "bratio1")
if mode == 'vary_bquarks':
    ls = ['3-track two-vertex ratio', '5-track two-vertex ratio']

fns = [fn1, fn2, fn3]
ntk = ['3-track', '4-track', '5-track']
names = ['3-track x 3-track', '4-track x 4-track', '#geq 5-track x #geq 5-track']

n2v_2017 = [651., 2.21, 1.]
n2v_2018 = [426., 5., 1.]

if year == '2017' :
    n2v = n2v_2017
elif year == '2018' :
    n2v = n2v_2018
elif year == '2017p8' :
    n2v = [sum(n2v_val) for n2v_val in zip(n2v_2017, n2v_2018)]
else :
    print("Unsupported year %s! Exiting." % year)
    sys.exit()

colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kMagenta, ROOT.kOrange, ROOT.kViolet, ROOT.kPink+1]

def write(font, size, x, y, text):
    w = ROOT.TLatex()
    w.SetNDC()
    w.SetTextFont(font)
    w.SetTextSize(size)
    w.DrawLatex(x, y, text)
    return w

x = []
ex = []
y1 = []
ey1 = []
y2 = []
ey2 = []
y3 = []
ey3 = []
for i in range(3):
    print ntk[i]

    if not is_mc:
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
                h.Draw('hist e')
            elif j == 1:
                h.Draw('hist e sames')
            hs.append(h)
            if j > 1:
                continue
            l1.AddEntry(h, ls[j])
        l1.SetFillColor(0)
        l1.Draw()
        ps.save('compare_dvvc_%s_%s' % (mode, ntk[i]))

        h2s = []
        l2 = ROOT.TLegend(0.15,0.75,0.50,0.85)
        for j in range(len(ls)):
            h = ROOT.TFile(fns[i][j]).Get('h_c1v_absdphivv')
            h.SetStats(0)
            h.SetLineColor(colors[j])
            h.SetLineWidth(2)
            h.Scale(n2v[i]/h.Integral())
            if j == 0:
                h.SetTitle(';|#Delta#phi_{VV}|;Events')
                h.SetMinimum(0)
                h.Draw('hist e')
            elif j == 1:
                h.Draw('hist e sames')
            h2s.append(h)
            if j > 1:
                continue
            l2.AddEntry(h, ls[j])
        l2.SetFillColor(0)
        l2.Draw()
        if not only_10pc and year == '2015p6':
            write(42, 0.040, 0.150, 0.700, names[i])
            write(61, 0.050, 0.098, 0.913, 'CMS')
            write(52, 0.035, 0.200, 0.913, 'Preliminary')
            write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')
        ps.save('compare_dphi_%s_%s' % (mode, ntk[i]))

        ebin = ebins['data%s_%s_%strack' % ('10pc' if only_10pc else '100pc', year, ntk[i][0])]

        c1 = hs[0].Integral(1,4)
        ec1 = ebin[0] * c1
        c2 = hs[0].Integral(5,7)
        ec2 = ebin[1] * c2
        c3 = hs[0].Integral(8,40)
        ec3 = ebin[2] * c3

        v1 = hs[1].Integral(1,4)
        ev1 = ebin[0] * v1
        v2 = hs[1].Integral(5,7)
        ev2 = ebin[1] * v2
        v3 = hs[1].Integral(8,40)
        ev3 = ebin[2] * v3

        r1 = v1/c1
        er1 = (v1/c1) * ((ev1/v1)**2 + (ec1/c1)**2)**0.5
        r2 = v2/c2
        er2 = (v2/c2) * ((ev2/v2)**2 + (ec2/c2)**2)**0.5
        r3 = v3/c3
        er3 = (v3/c3) * ((ev3/v3)**2 + (ec3/c3)**2)**0.5

        er1 *= (abs(r1-1))**0.5 / (1+r1)**0.5
        er2 *= (abs(r2-1))**0.5 / (1+r2)**0.5
        er3 *= (abs(r3-1))**0.5 / (1+r3)**0.5

        print
        print 'default construction: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (c1, ec1, c2, ec2, c3, ec3)
        print '           variation: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (v1, ev1, v2, ev2, v3, ev3)
        print ' variation / default: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (r1, er1, r2, er2, r3, er3)
        print
        print

        x.append(i-2)
        ex.append(0)
        y1.append(r1)
        ey1.append(er1)
        y2.append(r2)
        ey2.append(er2)
        y3.append(r3)
        ey3.append(er3)

    else:
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

        if i == 2:
            h2s = []
            l2 = ROOT.TLegend(0.15,0.75,0.50,0.85)
            for j in range(len(ls)):
                h = ROOT.TFile(fns[i][j]).Get('h_c1v_absdphivv')
                h.SetStats(0)
                h.SetLineColor(colors[j])
                h.SetLineWidth(2)
                h.Scale(n2v[i]/h.Integral())
                if j == 0:
                    h.SetTitle(';|#Delta#phi_{VV}|;Events')
                    h.SetMinimum(0)
                    h.Draw('hist e')
                elif j == 1:
                    h.Draw('hist e sames')
                h2s.append(h)
                if j > 1:
                    continue
                l2.AddEntry(h, ls[j])
            l2.SetFillColor(0)
            l2.Draw()
            ps.save('compare_dphi_%s' % mode)

        es1 = ROOT.Double(0)
        s1 = hh.IntegralAndError(1,4,es1)
        es2 = ROOT.Double(0)
        s2 = hh.IntegralAndError(5,7,es2)
        es3 = ROOT.Double(0)
        s3 = hh.IntegralAndError(8,40,es3)

        ebin = ebins['MCeffective_%s_%strack' % (year, ntk[i][0])]

        c1 = hs[0].Integral(1,4)
        ec1 = ebin[0] * c1
        c2 = hs[0].Integral(5,7)
        ec2 = ebin[1] * c2
        c3 = hs[0].Integral(8,40)
        ec3 = ebin[2] * c3

        v1 = hs[1].Integral(1,4)
        ev1 = ebin[0] * v1
        v2 = hs[1].Integral(5,7)
        ev2 = ebin[1] * v2
        v3 = hs[1].Integral(8,40)
        ev3 = ebin[2] * v3

        r1 = v1/c1
        er1 = (v1/c1) * ((ev1/v1)**2 + (ec1/c1)**2)**0.5
        r2 = v2/c2
        er2 = (v2/c2) * ((ev2/v2)**2 + (ec2/c2)**2)**0.5
        r3 = v3/c3
        er3 = (v3/c3) * ((ev3/v3)**2 + (ec3/c3)**2)**0.5

        er1 *= (abs(r1-1))**0.5 / (1+r1)**0.5
        er2 *= (abs(r2-1))**0.5 / (1+r2)**0.5
        er3 *= (abs(r3-1))**0.5 / (1+r3)**0.5

        print
        print '    simulated events: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (s1, es1, s2, es2, s3, es3)
        print 'default construction: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (c1, ec1, c2, ec2, c3, ec3)
        print '           variation: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (v1, ev1, v2, ev2, v3, ev3)
        print ' variation / default: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (r1, er1, r2, er2, r3, er3)
        print
        print

        x.append(i-2)
        ex.append(0)
        y1.append(r1)
        ey1.append(er1)
        y2.append(r2)
        ey2.append(er2)
        y3.append(r3)
        ey3.append(er3)

bins = ['bin1', 'bin2', 'bin3']
dvvc = ['d_{VV}^{C} < 400 #mum', '400 #mum < d_{VV}^{C} < 700 #mum', 'd_{VV}^{C} > 700 #mum']
ys = [y1, y2, y3]
eys = [ey1, ey2, ey3]
for i in range(3):
    g = ROOT.TGraphErrors(len(x), array('d',x), array('d',ys[i]), array('d',ex), array('d',eys[i]))
    g.SetMarkerStyle(21)
    g.SetTitle('variation / default (%s);3-track%12s4-track%12s5-or-more-track%2s' % (dvvc[i], '','',''))
    g.GetXaxis().SetLimits(-3,1)
    g.GetXaxis().SetLabelSize(0)
    g.GetXaxis().SetTitleOffset(0.5)
    g.GetYaxis().SetRangeUser(0,2)
    g.Draw('AP')

    line = ROOT.TLine(-3,1,1,1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()

    t5 = ROOT.TLatex()
    t5.SetTextFont(42)
    t5.SetTextSize(0.04)
    t5.DrawLatex(0, ys[i][2] - eys[i][2] - t5.GetTextSize(), '%.2f #pm %.2f' % (ys[i][2], eys[i][2]))

    t = ROOT.TLatex()
    t.SetTextFont(42)
    t.SetTextSize(0.04)
    t.DrawLatex(-2.5, 0.2, '#splitline{difference of 5-or-more-track ratio from 1:}{%.2f #pm %.2f}' % (abs(ys[i][2] - 1), eys[i][2]))

    ps.save('ratio_%s_%s' % (bins[i], mode))

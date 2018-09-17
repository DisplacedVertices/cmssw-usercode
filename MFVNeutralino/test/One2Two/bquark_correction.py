from JMTucker.Tools.ROOTTools import *
from array import array
ROOT.TH1.AddDirectory(0)

year = '2015p6'

mode = ''
#mode = 'ratio1'

set_style()
ps = plot_saver('../plots/bkgest/v15_v5/bquark_correction_%s%s' % (year, '' if mode == '' else '_%s'%mode), size=(700,700), root=False, log=False)

ntk = ['3-track', '4-track', '5-track', '4-track-3-track']

ebin1 = [0.0044, 0.0107, 0.0205, 0.0107]
ebin2 = [0.0039, 0.0129, 0.0525, 0.0129]
ebin3 = [0.0102, 0.0393, 0.1697, 0.0393]

if year == '2015':
    ebin1 = [0.0056, 0.0141, 0.0259, 0.0141]
    ebin2 = [0.0050, 0.0171, 0.0660, 0.0171]
    ebin3 = [0.0129, 0.0518, 0.2137, 0.0518]

if year == '2015p6':
    ebin1 = [0.0042, 0.0100, 0.0194, 0.0100]
    ebin2 = [0.0038, 0.0124, 0.0501, 0.0124]
    ebin3 = [0.0098, 0.0373, 0.1615, 0.0373]

x = []
ex = []
y1 = []
ey1 = []
y2 = []
ey2 = []
y3 = []
ey3 = []
for i,ntracks in enumerate([3,4,5,7]):
    print ntk[i]

    h0 = ROOT.TFile('2v_from_jets_%s_%itrack_nobquarks_v15_v5.root' % (year, ntracks)).Get('h_c1v_dvv')
    h0.SetStats(0)
    h0.SetLineColor(ROOT.kBlue)
    h0.SetLineWidth(2)
    h0.Scale(1./h0.Integral())
    h0.SetTitle(';d_{VV}^{C} (cm);Events')
    h0.GetYaxis().SetRangeUser(0,0.5)
    h0.Draw('hist e')

    hb = ROOT.TFile('2v_from_jets_%s_%itrack_bquarks_v15_v5.root' % (year, ntracks)).Get('h_c1v_dvv')
    hb.SetStats(0)
    hb.SetLineColor(ROOT.kRed)
    hb.SetLineWidth(2)
    hb.Scale(1./hb.Integral())
    hb.Draw('hist e sames')

    lb = ROOT.TLegend(0.35,0.75,0.85,0.85)
    lb.AddEntry(h0, 'without b quarks')
    lb.AddEntry(hb, 'with b quarks')
    lb.Draw()
    ps.save('compare_dvvc_bquarks_%s' % ntk[i])

    h1 = ROOT.TFile('2v_from_jets_%s_%itrack_bquark_uncorrected_v15_v5.root' % (year, ntracks)).Get('h_c1v_dvv')
    h1.SetStats(0)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(3)
    h1.Scale(1./h1.Integral())
    h1.SetTitle(';d_{VV}^{C} (cm);Events')
    h1.GetYaxis().SetRangeUser(0,0.5)
    h1.Draw('hist e')

    h2 = ROOT.TFile('2v_from_jets_%s_%itrack_bquark_corrected_v15_v5.root' % (year, ntracks)).Get('h_c1v_dvv')
    if mode == 'ratio1':
        h2 = ROOT.TFile('2v_from_jets_%s_%itrack_bquarks_v15_v5.root' % (year, ntracks)).Get('h_c1v_dvv')
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kViolet)
    h2.SetLineWidth(3)
    h2.Scale(1./h2.Integral())
    h2.Draw('hist e sames')

    l = ROOT.TLegend(0.35,0.75,0.85,0.85)
    l.AddEntry(h1, 'without b quark correction')
    l.AddEntry(h2, 'with b quark correction')
    l.Draw()
    ps.save('compare_dvvc_%s' % ntk[i])

    h = h2.Clone('%s' % ntk[i])
    h.Divide(h1)
    h.SetTitle('b quark correction;d_{VV}^{C} (cm);')
    h.Draw()
    ps.save('bquark_correction_%s' % ntk[i])

    c1 = h1.Integral(1,4)
    ec1 = ebin1[i] * c1
    c2 = h1.Integral(5,7)
    ec2 = ebin2[i] * c2
    c3 = h1.Integral(8,40)
    ec3 = ebin3[i] * c3

    v1 = h2.Integral(1,4)
    ev1 = ebin1[i] * v1
    v2 = h2.Integral(5,7)
    ev2 = ebin2[i] * v2
    v3 = h2.Integral(8,40)
    ev3 = ebin3[i] * v3

    r1 = v1/c1
    er1 = (v1/c1) * ((ev1/v1)**2 + (ec1/c1)**2)**0.5
    r2 = v2/c2
    er2 = (v2/c2) * ((ev2/v2)**2 + (ec2/c2)**2)**0.5
    r3 = v3/c3
    er3 = (v3/c3) * ((ev3/v3)**2 + (ec3/c3)**2)**0.5

    print 'default construction: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (c1, ec1, c2, ec2, c3, ec3)
    print '           variation: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (v1, ev1, v2, ev2, v3, ev3)
    print ' variation / default: 0-400 um: %6.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (r1, er1, r2, er2, r3, er3)
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
    g.SetTitle('b quark correction (%s);3-track%8s4-track%7s5-track%8s4x3-track%2s' % (dvvc[i], '','','',''))
    g.GetXaxis().SetLimits(-3,2)
    g.GetXaxis().SetLabelSize(0)
    g.GetXaxis().SetTitleOffset(0.5)
    g.GetYaxis().SetRangeUser(0,3)
    g.Draw('AP')

    line = ROOT.TLine(-3,1,2,1)
    line.SetLineStyle(2)
    line.SetLineWidth(2)
    line.Draw()

    for j in range(len(x)):
        t = ROOT.TLatex()
        t.SetTextFont(42)
        t.SetTextSize(0.03)
        t.DrawLatex(j-2+0.03, ys[i][j] + eys[i][j] - t.GetTextSize(), '%.2f #pm %.2f' % (ys[i][j], eys[i][j]))

    ps.save('bquark_correction_%s' % bins[i])

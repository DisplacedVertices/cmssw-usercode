from JMTucker.Tools.ROOTTools import *
from statmodel import ebins
from array import array
ROOT.TH1.AddDirectory(0)

version = 'V25m'
year = '2018'

mode = ''
#mode = 'ratio1'

compare_btags = False

set_style()
ps = plot_saver(plot_dir('bquark_correction_%s_%s%s' % (version.capitalize(), year, '' if mode == '' else '_%s'%mode)), size=(700,700), root=True, log=False)

ntk = ['3-track', '4-track', '5-track', '4-track-3-track']

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

    h0 = ROOT.TFile('2v_from_jets_%s_%itrack_nobquarks_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
    h0.SetStats(0)
    h0.SetLineColor(ROOT.kBlue)
    h0.SetLineWidth(2)
    h0.Scale(1./h0.Integral())
    h0.SetTitle(';d_{VV}^{C} (cm);Events')
    h0.GetYaxis().SetRangeUser(0,0.5)
    h0.Draw('hist e')

    hb = ROOT.TFile('2v_from_jets_%s_%itrack_bquarks_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
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

    if compare_btags:
        h0.SetLineWidth(3)
        h0.Draw('hist e')
        hb.SetLineWidth(3)
        hb.Draw('hist e sames')

        h0tag = ROOT.TFile('2v_from_jets_%s_%itrack_nobtags_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
        h0tag.SetStats(0)
        h0tag.SetLineColor(ROOT.kAzure+10)
        h0tag.SetLineWidth(2)
        h0tag.Scale(1./h0tag.Integral())
        h0tag.Draw('hist e sames')

        hbtag = ROOT.TFile('2v_from_jets_%s_%itrack_btags_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
        hbtag.SetStats(0)
        hbtag.SetLineColor(ROOT.kMagenta)
        hbtag.SetLineWidth(2)
        hbtag.Scale(1./hbtag.Integral())
        hbtag.Draw('hist e sames')

        lb.AddEntry(h0tag, 'without btags')
        lb.AddEntry(hbtag, 'with btags')
        lb.Draw()
        ps.save('compare_dvvc_btags_%s' % ntk[i])

    h1 = ROOT.TFile('2v_from_jets_%s_%itrack_bquark_uncorrected_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
    h1.SetStats(0)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(3)
    h1.Scale(1./h1.Integral())
    h1.SetTitle(';d_{VV}^{C} (cm);Events')
    h1.GetYaxis().SetRangeUser(0,0.5)
    h1.Draw('hist e')

    h2 = ROOT.TFile('2v_from_jets_%s_%itrack_bquark_corrected_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
    if mode == 'ratio1':
        h2 = ROOT.TFile('2v_from_jets_%s_%itrack_bquarks_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kViolet)
    h2.SetLineWidth(3)
    h2.Scale(1./h2.Integral())
    h2.Draw('hist e sames')

    l = ROOT.TLegend(0.35,0.75,0.85,0.85)
    l.AddEntry(h1, 'without b quark correction')
    l.AddEntry(h2, 'with b quark correction')
    l.Draw()
    ps.save('compare_dvvc_bquark_correction_%s' % ntk[i])

    if compare_btags:
        h1.Draw('hist e')
        h2.Draw('hist e sames')

        h3 = ROOT.TFile('2v_from_jets_%s_%itrack_btag_corrected_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
        if mode == 'ratio1':
            h3 = ROOT.TFile('2v_from_jets_%s_%itrack_btags_%s.root' % (year, ntracks, version)).Get('h_c1v_dvv')
        h3.SetStats(0)
        h3.SetLineColor(ROOT.kMagenta)
        h3.SetLineWidth(3)
        h3.Scale(1./h3.Integral())
        h3.Draw('hist e sames')

        l.AddEntry(h3, 'with btag correction')
        l.Draw()
        ps.save('compare_dvvc_btag_correction_%s' % ntk[i])

    h = h2.Clone('%s' % ntk[i])
    h.Divide(h1)
    h.SetTitle('b quark correction;d_{VV}^{C} (cm);')
    h.Draw()
    ps.save('bquark_correction_%s' % ntk[i])

    ebin = ebins['MCeffective_%s_%dtrack' % (year, 4 if ntracks==7 else ntracks)]

    c1 = h1.Integral(1,4)
    ec1 = ebin[0] * c1
    c2 = h1.Integral(5,7)
    ec2 = ebin[1] * c2
    c3 = h1.Integral(8,40)
    ec3 = ebin[2] * c3

    v1 = h2.Integral(1,4)
    ev1 = ebin[0] * v1
    v2 = h2.Integral(5,7)
    ev2 = ebin[1] * v2
    v3 = h2.Integral(8,40)
    ev3 = ebin[2] * v3

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

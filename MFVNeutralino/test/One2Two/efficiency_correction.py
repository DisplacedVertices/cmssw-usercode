from JMTucker.Tools.ROOTTools import *
from array import array
ROOT.TH1.AddDirectory(0)

is_mc = True
year = '2015p6'

set_style()
ps = plot_saver('../plots/bkgest/v15_v5/efficiency_correction%s_%s' % ('' if is_mc else '_data', year), size=(700,700), root=False, log=False)

ntk = ['3-track', '4-track', '5-track', '4-track-3-track']

if is_mc:
    ebin1 = [0.0032, 0.0091, 0.0249, 0.0091] if year == '2017' else [1, 1, 1, 1]
    ebin2 = [0.0030, 0.0113, 0.0648, 0.0113] if year == '2017' else [1, 1, 1, 1]
    ebin3 = [0.0078, 0.0348, 0.2124, 0.0348] if year == '2017' else [1, 1, 1, 1]
else:                                                                                                                                                      
    ebin1 = [1, 1, 1, 1] if year == '2017' else [1, 1, 1, 1]
    ebin2 = [1, 1, 1, 1] if year == '2017' else [1, 1, 1, 1]
    ebin3 = [1, 1, 1, 1] if year == '2017' else [1, 1, 1, 1]

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
for i,ntracks in enumerate([3,4,5,7]):
    print ntk[i]

    h1 = ROOT.TFile('2v_from_jets%s_%s_%itrack_noclearing_v15_v5.root' % ('' if is_mc else '_data', year, ntracks)).Get('h_c1v_dvv')
    h1.SetStats(0)
    h1.SetLineColor(ROOT.kBlack)
    h1.SetLineWidth(2)
    h1.Scale(1./h1.Integral())
    h1.SetTitle(';d_{VV}^{C} (cm);Events')
    if i == 2:
        h1.GetYaxis().SetRangeUser(0,0.4)
    h1.Draw('hist e')

    h2 = ROOT.TFile('2v_from_jets%s_%s_%itrack_default_v15_v5.root' % ('' if is_mc else '_data', year, ntracks)).Get('h_c1v_dvv')
    h2.SetStats(0)
    h2.SetLineColor(ROOT.kRed)
    h2.SetLineWidth(2)
    h2.Scale(1./h2.Integral())
    h2.Draw('hist e sames')

    l = ROOT.TLegend(0.35,0.75,0.85,0.85)
    l.AddEntry(h1, 'without efficiency correction')
    l.AddEntry(h2, 'with efficiency correction')
    l.Draw()
    if not is_mc and year == '2015p6':
        write(61, 0.050, 0.098, 0.913, 'CMS')
        write(52, 0.035, 0.200, 0.913, 'Preliminary')
        write(42, 0.050, 0.560, 0.913, '38.5 fb^{-1} (13 TeV)')
    ps.save('compare_dvvc_%s' % ntk[i])

    h = h2.Clone('%s' % ntk[i])
    h.Divide(h1)
    h.SetTitle('efficiency correction;d_{VV}^{C} (cm);')
    h.Draw()
    ps.save('efficiency_correction_%s' % ntk[i])

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
    g.SetTitle('efficiency correction (%s);3-track%8s4-track%7s5-track%8s4x3-track%2s' % (dvvc[i], '','','',''))
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

    ps.save('efficiency_correction_%s' % bins[i])

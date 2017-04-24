from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

year = '2016'

set_style()
ps = plot_saver('../plots/bkgest/v14/closure_%s' % year, size=(700,700), root=False, log=False)

fns = ['2v_from_jets_%s_3track_default_v14.root' % year, '2v_from_jets_%s_4track3track_default_v14.root' % year, '2v_from_jets_%s_4track_default_v14.root' % year, '2v_from_jets_%s_5track_default_v14.root' % year]
ntk = ['3-track', '4-track-3-track', '4-track', '5-track']

n2v = [934., 211., 7., 1.]
ebin1 = [0.0026, 0.0062, 0.0062, 0.0124]
ebin2 = [0.0023, 0.0078, 0.0078, 0.0328]
ebin3 = [0.0060, 0.0231, 0.0231, 0.1019]

if year == '2015':
    n2v = [44., 9., 1., 1.]
    ebin1 = [0.0118, 0.0291, 0.0291, 0.0567]
    ebin2 = [0.0106, 0.0371, 0.0371, 0.1513]
    ebin3 = [0.0271, 0.1100, 0.1100, 0.4761]

if year == '2015p6':
    n2v = [978., 220., 7., 1.]
    ebin1 = [0.0025, 0.0062, 0.0062, 0.0123]
    ebin2 = [0.0023, 0.0076, 0.0076, 0.0323]
    ebin3 = [0.0058, 0.0229, 0.0229, 0.1019]

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

    es = ROOT.Double(0)
    s = hh.IntegralAndError(1,40,es)
    if s == 0:
        s = 1
    es1 = ROOT.Double(0)
    s1 = hh.IntegralAndError(1,4,es1)
    if s1 == 0:
        s1 = 1
    es2 = ROOT.Double(0)
    s2 = hh.IntegralAndError(5,7,es2)
    if s2 == 0:
        s2 = 1
    es3 = ROOT.Double(0)
    s3 = hh.IntegralAndError(8,40,es3)
    if s3 == 0:
        s3 = 1

    ec = ROOT.Double(0)
    c = h.IntegralAndError(1,40,ec)
    c1 = h.Integral(1,4)
    ec1 = ebin1[i] * c1
    c2 = h.Integral(5,7)
    ec2 = ebin2[i] * c2
    c3 = h.Integral(8,40)
    ec3 = ebin3[i] * c3

    r = c/s
    er = (c/s) * ((ec/c)**2 + (es/s)**2)**0.5
    r1 = c1/s1
    er1 = (c1/s1) * ((ec1/c1)**2 + (es1/s1)**2)**0.5
    r2 = c2/s2
    er2 = (c2/s2) * ((ec2/c2)**2 + (es2/s2)**2)**0.5
    r3 = c3/s3
    er3 = (c3/s3) * ((ec3/c3)**2 + (es3/s3)**2)**0.5

    print ntk[i]
    print '   simulated events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (s, es, s1, es1, s2, es2, s3, es3)
    print ' constructed events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (c, ec, c1, ec1, c2, ec2, c3, ec3)
    print '   ratio dVVC / dVV: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (r, er, r1, er1, r2, er2, r3, er3)

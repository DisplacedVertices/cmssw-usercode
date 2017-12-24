from JMTucker.Tools.ROOTTools import *
ROOT.TH1.AddDirectory(0)

is_mc = True
only_10pc = False
year = '2015p6'

rebin = False

set_style()
ps = plot_saver('../plots/bkgest/v15_v5/closure%s%s_%s' % ('' if is_mc else '_data', '_10pc' if only_10pc else '', year), size=(700,700), root=False, log=False)

fns = ['2v_from_jets%s_%s_3track_default_v15%s.root' % ('' if is_mc else '_data', year, '' if only_10pc else '_v5'), '2v_from_jets%s_%s_7track_default_v15%s.root' % ('' if is_mc else '_data', year, '' if only_10pc else '_v5'), '2v_from_jets%s_%s_4track_default_v15%s.root' % ('' if is_mc else '_data', year, '' if only_10pc else '_v5'), '2v_from_jets%s_%s_5track_default_v15%s.root' % ('' if is_mc else '_data', year, '' if only_10pc else '_v5')]
ntk = ['3-track', '4-track-3-track', '4-track', '5-track']

n2v = [44., 9., 1., 1.] if year == '2015' else [946., 204., 8., 1.] if year == '2016' else [991., 213., 8., 1.]

if is_mc:
    ebin1 = [0.0118, 0.0297, 0.0297, 0.0595] if year == '2015' else [0.0026, 0.0064, 0.0064, 0.0125] if year == '2016' else [0.0025, 0.0062, 0.0062, 0.0122]
    ebin2 = [0.0107, 0.0364, 0.0364, 0.1501] if year == '2015' else [0.0023, 0.0078, 0.0078, 0.0317] if year == '2016' else [0.0023, 0.0077, 0.0077, 0.0312]
    ebin3 = [0.0272, 0.1092, 0.1092, 0.4846] if year == '2015' else [0.0060, 0.0230, 0.0230, 0.1021] if year == '2016' else [0.0059, 0.0229, 0.0229, 0.1005]
elif only_10pc:
    ebin1 = [0.0468, 0.1188, 0.1188, 0.2101] if year == '2015' else [0.0105, 0.0281, 0.0281, 0.0714] if year == '2016' else [0.0103, 0.0274, 0.0274, 0.0682]
    ebin2 = [0.0422, 0.1449, 0.1449, 0.5482] if year == '2015' else [0.0096, 0.0341, 0.0341, 0.1837] if year == '2016' else [0.0092, 0.0334, 0.0334, 0.1731]
    ebin3 = [0.1083, 0.4314, 0.4314, 1.5721] if year == '2015' else [0.0243, 0.1030, 0.1030, 0.5818] if year == '2016' else [0.0239, 0.0999, 0.0999, 0.5494]
else:
    ebin1 = [0.0148, 0.0375, 0.0375, 0.0687] if year == '2015' else [0.0034, 0.0088, 0.0088, 0.0225] if year == '2016' else [0.0033, 0.0086, 0.0086, 0.0212]
    ebin2 = [0.0132, 0.0459, 0.0459, 0.1731] if year == '2015' else [0.0030, 0.0108, 0.0108, 0.0566] if year == '2016' else [0.0030, 0.0104, 0.0104, 0.0542]
    ebin3 = [0.0341, 0.1363, 0.1363, 0.5575] if year == '2015' else [0.0077, 0.0324, 0.0324, 0.1848] if year == '2016' else [0.0076, 0.0314, 0.0314, 0.1750]

bins = to_array(0.0000, 0.0100, 0.0200, 0.0300, 0.0400, 0.0500, 0.0600, 0.0700, 0.0800, 0.0900, 0.1000, 0.4000)
ebins_3track = [0.0043, 0.0033, 0.0032, 0.0026, 0.0026, 0.0033, 0.0042, 0.0054, 0.0068, 0.0083, 0.0110]
ebins_4track = [0.0109, 0.0084, 0.0081, 0.0066, 0.0080, 0.0114, 0.0155, 0.0203, 0.0268, 0.0337, 0.0444]
ebins_5track = [0.0235, 0.0177, 0.0171, 0.0171, 0.0291, 0.0468, 0.0712, 0.0994, 0.1300, 0.1774, 0.1714]
ebins = [ebins_3track, ebins_4track, ebins_4track, ebins_5track]

#bins = to_array(0.0000, 0.0100, 0.0200, 0.0300, 0.0400, 0.0500, 0.0600, 0.0700, 0.0800, 0.0900, 0.1000, 0.1100, 0.1200, 0.1300, 0.1400, 0.1500, 0.1600, 0.1700, 0.1800, 0.1900, 0.2000, 0.2100, 0.2200, 0.2300, 0.2400, 0.2500, 0.2600, 0.2700, 0.2800, 0.2900, 0.3000, 0.3100, 0.3200, 0.3300, 0.3400, 0.3500, 0.3600, 0.3700, 0.3800, 0.3900, 0.4000)
#ebins_3track = [0.0043, 0.0033, 0.0031, 0.0026, 0.0026, 0.0032, 0.0042, 0.0054, 0.0066, 0.0081, 0.0099, 0.0116, 0.0140, 0.0162, 0.0192, 0.0213, 0.0253, 0.0282, 0.0314, 0.0379, 0.0435, 0.0492, 0.0578, 0.0629, 0.0656, 0.0798, 0.0793, 0.0965, 0.1182, 0.0966, 0.1272, 0.1340, 0.1445, 0.2003, 0.2222, 0.2087, 0.2332, 0.2101, 0.2060, 0.1022]
#ebins_4track = [0.0109, 0.0083, 0.0080, 0.0065, 0.0078, 0.0111, 0.0153, 0.0203, 0.0263, 0.0329, 0.0415, 0.0496, 0.0628, 0.0731, 0.0888, 0.0976, 0.1186, 0.1364, 0.1618, 0.1887, 0.2093, 0.2162, 0.2414, 0.2800, 0.3158, 0.3000, 0.3158, 0.3571, 0.4167, 0.4167, 0.3846, 0.5000, 0.5000, 0.5000, 0.4444, 0.4000, 0.4000, 0.5000, 0.4444, 0.1775]
#ebins_5track = [0.0235, 0.0170, 0.0168, 0.0171, 0.0282, 0.0452, 0.0680, 0.0936, 0.1300, 0.1613, 0.2093, 0.2414, 0.2609, 0.3529, 0.3571, 0.4545, 0.4000, 0.4000, 0.5000, 0.5714, 0.5000, 0.6000, 0.6000, 0.7500, 0.7500, 0.6667, 0.6667, 1.0000, 1.0000, 1.0000, 1.0000, 1.0000, 2.0000, 2.0000, 2.0000, 1.0000, 1.0000, 1.0000, 1.0000, 0.4098]
#ebins = [ebins_3track, ebins_4track, ebins_4track, ebins_5track]

for i in range(4):
    if not is_mc and i > 2:
        h = ROOT.TFile(fns[i]).Get('h_c1v_dvv')
        h.SetTitle(';d_{VV}^{C} (cm);')
        h.SetStats(0)
        h.SetLineColor(ROOT.kRed)
        h.SetLineWidth(2)
        h.Scale(1./h.Integral())
        if rebin:
            hr = h.Rebin(len(bins)-1, h.GetName() + '_rebin', bins)
            for j in range(len(ebins[i])):
                hr.SetBinError(j+1, ebins[i][j] * hr.GetBinContent(j+1))
            hr.Draw('hist e')
        else:
            h.Draw('hist e')
        ps.save('%s_dvvc' % ntk[i])

        ec = ROOT.Double(0)
        c = h.IntegralAndError(1,40,ec)
        c1 = h.Integral(1,4)
        ec1 = ebin1[i] * c1
        c2 = h.Integral(5,7)
        ec2 = ebin2[i] * c2
        c3 = h.Integral(8,40)
        ec3 = ebin3[i] * c3

        print ntk[i]
        print ' constructed events: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (c, ec, c1, ec1, c2, ec2, c3, ec3)
        print '    dVVC normalized: %7.3f +/- %5.3f, 0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % (c/c, ec/c, c1/c, ec1/c, c2/c, ec2/c, c3/c, ec3/c)

    hh = ROOT.TFile(fns[i]).Get('h_2v_dvv')
    hh.SetTitle(';d_{VV} (cm);Events')
    hh.SetStats(0)
    hh.SetLineColor(ROOT.kBlue)
    hh.SetLineWidth(2)
    if is_mc:
        if hh.Integral() > 0:
            hh.Scale(n2v[i]/hh.Integral())
        else:
            hh.SetMaximum(0.4)
    hh.SetMinimum(0)
    if rebin:
        hhr = hh.Rebin(len(bins)-1, hh.GetName() + '_rebin', bins)
        hhr.Draw()
    else:
        hh.Draw()

    h = ROOT.TFile(fns[i]).Get('h_c1v_dvv')
    h.SetStats(0)
    h.SetLineColor(ROOT.kRed)
    h.SetLineWidth(2)
    if is_mc:
        h.Scale(n2v[i]/h.Integral())
    else:
        if hh.Integral() > 0:
            h.Scale(hh.Integral()/h.Integral())
        else:
            h.Scale(1./h.Integral())
    if rebin:
        hr = h.Rebin(len(bins)-1, h.GetName() + '_rebin', bins)
        for j in range(len(ebins[i])):
            hr.SetBinError(j+1, ebins[i][j] * hr.GetBinContent(j+1))
        hr.Draw('hist e sames')
    else:
        h.Draw('hist e sames')

    l1 = ROOT.TLegend(0.35, 0.75, 0.85, 0.85)
    l1.AddEntry(hh, 'Simulated events' if is_mc else 'Data')
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
    print '     dVV normalized: %7.3f +/- %5.3f, 0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % (s/s, es/s, s1/s, es1/s, s2/s, es2/s, s3/s, es3/s)
    print '    dVVC normalized: %7.3f +/- %5.3f, 0-400 um: %7.3f +/- %5.3f, 400-700 um: %6.3f +/- %5.3f, 700-40000 um: %6.3f +/- %5.3f' % (c/c, ec/c, c1/c, ec1/c, c2/c, ec2/c, c3/c, ec3/c)
    print '   ratio dVVC / dVV: %7.2f +/- %5.2f, 0-400 um: %7.2f +/- %5.2f, 400-700 um: %6.2f +/- %5.2f, 700-40000 um: %6.2f +/- %5.2f' % (r, er, r1, er1, r2, er2, r3, er3)

    hh = ROOT.TFile(fns[i]).Get('h_2v_absdphivv')
    hh.SetTitle(';|#Delta#phi_{VV}|;Events')
    hh.SetStats(0)
    hh.SetLineColor(ROOT.kBlue)
    hh.SetLineWidth(2)
    if is_mc:
        if hh.Integral() > 0:
            hh.Scale(n2v[i]/hh.Integral())
        else:
            hh.SetMaximum(0.4)
    hh.SetMinimum(0)
    hh.Draw()

    h = ROOT.TFile(fns[i]).Get('h_c1v_absdphivv')
    h.SetStats(0)
    h.SetLineColor(ROOT.kRed)
    h.SetLineWidth(2)
    if is_mc:
        h.Scale(n2v[i]/h.Integral())
    else:
        if hh.Integral() > 0:
            h.Scale(hh.Integral()/h.Integral())
        else:
            h.Scale(1./h.Integral())
    h.Draw('hist e sames')

    l1 = ROOT.TLegend(0.15, 0.75, 0.65, 0.85)
    l1.AddEntry(hh, 'Simulated events' if is_mc else 'Data')
    l1.AddEntry(h, 'Construction')
    l1.SetFillColor(0)
    l1.Draw()
    ps.save('%s_dphi' % ntk[i])

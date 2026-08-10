import gzip
from collections import defaultdict
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools.Samples import *

set_style()
ps = plot_saver(plot_dir('sigeff_2015v6_new'), size=(600,600), log=False)

kinds = 'ddbar', 'mfv'
def samples():
    for kind, ss in zip(kinds, (mfv_ddbar_samples, mfv_signal_samples)):
        for s in ss:
            yield kind, s

if 1:
    mfv_ddbar_tau00100um_M0300.ratio = (1.6652, 0.6007, 0.9593)
    mfv_ddbar_tau00100um_M0400.ratio = (1.3076, 0.2708, 0.3426)
    mfv_ddbar_tau00100um_M0500.ratio = (0.9364, 0.1429, 0.1685)
    mfv_ddbar_tau00100um_M0600.ratio = (1.3120, 0.1885, 0.2204)
    mfv_ddbar_tau00100um_M0800.ratio = (1.0424, 0.1285, 0.1466)
    mfv_ddbar_tau00100um_M1200.ratio = (1.2314, 0.1365, 0.1536)
    mfv_ddbar_tau00100um_M1600.ratio = (1.0412, 0.1189, 0.1343)
    mfv_ddbar_tau00300um_M0300.ratio = (1.3138, 0.1783, 0.2065)
    mfv_ddbar_tau00300um_M0400.ratio = (1.2059, 0.0925, 0.1002)
    mfv_ddbar_tau00300um_M0500.ratio = (1.1737, 0.0655, 0.0694)
    mfv_ddbar_tau00300um_M0600.ratio = (1.1764, 0.0557, 0.0585)
    mfv_ddbar_tau00300um_M0800.ratio = (1.1404, 0.0483, 0.0505)
    mfv_ddbar_tau00300um_M1200.ratio = (1.0965, 0.0434, 0.0451)
    mfv_ddbar_tau00300um_M1600.ratio = (1.0369, 0.0413, 0.0430)
    mfv_ddbar_tau01000um_M0300.ratio = (1.2177, 0.1006, 0.1096)
    mfv_ddbar_tau01000um_M0400.ratio = (1.1685, 0.0549, 0.0576)
    mfv_ddbar_tau01000um_M0500.ratio = (1.1115, 0.0363, 0.0375)
    mfv_ddbar_tau01000um_M0600.ratio = (1.1078, 0.0309, 0.0317)
    mfv_ddbar_tau01000um_M0800.ratio = (1.0475, 0.0252, 0.0258)
    mfv_ddbar_tau01000um_M1200.ratio = (1.0534, 0.0242, 0.0247)
    mfv_ddbar_tau01000um_M1600.ratio = (1.0574, 0.0240, 0.0245)
    mfv_ddbar_tau10000um_M0300.ratio = (1.2706, 0.1011, 0.1099)
    mfv_ddbar_tau10000um_M0400.ratio = (1.1683, 0.0490, 0.0512)
    mfv_ddbar_tau10000um_M0500.ratio = (1.2012, 0.0327, 0.0336)
    mfv_ddbar_tau10000um_M0600.ratio = (1.1029, 0.0236, 0.0241)
    mfv_ddbar_tau10000um_M0800.ratio = (1.0713, 0.0196, 0.0200)
    mfv_ddbar_tau10000um_M1200.ratio = (1.0582, 0.0182, 0.0185)
    mfv_ddbar_tau10000um_M1600.ratio = (1.0273, 0.0172, 0.0175)
    mfv_ddbar_tau30000um_M0300.ratio = (1.0867, 0.1454, 0.1680)
    mfv_ddbar_tau30000um_M0400.ratio = (1.0691, 0.0708, 0.0758)
    mfv_ddbar_tau30000um_M0500.ratio = (1.0789, 0.0424, 0.0441)
    mfv_ddbar_tau30000um_M0600.ratio = (1.1481, 0.0332, 0.0342)
    mfv_ddbar_tau30000um_M0800.ratio = (1.0867, 0.0252, 0.0258)
    mfv_ddbar_tau30000um_M1200.ratio = (1.0731, 0.0226, 0.0231)
    mfv_ddbar_tau30000um_M1600.ratio = (1.0762, 0.0214, 0.0218)
    mfv_ddbar_tau00100um_M3000.ratio = (0.9811, 0.1228, 0.1403)
    mfv_ddbar_tau00300um_M3000.ratio = (1.0223, 0.0435, 0.0455)
    mfv_ddbar_tau01000um_M3000.ratio = (1.0027, 0.0231, 0.0237)
    mfv_ddbar_tau10000um_M3000.ratio = (1.0301, 0.0171, 0.0174)
    mfv_ddbar_tau30000um_M3000.ratio = (1.0191, 0.0185, 0.0189)
    mfv_neu_tau00100um_M0300.ratio = (1.1428, 0.4609, 0.7130)
    mfv_neu_tau00300um_M0300.ratio = (1.2790, 0.1863, 0.2162)
    mfv_neu_tau01000um_M0300.ratio = (1.2528, 0.1031, 0.1121)
    mfv_neu_tau10000um_M0300.ratio = (1.2408, 0.0934, 0.1008)
    mfv_neu_tau30000um_M0300.ratio = (0.9570, 0.1773, 0.2176)
    mfv_neu_tau00100um_M0400.ratio = (0.8096, 0.2123, 0.2785)
    mfv_neu_tau00300um_M0400.ratio = (1.4301, 0.1028, 0.1105)
    mfv_neu_tau01000um_M0400.ratio = (1.2121, 0.0525, 0.0548)
    mfv_neu_tau10000um_M0400.ratio = (1.0545, 0.0419, 0.0436)
    mfv_neu_tau30000um_M0400.ratio = (1.1235, 0.0926, 0.1010)
    mfv_neu_tau00100um_M0500.ratio = (0.8714, 0.1767, 0.2214)
    mfv_neu_tau00300um_M0500.ratio = (1.2193, 0.0859, 0.0924)
    mfv_neu_tau01000um_M0500.ratio = (1.0886, 0.0438, 0.0456)
    mfv_neu_tau10000um_M0500.ratio = (1.1079, 0.0364, 0.0376)
    mfv_neu_tau30000um_M0500.ratio = (1.1937, 0.0581, 0.0611)
    mfv_neu_tau00100um_M0600.ratio = (0.9551, 0.1451, 0.1711)
    mfv_neu_tau00300um_M0600.ratio = (1.0874, 0.0504, 0.0528)
    mfv_neu_tau01000um_M0600.ratio = (1.1200, 0.0289, 0.0296)
    mfv_neu_tau10000um_M0600.ratio = (1.1031, 0.0261, 0.0267)
    mfv_neu_tau30000um_M0600.ratio = (1.0675, 0.0344, 0.0355)
    mfv_neu_tau00100um_M0800.ratio = (1.1273, 0.1033, 0.1133)
    mfv_neu_tau00300um_M0800.ratio = (1.1362, 0.0348, 0.0359)
    mfv_neu_tau01000um_M0800.ratio = (1.0705, 0.0183, 0.0187)
    mfv_neu_tau10000um_M0800.ratio = (1.0644, 0.0136, 0.0138)
    mfv_neu_tau30000um_M0800.ratio = (1.0377, 0.0226, 0.0231)
    mfv_neu_tau00100um_M1200.ratio = (1.1406, 0.0849, 0.0915)
    mfv_neu_tau00300um_M1200.ratio = (1.0937, 0.0294, 0.0302)
    mfv_neu_tau01000um_M1200.ratio = (1.0530, 0.0163, 0.0165)
    mfv_neu_tau10000um_M1200.ratio = (1.0288, 0.0120, 0.0122)
    mfv_neu_tau30000um_M1200.ratio = (1.0355, 0.0196, 0.0200)
    mfv_neu_tau00100um_M1600.ratio = (0.9993, 0.0729, 0.0784)
    mfv_neu_tau00300um_M1600.ratio = (1.0195, 0.0267, 0.0274)
    mfv_neu_tau01000um_M1600.ratio = (1.0392, 0.0157, 0.0159)
    mfv_neu_tau10000um_M1600.ratio = (1.0219, 0.0117, 0.0118)
    mfv_neu_tau30000um_M1600.ratio = (1.0145, 0.0182, 0.0185)
    mfv_neu_tau00100um_M3000.ratio = (0.9271, 0.0974, 0.1088)
    mfv_neu_tau00300um_M3000.ratio = (1.0129, 0.0355, 0.0367)
    mfv_neu_tau01000um_M3000.ratio = (1.0075, 0.0208, 0.0213)
    mfv_neu_tau10000um_M3000.ratio = (1.0055, 0.0154, 0.0157)
    mfv_neu_tau30000um_M3000.ratio = (1.0269, 0.0169, 0.0172)
else:
    suppl = eval(gzip.GzipFile('/uscms/home/tucker/public/mfv/scanpacks/scanpack2015supplement_try3.list.hadded.gz').read())

    def getit(s):
        s.z = {}
        for year in 2015, 2016:
            if year == 2015:
                fn = suppl[s.name+'_2015'][0]
            else:
                fn = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV16/%s.root' % s.name
            f = ROOT.TFile.Open(fn)
            t = f.Get('mfvMiniTree/t')
            hr = draw_hist_register(t, True)
            h,n = hr.draw('svdist', 'nvtx>=2', binning='400,0,4', get_n=True, goff=True)
            assert h.GetXaxis().GetBinLowEdge(1) == 0.
            assert h.GetXaxis().GetBinLowEdge(5) == 0.04
            assert h.GetXaxis().GetBinLowEdge(8) == 0.07
            N = norm_from_file(f)
            n = h.Integral(1,10000)
            b1 = h.Integral(1,4)
            b2 = h.Integral(5,7)
            b3 = h.Integral(8,10000)
            #print s.name, N, n, b1, b2, b3
            s.z[year] = (N,n,b1,b2,b3)

        N15, n15 = s.z[2015][:2]
        N16, n16 = s.z[2016][:2]
        s.ratio = [x * N16/N15 for x in clopper_pearson_poisson_means(n15, n16)]
        s.ratio[1] = s.ratio[0] - s.ratio[1]
        s.ratio[2] = s.ratio[2] - s.ratio[0]
        s.ratio = tuple(s.ratio)
        print s.name.ljust(30), '%.4f - %.4f + %.4f' % s.ratio

    for kind, s in samples():
        getit(s)

z = {kind : defaultdict(list) for kind in kinds}
for kind, s in samples():
    z[kind][s.tau].append(s)

def fitit(g, name, c=ROOT.kBlack):
    fcn = ROOT.TF1('fcn_%s' % name, '2. - [0] * TMath::Erf((x - [1])/[2])', 298, 3002)
    fcn.SetParameters(1, 300, 100)
    fcn.SetLineWidth(2)
    fcn.SetLineColor(c)
    res = g.Fit(fcn, 'QRS')
    return fcn, res
    
def drawem(l, ll, name):
    l[0].Draw('AP')
    for g in l[1:]:
        g.Draw('P')
    ps.save(name)

    g = tgraph(ll)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(0.8)
    g.SetTitle('%s;M (GeV);efficiency ratio 2015/2016' % name)
    g.Draw('AP')
    g.GetYaxis().SetRangeUser(0.4, 3)
    fcn, res = fitit(g, name)
    ps.save('all_%s' % name)

colordeltas = [2,1,0,-3,-7]
ggg, gggss = [], []
for kind in kinds:
    gg, ggss = [], []
    pars = defaultdict(list)
    for itau, tau in enumerate((100, 300, 1000, 10000, 30000)):
        ss = z[kind][tau]
        l = [(s.mass, 0, 0) + s.ratio for s in ss]
        g = tgraph(l)
        gg.append(g)
        ggss.extend(l)
        ggg.append(g)
        gggss.extend(l)

        c = (ROOT.kRed if kind == 'ddbar' else ROOT.kBlue) + colordeltas[itau]
        g.SetMarkerColor(c)
        g.SetLineColor(c)
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.8)
        g.Draw('AP')
        g.SetTitle('%s, #tau = %i #mum;M (GeV);efficiency ratio 2015/2016' % (kind, tau))
        g.GetYaxis().SetRangeUser(0.5, 2.2)

        name = '%s_tau%06ium' % (kind, tau)
        fcn, res = fitit(g, name)
        print '@300:', fcn.Eval(300)
    
        for i in 0,1,2:
            pars[i].append((tau, fcn.GetParameter(i), fcn.GetParError(i)))

        l = ROOT.TLine(300, 1, 3000, 1)
        l.SetLineStyle(2)
        l.Draw()

        ps.save(name)

    drawem(gg, ggss, kind)

    for i in 0,1,2:
        g = tgraph(pars[i])
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.8)
        g.Draw('AP')
        g.SetTitle('%s;#tau (#mum);par #%i' % (kind,i))
        ps.save('%s_par%i' % (kind,i))

drawem(ggg, gggss, 'all')

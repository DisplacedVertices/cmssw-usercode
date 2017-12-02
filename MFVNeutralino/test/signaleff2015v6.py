from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Sample import norm_from_file
from JMTucker.Tools.Samples import *
from JMTucker.MFVNeutralino.PerSignal import PerSignal

xxx = [
(mfv_neu_tau00100um_M0300_2015, 0.05 , 0.01),
(mfv_neu_tau00100um_M0300, 0.02 , 0.00),
(mfv_neu_tau00100um_M0400_2015, 0.08 , 0.02),
(mfv_neu_tau00100um_M0400, 0.07 , 0.01),
(mfv_neu_tau00100um_M0800_2015, 0.49 , 0.04),
(mfv_neu_tau00100um_M0800, 0.43 , 0.01),
(mfv_neu_tau00100um_M1200_2015, 0.69 , 0.05),
(mfv_neu_tau00100um_M1200, 0.63 , 0.02),
(mfv_neu_tau00100um_M1600_2015, 0.83 , 0.06),
(mfv_neu_tau00100um_M1600, 0.74 , 0.02),
(mfv_neu_tau00300um_M0300_2015, 0.22 , 0.03),
(mfv_neu_tau00300um_M0300, 0.15 , 0.01),
(mfv_neu_tau00300um_M0400_2015, 0.72 , 0.05),
(mfv_neu_tau00300um_M0400, 0.55 , 0.01),
(mfv_neu_tau00300um_M0800_2015, 4.36 , 0.13),
(mfv_neu_tau00300um_M0800, 3.75 , 0.04),
(mfv_neu_tau00300um_M1200_2015, 5.42 , 0.15),
(mfv_neu_tau00300um_M1200, 5.03 , 0.04),
(mfv_neu_tau00300um_M1600_2015, 6.14 , 0.16),
(mfv_neu_tau00300um_M1600, 5.64 , 0.05),
(mfv_neu_tau01000um_M0300_2015, 0.61 , 0.05),
(mfv_neu_tau01000um_M0300, 0.47 , 0.01),
(mfv_neu_tau01000um_M0400_2015, 2.10 , 0.09),
(mfv_neu_tau01000um_M0400, 1.77 , 0.03),
(mfv_neu_tau01000um_M0800_2015, 13.55 , 0.23),
(mfv_neu_tau01000um_M0800, 12.65 , 0.07),
(mfv_neu_tau01000um_M1200_2015, 16.40 , 0.26),
(mfv_neu_tau01000um_M1200, 15.82 , 0.08),
(mfv_neu_tau01000um_M1600_2015, 17.48 , 0.27),
(mfv_neu_tau01000um_M1600, 16.75 , 0.08),
(mfv_neu_tau10000um_M0300_2015, 0.76 , 0.06),
(mfv_neu_tau10000um_M0300, 0.57 , 0.01),
(mfv_neu_tau10000um_M0400_2015, 2.77 , 0.11),
(mfv_neu_tau10000um_M0400, 2.38 , 0.03),
(mfv_neu_tau10000um_M0800_2015, 23.87 , 0.31),
(mfv_neu_tau10000um_M0800, 22.90 , 0.09),
(mfv_neu_tau10000um_M1200_2015, 28.64 , 0.34),
(mfv_neu_tau10000um_M1200, 28.13 , 0.10),
(mfv_neu_tau10000um_M1600_2015, 30.29 , 0.35),
(mfv_neu_tau10000um_M1600, 29.69 , 0.11),
]

def getit(s):
    fn = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV16/%s.root' % s.name
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree/t')
    hr = draw_hist_register(t, True)
    h,n = hr.draw('svdist', 'nvtx>=2', binning='400,0,4', get_n=True, goff=True)
    assert h.GetXaxis().GetBinLowEdge(1) == 0.
    assert h.GetXaxis().GetBinLowEdge(5) == 0.04
    assert h.GetXaxis().GetBinLowEdge(8) == 0.07
    norm = norm_from_file(f)
    b1 = h.Integral(1,4)
    b2 = h.Integral(5,7)
    b3 = h.Integral(8,1000)
    #print s.name, norm, b1, b2, b3
    def eff(a,b):
        e,l,u = clopper_pearson(a,b)
        return e, (u-l)/2
    s.ys = [
        None,
        eff(b1+b2+b3,norm),
        eff(b1,norm),
        eff(b2,norm),
        eff(b3,norm),
        ]
    print s.name, s.ys

s_2015, s_2016 = [], []

for s, y, ye in xxx:
    (s_2015 if s.name.endswith('_2015') else s_2016).append(s)
    getit(s)
    s.ys[0] = (y / 35.916, ye / 35.916)

for ss in s_2015, s_2016:
    ss.sort(key=lambda s: s.name)

set_style()
ps = plot_saver(plot_dir('sigeff_2015v6'), size=(600,600), log=False)

for i,t in enumerate(['typedin', 'overall', 'bin1', 'bin2', 'bin3']):
    for s in s_2015 + s_2016:
        s.y, s.ye  = s.ys[i]

    per = PerSignal('efficiency_%s' % t, y_range=(0.,1.05))
    per.add(s_2015, title='2015')
    per.add(s_2016, title='2016', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_%s' % t)

    for s15, s16 in zip(s_2015, s_2016):
        a,b = s16.y, s15.y
        ae,be = s16.ye, s15.ye
        if a == 0.:
            a = 1e-12
        if b == 0.:
            b = 1e-12
        print s15.name, s16.name, a, ae, b, be
        s16.y = a/b
        s16.ye = a/b * ((ae/a)**2 + (be/b)**2)**0.5

    per = PerSignal('ratio_%s' % t, y_range=(0.,2.05))
    per.add(s_2016, title='2016/2015')
    per.draw(canvas=ps.c)
    ps.save('ratio_%s' % t)

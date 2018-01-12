#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_ratio_miniaod'), size=(600,600), log=False)

samples = [s for s in Samples.mfv_signal_samples if s.has_dataset('ntuplev16m')]

def getit(fn):
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree/t')
    hr = draw_hist_register(t, True)
    h,n = hr.draw('weight', 'nvtx>=2', binning='1,0,1', get_n=True, goff=True)
    #i = get_integral(h)[0]
    #c = i/n
    d = Samples.norm_from_file(f)
    e,l,u = clopper_pearson(n, d)
    ee = (u-l)/2
    return e,ee,n,d

for sample in samples:
    sample.e1 = getit('/uscms_data/d2/tucker/crab_dirs/MiniTreeV16/%s.root'  % sample.name)
    sample.e2 = getit('/uscms_data/d2/tucker/crab_dirs/MiniTreeV16m/%s.root' % sample.name)
    print '%26s: efficiency = %.3f +- %.3f -> %.3f +- %.3f' % ((sample.name,) + sample.e1[:2] + sample.e2[:2])
    print '%26s     %r %r' % ('', sample.e1, sample.e2)

per = PerSignal('efficiency', y_range=(0.,1.05))
for s in samples:
    s.y,s.ye = s.e1[:2]
per.add(samples, title='aod', color=ROOT.kRed)
PerSignal.clear_samples(samples)
for s in samples:
    s.y,s.ye = s.e2[:2]
per.add(samples, title='miniaod', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('eff')

per = PerSignal('ratio miniaod/aod', y_range=(0.6,1.15))
PerSignal.clear_samples(samples)
for s in samples:
    s.y, s.yl, s.yh = clopper_pearson_poisson_means(s.e2[2], s.e1[2])
per.add(samples, color=ROOT.kMagenta)
per.draw(canvas=ps.c)
ps.save('eff_ratio')

#!/usr/bin/env python

from os.path import join, isfile
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

titles = 'v23', 'v22'
paths = ('/uscms_data/d2/tucker/crab_dirs/MiniTreeV23m',
         '/uscms_data/d2/tucker/crab_dirs/MiniTreeV22m')

set_style()
ps = plot_saver(plot_dir('sigeff_ratio_%sV%s' % titles), size=(600,600), log=False)

samples = Samples.all_signal_samples_2017
def available(samples):
    return [s for s in samples if isfile(join(paths[0], '%s.root' % s.name)) and isfile(join(paths[1], '%s.root' % s.name))]
samples = available(samples)

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
    sample.e1 = getit(join(paths[0], '%s.root' % sample.name))
    sample.e2 = getit(join(paths[1], '%s.root' % sample.name))
    print '%26s: efficiency = %.3f +- %.3f -> %.3f +- %.3f' % ((sample.name,) + sample.e1[:2] + sample.e2[:2])
    print '%26s     %r %r' % ('', sample.e1, sample.e2)

per = PerSignal('efficiency', y_range=(0.,1.05))
for s in samples:
    s.y,s.ye = s.e1[:2]
per.add(available(Samples.mfv_signal_samples_2017),       title=titles[0] + ' multijet', color=ROOT.kRed)
per.add(available(Samples.mfv_stopdbardbar_samples_2017), title=titles[0] + ' dijet',    color=ROOT.kBlue)
PerSignal.clear_samples(samples)
for s in samples:
    s.y,s.ye = s.e2[:2]
per.add(available(Samples.mfv_signal_samples_2017),       title=titles[1] + ' multijet', color=ROOT.kRed)
per.add(available(Samples.mfv_stopdbardbar_samples_2017), title=titles[1] + ' dijet',    color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('eff')

per = PerSignal('ratio %s/%s' % titles, y_range=(0.6,1.15))
PerSignal.clear_samples(samples)
for s in samples:
    s.y, s.yl, s.yh = clopper_pearson_poisson_means(s.e1[2], s.e2[2])
per.add(available(Samples.mfv_signal_samples_2017),       title='multijet', color=ROOT.kPink)
per.add(available(Samples.mfv_stopdbardbar_samples_2017), title='dijet',    color=ROOT.kCyan)
per.draw(canvas=ps.c)
ps.save('eff_ratio')

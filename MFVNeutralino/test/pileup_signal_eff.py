#!/usr/bin/env python

from os.path import join, isfile
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

titles = 'default', 'mbxsecm5pc', 'mbxsecp5pc'
paths = ('/uscms_data/d2/tucker/crab_dirs/MiniTreeV23m',
         '/uscms_data/d3/dquach/crab3dirs/MiniTreeV23m_mbxsecm5pc',
         '/uscms_data/d3/dquach/crab3dirs/MiniTreeV23m_mbxsecp5pc')

set_style()
ps = plot_saver(plot_dir('sigeff_pileup_ratio_avg'), size=(600,600), log=False)

samples = Samples.all_signal_samples_2017
def available(samples):
    return [s for s in samples if isfile(join(paths[0], '%s.root' % s.name)) and isfile(join(paths[1], '%s.root' % s.name))]
samples = available(samples)

def getit(fn):
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree/t')
    hr = draw_hist_register(t, True)
    h,n = hr.draw('weight', 'nvtx>=2', binning='1,0,1', get_n=True, goff=True)
    i = get_integral(h)[0]
    d = Samples.norm_from_file(f)
    e,l,u = clopper_pearson(i, d)
    ee = (u-l)/2
    return e,ee,i,d

for sample in samples:
    sample.e1 = getit(join(paths[0], '%s.root' % sample.name))
    sample.e2 = getit(join(paths[1], '%s.root' % sample.name))
    sample.e3 = getit(join(paths[2], '%s.root' % sample.name))

per = PerSignal('ratio avg', y_range=(0.,0.1))
PerSignal.clear_samples(samples)
for s in samples:
    i1, i2, i3 = s.e1[2], s.e2[2], s.e3[2]
    d1, d2, d3 = s.e1[3], s.e2[3], s.e3[3]
    y1, yl1, yh1 = [x*d1/d2 for x in clopper_pearson_poisson_means(i2, i1)]
    y2, yl2, yh2 = [x*d1/d3 for x in clopper_pearson_poisson_means(i3, i1)]
    s.y = (abs(y1-1) + abs(y2-1)) / 2.
per.add(available(Samples.mfv_signal_samples_2017),       title='multijet', color=ROOT.kRed)
per.add(available(Samples.mfv_stopdbardbar_samples_2017), title='dijet',    color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('eff_ratio')

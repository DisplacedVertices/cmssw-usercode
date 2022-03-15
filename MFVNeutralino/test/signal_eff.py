#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'V28Bm_noVeto'
ps = plot_saver(plot_dir('sigeff_%s' % version), size=(600,600), pdf=True, log=False)


stopbbarbbar = Samples.mfv_signal_samples_2017
stopdbardbar = Samples.mfv_stopdbardbar_samples_2017

for sample in stopbbarbbar + stopdbardbar:
    fn = os.path.join('/uscms_data/d3/shogan/crab_dirs/MiniTreeV28Bm/' + sample.name + '.root')
    #fn = os.path.join('/uscms_data/d3/shogan/crab_dirs/MiniTreeV28BmwVeto/' + sample.name + '.root')
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('mfvMiniTree/t')
    hr = draw_hist_register(t, True)
    cut = 'nvtx>=2' # && svdist > 0.04'
    h = hr.draw('weight', cut, binning='1,0,1', goff=True)
    num, _ = get_integral(h)
    #den = Samples.norm_from_file(f)
    den = f.Get('mfvWeight').Get('h_npu').Integral()
    print(den)
    sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('efficiency', y_range=(0.,1.05))
per.add(stopbbarbbar, title='Multijet')
per.add(stopdbardbar, title='Dijet (d)', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('sigeff')

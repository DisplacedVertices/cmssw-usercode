#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('thetaoutliers_v15'), size=(900,600), log=False)

root_file_dir = '.'
paths = [
#    ('h_5000', ROOT.kBlack),
    ('h_8000', ROOT.kBlue),
    ('h_9500', ROOT.kRed),
    ('h_9900', ROOT.kGreen+2),
#    ('h_9990', ROOT.kBlue),
#    ('h_9999', ROOT.kOrange+2),
#    ('h_10000',ROOT.kMagenta),
    ]

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples

#for kind, samples in ('multijet', multijet), ('dijet', dijet):
per = PerSignal('cut', y_range=(0, 500))
for path,color in paths:
    pathname = path.replace('h_', '')
    #pathname = '%s.%s%%' % (pathname[:-2], pathname[-2:])
    pathname = '%s%%' % (pathname[:-2])
    for sample in multijet + dijet:
        if not hasattr(sample, 'f'):
            sample.f = ROOT.TFile(os.path.join(root_file_dir, sample.name + '.root'))
        h = sample.f.Get(path)
        assert h.GetEntries() == 1
        sample.y = h.GetMean()
        print sample.name, path, sample.y
    title = 'keep %s' % pathname
    per.add(multijet, color=color, title=title)
    per.add(dijet,    color=color, style=2, in_legend=False)
per.draw(canvas=ps.c)
ps.save('duh')

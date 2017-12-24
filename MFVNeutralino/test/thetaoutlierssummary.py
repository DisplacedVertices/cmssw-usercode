#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

cutplays = True

plot_path = 'thetaoutliers_v15'
root_file_dir = '.'
if cutplays:
    plot_path += '_cutplays'
    root_file_dir = '/uscms_data/d2/tucker/crab_dirs/CutPlayV15'

set_style()
ps = plot_saver(plot_dir(plot_path), size=(900,600), log=False)

colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue]
if cutplays:
    xs = [50, 75, 100]
    ymax = 1.05
else:
    xs = ['h_8000', 'h_9500', 'h_9900']
    ymax = 500

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples

per = PerSignal('cut', y_range=(0, ymax))
for x, color in zip(xs, colors):
    for sample in multijet + dijet:
        fn = os.path.join(root_file_dir, sample.name + '.root')
        if not os.path.exists(fn):
            continue
        if not hasattr(sample, 'f'):
            sample.f = ROOT.TFile(fn)

        if cutplays:
            h = sample.f.Get('SimpleTriggerEfficiency/triggers_pass_num')
            ibin = x + 2
            num = h.GetBinContent(ibin)
            den = h.GetBinContent(1)
            sample.y, sample.yl, sample.yh = clopper_pearson(num, den)
        else:
            h = sample.f.Get(x)
            assert h.GetEntries() == 1
            sample.y = h.GetMean()
            print sample.name, x, sample.y

    if cutplays:
        title = 'cut at %s' % x
    else:
        title = 'keep %s%%' % (x.replace('h_', '')[:-2])
    per.add(multijet, color=color, title=title)
    per.add(dijet,    color=color, style=2, in_legend=False)
per.draw(canvas=ps.c)
ps.save('duh')



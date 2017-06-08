#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_v15'), size=(600,600), log=False)

root_file_dir = '/uscms_data/d2/tucker/crab_dirs/HistosV15'
num_path = 'mfvEventHistosFullSel/h_bsx'

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples

for sample in multijet + dijet:
    fn = os.path.join(root_file_dir, sample.name + '.root')
    if not os.path.exists(fn):
        continue
    f = ROOT.TFile(fn)
    hnum = f.Get(num_path)
    hden = f.Get('mfvWeight/h_sums')
    num = hnum.Integral(0, hnum.GetNbinsX() + 2)
    den = hden.GetBinContent(1)
    sample.y, sample.yl, sample.yh = clopper_pearson(num, den)
    
per = PerSignal('efficiency', y_range=(0.,1.05))
per.add(multijet, title='#tilde{N} #rightarrow tbs')
per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('sigeff')

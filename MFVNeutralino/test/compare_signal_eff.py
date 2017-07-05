#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

mode = 'vary_pileup'

set_style()
ps = plot_saver('plots/sigeff/v15/compare_sigeff_%s' % mode, size=(700,700), log=False, root=False)

if mode == 'vary_pileup':
    root_file_dirs = ['/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_0', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_1', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_2']
    ls = ['2016', '2016mbxsecm5pc', '2016mbxsecp5pc']

num_path = 'mfvEventHistosFullSel/h_bsx'

nevs = []
for i,root_file_dir in enumerate(root_file_dirs):
    print ls[i]

    multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
    dijet = Samples.mfv_ddbar_samples

    nev = []
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
        print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)
        nev.append(num)
    
    per = PerSignal('efficiency', y_range=(0.,1.05))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_%s' % ls[i])
    nevs.append(nev)

for i,nev in enumerate(nevs):
    print ls[i]

    multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
    dijet = Samples.mfv_ddbar_samples

    for j,sample in enumerate(multijet + dijet):
        sample.y, sample.yl, sample.yh = clopper_pearson_poisson_means(nev[j], nevs[0][j])
        print '%26s: ratio = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

    per = PerSignal('ratio of efficiencies', y_range=(0.9,1.1))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_ratio_%s' % ls[i])

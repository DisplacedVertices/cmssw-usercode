#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'ULV30LepMum_SingleLep'
ps = plot_saver(plot_dir('sigeff_wrt_presel_beampipe_origin_%s_correct_release_2017' % version), size=(600,600), pdf=True, log=False)

WplusH = Samples.WplusHToSSTodddd_samples_2017
WminusH = Samples.WminusHToSSTodddd_samples_2017
ZH = Samples.ZHToSSTodddd_samples_2017

for sample in WplusH + WminusH + ZH:
    fn = os.path.join('/uscms/home/pkotamni/nobackup/crabdirs/Histos%s' % version, sample.name + '.root')
    print(fn)
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    t = f.Get('SimpleTriggerResults/t')
    hr = draw_hist_register(t, True)
    cut_den = 'pEventPreSel'
    h_den = hr.draw('weight', cut_den, binning='1,0,1', goff=True)
    cut_num = 'pFullSel'
    h_num = hr.draw('weight', cut_num, binning='1,0,1', goff=True)

    den, _ = get_integral(h_den)
    num, _ = get_integral(h_num)
    sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    print '%26s: efficiency = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('efficiency', y_range=(0.,1.05)) 
per.add(WplusH, title='Wplus(#rightarrow #mu #nu) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}', color=ROOT.kAzure+8)
per.add(WminusH, title='Wminus(#rightarrow #mu #nu) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}', color=ROOT.kRed-9)
per.add(ZH, title='Z(#rightarrow #mu bar{#mu}) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}', color=ROOT.kGreen-3)
per.draw(canvas=ps.c)
ps.save('sigeff')

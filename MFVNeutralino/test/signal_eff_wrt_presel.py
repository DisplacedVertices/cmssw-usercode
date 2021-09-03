#!/usr/bin/env python

import os
from DVCode.Tools.ROOTTools import *
from DVCode.Tools import Samples
from DVCode.MFVNeutralino.PerSignal import PerSignal

set_style()
version = 'V27m'
ps = plot_saver(plot_dir('sigeff_wrt_presel_beampipe_origin_%s_correct_release_2018' % version), size=(600,600), pdf=True, log=False)

multijet = Samples.mfv_signal_samples_2018
dijet = Samples.mfv_stopdbardbar_samples_2018

for sample in multijet + dijet:
    fn = os.path.join('/uscms/home/joeyr/crabdirs/Histos_within_fiducial_fixed_beampipe_wrt_origin_correct_release%s' % version, sample.name + '.root')
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
per.add(multijet, title='#tilde{N} #rightarrow tbs')
per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('sigeff')

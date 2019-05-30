#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('hem1516'), size=(600,600), pdf=True, log=False)

multijet = Samples.mfv_signal_samples_2017
dijet = Samples.mfv_stopdbardbar_samples_2017

for svdist in 0., 0.04, 0.07:
    PerSignal.clear_samples(multijet + dijet)
    for sample in multijet + dijet:
        fn = os.path.join('/uscms_data/d2/tucker/crab_dirs/MiniTreeV24m', sample.name + '.root')
        if not os.path.exists(fn):
            print 'no', sample.name
            continue

        f = ROOT.TFile(fn)
        t = f.Get('mfvMiniTree/t')
        hr = draw_hist_register(t, True)
        def n(cut):
            return get_integral(hr.draw('weight', cut, binning='1,0,1', goff=True))[0]

        t.SetAlias('jet_hem1516', 'jet_eta<-1.3&&jet_phi<-0.87&&jet_phi>-1.57')
        t.SetAlias('njets_hem1516', 'Sum$(!jet_hem1516)')
        t.SetAlias('jetht_hem1516', 'Sum$(jet_pt*(jet_pt>40&&!jet_hem1516))')

        den = n('nvtx>=2 && svdist > %f' % svdist)
        num = n('nvtx>=2 && svdist > %f && njets_hem1516 >= 4 && jetht_hem1516 >= 1200' % svdist)
        sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # JMTBAD same events
        print '%26s: num = %.1f den = %.1f ratio = %.3f (%.3f, %.3f)' % (sample.name, num, den, sample.y, sample.yl, sample.yh)

    per = PerSignal('hem1516/nominal', y_range=(0.8,1.01), decay_paves_at_top=False)
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_svdist%.2f' % svdist)

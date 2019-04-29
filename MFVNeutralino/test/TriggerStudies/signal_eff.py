#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_trig'), size=(600,600), log=False)

root_file_dir = '/uscms_data/d2/tucker/crab_dirs/TrigFiltCheckV1'
trigs = ['Trigger']
nice = ['PFHT1050']
colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kBlack]

def sample_ok(s):
    return True #s.mass not in (500,3000)
multijet = [s for s in Samples.mfv_signal_samples_2017 if sample_ok(s)]
dijet = [s for s in Samples.mfv_stopdbardbar_samples_2017 if sample_ok(s)]

def getit(f, n):
    hnum = f.Get('SimpleTriggerEfficiency/triggers_pass_num')
    hden = f.Get('SimpleTriggerEfficiency/triggers_pass_den')
    for ibin in xrange(1, hnum.GetNbinsX()+1):
        if hnum.GetXaxis().GetBinLabel(ibin) == n:
            break
    return clopper_pearson(hnum.GetBinContent(ibin), hden.GetBinContent(ibin))

def mvpave(pave, x1, y1, x2, y2):
    pave.SetX1(x1)
    pave.SetX2(x2)
    pave.SetY1(y1)
    pave.SetY2(y2)

for sample in multijet + dijet:
    fn = os.path.join(root_file_dir, sample.name + '.root')
    if not os.path.exists(fn):
        continue
    f = ROOT.TFile(fn)
    sample.ys = {n: getit(f,'p'+n) for n in trigs}

if len(trigs) > 1:
    for kind, samples in ('multijet', multijet), ('dijet', dijet):
        per = PerSignal('efficiency', y_range=(0.,1.15))
        for itrig, trig in enumerate(trigs):
            for sample in samples:
                sample.y, sample.yl, sample.yh = sample.ys[trig]
            per.add(samples, title=nice[itrig], color=colors[itrig])
        per.draw(canvas=ps.c)

    mvpave(per.decay_paves[0], 0.703, 1.018, 6.227, 1.098)
    mvpave(per.decay_paves[1], 6.729, 1.021, 14.073, 1.101)
    mvpave(per.decay_paves[2], 14.45, 1.033, 21.794, 1.093) 

    ps.save(kind)
else:
    for sample in multijet + dijet:
        sample.y, sample.yl, sample.yh = sample.ys[trigs[0]]
    per = PerSignal('efficiency', y_range=(0.,1.05))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('trigeff')


#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sig_nevts'), size=(600,600), log=False, pdf=True)

def sample_ok(s):
    return True #s.mass not in (500,3000)
multijet = [s for s in Samples.mfv_signal_samples_2016 if sample_ok(s)]
dijet_d = [s for s in Samples.mfv_stopdbardbar_samples_2016 if sample_ok(s)]
dijet_b = [s for s in Samples.mfv_stopbbarbbar_samples_2016 if sample_ok(s)]

def mvpave(pave, x1, y1, x2, y2):
    pave.SetX1(x1)
    pave.SetX2(x2)
    pave.SetY1(y1)
    pave.SetY2(y2)

for sample in multijet + dijet_d + dijet_b:
    sample.y  = sample.nevents_orig
    sample.yl = sample.nevents_orig - 10
    sample.yh = sample.nevents_orig + 10

per = PerSignal('generated nevents', y_range=(0.,210000))
per.add(multijet, title='#tilde{N} #rightarrow tbs')
per.add(dijet_d, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kGreen+2)
per.add(dijet_b, title='#tilde{t} #rightarrow #bar{b}#bar{b}', color=ROOT.kBlue)
per.draw(canvas=ps.c)
mvpave(per.decay_paves[0], 30.703, 180000, 36.2, 200000)
mvpave(per.decay_paves[1], 30.703, 160000, 36.2, 180000)
mvpave(per.decay_paves[2], 30.703, 140000, 36.2, 160000)
#mvpave(per.decay_paves[3], 0.703, 0.038, 8, 0.098)
ps.save('sig_nevts_2016')

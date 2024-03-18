#!/usr/bin/env python

import os
import numpy as np
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_trig'), size=(600,600), log=False, pdf=True)

# where "new" triggers = bjet and displaced dijet triggers
study_new_triggers = True

if study_new_triggers :
    num_file_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_TrigStudy_July13_DispTkVetoOnly_On'
    trigs = ['Logical OR']
    nice = ['Logical OR']
    colors = [ROOT.kOrange+2]

def sample_ok(s):
    return True #s.mass not in (500,3000)
multijet = [s for s in Samples.mfv_signal_samples_temp_2017 if sample_ok(s)]
dijet_d  = [s for s in Samples.mfv_stopdbardbar_samples_temp_2017 if sample_ok(s)]
dijet_b  = [s for s in Samples.mfv_stopbbarbbar_samples_temp_2017 if sample_ok(s)]
higgs    = [s for s in Samples.HToSSTodddd_samples_2017 if sample_ok(s)]

def getit(fnum):
    hnum = fnum.Get('mfvEventHistosBjetAgnost/h_npu')
    nnum = hnum.Integral()
    return nnum

def mvpave(pave, x1, y1, x2, y2):
    pave.SetX1(x1)
    pave.SetX2(x2)
    pave.SetY1(y1)
    pave.SetY2(y2)

for sample in multijet + dijet_d + dijet_b + higgs:
    fnnum = os.path.join(num_file_dir, sample.name + '.root')
    if not os.path.exists(fnnum):
        continue
    fnum = ROOT.TFile(fnnum)
    #sample.ys = {n: getit(fnum, fden) for n in trigs}
    sample.y = getit(fnum)
    sample.yl = sample.y
    sample.yh = sample.y 

per = PerSignal('yield', y_range=(0.,15000.0))
per.add(multijet, title='#tilde{N} #rightarrow tbs')
per.add(dijet_d, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kGreen+2)
per.add(dijet_b, title='#tilde{t} #rightarrow #bar{b}#bar{b}', color=ROOT.kBlue)
per.add(higgs, title='H #rightarrow SS #rightarrow 4d', color=ROOT.kBlack)
per.draw(canvas=ps.c)
mvpave(per.decay_paves[0], 0.703, 0.218, 6, 0.278)
mvpave(per.decay_paves[1], 0.703, 0.158, 6, 0.218)
mvpave(per.decay_paves[2], 0.703, 0.098, 6, 0.158)
mvpave(per.decay_paves[3], 0.703, 0.038, 8, 0.098)
ps.save('trigyield')

#for sample in higgs:
#    fnnum = os.path.join(num_file_dir, sample.name + '.root')
#    fnden = os.path.join(den_file_dir, sample.name + '.root')
#    if not os.path.exists(fnnum) or not os.path.exists(fnden):
#        continue
#    fnum = ROOT.TFile(fnnum)
#    fden = ROOT.TFile(fnden)
#    #sample.ys = {n: getit(fnum, fden) for n in trigs}
#    sample.y, sample.yl, sample.yh = getit(fnum, fden)
#    print('{}   eff: {} ({}, {})'.format(sample.name, round(sample.y, 3), round(sample.y-sample.yl, 3), round(sample.yh-sample.y, 3)))

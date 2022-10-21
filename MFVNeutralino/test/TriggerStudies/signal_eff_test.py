#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

set_style()
ps = plot_saver(plot_dir('sigeff_trig'), size=(600,600), log=False)

# where "new" triggers = bjet and displaced stopdbardbar triggers
study_new_triggers = True

if study_new_triggers :
    root_file_dir = '/uscms_data/d3/shogan/crab_dirs/TrigFiltCheckV1'
    trigs = ['Trigger','TriggerBjets','TriggerDispDijet','TriggerOR']
    nice = ['HT1050','Bjet','DisplacedDijet','Logical OR']
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+3]
else :
    root_file_dir = '/uscms_data/d2/tucker/crab_dirs/TrigFiltCheckV1'
    trigs = ['Trigger']
    nice = ['PFHT1050']
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kBlack]

def sample_ok(s):
    return True #s.mass not in (500,3000)
stopbbarbbar = [s for s in Samples.mfv_stopbbarbbar_samples_2017 if sample_ok(s)]
#stopbbarbbar = [s for s in Samples.ZH_HToSSTodddd_ZToll_samples_2017 if sample_ok(s)]
#stopdbardbar = [s for s in Samples.ZH_HToSSTodddd_ZToll_samples_2017 if sample_ok(s)]
stopdbardbar = [s for s in Samples.mfv_stopdbardbar_samples_2017 if sample_ok(s)]

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

for sample in stopbbarbbar + stopdbardbar:
    fn = os.path.join(root_file_dir, sample.name + '.root')
    if not os.path.exists(fn):
        continue
    f = ROOT.TFile(fn)
    sample.ys = {n: getit(f,'p'+n) for n in trigs}

if len(trigs) > 1:
    for kind, samples in ('stopbbarbbar', stopbbarbbar), ('stopdbardbar', stopdbardbar):
        per = PerSignal('efficiency', y_range=(0.,1.05))
        for itrig, trig in enumerate(trigs):
            for sample in samples:
                sample.y, sample.yl, sample.yh = sample.ys[trig]
                if sample.name.startswith('ZH'):
                    sample.y  *= (1.0/0.043478)
                    sample.yl *= (1.0/0.043478)
                    sample.yh *= (1.0/0.043478)
            per.add(samples, title=nice[itrig], color=colors[itrig])
        per.draw(canvas=ps.c)

        if study_new_triggers :
            mvpave(per.decay_paves[0], 1.00, 0.84, 2.7, 0.94)
            mvpave(per.decay_paves[1], 3.0, 0.84, 3.9, 0.94)
            mvpave(per.decay_paves[2], 4.3,  0.84, 6.15, 0.94) 
            mvpave(per.decay_paves[3], 6.4, 0.84, 8.1, 0.94) 
            #mvpave(per.decay_paves[0], 0.803,  0.040, 2.200, 0.044)
            #mvpave(per.decay_paves[1], 2.650,  0.040, 3.250,  0.044)
            #mvpave(per.decay_paves[2], 3.800,  0.040, 6.200,  0.044) 
            #mvpave(per.decay_paves[3], 6.300,  0.040, 8.200, 0.044) 
        else :
            mvpave(per.decay_paves[0], 0.703, 1.018, 6.227, 1.098)
            mvpave(per.decay_paves[1], 6.729, 1.021, 14.073, 1.101)
            mvpave(per.decay_paves[2], 14.45, 1.033, 21.794, 1.093) 

        tlatex = ROOT.TLatex()
        tlatex.SetTextSize(0.04)
        if kind == 'stopbbarbbar' :
            tlatex.DrawLatex(0.825, .96, 'ZH, H#rightarrowSS#rightarrow4d,Z#rightarrowll')
        elif kind == 'stopdbardbar' :
            tlatex.DrawLatex(0.725, 1.05, '#tilde{t} #rightarrow #bar{d}#bar{d}')

        ps.save(kind)
else:
    for sample in stopbbarbbar + stopdbardbar:
        sample.y, sample.yl, sample.yh = sample.ys[trigs[0]]
    per = PerSignal('efficiency', y_range=(0.,1.05))
    per.add(stopbbarbbar, title='#tilde{t} #rightarrow #bar{b}#bar{b}', color=ROOT.kBlue)
    per.add(stopdbardbar, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    mvpave(per.decay_paves[0], 0.703, 0.098, 6, 0.158)
    mvpave(per.decay_paves[1], 0.703, 0.038, 6, 0.098)
    ps.save('trigeff')


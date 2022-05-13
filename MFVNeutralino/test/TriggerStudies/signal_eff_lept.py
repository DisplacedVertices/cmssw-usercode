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
    root_file_dir = '/uscms_data/d3/shogan/crab_dirs/TrigFiltCheckV1_lept'
    #trigs = ['Trigger','TriggerBjets','TriggerDispDijet','TriggerOR']
    trigs = ['Trigger', 'TriggerMonolept', 'TriggerDilept', 'TriggerDispDilept']
    nice = ['HT1050','Monolept','Dilept','Disp. Dilept']
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kOrange+3]
else :
    root_file_dir = '/uscms_data/d2/tucker/crab_dirs/TrigFiltCheckV1'
    trigs = ['Trigger']
    nice = ['PFHT1050']
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen+2, ROOT.kBlack]

def sample_ok(s):
    return True #s.mass not in (500,3000)
stopbbarbbar = [s for s in Samples.ZH_HToSSTodddd_ZToll_samples_2017 if sample_ok(s)]
#stopdbardbar = [s for s in Samples.ZH_HToSSTodddd_ZToll_samples_2017 if sample_ok(s)]
stopdbardbar = [s for s in Samples.WplusH_HToSSTodddd_WToLNu_samples_2017 if sample_ok(s)]

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
                if "1000mm" in sample.name: continue
                sample.y, sample.yl, sample.yh = sample.ys[trig]
                print trig, sample.y
                if sample.name.startswith('ZH'):
                    sample.y  *= (1.0/0.043478)
                    sample.yl *= (1.0/0.043478)
                    sample.yh *= (1.0/0.043478)
                if sample.name.startswith('W'):
                    sample.y  *= (1.0/0.03225)
                    sample.yl *= (1.0/0.03225)
                    sample.yh *= (1.0/0.03225)
            per.add(samples, title=nice[itrig], color=colors[itrig])
        per.draw(canvas=ps.c)

        if study_new_triggers :
            mvpave(per.decay_paves[0], 1.00, 0.84, 2.7, 0.94)
            mvpave(per.decay_paves[1], 2.8, 0.84, 4.5, 0.94)
            mvpave(per.decay_paves[2], 4.75,  0.84, 6.15, 0.94) 
            mvpave(per.decay_paves[3], 6.4, 0.84, 8.1, 0.94) 
        else :
            mvpave(per.decay_paves[0], 0.703, 1.018, 6.227, 1.098)
            mvpave(per.decay_paves[1], 6.729, 1.021, 14.073, 1.101)
            mvpave(per.decay_paves[2], 14.45, 1.033, 21.794, 1.093) 

        tlatex = ROOT.TLatex()
        tlatex.SetTextSize(0.04)
        if kind == 'stopbbarbbar' :
            tlatex.DrawLatex(1.03, 0.96, 'ZH, H#rightarrowSS#rightarrow4d,Z#rightarrowll')
        elif kind == 'stopdbardbar' :
            tlatex.DrawLatex(1.03, 0.96, 'W^{+}H, H#rightarrowSS#rightarrow4d, W^{+}#rightarrowl#nu')

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


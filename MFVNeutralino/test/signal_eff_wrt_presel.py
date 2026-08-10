#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

lep = 'lep' in sys.argv
bjet = 'bjet' in sys.argv
year = '2017' if len(sys.argv) < 3 else sys.argv[1]
trigname = 'NA' if len(sys.argv) < 4 else sys.argv[2] 
signame = 'rpv' if len(sys.argv) < 5 else sys.argv[3] 
print("trig channel: %s" % trigname)
print("signal : %s" % signame)

rpv = 'rpv' in sys.argv
ggh = 'ggh' in sys.argv
vh = 'vh' in sys.argv

set_style()
if bjet :
    version = '_LepIPCut_FixHT2016_OnnormdzULV30BvetoLHTm_noef'
if lep :
    version = '_LepIPCut_OnnormdzULV30Lepm_noef'
ps = plot_saver(plot_dir('sigpreseleff_%s_%s_April7_25' % (version, year)), size=(600,600), pdf=True, log=False)

WplusH = Samples.WplusHToSSTodddd_samples_2017
WminusH = Samples.WminusHToSSTodddd_samples_2017
ZH = Samples.ZHToSSTodddd_samples_2017

multijet = Samples.mfv_signal_samples_2017
dijet_d  = Samples.mfv_stopdbardbar_samples_2017
dijet_b  = Samples.mfv_stopbbarbbar_samples_2017
higgs    = Samples.ggHToSSTodddd_samples_2017

if year == '20161' :
    WplusH = Samples.WplusHToSSTodddd_samples_20161
    WminusH = Samples.WminusHToSSTodddd_samples_20161
    ZH = Samples.ZHToSSTodddd_samples_20161

    multijet = Samples.mfv_signal_samples_20161
    dijet_d  = Samples.mfv_stopdbardbar_samples_20161
    dijet_b  = Samples.mfv_stopbbarbbar_samples_20161
    higgs    = Samples.ggHToSSTodddd_samples_20161
elif year == '20162' :
    WplusH = Samples.WplusHToSSTodddd_samples_20162
    WminusH = Samples.WminusHToSSTodddd_samples_20162
    ZH = Samples.ZHToSSTodddd_samples_20162

    multijet = Samples.mfv_signal_samples_20162
    dijet_d  = Samples.mfv_stopdbardbar_samples_20162
    dijet_b  = Samples.mfv_stopbbarbbar_samples_20162
    higgs    = Samples.ggHToSSTodddd_samples_20162
elif year == '2018' :
    WplusH = Samples.WplusHToSSTodddd_samples_2018
    WminusH = Samples.WminusHToSSTodddd_samples_2018
    ZH = Samples.ZHToSSTodddd_samples_2018

    multijet = Samples.mfv_signal_samples_2018
    dijet_d  = Samples.mfv_stopdbardbar_samples_2018
    dijet_b  = Samples.mfv_stopbbarbbar_samples_2018
    higgs    = Samples.ggHToSSTodddd_samples_2018


samples = multijet + dijet_d + dijet_b
max_eff = 1.0
if vh :
    max_eff = 0.01
    samples = WplusH + WminusH + ZH
if ggh :
    samples = higgs


for sample in samples: 
    fn = os.path.join('/uscms/home/pkotamni/nobackup/crabdirs/Histos%s' % version, sample.name + '.root')
    print(fn)
    if not os.path.exists(fn):
        print 'no', sample.name
        continue
    f = ROOT.TFile(fn)
    def get_n(dir_name):
        h = f.Get('%s/h_w' % dir_name)
        return h.Integral(0,1000000) if integral else h.GetEntries(), h.GetEntries()

    num, _ = get_n('mfvEventHistosFullSel')
    den, _ = get_n('mfvEventHistosPreSel')
    sample.y, sample.yl, sample.yh = clopper_pearson(num, den) # ignore integral != entries, just get central value right
    print '%26s: signal efficiency w.r.t trigger= %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('signal efficiency w.r.t trigger', y_range=(0.,max_eff)) 
if vh :
    per.add(WplusH, title='Wplus(#rightarrow #mu #nu) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}', color=ROOT.kAzure+1)
    per.add(WminusH, title='Wminus(#rightarrow #mu #nu) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}', color=ROOT.kRed-7)
    per.add(ZH, title='Z(#rightarrow #mu #bar{#mu}) H #rightarrow SS #rightarrow d#bar{d}d#bar{d}', color=ROOT.kGreen+2)
elif ggh :
    per.add(higgs, title='H #rightarrow SS #rightarrow 4d', color=ROOT.kOrange+2)
else :
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet_d, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kGreen+2)
    per.add(dijet_b, title='#tilde{t} #rightarrow #bar{b}#bar{b}', color=ROOT.kBlue)

per.draw(canvas=ps.c)
ps.save('sigpreseleff_%s' % year)

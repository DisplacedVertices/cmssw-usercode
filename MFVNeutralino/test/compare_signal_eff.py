#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

mode = 'vary_pileup'
#mode = 'vary_jes'

set_style()
ps = plot_saver('plots/sigeff/v15/compare_sigeff_%s' % mode, size=(700,700), log=False, root=False)

if mode == 'vary_pileup':
    root_file_dirs = ['/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_0', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_1', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_2']
    num_paths = ['mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx']
    ls = ['2016', '2016mbxsecm5pc', '2016mbxsecp5pc']

if mode == 'vary_jes':
    root_file_dirs = ['/uscms_data/d3/dquach/crab3dirs/JetEnergyHistosV15', '/uscms_data/d3/dquach/crab3dirs/JetEnergyHistosV15', '/uscms_data/d3/dquach/crab3dirs/JetEnergyHistosV15']
    num_paths = ['mfvJetEnergyHistos/h_jet_ht_40_1000cut', 'mfvJetEnergyHistos/h_jet_ht_40_down_1000cut', 'mfvJetEnergyHistos/h_jet_ht_40_up_1000cut']
    ls = ['2016', '2016jesdown', '2016jesup']

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
        hnum = f.Get(num_paths[i])
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
        v = nev[j]
        c = nevs[0][j]

        ev = v**0.5
        ec = c**0.5

        r = v/c
        er = (v/c) * ((ev/v)**2 + (ec/c)**2)**0.5
        er *= (abs(r-1))**0.5 / (1+r)**0.5

        sample.y = r
        sample.yl = r-er
        sample.yh = r+er
        print '%26s: ratio = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

    per = PerSignal('ratio of efficiencies', y_range=(0.9,1.1))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_ratio_%s' % ls[i])

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples

for j,sample in enumerate(multijet + dijet):
    c = nevs[0][j]
    v1 = nevs[1][j]
    v2 = nevs[2][j]

    ec = c**0.5
    ev1 = v1**0.5
    ev2 = v2**0.5

    r1 = v1/c
    er1 = (v1/c) * ((ev1/v1)**2 + (ec/c)**2)**0.5 * (abs(r1-1))**0.5 / (1+r1)**0.5

    r2 = v2/c
    er2 = (v2/c) * ((ev2/v2)**2 + (ec/c)**2)**0.5 * (abs(r2-1))**0.5 / (1+r2)**0.5

    r = (abs(r1-1) + abs(r2-1)) / 2
    er = (er1**2 + er2**2)**0.5 / 2

    sample.y = r
    sample.yl = r-er
    sample.yh = r+er
    print '%26s: uncertainty = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('uncertainty in signal efficiency', y_range=(0.,0.1))
per.add(multijet, title='#tilde{N} #rightarrow tbs')
per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('sigeff_uncertainty_%s' % mode)
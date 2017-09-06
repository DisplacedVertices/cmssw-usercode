#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

mode = 'vary_pileup'
#mode = 'vary_jes'
#mode = 'vary_sigmadxy'
#mode = 'vary_sigmadxy_dbv300um'

combine_masses = False

set_style()
ps = plot_saver('plots/sigeff/v15/compare_sigeff_%s%s' % (mode, '_combine_masses' if combine_masses else ''), size=(700,700), log=False, root=False)

if mode == 'vary_pileup':
    root_file_dirs = ['/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_0', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_1', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_2']
    num_paths = ['mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx']
    ls = ['2016', '2016mbxsecm5pc', '2016mbxsecp5pc']

if mode == 'vary_jes':
    root_file_dirs = ['/uscms_data/d3/dquach/crab3dirs/JetEnergyHistosV15', '/uscms_data/d3/dquach/crab3dirs/JetEnergyHistosV15', '/uscms_data/d3/dquach/crab3dirs/JetEnergyHistosV15']
    num_paths = ['mfvJetEnergyHistos/h_jet_ht_40_1000cut', 'mfvJetEnergyHistos/h_jet_ht_40_down_1000cut', 'mfvJetEnergyHistos/h_jet_ht_40_up_1000cut']
    ls = ['2016', '2016jesdown', '2016jesup']

if mode == 'vary_sigmadxy':
    root_file_dirs = ['/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_0', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_sigmadxy3p7', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_sigmadxy3p8', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_sigmadxy3p9', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_sigmadxy4p1', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_sigmadxy4p2', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_sigmadxy4p3']
    num_paths = ['mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx']
    ls = ['sigmadxy4p0', 'sigmadxy3p7', 'sigmadxy3p8', 'sigmadxy3p9', 'sigmadxy4p1', 'sigmadxy4p2', 'sigmadxy4p3']

if mode == 'vary_sigmadxy_dbv300um':
    root_file_dirs = ['/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3_sigmadxy3p7', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3_sigmadxy3p8', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3_sigmadxy3p9', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3_sigmadxy4p1', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3_sigmadxy4p2', '/uscms_data/d1/jchu/crab_dirs/mfv_8025/HistosV15_3_sigmadxy4p3']
    num_paths = ['mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx', 'mfvEventHistosFullSel/h_bsx']
    ls = ['sigmadxy4p0_dbv300um', 'sigmadxy3p7_dbv300um', 'sigmadxy3p8_dbv300um', 'sigmadxy3p9_dbv300um', 'sigmadxy4p1_dbv300um', 'sigmadxy4p2_dbv300um', 'sigmadxy4p3_dbv300um']

nevs = []
for i,root_file_dir in enumerate(root_file_dirs):
    print ls[i]

    multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
    dijet = Samples.mfv_ddbar_samples

    nev = []
    for sample in sorted(multijet, key=lambda s: s.name) + sorted(dijet, key=lambda s: s.name):
        fn = os.path.join(root_file_dir, sample.name + '.root')
        if not os.path.exists(fn):
            continue
        f = ROOT.TFile(fn)
        hnum = f.Get(num_paths[i])
        hden = f.Get('mfvWeight/h_sums')
        num = hnum.Integral(0, hnum.GetNbinsX() + 2)
        den = hden.GetBinContent(1)
        sample.y, sample.yl, sample.yh = clopper_pearson(num, den)
        print '%26s: numerator = %8.1f, denominator = %8.1f, efficiency = %.3f (%.3f, %.3f)' % (sample.name, num, den, sample.y, sample.yl, sample.yh)
        nev.append(num)
    
    per = PerSignal('efficiency', y_range=(0.,1.05))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_%s' % ls[i])
    nevs.append(nev)

print
multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples
samples = sorted(multijet, key=lambda s: s.name) + sorted(dijet, key=lambda s: s.name)
print 'samples = [%s]' % (', '.join('%d: %s' % (i,s.name) for i,s in enumerate(samples)))

print
for i,nev in enumerate(nevs):
    print '%s: numerators = [%s]' % (ls[i], ', '.join('%.1f' % n for n in nev))

if combine_masses:
    print
    print 'combine masses'

    def add(nev, isamples):
        ntot = 0
        for i in isamples:
            ntot += nev[i]
        for i in isamples:
            nev[i] = ntot

    for i,nev in enumerate(nevs):
        add(nev, [0, 1, 2]) # mfv_neu_tau00100um: M0300 + M0400 + M0600
        add(nev, [3, 4, 5]) # mfv_neu_tau00100um: M0800 + M1200 + M1600
        add(nev, [35, 36, 37, 38]) # mfv_ddbar_tau00100um: M0300 + M0400 + M0500 + M0600
        add(nev, [39, 40, 41]) # mfv_ddbar_tau00100um: M0800 + M1200 + M1600
        print '%s: numerators = [%s]' % (ls[i], ', '.join('%.1f' % n for n in nev))

def ratio_of_numerators(v, d):
    ev = v**0.5
    ed = d**0.5

    r = v/d
    er = r * ((ev/v)**2 + (ed/d)**2)**0.5
    er *= (abs(r-1))**0.5 / (1+r)**0.5

    return r, er

print
for i,nev in enumerate(nevs):
    print ls[i]

    multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
    dijet = Samples.mfv_ddbar_samples

    for j,sample in enumerate(sorted(multijet, key=lambda s: s.name) + sorted(dijet, key=lambda s: s.name)):
        v = nev[j]
        d = nevs[0][j]
        r, er = ratio_of_numerators(v, d)

        sample.y = r
        sample.yl = r-er
        sample.yh = r+er
        print '%26s: variation = %8.1f, default = %8.1f, ratio = %.3f (%.3f, %.3f)' % (sample.name, v, d, sample.y, sample.yl, sample.yh)

    per = PerSignal('ratio of efficiencies', y_range=(0.9,1.1) if 'vary_sigmadxy' not in mode else (0.,2.))
    per.add(multijet, title='#tilde{N} #rightarrow tbs')
    per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
    per.draw(canvas=ps.c)
    ps.save('sigeff_ratio_%s' % ls[i])

multijet = [s for s in Samples.mfv_signal_samples if not s.name.startswith('my_')]
dijet = Samples.mfv_ddbar_samples

for j,sample in enumerate(sorted(multijet, key=lambda s: s.name) + sorted(dijet, key=lambda s: s.name)):
    d = nevs[0][j]

    v1 = nevs[1][j]
    r1, er1 = ratio_of_numerators(v1, d)

    r = abs(r1-1)
    er = er1

    if len(nevs) > 2:
        v2 = nevs[2][j]
        r2, er2 = ratio_of_numerators(v2, d)

        r = (abs(r1-1) + abs(r2-1)) / 2
        er = (er1**2 + er2**2)**0.5 / 2

    if 'vary_sigmadxy' in mode:
        v3 = nevs[3][j]
        r3, er3 = ratio_of_numerators(v3, d)

        v4 = nevs[4][j]
        r4, er4 = ratio_of_numerators(v4, d)

        v5 = nevs[5][j]
        r5, er5 = ratio_of_numerators(v5, d)

        r = abs(((8.65/35.93)*r1 + (7.58/35.93)*r2 + (3.11/35.93)*r3 + (4.03/35.93) + (6.81/35.93)*r4 + (5.75/35.93)*r5) - 1)
        er = (((8.65/35.93)*er1)**2 + ((7.58/35.93)*er2)**2 + ((3.11/35.93)*er3)**2 + ((6.81/35.93)*er4)**2 + ((5.75/35.93)*er5)**2)**0.5

    sample.y = r
    sample.yl = r-er
    sample.yh = r+er
    print '%26s: uncertainty = %.3f (%.3f, %.3f)' % (sample.name, sample.y, sample.yl, sample.yh)

per = PerSignal('uncertainty in signal efficiency', y_range=(0.,0.1) if 'vary_sigmadxy' not in mode else (0.,1.))
per.add(multijet, title='#tilde{N} #rightarrow tbs')
per.add(dijet, title='X #rightarrow d#bar{d}', color=ROOT.kBlue)
per.draw(canvas=ps.c)
ps.save('sigeff_uncertainty_%s' % mode)

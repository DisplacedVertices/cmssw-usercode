#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

mode = 'hem1516' # 'l1ee'
print mode
hem1516 = mode == 'hem1516'
l1ee = mode == 'l1ee'
assert hem1516 or l1ee

set_style()
ps = plot_saver(plot_dir('punish4%s' % mode), size=(600,600), pdf=True, log=False)

if hem1516:
    multijet = Samples.mfv_signal_samples_2018
    dijet = Samples.mfv_stopdbardbar_samples_2018
elif l1ee:
    multijet = Samples.mfv_signal_samples_2017
    dijet = Samples.mfv_stopdbardbar_samples_2017

for presel in 1,0:
    for gen in 0,1:
        if presel and gen:
            continue
        print 'presel %i gen %i' % (presel, gen)
        for svdist in 0., 0.04, 0.07:
            print 'svdist %.02f' % svdist
            PerSignal.clear_samples(multijet + dijet)
            for sample in multijet + dijet:
                path = '/uscms_data/d2/tucker/crab_dirs/MiniTreeV27m'
                if not presel:
                    path += '_NoPresel'
                fn = os.path.join(path, sample.name + '.root')
                if not os.path.exists(fn):
                    print 'no', fn
                    continue

                f = ROOT.TFile(fn)
                t = f.Get('mfvMiniTree/t')
                hr = draw_hist_register(t, True)
                def n(cut):
                    return get_integral(hr.draw('weight', cut, binning='1,0,1', goff=True))[0]

                if gen:
                    t.SetAlias('gen_is_jet', 'abs(gen_daughter_id) >= 1 && abs(gen_daughter_id) <= 5 && abs(gen_daughters.Eta()) < 2.5')
                    if hem1516:
                        t.SetAlias('jet_punish', 'gen_is_jet && gen_daughters.Eta() < -1.3 && gen_daughters.Phi() < -0.87 && gen_daughters.Phi() > -1.57')
                    elif l1ee:
                        t.SetAlias('jet_punish', 'gen_is_jet && abs(gen_daughters.Eta()) > 2.25 && gen_daughters.Pt() > 100')
                    t.SetAlias('njets_punish', 'Sum$(gen_is_jet && !jet_punish)')
                    t.SetAlias('jetht_punish', 'Sum$(gen_daughters.Pt() * (gen_daughters.Pt() > 40 && gen_is_jet && !jet_punish))')
                    t.SetAlias('njets_all', 'Sum$(!!gen_is_jet)') # !! is because ROOT is very stupid and I hate it
                    t.SetAlias('jetht_all', 'Sum$(gen_daughters.Pt() * (gen_is_jet && gen_daughters.Pt() > 40))')
                else:
                    if hem1516:
                        t.SetAlias('jet_punish', 'jet_eta < -1.3 && jet_phi < -0.87 && jet_phi > -1.57')
                    elif l1ee:
                        t.SetAlias('jet_punish', 'abs(jet_eta) > 2.25 && jet_pt > 100')
                    t.SetAlias('njets_punish', 'Sum$(!jet_punish)')
                    t.SetAlias('jetht_punish', 'Sum$(jet_pt * (jet_pt > 40 && !jet_punish))')
                    t.SetAlias('njets_all', 'njets')
                    t.SetAlias('jetht_all', 'jetht')

                base = 'nvtx>=2 && svdist > %f' % svdist
                if not presel:
                    base += ' && njets_all >= 4 && jetht_all >= 1200'
                den = n(base)
                num = n(base + ' && njets_punish >= 4 && jetht_punish >= 1200')
                sample.y, sample.yl, sample.yh = clopper_pearson(num, den)
                print '%26s: num = %.1f den = %.1f ratio = %.3f (%.3f, %.3f)' % (sample.name, num, den, sample.y, sample.yl, sample.yh)

            per = PerSignal('punish4%s%s/nominal' % (mode, ' (gen)' if gen else ''), y_range=(0.8,1.01), decay_paves_at_top=False)
            per.add(multijet, title='#tilde{N} #rightarrow tbs')
            per.add(dijet, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kBlue)
            per.draw(canvas=ps.c)
            ps.save('sigeff_svdist%.2f_presel%i_gen%i' % (svdist, presel, gen))

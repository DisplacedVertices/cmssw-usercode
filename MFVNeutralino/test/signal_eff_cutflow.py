#!/usr/bin/env python

import os
from DVCode.Tools.ROOTTools import *
from DVCode.Tools import Samples
from DVCode.MFVNeutralino.PerSignal import PerSignal

set_style()

root_file_dir = '/uscms_data/d1/jchu/crab_dirs/mfv_8025/TheoristRecipeV30'

samples_list = [(Samples.mfv_signal_samples,  'neu'),
                (Samples.mfv_ddbar_samples,   'ddbar'),
                (Samples.mfv_bbbar_samples,   'bbbar'),
                (Samples.mfv_neuuds_samples,  'neuuds'),
                (Samples.mfv_neuudmu_samples, 'neuudmu'),
                ]

paths = [('TwoVtxDvv400um',   'NoCuts'),
         ('OfflineJets',      'NoCuts'),
         ('TrigSel',          'OfflineJets'),
         ('PreSel',           'TrigSel'),
         ('TwoVtxNoCuts',     'PreSel'),
         ('TwoVtxBsbs2ddist', 'TwoVtxNoCuts'),
         ('TwoVtxGeo2ddist',  'TwoVtxBsbs2ddist'),
         ('TwoVtxNtracks',    'TwoVtxGeo2ddist'),
         ('TwoVtxBs2derr',    'TwoVtxNtracks'),
         ('TwoVtxDvv400um',   'TwoVtxBs2derr'),
         ('PreSel',           'NoCuts'),
         ('TwoVtxDvv400um',   'PreSel'),
         ('TwoVtxGeo2ddist',  'PreSel'),
         ('TwoVtxBs2derr',    'TwoVtxGeo2ddist'),
         ]

for samples, samples_name in samples_list:
    ps = plot_saver('plots/theorist_recipe/sigeff_cutflow/%s' % samples_name, size=(700,700), root=False, log=False)

    for num_path, den_path in paths:
        for sample in samples:
            fn = os.path.join(root_file_dir, sample.name + '.root')
            if not os.path.exists(fn):
                continue
            f = ROOT.TFile(fn)
            hnum = f.Get('mfvTheoristRecipe%s/h_gen_dvv' % num_path)
            hden = f.Get('mfvTheoristRecipe%s/h_gen_dvv' % den_path)
            num = hnum.Integral(0, hnum.GetNbinsX() + 2)
            den = hden.Integral(0, hnum.GetNbinsX() + 2)
            sample.y, sample.yl, sample.yh = clopper_pearson(num, den)
            print '%28s: %s/%s efficiency = %.3f (%.3f, %.3f)' % (sample.name, num_path, den_path, sample.y, sample.yl, sample.yh)
     
        per = PerSignal('efficiency', y_range=(0.,1.05))
        per.add(samples)
        per.draw(canvas=ps.c, do_decay_paves=False)
        ps.save('sigeff_%s_%s_divide_%s' % (samples_name, num_path, den_path))

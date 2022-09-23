#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

alpha = 1.0 - 0.6827
use_effective = True

set_style()
version = 'test'
ps = plot_saver(plot_dir('filter_tocs_%s' % version), size=(1000,800), pdf=False, log=False)

filter_hist_dir = 'mfvFilterHistosNoCuts'

fn = '/uscms_data/d3/shogan/crab_dirs/HistosV30MinSelFilterBitSkipL1/ggh_combined_1mm.root'    # Black curve
zn = '/uscms_data/d3/shogan/crab_dirs/HistosV30MinSelFilterBitSkipL1/ggh_combined_10mm.root'    # Red curve
an = '/uscms_data/d3/shogan/crab_dirs/HistosV30MinSelFilterBitSkipL1/ttbar_2017.root'    # Blue curve

f = ROOT.TFile(fn)
t = f.Get(filter_hist_dir)

z = ROOT.TFile(zn)
v = z.Get(filter_hist_dir)

a = ROOT.TFile(an)
b = a.Get(filter_hist_dir)

for hist in ['h_filter_07', 'h_filter_08', 'h_filter_09', 'h_filter_10', 'h_filter_11', 'h_filter_12']:


    c1 = ROOT.TCanvas('c1', '', 1000, 800)

    t_den = t.Get(hist+'_den')
    t_num = t.Get(hist+'_num')

    v_den = v.Get(hist+'_den')
    v_num = v.Get(hist+'_num')

    b_den = b.Get(hist+'_den')
    b_num = b.Get(hist+'_num')

    for blah in [t_den, t_num, v_den, v_num, b_den, b_num]:
        blah.Rebin(4)

    t_rat = histogram_divide(t_num, t_den, confint_params=(alpha,), use_effective=use_effective)
    v_rat = histogram_divide(v_num, v_den, confint_params=(alpha,), use_effective=use_effective)
    b_rat = histogram_divide(b_num, b_den, confint_params=(alpha,), use_effective=use_effective)


    t_rat.SetTitle('')
    t_rat.SetLineWidth(2)
    t_rat.SetLineColor(ROOT.kBlack)
    t_rat.GetYaxis().SetRangeUser(0.0,1.05)

    tmp_title = (t_den.GetXaxis().GetTitle() if hist != 'h_filter_12' else 'HT(30) (GeV)')
    t_rat.GetXaxis().SetTitle(tmp_title)
    t_rat.GetYaxis().SetTitle('filter eff.')
    t_rat.SetTitle(t_num.GetTitle())

    v_rat.SetTitle('')
    v_rat.SetLineWidth(2)
    v_rat.SetLineColor(ROOT.kRed)

    b_rat.SetTitle('')
    b_rat.SetLineWidth(2)
    b_rat.SetLineColor(ROOT.kBlue)

    t_rat.Draw()
    v_rat.Draw('same')
    b_rat.Draw('same')

    ps.save(hist, other_c=c1)

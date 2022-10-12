#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

alpha = 1.0 - 0.6827
use_effective = True

set_style()
ROOT.gStyle.SetPadTickY(0)
version = 'test'
ps = plot_saver(plot_dir('filter_tocs_%s' % version), size=(1000,800), pdf=False, log=False)

filter_hist_dir = 'mfvFilterHistosNoCuts'


fn = '/uscms_data/d3/shogan/crab_dirs/HistosULV1BmLooseDeepFlav/mfv_neu_tau000300um_M0200_2017.root'
gn = '/uscms_data/d3/shogan/crab_dirs/HistosULV1BmLooseDeepFlav/mfv_stopdbardbar_tau000300um_M0200_2017.root'
hn = '/uscms_data/d3/shogan/crab_dirs/HistosULV1BmLooseDeepFlav/mfv_stopbbarbbar_tau000300um_M0200_2017.root'


f = ROOT.TFile(fn)
t = f.Get(filter_hist_dir)

g = ROOT.TFile(gn)
v = g.Get(filter_hist_dir)

y = ROOT.TFile(hn)
z = y.Get(filter_hist_dir)

for hist in ['h_di_filter_00', 'h_di_filter_01', 'h_di_filter_02', 'h_di_filter_03',
             'h_tri_filter_00', 'h_tri_filter_01', 'h_tri_filter_02', 'h_tri_filter_03',
             'h_tri_filter_04', 'h_tri_filter_05', 'h_tri_filter_06', 'h_tri_filter_07',
             'h_tri_filter_08', 'h_tri_filter_09']:

    c1 = ROOT.TCanvas('c1', '', 1000, 800)

    t_den = t.Get(hist+'_den')
    t_num = t.Get(hist+'_num')

    for blah in [t_den, t_num]:
        blah.Rebin(2)

    t_rat = histogram_divide(t_num, t_den, confint_params=(alpha,), use_effective=use_effective)

    tmp_ymax = t_den.GetMaximum()

    t_rat.SetTitle('')
    t_rat.SetLineWidth(2)
    t_rat.SetLineColor(ROOT.kBlack)
    t_rat.GetYaxis().SetRangeUser(0.0,1.05)
    t_rat.GetYaxis().SetTitle('efficiency')
    t_rat.GetXaxis().SetTitle(t_num.GetXaxis().GetTitle())

    t_rat.Draw()

    if True:
        v_den = v.Get(hist+'_den')
        v_num = v.Get(hist+'_num')
    
        for blah in [v_den, v_num]:
            blah.Rebin(2)
    
        v_rat = histogram_divide(v_num, v_den, confint_params=(alpha,), use_effective=use_effective)
    
        v_rat.SetTitle('')
        v_rat.SetLineWidth(2)
        v_rat.SetLineColor(ROOT.kRed)
        v_rat.GetYaxis().SetRangeUser(0.0,1.05)
        v_rat.GetYaxis().SetTitle('efficiency')
        v_rat.GetXaxis().SetTitle(v_num.GetXaxis().GetTitle())
    
        v_rat.Draw("same")

    if True:
        z_den = z.Get(hist+'_den')
        z_num = z.Get(hist+'_num')
    
        for blah in [z_den, z_num]:
            blah.Rebin(2)
    
        z_rat = histogram_divide(z_num, z_den, confint_params=(alpha,), use_effective=use_effective)
    
        z_rat.SetTitle('')
        z_rat.SetLineWidth(2)
        z_rat.SetLineColor(ROOT.kBlue)
        z_rat.GetYaxis().SetRangeUser(0.0,1.05)
        z_rat.GetYaxis().SetTitle('efficiency')
        z_rat.GetXaxis().SetTitle(z_num.GetXaxis().GetTitle())
    
        z_rat.Draw("same")

    ps.save(hist, other_c=c1)


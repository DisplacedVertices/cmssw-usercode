#!/usr/bin/env python

import os
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

alpha = 1.0 - 0.6827
use_effective = True

linear = ROOT.TF1("f1", "pol1")

set_style()
version = 'test'
ps = plot_saver(plot_dir('filter_tocs_%s' % version), size=(1000,800), pdf=False, log=False)

#filter_hist_dir = 'mfvFilterHistosNoCuts'
filter_hist_dir = 'mfvFilterHistosNhltCalo9Plus'

rb = 2

fn = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_TrigStudy_June27_OneMoreSlice/data_bkg.root' # Black
gn = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_TrigStudy_June27_OneMoreSlice/mc_bkg.root' # Red
hn = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_TrigStudy_June27_OneMoreSlice/mfv_neu_tau010000um_M0300_2017.root' # Blue

f = ROOT.TFile(fn)
t = f.Get(filter_hist_dir)

g = ROOT.TFile(gn)
v = g.Get(filter_hist_dir)

y = ROOT.TFile(hn)
z = y.Get(filter_hist_dir)

den_choice = '_den0'
num_choice = '_num0'
config_str = '_b'

for hist in [#'h_di_filter_00', 'h_di_filter_01', 'h_di_filter_02', 'h_di_filter_03',

             #'h_tri_filter_00', 'h_tri_filter_01', 'h_tri_filter_02', 'h_tri_filter_03',
             #'h_tri_filter_04', 'h_tri_filter_05', 'h_tri_filter_06', 'h_tri_filter_07',
             #'h_tri_filter_08', 'h_tri_filter_09',

             'h_dd_dtk_filter_00', 'h_dd_dtk_filter_alt_a_00','h_dd_dtk_filter_alt_b_00', 'h_dd_dtk_filter_alt_c_00', 'h_dd_dtk_filter_alt_d_00', 'h_dd_dtk_filter_01', 'h_dd_dtk_filter_02', 'h_dd_dtk_filter_03', 'h_dd_dtk_filter_04',

             #'h_dd_inc_filter_00', 'h_dd_inc_filter_alt_a_00', 'h_dd_inc_filter_alt_b_00', 'h_dd_inc_filter_alt_c_00', 'h_dd_inc_filter_alt_d_00', 'h_dd_inc_filter_01', 'h_dd_inc_filter_02', 'h_dd_inc_filter_03',

             #'h_calojet_pt', 'h_calojet_eta']:
             ]:
             #'h_calojet_nprompt_tks', 'h_calojet_ndisp_tks']:

    c1 = ROOT.TCanvas('c1', '', 1000, 800)

    print(hist)

    if 'filter' in hist:
        t_den = t.Get(hist+'_den')
        t_num = t.Get(hist+'_num')

    else:
        t_den = t.Get(hist+den_choice)
        t_num = t.Get(hist+num_choice)
    
    for blah in [t_den, t_num]:
        blah.Rebin(rb)

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
        if 'filter' in hist:
          v_den = v.Get(hist+'_den')
          v_num = v.Get(hist+'_num')

        else:
            v_den = v.Get(hist+den_choice)
            v_num = v.Get(hist+num_choice)

        #else:
          #old_hist = hist
          #new_hist = hist.replace("calojet_n", "calojet_matched_n")
          #v_den = v.Get(old_hist)
          #v_num = v.Get(new_hist)

   
        for blah in [v_den, v_num]:
            blah.Rebin(rb)
    
        v_rat = histogram_divide(v_num, v_den, confint_params=(alpha,), use_effective=use_effective)
    
        v_rat.SetTitle('')
        v_rat.SetLineWidth(2)
        v_rat.SetLineColor(ROOT.kRed)
        v_rat.GetYaxis().SetRangeUser(0.0,1.05)
        v_rat.GetYaxis().SetTitle('efficiency')
        v_rat.GetXaxis().SetTitle(v_num.GetXaxis().GetTitle())
    
        v_rat.Draw("same")
        

    if True:
        if 'filter' in hist:
          z_den = z.Get(hist+'_den')
          z_num = z.Get(hist+'_num')

        else:
            z_den = z.Get(hist+den_choice)
            z_num = z.Get(hist+num_choice)

        #else:
          #old_hist = hist
          #new_hist = hist.replace("calojet_n", "calojet_matched_n")
          #z_den = z.Get(old_hist)
          #z_num = z.Get(new_hist)

   
        for blah in [z_den, z_num]:
            blah.Rebin(rb)
    
        z_rat = histogram_divide(z_num, z_den, confint_params=(alpha,), use_effective=use_effective)
    
        z_rat.SetTitle('')
        z_rat.SetLineWidth(2)
        z_rat.SetLineColor(ROOT.kBlue)
        z_rat.GetYaxis().SetRangeUser(0.0,1.05)
        z_rat.GetYaxis().SetTitle('efficiency')
        z_rat.GetXaxis().SetTitle(z_num.GetXaxis().GetTitle())
    
        z_rat.Draw("same")

    ps.save(hist + config_str, other_c=c1)


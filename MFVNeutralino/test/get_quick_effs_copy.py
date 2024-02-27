#!/usr/bin/env python

import os
import ROOT
import numpy as np
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

ROOT.gStyle.SetOptStat(0)

set_style()
ps = plot_saver(plot_dir('btag_trig_effs'), size=(1000,800), pdf=False, log=False)

def make_eff_curve(fn, dirstr, den_pfx, num_pfx, hist, rebin, color=ROOT.kBlack):
    f_den = ROOT.TFile(den_pfx + fn)
    f_num = ROOT.TFile(num_pfx + fn)
    alpha = 1.0 - 0.6827
    use_effective = True
    h_den = f_den.Get(dirstr).Get(hist)
    h_num = f_num.Get(dirstr).Get(hist)

    h_num.Rebin(rebin)
    h_den.Rebin(rebin)

    h_rat = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)
    h_rat.SetLineWidth(2)
    h_rat.SetLineColor(color)
    h_rat.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())

    return h_rat

filter_hist_dir = 'mfvEventHistosPreSel'

prefix_no_trig   = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BjetRevisit_NoTrig_Aug30/'
prefix_with_trig = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BjetRevisit_WithTrig_Aug30/'

#names = ['neu->tbs, 1mm, M200', 'neu->tbs, 10mm, M200', 'stop->dd, 1mm, M300', 'stop->dd, 10mm, M300', 'H->SS->4d, 1mm, M55', 'H->SS->4d, 10mm, M55']
fnames = ['data_bkg.root', 'mc_bkg.root']

for hist in ['h_trig_csvtags', 'h_trig_hardcsvtags']:
    c1 = ROOT.TCanvas('c1', '', 1000, 800)
    rat_dat = make_eff_curve(fnames[0], filter_hist_dir, prefix_no_trig, prefix_with_trig, hist, 1, ROOT.kBlue);
    rat_sim = make_eff_curve(fnames[1], filter_hist_dir, prefix_no_trig, prefix_with_trig, hist, 1, ROOT.kRed);
    
    rat_dat.GetYaxis().SetRangeUser(0.0, 1.05)
    rat_dat.Draw()
    rat_sim.Draw('same')

    for j in range(rat_dat.GetN()):
            x_dat, y_dat, e_dat_lo, e_dat_hi = ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
            x_sim, y_sim, e_sim_lo, e_sim_hi = ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
            rat_dat.GetPoint(j, x_dat, y_dat)
            rat_sim.GetPoint(j, x_sim, y_sim)
    
            e_dat_lo = rat_dat.GetErrorYlow(j)
            e_dat_hi = rat_dat.GetErrorYhigh(j)
            e_sim_lo = rat_sim.GetErrorYlow(j)
            e_sim_hi = rat_sim.GetErrorYhigh(j)
    
            y_sim = max(y_sim, 0.0)
    
            try:
                if y_dat > y_sim:
                    factor = (1 - y_dat) / (1 - y_sim)
                else:
                    factor = -1* (y_dat / y_sim)
            except ZeroDivisionError:
                factor = 1.0

            print('n: {0}    factor: {1}'.format(np.floor(x_dat), factor))

    ps.save(hist + '_eff', other_c=c1)

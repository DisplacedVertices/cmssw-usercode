#!/usr/bin/env python

import os
import ROOT
import numpy as np
from JMTucker.Tools.ROOTTools import *
from JMTucker.MFVNeutralino.PerSignal import PerSignal

ROOT.gStyle.SetOptStat(0)

######################################################################################################################### 

def make_eff_curve(fn, dirstr, h_pfx, den, num, rebin, color=ROOT.kBlack):
    f = ROOT.TFile(fn)
    alpha = 1.0 - 0.6827
    use_effective = True
    print(fn)
    print(h_pfx+'_'+den)
    h_den = f.Get(dirstr).Get(h_pfx+'_'+den)
    h_num = f.Get(dirstr).Get(h_pfx+'_'+num)

    h_num.Rebin(rebin)
    h_den.Rebin(rebin)

    h_rat = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)
    h_rat.SetLineWidth(3)
    h_rat.SetLineColor(color)
    h_rat.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())

    return h_rat

######################################################################################################################### 

def get_alt_efficiencies(fn, dirstr, h_pfx, den, num):
    effs = []
    errs = []
    f = ROOT.TFile(fn)
    h_den = f.Get(dirstr).Get(h_pfx+'_'+den)
    h_num = f.Get(dirstr).Get(h_pfx+'_'+num)

    for i in range(1, h_num.GetNbinsX()):
        try:
            eff = h_num.GetBinContent(i)/h_den.GetBinContent(i)
            err = np.sqrt(eff * (1 - eff) / h_den.GetBinContent(i))
        except ZeroDivisionError:
            eff = 0.0
            err = 0.0

        effs.append(eff)
        errs.append(err)

    return effs, errs

######################################################################################################################### 

def are_compatible_q(eff_dat, err_dat, eff_sim, err_sim):
    # err_dat = [low_err, high_err]
    if eff_dat > eff_sim:
        return (eff_dat - err_dat[0]) < (eff_sim + err_sim[1])
    else:
        return (eff_sim - err_sim[0]) < (eff_dat + err_dat[1])
   
######################################################################################################################### 

alpha = 1.0 - 0.6827
use_effective = True

set_style()
version = 'test'
ps = plot_saver(plot_dir('jet_tk_effs_%s' % version), size=(1000,800), pdf=True, log=False)

year   = '2018'
fn_dat = '/uscms_data/d3/shogan/crab_dirs/HistosULV9_trigstudy_Bm_2018_FULL_PRESUITE_Feb15/DisplacedJet_'+year+'.root'
fn_sim = '/uscms_data/d3/shogan/crab_dirs/HistosULV9_trigstudy_Bm_2018_FULL_PRESUITE_Feb15/mc_bkg_qcd.root'

dirstr = 'mfvJetTksHistosOnlineTkFactors'
all_hist_labels = [['h_calojet_nprompttks', 'all', 'pass_prmpt', 'prompt'], ['h_calojet_ndisptks', 'pass_prmpt', 'pass_disp', 'disp']]

for i, hist_labels in enumerate(all_hist_labels):
    c1 = ROOT.TCanvas('c1', '', 1000, 800)
    c1.SetGridx(1)
    c1.SetGridy(1)
    rebin = 1
    print(hist_labels[0])

    rat_dat = make_eff_curve(fn_dat, dirstr, hist_labels[0], hist_labels[1], hist_labels[2], rebin, ROOT.kBlue)
    rat_sim = make_eff_curve(fn_sim, dirstr, hist_labels[0], hist_labels[1], hist_labels[2], rebin, ROOT.kRed)

    rat_dat.GetYaxis().SetRangeUser(0, 1.05)
    rat_dat.GetXaxis().SetRangeUser(0, 35.0)
    rat_dat.GetXaxis().SetTitle('n(%s tracks in calojets)' % (hist_labels[3]))
    rat_dat.GetYaxis().SetTitle('Eff. to survive track filter')
    rat_dat.SetTitle('Online Prompt Track Veto Survival Eff.')
    rat_dat.Draw()
    rat_sim.Draw('same')   

    x_offset = 0.05
    y_offset = 0.62
    leg = ROOT.TLegend(0.10+x_offset, 0.12+y_offset, 0.38+x_offset, 0.23+y_offset)
    leg.AddEntry(rat_dat, "DisplacedJet" + year)
    leg.AddEntry(rat_sim, "Bkg MC")
    leg.Draw("same")

    for j in range(rat_dat.GetN()):
        x_dat, y_dat, e_dat_lo, e_dat_hi = ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
        x_sim, y_sim, e_sim_lo, e_sim_hi = ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
        rat_dat.GetPoint(j, x_dat, y_dat)
        rat_sim.GetPoint(j, x_sim, y_sim)

        e_dat_lo = rat_dat.GetErrorYlow(j)
        e_dat_hi = rat_dat.GetErrorYhigh(j)
        e_sim_lo = rat_sim.GetErrorYlow(j)
        e_sim_hi = rat_sim.GetErrorYhigh(j)

        compatible = are_compatible_q(y_dat, [e_dat_lo, e_dat_hi], y_sim, [e_sim_lo, e_sim_hi])

        y_sim = max(y_sim, 0.0)

        try:
            if y_dat > y_sim:
                factor = (1 - y_dat) / (1 - y_sim)
            else:
                factor = -1* (y_dat / y_sim)
        except ZeroDivisionError:
            factor = 1.0

        avg_err_dat = (e_dat_lo + e_dat_hi)/2.0
        avg_err_sim = (e_sim_lo + e_sim_hi)/2.0

        print("j: %i   x: %2.1f     y_dat: %6.5f   y_sim: %6.5f   compatible: %i     factor: %7.6f" % (j, x_dat-0.5, y_dat, y_sim, compatible, factor))

    ps.save(hist_labels[0], other_c=c1)

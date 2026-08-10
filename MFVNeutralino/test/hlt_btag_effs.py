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

    #print "Den hist: ", h_pfx + den
    #print "num hist: ", h_pfx + num
    h_den = f.Get(dirstr).Get(h_pfx + den)
    h_num = f.Get(dirstr).Get(h_pfx + num)

    h_num.Rebin(rebin)
    h_den.Rebin(rebin)

    h_rat = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)
    h_rat.SetLineWidth(3)
    h_rat.SetLineColor(color)
    h_rat.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())

    return h_rat

######################################################################################################################### 

alpha = 1.0 - 0.6827
use_effective = True

set_style()
version = 'test'
ps = plot_saver(plot_dir('jet_hlt_btag_eff_%s' % version), size=(1000,800), pdf=True, log=False)

year = '2016APV'
#fdir = '/uscms_data/d3/shogan/crab_dirs/HistosULV9_trigstudy_Bm_2016_PreSuite_Feb14/'
fdir = '/uscms_data/d3/shogan/crab_dirs/HistosULV9_trigstudy_Bm_2016APV_FULL_PRESUITE_Feb19/'

hists = ["h_jet_bdisc_deepflav_", "h_jet_bdisc_deepcsv_", "h_jet_bdisc_csv_", "h_jet_bdisc_csv_", "h_jet_bdisc_deepcsv_", "h_jet_bdisc_deepflav_"]

for i, hist in enumerate(hists):
    print(hist)
    c1 = ROOT.TCanvas('c1', '', 1000, 800)
    c1.SetGridx(1)
    c1.SetGridy(1)
    rebin = 10

    if year in ['2017', '2018']:
        title = 'Online Btagging Efficiency' if i < 3 else 'Online Calo Btag Efficiency'
        dirstr = 'mfvJetTksHistosPFJetBtagFactors' if i < 3 else 'mfvJetTksHistosCaloJetBtagFactors'
        num = 'pass_hlt' if i < 3 else 'pass_hlt_calo'
        mod = '' if i < 3 else '_hlt_calo'
        
    else:
        title = 'Online Calo b tag Efficiency' if i < 3 else 'Online Calo Btag Efficiency'
        dirstr = 'mfvJetTksHistosCaloJetBtagFactors' if i < 3 else 'mfvJetTksHistosCaloJetLowBtagFactors'
        num = 'pass_hlt_calo' if i < 3 else 'pass_hlt_lo_calo'
        mod = '_hlt_calo' if i < 3 else '_hlt_lo_calo'

    den = 'pass_or_fail'

    x_offset = 0.45
    y_offset = 0.12
    leg = ROOT.TLegend(0.10+x_offset, 0.12+y_offset, 0.38+x_offset, 0.23+y_offset)

    rat_C = make_eff_curve(fdir+'MuonEG_' + year + '.root',  dirstr, hist, den, num, rebin, ROOT.kRed)
    rat_sim = make_eff_curve(fdir+'ttbar_ll_' + year + '.root', dirstr, hist, den, num, rebin, ROOT.kRed)

    rat_C.GetYaxis().SetRangeUser(0, 1.0)
    rat_C.GetXaxis().SetRangeUser(0, 1.0)
    rat_C.GetYaxis().SetTitle('Online Btag Eff')
    rat_C.GetXaxis().SetTitle('PFJet b score')
    rat_C.SetTitle(title)
    rat_C.SetMarkerStyle(20)   # Solid circle for data
    rat_C.SetMarkerColor(ROOT.kRed)
    rat_C.Draw("AP")

    rat_sim.SetMarkerStyle(24)   # Open circle for MC
    rat_sim.SetMarkerColor(ROOT.kRed)
    rat_sim.Draw("SAMEP")   

    if hist.startswith('h_jet_bdisc_deepflav'):
        out_array = []
        for j in range(rat_C.GetN()):
            x_dat, y_dat, e_dat_lo, e_dat_hi = ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
            x_sim, y_sim, e_sim_lo, e_sim_hi = ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0), ROOT.Double(0.0)
            rat_C.GetPoint(j, x_dat, y_dat)
            rat_sim.GetPoint(j, x_sim, y_sim)
        
            try:
                if (y_dat > y_sim):
                    out_array.append(round(-1*(1-y_dat)/(1-y_sim), 3))
                elif (y_sim > y_dat):
                    out_array.append(round(y_dat/y_sim, 3))
            except:
                out_array.append(1.00)
        print out_array

    leg.AddEntry(rat_C, "MuonEG" + year)
    leg.AddEntry(rat_sim, "Bkg MC")
    leg.Draw("same")

    ps.save(hist[:-1]+mod, other_c=c1)

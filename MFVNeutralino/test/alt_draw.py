#!/usr/bin/env python

import os
import numpy as np
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

alpha = 1.0 - 0.6827
use_effective = True

set_style()
ROOT.gStyle.SetOptStat(0)
ps = plot_saver(plot_dir('jet_tks_histos'), size=(750,600), pdf=False, log=False)

#hist_dir = 'mfvJetTksHistosSigReg'
hist_dir = 'mfvJetTksHistosNoCuts'
hists = ["h_jet_pt","h_jet_eta","h_jet_phi","h_jet_dbv","h_jet_skeweta","h_jet_skewphi","h_jet_skew_dR","h_jet_ntks","h_jet_bdisc",
         "h_jet_bdisc_old","h_jet_tks_pt","h_jet_tks_ptrel","h_jet_tks_eta","h_jet_tks_etarel","h_jet_tks_dR","h_jet_tks_nsigmadxy",
         "h_jet_tks_nsigmadxyz", "h_jet_sum_nsigmadxy","h_jet_sum_nsigmadxyz","h_jet_tk_nsigmadxy_avg","h_jet_tk_nsigmadxy_med",
         "h_jet_tk_nsigmadxy_0","h_jet_tk_nsigmadxy_1","h_jet_tk_nsigmadxyz_avg","h_jet_tk_nsigmadxyz_med","h_jet_tk_nsigmadxyz_0",
         "h_jet_tk_nsigmadxyz_1","h_jet_sumtk_pt_ratio","h_jet_sumtk_dR"]

fn = 'histos.root'
#fn = '/uscms_data/d3/shogan/crab_dirs/HistosV31CSVTight/ggh_combined_1mm.root'
f  = ROOT.TFile(fn)

opt = 'hlt'
for hist in hists:
    c2 = ROOT.TCanvas('c2', '', 750, 600)
    h_all = f.Get(hist_dir).Get(hist+'_pass_or_fail')
    h_p   = f.Get(hist_dir).Get(hist+'_pass_'+opt)
    h_asym = ROOT.TGraphAsymmErrors(h_p, h_all, "cl=0.683 b(1,1) mode")
    
    title = h_p.GetXaxis().GetTitle()
    for delete in ['which', 'pass_off', 'fail_off', 'fail_hlt', 'that', 'b-tag', 'pass_or_fail']:
        title = title.replace(delete, '')
    
    
    h_asym.SetLineWidth(3)
    h_asym.SetLineColor(ROOT.kBlue)
    h_asym.GetYaxis().SetRangeUser(0,1.05)
    h_asym.GetYaxis().SetTitle('btag eff.')
    h_asym.GetXaxis().SetTitle(title)

    #leg1 = ROOT.TLegend(0.650, 0.735, 0.850, 0.852)
    #leg1.AddEntry(h_p, 'Pass b-tag')
    #leg1.SetBorderSize(2)
    #leg1.SetTextSize(0.04)
    #leg1.SetFillStyle(0)
    
    #h_f.Draw('same')
    h_asym.Draw()
    #leg1.Draw('same')
    
    ps.save('rat_'+hist, other_c=c2)

for hist in hists:
    c1 = ROOT.TCanvas('c1', '', 750, 600)
    h_f = f.Get(hist_dir).Get(hist+'_fail_'+opt)
    h_p = f.Get(hist_dir).Get(hist+'_pass_'+opt)

    h_f.Rebin(2)
    h_p.Rebin(2)
    
    h_f.Scale(1.0/h_f.Integral())
    h_p.Scale(1.0/h_p.Integral())
    
    maxes = [h_f.GetMaximum(), h_p.GetMaximum()]
    title = h_f.GetXaxis().GetTitle()
    for delete in ['which', 'fail_off', 'fail_hlt', 'that', 'b-tag']:
        title = title.replace(delete, '')
    
    upper_lim = float(max(maxes))*1.09
    
    h_f.SetLineWidth(3)
    h_f.SetLineColor(ROOT.kRed)
    h_f.GetYaxis().SetRangeUser(0.0, upper_lim)
    h_f.GetXaxis().SetTitle(title)
    
    h_p.SetLineWidth(3)
    h_p.SetLineColor(ROOT.kBlue)

    leg1 = ROOT.TLegend(0.600, 0.735, 0.880, 0.852)
    leg1.AddEntry(h_f, 'Fail HLT b-tag')
    leg1.AddEntry(h_p, 'Pass HLT b-tag')
    leg1.SetBorderSize(2)
    leg1.SetTextSize(0.04)
    leg1.SetFillStyle(0)
    
    h_f.Draw('same')
    h_p.Draw('same')
    leg1.Draw('same')
    
    ps.save('plt_'+hist, other_c=c1)



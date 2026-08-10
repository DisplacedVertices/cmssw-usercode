#!/usr/bin/env python

import os
import ROOT
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

def make_curve(fn, dirstr, hn, rebin, color_p = ROOT.kRed, color_f = ROOT.kBlue):
    f = ROOT.TFile(fn)
    alpha = 1.0 - 0.6827
    use_effective = True
    h_pass = f.Get(dirstr).Get(hn+'_pass_hlt')
    h_fail = f.Get(dirstr).Get(hn+'_fail_hlt')

    h_num.Rebin(rebin)
    h_den.Rebin(rebin)

    h_rat = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)
    h_rat.SetLineWidth(2)
    h_rat.SetLineColor(color)
    h_rat.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())

    return h_rat

ROOT.gStyle.SetOptStat(0)
set_style()
ps = plot_saver(plot_dir('transfer'), size=(1000,800), pdf=False, log=True)
ROOT.gStyle.SetOptStat(0)

dirstr = 'mfvJetTksHistosNoCuts'
rb = 2

prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4_dilepBm_NtupleV6_TagProbe_pT_split_Oct31/'

fn = prefix + 'ttbar_ll_2017.root'
f  = ROOT.TFile(fn)

hists = ["h_jet_pt_", "h_jet_eta_", "h_jet_phi_", "h_jet_dbv_", "h_jet_ntks_", "h_jet_bdisc_deepflav_", "h_jet_bdisc_deepcsv_", "h_jet_bdisc_csv_", "h_jet_tks_pt_",
"h_jet_tks_ptrel_", "h_jet_tks_eta_", "h_jet_tks_etarel_", "h_jet_tks_dR_", "h_jet_tks_dxy_", "h_jet_tks_dxyz_", "h_jet_tks_nsigmadxy_",
"h_jet_tks_nsigmadxyz_", "h_jet_sum_nsigmadxy_", "h_jet_sum_nsigmadxyz_", "h_jet_tk_nsigmadxy_avg_",  "h_jet_tk_nsigmadxy_med_", 
"h_jet_tk_nsigmadxy_0_", "h_jet_tk_nsigmadxy_1_", "h_jet_tk_nsigmadxyz_avg_", "h_jet_tk_nsigmadxyz_med_", "h_jet_tk_nsigmadxyz_0_",
"h_jet_tk_nsigmadxyz_1_", "h_jet_sumtk_pt_ratio_", "h_jet_sumtk_dR_"]

for i, hist in enumerate(hists):
    c1 = ROOT.TCanvas('c1', '', 1000, 800)

    x_offset = 0.5
    y_offset = 0.63
    leg = ROOT.TLegend(0.10+x_offset, 0.12+y_offset, 0.30+x_offset, 0.25+y_offset)

    print(hist)

    h_pass = f.Get(dirstr).Get(hist+'pass_hlt')
    h_fail = f.Get(dirstr).Get(hist+'fail_hlt')

    h_pass.Scale(1.0/h_pass.Integral())
    h_fail.Scale(1.0/h_fail.Integral())

    pass_max = h_pass.GetBinContent(h_pass.GetMaximumBin())
    fail_max = h_fail.GetBinContent(h_fail.GetMaximumBin())
    pass_min = h_pass.GetBinContent(h_pass.GetMinimumBin())
    fail_min = h_fail.GetBinContent(h_fail.GetMinimumBin())

    h_pass.GetYaxis().SetRangeUser(1e-4, max(pass_max, fail_max)*1.1)
    h_pass.SetLineColor(ROOT.kRed)
    h_pass.SetLineWidth(3)
    h_pass.Draw("sames")

    h_fail.SetLineColor(ROOT.kBlue)
    h_fail.SetLineWidth(3)
    h_fail.Draw("sames")
    
    leg.AddEntry(h_pass, "Found at HLT")
    leg.AddEntry(h_fail, "Not Found at HLT")
    leg.Draw("same")

    ps.save(hist[:-1], other_c=c1)

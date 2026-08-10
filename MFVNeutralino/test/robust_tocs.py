#!/usr/bin/env python

import os
import ROOT
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

def make_eff_curve(fn, dirstr, hn, rebin, color=ROOT.kBlack):
    f = ROOT.TFile(fn)
    alpha = 1.0 - 0.6827
    use_effective = True
    h_num = f.Get(dirstr).Get(hn+'_num')
    h_den = f.Get(dirstr).Get(hn+'_den')

    h_num.Rebin(rebin)
    h_den.Rebin(rebin)

    h_rat = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)
    h_rat.SetLineWidth(2)
    h_rat.SetLineColor(color)
    h_rat.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())

    return h_rat

def make_ntagged_eff_curve(fn, numstr, denstr, color=ROOT.kBlack):
    f = ROOT.TFile(fn)
    h_num = f.Get(numstr).Get('h_calojet_ntagged')
    h_den = f.Get(denstr).Get('h_calojet_ntagged')

    h_num.Divide(h_num, h_den, 1, 1, "B")
    h_num.SetLineWidth(3)
    h_num.SetLineStyle(0)
    h_num.SetLineColor(color)
    h_num.SetDirectory(0)

    return h_num
    
set_style()
version = 'test'
ps = plot_saver(plot_dir('filter_tocs_%s' % version), size=(1000,800), pdf=False, log=False)

do_ntagged_tocs = False
filter_hist_dir = 'mfvFilterHistosNoCuts'
#filter_hist_dir = 'mfvFilterHistos5HLTCaloJet'

rb = 2

#prefix_17 = '/uscms_data/d3/shogan/crab_dirs/HistosULV9_dileptrigBm_2017_PreSuite_Feb08/'
prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV9_trigstudy_Bm_2016APV_FULL_PRESUITE_Feb19/'

fn = prefix + 'SingleMuon_2016APV.root'
gn = prefix + 'ttbar_2016APV.root'
#hn = prefix + 'MuonEG_2018.root'
#jn = prefix + 'ttbar_ll_2018.root'


colors = [ROOT.kRed, ROOT.kOrange+1, ROOT.kGreen+1, ROOT.kBlue, ROOT.kMagenta, ROOT.kViolet-1, ROOT.kBlack, ROOT.kGray+1]

x_labels = ['p_{T} of sub-leading calojet (GeV)', '', '', '',

            'p_{T} of 4th-leading calojet (GeV)', 'CaloHT(30) (GeV)', '', '', '', '', '', '', '', '',]


for i, hist in enumerate(['h_di_filter_00', 'h_di_filter_01', 'h_di_filter_02', 'h_di_filter_03',

             'h_tri_filter_00', 'h_tri_filter_01', 'h_tri_filter_02', 'h_tri_filter_03',
             'h_tri_filter_04', 'h_tri_filter_05', 'h_tri_filter_06', 'h_tri_filter_07',
             'h_tri_filter_08', 'h_tri_filter_09',

             'h_tri_symm_filter_00', 'h_tri_symm_filter_01', 'h_tri_symm_filter_02',

             'h_tri_skew_filter_00', 'h_tri_skew_filter_01', 'h_tri_skew_filter_02', 'h_tri_skew_filter_03', 'h_tri_skew_filter_04',

             'h_dd_dtk_filter_00', 'h_dd_dtk_filter_alt_d_00', 'h_dd_dtk_filter_01',# 'h_dd_dtk_filter_02', 'h_dd_dtk_filter_03', 'h_dd_dtk_filter_04',

             'h_dd_inc_filter_00', 'h_dd_inc_filter_alt_d_00', 'h_dd_inc_filter_01',# 'h_dd_inc_filter_02', 'h_dd_inc_filter_03',

             ]):

    c1 = ROOT.TCanvas('c1', '', 1000, 800)

    x_offset = 0.5
    y_offset = 0.15
    leg = ROOT.TLegend(0.10+x_offset, 0.12+y_offset, 0.38+x_offset, 0.33+y_offset)

    print(hist)

    try:
        rat_0 = make_eff_curve(fn, filter_hist_dir, hist, rb, colors[0])
        rat_1 = make_eff_curve(gn, filter_hist_dir, hist, rb, colors[3])
        #rat_2 = make_eff_curve(hn, filter_hist_dir, hist, rb, colors[1])
        #rat_3 = make_eff_curve(jn, filter_hist_dir, hist, rb, colors[4])
    
        rat_0.SetTitle('')
        rat_0.GetYaxis().SetRangeUser(0.0,1.05)
        rat_0.GetYaxis().SetTitle('efficiency')
    
        if (i < len(x_labels) and x_labels[i] != ''):
            rat_0.GetXaxis().SetTitle(x_labels[i])
    
    
        rat_0.Draw()
        rat_1.Draw("same")
        #rat_2.Draw("same")
        #rat_3.Draw("same")
    
        leg.AddEntry(rat_0, "MuonEG 2017")
        #leg.AddEntry(rat_2, "MuonEG no offline")
        leg.AddEntry(rat_1, "ttbar_ll MC")
        #leg.AddEntry(rat_3, "tt_dilep no offline")
        #leg.AddEntry(rat_0, "MuonEG ('18)")
        #leg.AddEntry(rat_2, "MuonEG ('17)")
        #leg.AddEntry(rat_1, "tt_dilep MC ('18)")
        #leg.AddEntry(rat_3, "ttbar MC ('17)")
        leg.Draw("same")
    
        ps.save(hist, other_c=c1)
    
    except:
        continue

if do_ntagged_tocs:
    num_dir = 'mfvJetTksHistosDijet650TrigOn'
    den_dir = 'mfvJetTksHistosDijet650TrigOff'

    c1 = ROOT.TCanvas('c1', '', 1000, 800)
    ROOT.gStyle.SetOptStat(0)

    x_offset = 0.5
    y_offset = 0.15
    leg = ROOT.TLegend(0.05+x_offset, 0.12+y_offset, 0.38+x_offset, 0.33+y_offset)

    rat_0 = make_ntagged_eff_curve(fn, num_dir, den_dir, colors[0])
    rat_1 = make_ntagged_eff_curve(gn, num_dir, den_dir, colors[1])
    rat_2 = make_ntagged_eff_curve(hn, num_dir, den_dir, colors[2])
    rat_3 = make_ntagged_eff_curve(jn, num_dir, den_dir, colors[3])
    rat_4 = make_ntagged_eff_curve(kn, num_dir, den_dir, colors[4])
    rat_5 = make_ntagged_eff_curve(ln, num_dir, den_dir, colors[5])
    rat_bkg_d = make_ntagged_eff_curve(bkg_d, num_dir, den_dir, colors[6])
    rat_bkg_s = make_ntagged_eff_curve(bkg_s, num_dir, den_dir, colors[7])

    rat_0.SetTitle('')
    rat_0.GetYaxis().SetRangeUser(0.0,1.05)
    rat_0.GetXaxis().SetRangeUser(0,10)
    rat_0.GetYaxis().SetTitle('efficiency')

    rat_0.Draw()
    rat_1.Draw("same")
    rat_2.Draw("same")
    rat_3.Draw("same")
    rat_4.Draw("same")
    rat_5.Draw("same")
    rat_bkg_d.Draw("same")
    rat_bkg_s.Draw("same")

    line = ROOT.TLine(2.0, 0.0, 2.0, 1.05)
    line.Draw("same")

    leg.AddEntry(rat_0, "tbs, 300GeV, 1mm")
    leg.AddEntry(rat_1, "tbs, 300GeV, 10mm")
    leg.AddEntry(rat_2, "dd, 300GeV, 1mm")
    leg.AddEntry(rat_3, "dd, 300GeV, 10mm")
    leg.AddEntry(rat_4, "H->SS, 55GeV, 1mm")
    leg.AddEntry(rat_5, "H->SS, 55GeV, 10mm")
    leg.AddEntry(rat_bkg_d, "SingleMuon")
    leg.AddEntry(rat_bkg_s, "MC Bkgd")
    leg.Draw("same")

    ps.save('h_calojet_ntagged', other_c=c1)

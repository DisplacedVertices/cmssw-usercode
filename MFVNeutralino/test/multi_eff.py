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

filenames = ['ggHToSSTodddd_tau1mm_M55_2017', 'mfv_neu_tau000300um_M0400_2017', 'ttbar_2017']
dirnames  = ['/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetSkinnyMinSel/',
             '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetSkinnyHalfSel/',
             '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetSkinnyFullSel/'
            ]

#colors = [ROOT.kRed, ROOT.kGreen+2, ROOT.kBlue]

garbage = []

ROOT.gStyle.SetOptStat(0)
ROOT.gPad.SetBottomMargin(500)
            
for fn in filenames:
    c1 = ROOT.TCanvas('c1', '', 1000, 800)
    c1.SetGridx()
    c1.SetTicky()

    # Python doesn't like looping over TH1's so we're doing this manually. >_>
    f_min = ROOT.TFile(dirnames[0] + fn + '.root')
    f_hlf = ROOT.TFile(dirnames[1] + fn + '.root')
    f_ful = ROOT.TFile(dirnames[2] + fn + '.root')

    h_min = f_min.Get(filter_hist_dir).Get('h_filt_nsurvive')
    h_hlf = f_hlf.Get(filter_hist_dir).Get('h_filt_nsurvive')
    h_ful = f_ful.Get(filter_hist_dir).Get('h_filt_nsurvive')
    
    min_frac = h_min.Clone()
    hlf_frac = h_hlf.Clone()
    ful_frac = h_ful.Clone()

    for pair in [[min_frac, h_min, ROOT.kRed], [hlf_frac, h_hlf, ROOT.kGreen+2], [ful_frac, h_ful, ROOT.kBlue]]:
        nbins = pair[1].GetNbinsX()

        for i in range(1, nbins + 1):
            if i==1:
              pair[0].SetBinContent(i, 1.0)
              pair[0].SetBinError(i, 0.001)
            else:
              num = pair[1].GetBinContent(i)
              den = pair[1].GetBinContent(i-1)
              eff = num/den
              pair[0].SetBinContent(i, eff)
              pair[0].SetBinError(i, eff*(1-eff)/num)

        pair[0].GetYaxis().SetRangeUser(0, 1.05)
        pair[0].SetLineWidth(3)
        pair[0].SetLineColor(pair[2])
        pair[0].GetYaxis().SetTitle('eff. relative to prev step')
        pair[0].Draw('same')

    ps.save(fn, other_c=c1)

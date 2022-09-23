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

#fn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetTest4/mfv_neu_tau000300um_M0400_2017.root'    # Black curve
#zn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetTest4/ggHToSSTodddd_tau1mm_M40_2017.root'    # Red curve


#fn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetSkinny11/mfv_combined.root'
#color = ROOT.kViolet

fn = 'histos.root'
#fn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetSkinny11/ggh_combined.root'
color = ROOT.kRed

#fn = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetSkinny11/ttbar_2017.root'
#color = ROOT.kBlue

f = ROOT.TFile(fn)
t = f.Get(filter_hist_dir)

for hist in ['h_filter_07', 'h_filter_08', 'h_filter_09', 'h_filter_10', 'h_filter_11']:


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
    t_rat.GetXaxis().SetTitle('jet p_{T} (GeV)')

    t_rat.Draw()
    
    new_axis = ROOT.TGaxis(t_rat.GetXaxis().GetXmax(), 0, t_rat.GetXaxis().GetXmax(), 1.05, 0, 1.05*tmp_ymax, 510, '+L');
    new_axis.SetLabelColor(color)
    new_axis.SetLineColor(color)

    t_num.Scale(1.0/tmp_ymax)
    t_num.Draw('same')
    t_num.SetLineColor(color+3)
    t_num.SetFillColor(color+3)
    t_num.SetLineWidth(3)

    t_den.Scale(1.0/t_den.GetMaximum())
    t_den.Draw('same')
    t_den.SetLineColor(color)
    t_den.SetLineWidth(3)

    new_axis.Draw('same')

    ps.save(hist, other_c=c1)


# Now, draw the original filterflow hist, and then construct+draw the fractional version
ROOT.gStyle.SetOptStat(0)
ROOT.gPad.SetBottomMargin(500)
c2 = ROOT.TCanvas('c2', '', 1000, 800)
c2.SetGridx()
c2.SetTicky()
c2.SetTickx()

h_surv_orig = t.Get('h_filt_nsurvive')
h_surv_orig.SetLineWidth(3)
h_surv_orig.SetLineColor(color)
h_surv_orig.Draw()
ps.save('h_surv_orig', other_c=c2)

nbins = h_surv_orig.GetNbinsX()
nbins = h_surv_orig.GetNbinsX()
print(nbins)

h_surv_frac = h_surv_orig.Clone()

for i in range(1, nbins + 1):
    if i==1:
      h_surv_frac.SetBinContent(i, 1.0)
      h_surv_frac.SetBinError(i, 0.001)
    else:
      num = h_surv_orig.GetBinContent(i)
      den = h_surv_orig.GetBinContent(i-1)
      eff = num/den
      h_surv_frac.SetBinContent(i, eff)
      h_surv_frac.SetBinError(i, eff*(1-eff)/num)

h_surv_frac.GetYaxis().SetRangeUser(0, 1.05)
h_surv_frac.SetLineWidth(3)
h_surv_frac.SetLineColor(color)
h_surv_frac.GetYaxis().SetTitle('eff. relative to prev step')
h_surv_frac.Draw()
ps.save('h_surv_frac', other_c=c2)





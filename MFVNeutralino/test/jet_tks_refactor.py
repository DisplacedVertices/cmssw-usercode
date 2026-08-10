#!/usr/bin/env python

import os
import ROOT
from JMTucker.Tools.ROOTTools import *
from JMTucker.MFVNeutralino.PerSignal import PerSignal

ROOT.gStyle.SetOptStat(0)

######################################################################################################################### 

def make_eff_curve(fn, dirstr, h_pfx, den, num, rebin, color=ROOT.kBlack):
    f = ROOT.TFile(fn)
    alpha = 1.0 - 0.6827
    use_effective = True
    print(fn)
    h_den = f.Get(dirstr).Get(h_pfx+'_'+den)
    h_num = f.Get(dirstr).Get(h_pfx+'_'+num)

    h_num.Rebin(rebin)
    h_den.Rebin(rebin)

    h_rat = histogram_divide(h_num, h_den, confint_params=(alpha,), use_effective=use_effective)
    h_rat.SetLineWidth(2)
    h_rat.SetLineColor(color)
    h_rat.GetXaxis().SetTitle(h_num.GetXaxis().GetTitle())

    return h_rat

######################################################################################################################### 

def are_compatible_q(eff_dat, err_dat, eff_sim, err_sim):
    # err_dat = [low_err, high_err]
    if eff_dat > eff_sim:
        return (eff_dat - err_dat[0]) < (eff_sim + err_sim[1])
    else:
        return (eff_sim - err_sim[0]) < (eff_dat + err_dat[1])
   
######################################################################################################################### 

fdir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_PTV_RedoRefactor_SignalMC_Aug23/'
#fdir = '/uscms/homes/s/shogan/work/mfv_10627/src/JMTucker/MFVNeutralino/test/'
flist = os.listdir(fdir)
flist.sort()

for fname in flist:
    if not fname.endswith('root'):
        continue

    f = ROOT.TFile(fdir+fname)

    h_nom = f.Get('mfvJetTksHistosLowHtNoCuts').Get('h_calojet_npassprompt')
    h_ref = f.Get('mfvJetTksHistosLowHtRefactor').Get('h_calojet_npassprompt')

    n_nom = h_nom.Integral(3, 9999)
    n_ref = h_ref.Integral(3, 9999)

    err = 100*(1-n_nom/n_ref)
    #err = 100* abs(n_nom - n_ref)/(0.5*(n_nom + n_ref))

    print('{0: >s}    {1: <8.1f}    {2: <8.1f}     {3: >8.1f}'.format(fname[0:-5], n_nom, n_ref, abs(err)))

#!/usr/bin/env python

import os
import ROOT
import numpy as np
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

ROOT.gROOT.SetBatch() # don't pop up canvases

def get_eff_and_err(fn, num_dir, den_dir, hist_dir):
    den_fn = den_dir + fn
    num_fn = num_dir + fn

    if (not os.path.exists(num_fn)) or (not os.path.exists(den_fn)):
        return -1.0, -1.0

    num_f = ROOT.TFile(num_fn)
    den_f = ROOT.TFile(den_fn)
    
    den_n = den_f.Get('mfvEventHistosNoCuts').Get('h_w').Integral()
    #den_n = den_f.Get(hist_dir).Get('h_w').Integral()
    num_n = num_f.Get(hist_dir).Get('h_w').Integral()

    #print(round(num_n), round(den_n))
    eff = round(num_n/den_n, 4)
    err = round(eff*(1-eff)/np.sqrt(den_n), 4)

    return eff, err


#num_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_TrigStudy_July10_AnalysisCutsTrigBitOn/'
#den_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_TrigStudy_July10_AnalysisCutsTrigBitOff/'
num_dir = '/uscms/home/pkotamni/nobackup/crabdirs/HistosU17LV9_redo_Bm_noef/'
den_dir = '/uscms/home/pkotamni/nobackup/crabdirs/HistosU17LV9_redo_Bm_noef/'
hist_dir = 'mfvEventHistosPreSel'


#samples = ['stopdbardbar',]
samples = ['neu', 'stopdbardbar', 'stopbbarbbar']
ctaus  = ['000100', '000300', '001000', '010000', '03000']
masses = ['1200', '0300', '0400', '0600', '0800']

for sample in samples:
    for ctau in ctaus:
        for mass in masses:
            fn = 'mfv_{}_tau{}um_M{}_2017.root'.format(sample, ctau, mass)
            eff, err = get_eff_and_err(fn, num_dir, den_dir, hist_dir)
            if (eff < 0) or (err < 0):
                continue
            print 'File: {}    eff:{} +/- {}'.format(fn, eff, err)
    print('\n')



higgs_ctaus_um = ['1', '3']
higgs_ctaus_mm = ['1', '10', '3', '30']
higgs_ctaus = ['1', '3', '10']

"""
for ctau in higgs_ctaus_um:
    fn = 'WplusHToSSTodddd_tau{}00um_M55_2017.root'.format(ctau)
    eff, err = get_eff_and_err(fn, num_dir, den_dir, hist_dir)
    if (eff < 0) or (err < 0):
        continue
    print 'File: {}    eff:{} +/- {}'.format(fn, eff, err)

for ctau in higgs_ctaus_mm:
    fn = 'WplusHToSSTodddd_tau{}mm_M55_2017.root'.format(ctau)
    eff, err = get_eff_and_err(fn, num_dir, den_dir, hist_dir)
    if (eff < 0) or (err < 0):
        continue
    print 'File: {}    eff:{} +/- {}'.format(fn, eff, err)

"""
"""
for ctau in higgs_ctaus:
    fn = 'ggHToSSTodddd_tau{}mm_M55_2017.root'.format(ctau)
    eff, err = get_eff_and_err(fn, num_dir, den_dir, hist_dir)
    if (eff < 0) or (err < 0):
        continue
    print 'File: {}    eff:{} +/- {}'.format(fn, eff, err)
"""

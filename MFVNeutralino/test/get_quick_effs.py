#!/usr/bin/env python

import os
import ROOT
import numpy as np
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

# For HT(30) dists, xbin=33 corresponds to HT's starting at 320GeV
#                   xbin=41 corresponds to HT's starting at 400GeV ("nominal")
#                   xbin=43 corresponds to HT's starting at 420GeV

def get_effs_and_yield(fn, dirstr, hn):
    yields    = []
    effs_tot  = [] # Efficiencies wrt total number of starting events (passing, say, L1)
    effs_cut  = [] # Efficiencies wrt number that survive whatever offline cut we apply
    errs_tot  = []
    errs_cut  = []
    f = ROOT.TFile(fn)
    
    h_num = f.Get(dirstr).Get(hn+'_num')
    h_den = f.Get(dirstr).Get(hn+'_den')
    
    nnom = h_num.Integral(61,99999)
    ntot = h_den.Integral()
    for xbin in range(56,64):
        nden = h_den.Integral(xbin, 99999)
        nnum = h_num.Integral(xbin, 99999)

        effs_tot.append(round(nnum/ntot, 3))
        effs_cut.append(round(nnum/nden, 3))

        errs_tot.append(error_on_eff(nnum, ntot))
        errs_cut.append(error_on_eff(nnum, nden))
        yields.append(round(nnum/nnom, 3))

    return effs_tot, effs_cut, errs_tot, errs_cut, yields

def error_on_eff(nnum, nden):
    eff = nnum/nden
    err = np.sqrt(eff * (1-eff)/nden)
    return round(err, 3)
    
filter_hist_dir = 'mfvEventHistosFullSel'

prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_PTV_RedoRefactor_SignalMC_Aug23/'
flist = os.listdir(prefix)
flist.sort()


#names = ['neu->tbs, 1mm, M200', 'neu->tbs, 10mm, M200', 'stop->dd, 1mm, M300', 'stop->dd, 10mm, M300', 'H->SS->4d, 1mm, M55', 'H->SS->4d, 10mm, M55']

for hist in ['h_npu']:
    for i, f_name in enumerate(flist):
        if not f_name.endswith('.root'):
            continue
        out_dict = {}
        out_dict['name'] = f_name[:-5]
        effs_f_tot, effs_f_cut, errs_f_tot, errs_f_cut, yields_f = get_effs_and_yield(prefix+f_name, filter_hist_dir, hist)
        out_dict['effs_tot'] = effs_f_tot
        out_dict['effs_cut'] = effs_f_cut
        out_dict['errs_tot'] = errs_f_tot
        out_dict['errs_cut'] = errs_f_cut
        out_dict['yields']   = yields_f
        print out_dict

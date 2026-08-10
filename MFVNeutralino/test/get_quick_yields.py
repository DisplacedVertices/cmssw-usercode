#!/usr/bin/env python

import os
import ROOT
import pprint
import numpy as np
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

# For HT(30) dists, xbin=33 corresponds to HT's starting at 320GeV
#                   xbin=41 corresponds to HT's starting at 400GeV ("nominal")
#                   xbin=43 corresponds to HT's starting at 420GeV

def get_yield(fn, dirstr, hn):
    f = ROOT.TFile(fn)
    h = f.Get(dirstr).Get(hn)
    ntot = round(h.Integral())

    return ntot

def spaces(n):
    outstr = ''
    for i in range(n):
        outstr += ' '

    return outstr

out_dict = {}

fullsel_dir = 'mfvEventHistosFullSel'
notrig_dir  = 'mfvEventHistosFullSelNoTrig'

calo_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV9Bm_CaloPlateaus_Jan08/'
pf_prefix   = '/uscms_data/d3/shogan/crab_dirs/HistosULV9Bm_DataPlateaus_Jan08/'

flist = os.listdir(pf_prefix)
flist.sort()

#names = ['neu->tbs, 1mm, M200', 'neu->tbs, 10mm, M200', 'stop->dd, 1mm, M300', 'stop->dd, 10mm, M300', 'H->SS->4d, 1mm, M55', 'H->SS->4d, 10mm, M55']

#print 'File Name {0}   Calo Yield {1}    PF Yield {2}'.format(spaces(22), spaces(6), spaces(6))
for hist in ['h_npu']:
    for i, f_name in enumerate(flist):
        if not f_name.endswith('.root'):
            continue
        sub_dict = {}
        calo_full_yield = get_yield(calo_prefix + f_name, fullsel_dir, hist)
        pf_full_yield   = get_yield(pf_prefix + f_name,   fullsel_dir, hist)

        calo_notrig_yield = get_yield(calo_prefix + f_name, notrig_dir, hist)
        pf_notrig_yield   = get_yield(pf_prefix + f_name,   notrig_dir, hist)

        rat = round(pf_full_yield/calo_full_yield, 3)
        err = round((np.sqrt(abs(pf_full_yield - calo_full_yield)))/calo_full_yield, 3)

        calo_trig_eff = calo_full_yield/calo_notrig_yield
        pf_trig_eff   = pf_full_yield/pf_notrig_yield
        trig_eff_rat  = pf_trig_eff/calo_trig_eff
        trig_eff_err  = np.sqrt(abs(pf_full_yield - calo_full_yield))/calo_notrig_yield

        #print '{0}   {1: <7}             {2: <7}         {3: <4} +- {4: <4} '.format(f_name[:-5], calo_full_yield, pf_full_yield, rat, err)
        sub_dict['ratio'] = rat
        sub_dict['err']   = err
        sub_dict['trig_ratio'] = trig_eff_rat
        sub_dict['trig_err']   = trig_eff_err
        sub_dict['trig_eff_calo'] = calo_trig_eff
        sub_dict['trig_eff_pf']   = pf_trig_eff
        out_dict[f_name[:-5]] = sub_dict

pprint.pprint(out_dict)

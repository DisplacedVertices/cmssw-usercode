#!/usr/bin/env python

import os, sys, re
import ROOT
import numpy as np
import pprint
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

def get_yield(fn, dirstr, hn):
    f = ROOT.TFile(fn)
    h = f.Get(dirstr).Get(hn)
    ntot = h.Integral() + h.GetBinContent(0) + h.GetBinContent(h.GetNbinsX()+1)
    return ntot

csv_prefix          = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BtaggerYieldStudy_CSV_Sept19/'
deepcsv_prefix      = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BtaggerYieldStudy_DeepCSV_Sept19/'
deepflav_prefix     = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BtaggerYieldStudy_DeepFlav_Sept19/'
deepflav_den_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BtaggerYieldStudy_DeepFlav_TrigOff_Sept22/'

ctaus  = ['000100', '000300', '001000', '010000', '030000']
masses = ['0200', '0300', '0400', '0600', '0800']

flist = ['mfv_stopdbardbar_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['mfv_stopbbarbbar_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['mfv_neu_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['ggHToSSTodddd_tau1mm_M55_2017.root', 'ggHToSSTodddd_tau10mm_M55_2017.root', 'ggHToSSTodddd_tau100mm_M55_2017.root']

if __name__ == '__main__' and not hasattr(sys, 'argv'):
    csv_dict      = {}
    deepcsv_dict  = {}
    deepflav_dict = {}
    deepflav_eff_dict = {}
    
    for fname in flist:
        if not fname.endswith('.root'):
            continue
    
        if not os.path.isfile(csv_prefix+fname):
            csv_dict[fname[:-5]]      = None
            deepcsv_dict[fname[:-5]]  = None
            deepflav_dict[fname[:-5]] = None
            continue
    
        csv_yield          = get_yield(csv_prefix + fname, 'mfvEventHistosFullSel', 'h_npv')
        deepcsv_yield      = get_yield(deepcsv_prefix + fname, 'mfvEventHistosFullSel', 'h_npv')
        deepflav_yield     = get_yield(deepflav_prefix + fname, 'mfvEventHistosFullSel', 'h_npv')
        deepflav_den_yield = get_yield(deepflav_den_prefix + fname, 'mfvEventHistosFullSel', 'h_npv')
    
        csv_dict[fname[:-5]]      = round(csv_yield, 3)
        deepcsv_dict[fname[:-5]]  = round(deepcsv_yield, 3)
        deepflav_dict[fname[:-5]] = round(deepflav_yield, 3)
        deepflav_eff_dict[fname[:-5]] = round(deepflav_yield/deepflav_den_yield, 3)
    
        
    pprint.pprint(deepflav_eff_dict)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'trigeff' in sys.argv:

    default_dict = {'CSV':     {'Loose': [None, None], 'Medium': [None, None],  'Tight': [None, None]},
                    'DeepCSV': {'Loose': [None, None], 'Medium': [None, None],  'Tight': [None, None]},
                    'DeepJet': {'Loose': [None, None], 'Medium': [None, None],  'Tight': [None, None]}}
    den_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BtaggerYieldStudy_TrigOff_Sept25/'
    num_dir = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_BtaggerYieldStudy_TrigOn_Sept25/'

    out_dict = {}

    for fname in flist:
        if not os.path.isfile(den_dir + fname):
            out_dict[fname[:-5]] = default_dict
            continue
        tag_dict = {}
        for tagger in ['CSV', 'DeepCSV', 'DeepJet']:
                wp_dict = {}
                for wp in ['Loose', 'Medium', 'Tight']:
                   num = get_yield(num_dir + fname, 'mfvEventHistos'+tagger+wp, 'h_npv')
                   den = get_yield(den_dir + fname, 'mfvEventHistos'+tagger+wp, 'h_npv')
    
                   eff = round(num/den, 5)
                   err = round((np.sqrt(eff * (1-eff)/den)) ,5)
                   wp_dict[wp] = [eff, err]
                tag_dict[tagger] = wp_dict
        out_dict[fname[:-5]] = tag_dict 

    pprint.pprint(out_dict)

#!/usr/bin/env python

import os
import ROOT
import pprint
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

t_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_HLT_Offline_Study_Redo_FlagTrue_Oct17/'
f_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_HLT_Offline_Study_Redo_FlagFalse_Oct17/'

hist_dir  = 'mfvJetTksHistosPreSel'
hist_name = 'h_satisfies_online_tags'

# want bin 2

ctaus  = ['000100', '000300', '001000', '010000', '030000']
masses = ['0200', '0300', '0400', '0600', '0800']

flist = ['mfv_stopdbardbar_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['mfv_stopbbarbbar_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['mfv_neu_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['ggHToSSTodddd_tau1mm_M55_2017.root', 'ggHToSSTodddd_tau10mm_M55_2017.root', 'ggHToSSTodddd_tau100mm_M55_2017.root']

big_dict = {}

for fname in flist:
    if not fname.endswith('.root'):
        continue

    if not os.path.isfile(t_prefix+fname):
        #print '{0}     None'.format(fname[:-5])
        continue

    f_t = ROOT.TFile(t_prefix + fname)
    f_f = ROOT.TFile(f_prefix + fname)
    

    y_t = f_t.Get(hist_dir).Get(hist_name).GetBinContent(2)
    y_f = f_f.Get(hist_dir).Get(hist_name).GetBinContent(2)

    try:
        big_dict[fname[0:-5]] = round(y_t/y_f, 4)
        #print "{0}   {1}".format(fname, y_t/y_f)
    except:
        big_dict[fname[0:-5]] = 1.0
        #print "{0}   1.0".format(fname)


pprint.pprint(big_dict)

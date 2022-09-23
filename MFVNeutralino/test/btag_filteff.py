#!/usr/bin/env python

import os
import numpy as np
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal


prefix  = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetQS0/'
prefix  = '/uscms_data/d3/shogan/crab_dirs/HistosV30TmTriBjetDflt/'
files   = ['mfv_neu_tau000300um_M0400_2017', 'mfv_neu_tau001000um_M0400_2017', 'mfv_neu_tau000300um_M0600_2017', 'ggHToSSTodddd_tau1mm_M40_2017', 'ggHToSSTodddd_tau1mm_M55_2017']

for fn in files:
    
    oneVtxs = []
    twoVtxs = []


    f = ROOT.TFile(prefix+fn+'.root')
    hf = f.Get('mfvEventHistosPreSel').Get('h_filter_bits')
    btag_eff = hf.GetBinContent(8) / hf.GetBinContent(1)

    for one_tk_dir in ['Ntk3mfvEventHistosOnlyOneVtx', 'Ntk4mfvEventHistosOnlyOneVtx', 'mfvEventHistosOnlyOneVtx']:
        gf = f.Get(one_tk_dir).Get('h_filter_bits')
        oneVtxs.append([gf.GetBinContent(8), gf.GetBinContent(1)])

    for two_tk_dir in ['Ntk3mfvEventHistosFullSel', 'Ntk4mfvEventHistosFullSel', 'mfvEventHistosFullSel']:
        gf = f.Get(two_tk_dir).Get('h_filter_bits')
        twoVtxs.append([gf.GetBinContent(8), gf.GetBinContent(1)])


    effs = []
    errs = []

    for i in range(0,3):

        eff_t = 0.0
        err_t = 0.0

        eff_o = oneVtxs[i][0]/oneVtxs[i][1]
        err_o = np.sqrt(eff_o * (1-eff_o) / oneVtxs[i][1])

        if twoVtxs[i][1] > 0.1:
            eff_t = twoVtxs[i][0]/twoVtxs[i][1]
            err_t = np.sqrt(eff_t * (1-eff_t) / twoVtxs[i][1])

        effs.append(eff_o)
        effs.append(eff_t)
        
        errs.append(err_o)
        errs.append(err_t)

    print('\n')
    print(fn)
    print('--------------------------------------')
    print('Agnostic:             %4.3f \n'        % (btag_eff))
    print('                  3tk            4tk           5tk' )
    print("One-vtx:      %4.3f+-%4.3f   %4.3f+-%4.3f  %4.3f+-%4.3f"  % (effs[0], errs[0], effs[2], errs[2], effs[4], errs[4]))
    print("Two-vtx:      %4.3f+-%4.3f   %4.3f+-%4.3f  %4.3f+-%4.3f"  % (effs[1], errs[1], effs[3], errs[3], effs[5], errs[5]))

#!/usr/bin/env python

import os, sys, re
import ROOT
import numpy as np
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

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

def get_lifetime(fn):   # return ctau in um
    mo = re.search(r'(tau)(\d{1,6})([um]m)', fn)
    assert mo
    ctau, unit = int(mo.groups()[1]), mo.groups()[2]
    if unit == 'mm':
        ctau *= 1000
    return ctau

def rough_track_uncert(ctau):
    err_dict = {100: 37.0, 300: 34.0, 1000: 13.0, 10000: 2.0, 30000: 3.0, 100000: 8.0}
    return err_dict[ctau]

# Some parameters for now.
btag_uncert_addl  = 8.9
dijet_kine_uncert_rpv = 5.0
dijet_kine_uncert_higgs = 5.0

hist_dir = 'mfvEventHistosFullSel'

nom_prefix =      '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_PTV_RedoRefactor_SignalMC_Aug23/'
b_agnost_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_SignalMCHists_BjetAgnostic_Aug24/'
d_agnost_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_SignalMCHists_DijetAgnostic_Aug24/'
d_agnost_notrig_prefix = '/uscms_data/d3/shogan/crab_dirs/HistosULV4Bm_SignalMCHists_DijetAgnostic_NoTrig_Aug28/'
flist = os.listdir(nom_prefix)
flist.sort()

ctaus  = ['000100', '000300', '001000', '010000', '030000']
masses = ['0200', '0300', '0400', '0600', '0800']

flist = ['mfv_stopdbardbar_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['mfv_stopbbarbbar_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['mfv_neu_tau' + ctau + 'um_M' + mass + '_2017.root' for mass in masses for ctau in ctaus]
flist += ['ggHToSSTodddd_tau1mm_M55_2017.root', 'ggHToSSTodddd_tau10mm_M55_2017.root', 'ggHToSSTodddd_tau100mm_M55_2017.root']
print flist

for hist in ['h_npu']:
    for i, f_name in enumerate(flist):
        if not f_name.endswith('.root'):
            continue
        if not os.path.isfile(nom_prefix+f_name):
            print '{0}     None'.format(f_name[:-5])
            continue
        ctau = get_lifetime(f_name)
        nom_yield = get_yield(nom_prefix+f_name, hist_dir, hist)

        btag_num = get_yield(d_agnost_prefix+f_name, hist_dir, hist)
        btag_den = get_yield(d_agnost_notrig_prefix+f_name, hist_dir, hist)
        btag_uncert = 100*(1.0 - btag_num/btag_den)

        if (ctau >= 10000) or ('ggHToSSTodddd_tau1mm' in f_name):   # dijet triggers are dominant here
            num_p = get_yield(b_agnost_prefix+f_name, hist_dir, hist)
            err_p = np.hypot(dijet_kine_uncert_rpv, rough_track_uncert(ctau))

            num_s = nom_yield - num_p
            err_s = np.hypot(btag_uncert, btag_uncert_addl)

        else:  # bjet triggers are dominant
            num_p = get_yield(d_agnost_prefix+f_name, hist_dir, hist)
            err_p = np.hypot(btag_uncert, btag_uncert_addl)

            num_s = nom_yield - num_p
            err_s = np.hypot(dijet_kine_uncert_rpv, rough_track_uncert(ctau))


        delta_p = num_p * (err_p / 100.0)
        delta_s = num_s * (err_s / 100.0)

        delta_t = np.hypot(delta_p, delta_s)
        err_t   = round(delta_t/nom_yield, 5)

        print '{0}   {1: >7}'.format(f_name[:-5], err_t*100)

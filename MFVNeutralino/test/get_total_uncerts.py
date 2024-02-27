#!/usr/bin/env python

import os, sys, re
import ROOT
import numpy as np
import pprint
from JMTucker.Tools.ROOTTools import *
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

# Generic function to get yield for any histogram
def get_yield(fn, dirstr, hn):
    f = ROOT.TFile(fn)
    h = f.Get(dirstr).Get(hn)
    ntot = h.Integral() + h.GetBinContent(0) + h.GetBinContent(h.GetNbinsX()+1)
    return ntot

# Get uncertainty related to INefficiency of signal (bjet trigs)
def get_bjet_inefficiency_uncert(fn):
    trig_path   = 'mfvEventHistosDijetAgnosticTrigOn'
    notrig_path = 'mfvEventHistosDijetAgnosticTrigOff'
    num = get_yield(fn, trig_path, 'h_npv')
    den = get_yield(fn, notrig_path, 'h_npv')

    return round((1.0-(num/den)), 5)


# Get uncertainty pertaining to btagging scale factors and how
# that might effect signal yield.
def get_bjet_scale_factor_uncert(fn):
    nom_path   = 'mfvEventHistosDijetAgnosticTrigOn'
    vup_path   = 'mfvEventHistosDijetAgnosticTrigOnSFVarUp'
    vdn_path   = 'mfvEventHistosDijetAgnosticTrigOnSFVarDn'
    nom = get_yield(fn, nom_path, 'h_npv')
    vup = get_yield(fn, vup_path, 'h_npv')
    vdn = get_yield(fn, vdn_path, 'h_npv')

    delta_up = round(abs(1.0 - vup/nom), 5)
    delta_dn = round(abs(1.0 - vdn/nom), 5)

    out_dict = {'down': delta_dn, 'up': delta_up}

    return out_dict


# Get uncertainty pertaining to JER and how
# that might effect signal yield.
def get_jer_correction_uncert(fn):
    nom_path   = 'mfvEventHistosFullSel'
    vup_path   = 'mfvEventHistosFullSelUpJER'
    vdn_path   = 'mfvEventHistosFullSelDnJER'
    nom = get_yield(fn, nom_path, 'h_npv')
    vup = get_yield(fn, vup_path, 'h_npv')
    vdn = get_yield(fn, vdn_path, 'h_npv')

    delta_up = round(abs(1.0 - vup/nom), 5)
    delta_dn = round(abs(1.0 - vdn/nom), 5)

    out_dict = {'down': delta_dn, 'up': delta_up}

    return out_dict

# Get uncertainty pertaining to JES and how
# that might effect signal yield.
def get_jes_correction_uncert(fn):
    nom_path   = 'mfvEventHistosFullSel'
    vup_path   = 'mfvEventHistosFullSelUpJES'
    vdn_path   = 'mfvEventHistosFullSelDnJES'
    nom = get_yield(fn, nom_path, 'h_npv')
    vup = get_yield(fn, vup_path, 'h_npv')
    vdn = get_yield(fn, vdn_path, 'h_npv')

    delta_up = round(abs(1.0 - vup/nom), 5)
    delta_dn = round(abs(1.0 - vdn/nom), 5)

    out_dict = {'down': delta_dn, 'up': delta_up}

    return out_dict

# Get uncertainty related to INefficiency of signal (kinematic bit of disp. dijet)
# Since there are two dijet paths w/ different thresholds, just take the max uncert
def get_dijet_kine_ineff_uncert(fn):
    lo_ht_path = 'mfvFilterHistosLowHTPreSel'
    hi_ht_path = 'mfvFilterHistosHighHTPreSel'

    lo_num = get_yield(fn, lo_ht_path, 'h_dd_dtk_filter_01_num')
    lo_den = get_yield(fn, lo_ht_path, 'h_dd_dtk_filter_00_den')

    hi_num = get_yield(fn, hi_ht_path, 'h_dd_inc_filter_01_num')
    hi_den = get_yield(fn, hi_ht_path, 'h_dd_inc_filter_00_den')

    try:
        lo_uncert = 1.0-(lo_num/lo_den)
    except ZeroDivisionError:
        lo_uncert = 0.0

    try:
        hi_uncert = 1.0-(hi_num/hi_den)
    except ZeroDivisionError:
        hi_uncert = 0.0

    return round(max(lo_uncert, hi_uncert), 5)

# Get uncertainty related to correctly counting offline prompt/non-prompt tracks
def get_dijet_offline_track_uncert(fn):
    f = ROOT.TFile(fn)
    nom_path = 'mfvJetTksHistosLowHtRefactor'
    ref_path = 'mfvJetTksHistosLowHtRefactor2'
    hname = 'h_calojet_npassprompt'

    # Need to get yields differently, so we won't use get_yield()
    h_nom = f.Get(nom_path).Get(hname)
    h_ref = f.Get(ref_path).Get(hname)
    nom_yield = h_nom.Integral(3, 9999)
    ref_yield = h_ref.Integral(3, 9999)

    return round((1.0-(nom_yield/ref_yield)), 5)

# Get uncertainty related to online tracking behaviors
def get_dijet_hlt_track_uncert(fn):
    f = ROOT.TFile(fn)
    nom_path = 'mfvJetTksHistosLowHtNominal'
    ref_path = 'mfvJetTksHistosLowHtRefactor'
    hname = 'h_calojet_npassprompt'

    # Need to get yields differently, so we won't use get_yield()
    h_nom = f.Get(nom_path).Get(hname)
    h_ref = f.Get(ref_path).Get(hname)
    nom_yield = h_nom.Integral(3, 9999)
    ref_yield = h_ref.Integral(3, 9999)

    return round((1.0-(ref_yield/nom_yield)), 5)

# Get uncertainty related to differences in HLT btagging between data and MC
def get_hlt_btagging_uncert(fn):
    f = ROOT.TFile(fn)
    nom_path = 'mfvJetTksHistosHLTBtagStudyNom'
    var_path = 'mfvJetTksHistosHLTBtagStudyVar'

    # Need to get yields differently, so we won't use get_yield()
    h_nom = f.Get(nom_path).Get('h_satisfies_online_tags')
    h_var = f.Get(var_path).Get('h_satisfies_online_tags')
    nom_yield = h_nom.GetBinContent(2)
    var_yield = h_var.GetBinContent(2)

    try:
        out_uncert = round((1.0-(nom_yield/var_yield)), 5)
    except:
        out_uncert = 0.0

    return out_uncert


def bjet_is_primary_q(bjet_uncerts, dijet_uncerts):
    return bjet_uncerts < dijet_uncerts

# Uncertainties which don't change per sample
bjet_data_mc_kine_uncert       = .02  # THIS IS A PLACEHOLDER! FIXME
#bjet_data_mc_uncert       = .093
dijet_kine_data_mc_uncert = .005

ctaus  = ['000100', '000300', '001000', '010000', '030000']
masses = ['0200', '0300', '0400', '0600', '0800']

flist = []
flist += ['mfv_stopdbardbar_tau' + ctau + 'um_M' + mass + '_2016APV.root' for mass in masses for ctau in ctaus]
flist += ['mfv_stopbbarbbar_tau' + ctau + 'um_M' + mass + '_2016APV.root' for mass in masses for ctau in ctaus]
flist += ['mfv_neu_tau' + ctau + 'um_M' + mass + '_2016APV.root' for mass in masses for ctau in ctaus]
flist += ['ggHToSSTodddd_tau1mm_M55_2016APV.root', 'ggHToSSTodddd_tau10mm_M55_2016APV.root', 'ggHToSSTodddd_tau100mm_M55_2016APV.root']
flist = ['histos.root']

#dirname  = '/uscms_data/d3/shogan/crab_dirs/HistosULV9Bm_2016APV_UNCERTS_NewOfflineReqs_Feb22/'
dirname  = './'

big_dict = {}

for fname in flist:
    logical_name = dirname+fname
    if not fname.endswith('.root'):
        continue

    if not os.path.isfile(logical_name):
        #print '{0}     None'.format(fname[:-5])
        continue

    sub_dict = {}

    dijet_hlt_track_uncert = get_dijet_hlt_track_uncert(logical_name)
    dijet_off_track_uncert = get_dijet_offline_track_uncert(logical_name)
    dijet_kine_uncert      = get_dijet_kine_ineff_uncert(logical_name)
    bjet_signal_uncert     = get_bjet_inefficiency_uncert(logical_name)
    bjet_tag_sf_uncert     = get_bjet_scale_factor_uncert(logical_name)
    bjet_hlt_tag_uncert    = get_hlt_btagging_uncert(logical_name)
    jer_uncert             = get_jer_correction_uncert(logical_name)
    jes_uncert             = get_jes_correction_uncert(logical_name)

    sub_dict['tracking_hlt']    = dijet_hlt_track_uncert
    sub_dict['tracking_count']  = dijet_off_track_uncert
    sub_dict['dijet_kine']  = dijet_kine_uncert
    sub_dict['bjet_signal'] = bjet_signal_uncert
    sub_dict['bjet_sf_dn']  = bjet_tag_sf_uncert['down']
    sub_dict['bjet_sf_up']  = bjet_tag_sf_uncert['up']
    sub_dict['bjet_hlt']    = bjet_hlt_tag_uncert
    sub_dict['jer_dn']      = jer_uncert['down']
    sub_dict['jer_up']      = jer_uncert['up']
    sub_dict['jes_dn']      = jes_uncert['down']
    sub_dict['jes_up']      = jes_uncert['up']

    avg_bjet_tag_sf_uncert = (bjet_tag_sf_uncert['down'] + bjet_tag_sf_uncert['up']) / 2.0
    avg_jer_uncert = (jer_uncert['down'] + jer_uncert['up']) / 2.0
    avg_jes_uncert = (jes_uncert['down'] + jes_uncert['up']) / 2.0

    sub_dict['bjet_sf_avg'] = avg_bjet_tag_sf_uncert
    sub_dict['jer_avg'] = avg_jer_uncert
    sub_dict['jes_avg'] = avg_jes_uncert

    total_dijet_uncert = np.sqrt(dijet_off_track_uncert**2 + dijet_hlt_track_uncert**2 + dijet_kine_uncert**2 + dijet_kine_data_mc_uncert**2)
    total_bjet_uncert  = np.sqrt(bjet_signal_uncert**2 + bjet_data_mc_kine_uncert**2 + avg_bjet_tag_sf_uncert**2 + bjet_hlt_tag_uncert**2)

    sub_dict['dijet'] = round(total_dijet_uncert, 5)
    sub_dict['bjet']  = round(total_bjet_uncert, 5)
    
    yield_only_bjets  = get_yield(logical_name, 'mfvEventHistosFullSelDijetAgnostic', 'h_npv')
    yield_only_dijets = get_yield(logical_name, 'mfvEventHistosFullSelBjetAgnostic', 'h_npv')
    yield_total       = get_yield(logical_name, 'mfvEventHistosFullSel', 'h_npv')

    sub_dict['yield_bjet']  = round(yield_only_bjets, 2)
    sub_dict['yield_dijet'] = round(yield_only_dijets, 2)
    sub_dict['yield_total'] = round(yield_total, 2)
    
    # Abbreviation scheme:
    #  yx = "yield in x"
    #  ex = "uncert in x"
    #  dx = "fluctuation in event yield due to x"
    # Where x can be p (primary), s (secondary), or t (total)
    if bjet_is_primary_q(total_bjet_uncert, total_dijet_uncert):
        yp = yield_only_bjets
        ep = total_bjet_uncert
    
        ys = yield_total - yield_only_bjets
        es = total_dijet_uncert
    
    else:
        yp = yield_only_dijets
        ep = total_dijet_uncert
    
        ys = yield_total - yield_only_dijets
        es = total_bjet_uncert
    
    dp = yp * ep 
    ds = ys * es
    dt = dp + ds 
    
    et = dt/yield_total

    sub_dict['total'] = round(np.sqrt(et**2 + avg_jer_uncert**2 + avg_jes_uncert**2), 5)
    
    #print logical_name, '   ', round(et, 5)

    big_dict[fname[0:-5]] = sub_dict

pprint.pprint(big_dict)

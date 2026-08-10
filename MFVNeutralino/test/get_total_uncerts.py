#!/usr/bin/env python

import os, sys, re
import ROOT
import numpy as np
import pprint
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools import Samples
#from JMTucker.Tools import Samples
from JMTucker.MFVNeutralino.PerSignal import PerSignal

# Generic function which converts num/dens into uncerts (and errors):
def sigma(num, den):
    rat = abs(1-num/den)
    err = np.sqrt(abs(num-den))/den

    return rat, err

def avg_btag_sf_uncert(key, d):
    bjet_sf = ['bjet_sf_up', 'bjet_sf_dn']
    num_up = d[key][bjet_sf[0]]['num']
    num_dn = d[key][bjet_sf[1]]['num']
    den    = d[key][bjet_sf[0]]['den']

    err_bjet_sf_up = abs(1-(num_up/den))
    err_bjet_sf_dn = abs(1-(num_dn/den))
    err_bjet_sf_avg = (err_bjet_sf_up + err_bjet_sf_dn)/2
    error_bar = np.sqrt((np.sqrt(abs(num_up-den))/den)**2 + (np.sqrt(abs(num_dn-den))/den)**2)/2

    return err_bjet_sf_avg, error_bar


# Placeholder comment
def eff_from_dict(key, component, my_dict, yr, normalize=False):
    try:

        if component != 'bjet_sf_avg':
            comp = my_dict[key][component]
            
            num = comp['num']
            den = comp['den']
            try:
                rat, err = sigma(num, den)
            except:
                rat = 0.0
                err = 0.0

        else: 
            rat, err = avg_btag_sf_uncert(key, my_dict)
        
        if normalize:
            bjet_primary = bjet_is_primary_q(my_dict[key])
            ntot  = my_dict[key]['yield_total']
            nbjet = my_dict[key]['yield_bjet']
            ndjet = my_dict[key]['yield_dijet']
            
            if bjet_primary:  # bjet uncertainties are lower
                if 'bjet' in component:
                    nrel = nbjet
                else:
                    nrel = ntot - nbjet
                    
            else:      # dijet uncertainties are lower
                if 'bjet' in component:
                    nrel = ntot - ndjet
                else:
                    nrel = ndjet
                    
            rat = (rat*nrel/ntot)
            err = (err*nrel/ntot)

    except KeyError:
        return 0.0, 0.0

    return rat, err

# Taken from Jordan's code
def mvpave(pave, x1, y1, x2, y2):
    pave.SetX1(x1)
    pave.SetX2(x2)
    pave.SetY1(y1)
    pave.SetY2(y2)

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

    return {'num': num, 'den': den}


# Get uncertainty pertaining to btagging scale factors and how
# that might effect signal yield.
def get_bjet_scale_factor_uncert(fn):
    nom_path   = 'mfvEventHistosDijetAgnosticTrigOn'
    vup_path   = 'mfvEventHistosDijetAgnosticTrigOnSFVarUp'
    vdn_path   = 'mfvEventHistosDijetAgnosticTrigOnSFVarDn'
    nom = get_yield(fn, nom_path, 'h_npv')
    vup = get_yield(fn, vup_path, 'h_npv')
    vdn = get_yield(fn, vdn_path, 'h_npv')

    delta_up = {'num': vup, 'den': nom}
    delta_dn = {'num': vdn, 'den': nom}

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

    delta_up = {'num': vup, 'den': nom}
    delta_dn = {'num': vdn, 'den': nom}

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

    delta_up = {'num': vup, 'den': nom}
    delta_dn = {'num': vdn, 'den': nom}

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

    if lo_uncert > hi_uncert:
        return {'num': lo_num, 'den': lo_den}
    else:
        return {'num': hi_num, 'den': hi_den}

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

    return {'num': ref_yield, 'den': nom_yield}

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

    return {'num': ref_yield, 'den': nom_yield}

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

    return {'num': var_yield, 'den': nom_yield}

def bjet_is_primary_q(d):
    bjet_sources = ["bjet_hlt", "bjet_signal", "bjet_dat_sim_kin"]
    bjet_sf      = ["bjet_sf_up", "bjet_sf_dn"]
    djet_sources = ["dijet_kine", "tracking_count", "tracking_hlt", "dijet_dat_sim_kin"]
    bjet_unc = 0.0
    djet_unc = 0.0
    
    err_bjet_sf_up = abs(1-d[bjet_sf[0]]['num']/d[bjet_sf[0]]['den'])
    err_bjet_sf_dn = abs(1-d[bjet_sf[1]]['num']/d[bjet_sf[1]]['den'])
    err_bjet_sf_avg = (err_bjet_sf_up + err_bjet_sf_dn)/2

    bjet_unc += (err_bjet_sf_avg**2)
    
    for s in bjet_sources:
        try:
            err_bjet_s = abs(1-d[s]['num']/d[s]['den'])
        except:
            err_bjet_s = 0.0
        bjet_unc += (err_bjet_s ** 2)
        
    for s in djet_sources:
        try:
            err_djet_s = abs(1-d[s]['num']/d[s]['den'])
        except:
            err_djet_s = 0.0
        djet_unc += (err_djet_s ** 2)
        
    return bjet_unc < djet_unc

# Uncertainties which don't change per sample
bjet_data_mc_kine_uncert       = .02  # THIS IS A PLACEHOLDER! FIXME
#bjet_data_mc_uncert       = .093
dijet_kine_data_mc_uncert = .005

ctaus  = ['000100', '000300', '001000', '010000', '030000']
masses = ['0200', '0300', '0400', '0600', '0800', '1200', '1600', '3000']

yr   = '2017' # FIXME do this a bit better
flist = ['mfv_stopdbardbar_tau' + ctau + 'um_M' + mass + '_' + yr + '.root' for mass in masses for ctau in ctaus]
flist += ['mfv_stopbbarbbar_tau' + ctau + 'um_M' + mass + '_' + yr + '.root' for mass in masses for ctau in ctaus]
flist += ['mfv_neu_tau' + ctau + 'um_M' + mass + '_' + yr + '.root' for mass in masses for ctau in ctaus]
flist += ['ggHToSSTodddd_tau1mm_M55_' +yr+'.root', 'ggHToSSTodddd_tau10mm_M55_'+yr+'.root', 'ggHToSSTodddd_tau100mm_M55_'+yr+'.root']
#flist = ['histos.root']

#dirname  = '/uscms_data/d3/shogan/crab_dirs/HistosULV9Bm_2018_UncertSuite_reFix_Feb02/'
dirname  = '/uscms_data/d3/shogan/crab_dirs/HistosULV9Bm_2017_UncertSuite_newFix_Jan2/'
#dirname = '/uscms_data/d3/shogan/crab_dirs/HistosULV9Bm_2016APV_UNCERTS_SomeFixes_Feb23/'

big_dict = {}

for fname in flist:
    logical_name = dirname + fname
    #logical_name = fname
    if not fname.endswith('.root'):
        continue

    if not os.path.isfile(logical_name):
        #print '{0}     None'.format(fname[:-5])
        continue

    sub_dict = {}
    # Uncertainties which don't change per sample
    bjet_data_mc_kine_uncert   = {'num': 98.0, 'den': 100.0}   # Bad way of doing things. These are dummy numbers that give an uncert of 2%
    dijet_kine_data_mc_uncert  = {'num': 995.0, 'den': 1000.0} # See above. These dummy numbers give an uncert of 0.5%

    dijet_hlt_track_uncert = get_dijet_hlt_track_uncert(logical_name)
    dijet_off_track_uncert = get_dijet_offline_track_uncert(logical_name)
    dijet_kine_uncert      = get_dijet_kine_ineff_uncert(logical_name)
    bjet_signal_uncert     = get_bjet_inefficiency_uncert(logical_name)
    bjet_tag_sf_uncert     = get_bjet_scale_factor_uncert(logical_name)
    bjet_hlt_tag_uncert    = get_hlt_btagging_uncert(logical_name)
    jer_uncert             = get_jer_correction_uncert(logical_name)
    jes_uncert             = get_jes_correction_uncert(logical_name)

    sub_dict['tracking_hlt']      = get_dijet_hlt_track_uncert(logical_name)
    sub_dict['tracking_count']    = get_dijet_offline_track_uncert(logical_name)
    sub_dict['dijet_kine']        = get_dijet_kine_ineff_uncert(logical_name)
    sub_dict['dijet_dat_sim_kin'] = dijet_kine_data_mc_uncert
    sub_dict['bjet_signal']      = get_bjet_inefficiency_uncert(logical_name)
    sub_dict['bjet_sf_dn']       = get_bjet_scale_factor_uncert(logical_name)['down']
    sub_dict['bjet_sf_up']       = get_bjet_scale_factor_uncert(logical_name)['up']
    sub_dict['bjet_hlt']         = get_hlt_btagging_uncert(logical_name)
    sub_dict['bjet_dat_sim_kin'] = bjet_data_mc_kine_uncert
    sub_dict['jer_dn']    = get_jer_correction_uncert(logical_name)['down']
    sub_dict['jer_up']    = get_jer_correction_uncert(logical_name)['up']
    sub_dict['jes_dn']    = get_jes_correction_uncert(logical_name)['down']
    sub_dict['jes_up']    = get_jes_correction_uncert(logical_name)['up']

    yield_only_bjets  = get_yield(logical_name, 'mfvEventHistosFullSelDijetAgnostic', 'h_npv')
    yield_only_dijets = get_yield(logical_name, 'mfvEventHistosFullSelBjetAgnostic', 'h_npv')
    yield_total       = get_yield(logical_name, 'mfvEventHistosFullSel', 'h_npv')

    sub_dict['yield_bjet']  = round(yield_only_bjets, 2)
    sub_dict['yield_dijet'] = round(yield_only_dijets, 2)
    sub_dict['yield_total'] = round(yield_total, 2)
    
    big_dict[fname[0:-5]] = sub_dict


#######################################################################################################################################

if __name__ == '__main__' and hasattr(sys, 'argv') and 'getdict' in sys.argv:
    print "here!"
    pprint.pprint(big_dict)


#######################################################################################################################################


if __name__ == '__main__' and hasattr(sys, 'argv') and 'geteffdict' in sys.argv:
    eff_dict = {}
    root_file_dir = dirname

    multijet = [s for s in Samples.mfv_signal_samples_2017]
    dijet_d = [s for s in Samples.mfv_stopdbardbar_samples_2017]
    dijet_b = [s for s in Samples.mfv_stopbbarbbar_samples_2017]
    
    for sample in multijet + dijet_d + dijet_b:
        fn = os.path.join(root_file_dir, sample.name + '.root')
        if not os.path.exists(fn):
            continue

        sub_dict = {}
 
        for key in ['tracking_hlt', 'tracking_count', 'dijet_dat_sim_kin', 'dijet_kine', 'bjet_signal', 'bjet_sf_avg', 'bjet_dat_sim_kin', 'bjet_hlt', 'jer_dn', 'jer_up', 'jes_dn', 'jes_up']:
            comp = key
            eff, err = eff_from_dict(sample.name, comp, big_dict, yr, normalize=True)

            sub_dict[key] = round(eff, 5)

        sigma_sq_b = 0 # bjet
        sigma_sq_d = 0 # dijet

        for key in ['bjet_signal', 'bjet_sf_avg', 'bjet_hlt', 'bjet_dat_sim_kin']:
            sigma_sq_b += sub_dict[key]**2

        for key in ['tracking_hlt', 'tracking_count', 'dijet_kine', 'dijet_dat_sim_kin']:
            sigma_sq_d += sub_dict[key]**2

        sigma_b = np.sqrt(sigma_sq_b)
        sigma_d = np.sqrt(sigma_sq_d)

        avg_jer_uncert = (sub_dict['jer_dn'] + sub_dict['jer_up']) / 2.0
        avg_jes_uncert = (sub_dict['jes_dn'] + sub_dict['jes_up']) / 2.0

        uncert_total = np.sqrt((sigma_b + sigma_d)**2 + avg_jer_uncert**2 + avg_jes_uncert**2)
        sub_dict['bjet_total'] = sigma_b
        sub_dict['djet_total'] = sigma_d
        sub_dict['total']      = round(uncert_total, 5)
            
        eff_dict[sample.name] = sub_dict

    pprint.pprint(eff_dict)


#######################################################################################################################################


if __name__ == '__main__' and hasattr(sys, 'argv') and 'makeplots' in sys.argv:
    set_style()
    ps = plot_saver(plot_dir('trigger_uncerts'), size=(600,600), log=False, pdf=True)

    root_file_dir = dirname
    for key in ['tracking_hlt', 'tracking_count', 'dijet_kine', 'bjet_signal', 'bjet_sf_avg', 'bjet_hlt', 'jer_dn', 'jer_up', 'jes_dn', 'jes_up']:
        comp = key
    
        multijet = [s for s in Samples.mfv_signal_samples_2017]
        dijet_d = [s for s in Samples.mfv_stopdbardbar_samples_2017]
        dijet_b = [s for s in Samples.mfv_stopbbarbbar_samples_2017]
    
        for sample in multijet + dijet_d + dijet_b:# + higgs:
            fn = os.path.join(root_file_dir, sample.name + '.root')
            if not os.path.exists(fn):
                continue
    
            eff, err = eff_from_dict(sample.name, comp, big_dict, yr, normalize=True)
            sample.y, sample.yl, sample.yh = eff, eff-err, eff+err
    
        per = PerSignal('fractional uncertainty', y_range=(0.,0.305))
        per.add(multijet, title='#tilde{N} #rightarrow tbs')
        per.add(dijet_d, title='#tilde{t} #rightarrow #bar{d}#bar{d}', color=ROOT.kGreen+2)
        per.add(dijet_b, title='#tilde{t} #rightarrow #bar{b}#bar{b}', color=ROOT.kBlue)
        per.draw(canvas=ps.c)
        mvpave(per.decay_paves[0], 2.203, 0.278, 7.5, 0.298)
        mvpave(per.decay_paves[1], 2.203, 0.258, 7.5, 0.278)
        mvpave(per.decay_paves[2], 2.203, 0.238, 7.5, 0.258)
        ps.save(key + '_' + str(yr))

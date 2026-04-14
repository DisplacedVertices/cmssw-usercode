from __future__ import absolute_import
import numpy as np

import helper_PyStorage_objects as sth

import nuisance_configs as ns_conf # dictionaries to make this ad-hoc code work
import sig_and_bkg_configs as sb_conf
import script_configs as config


"""
This file is called by getNuisanceFromSig.py

-INPUTS-
nuis_name: string. It becomes the nuisance name, and indexes dictionaries.

Required inputs for NuisanceInfo:
nuis_name: string
nuis_val: float or array-like, values (meaningless for shape uncertainties)
make_updn: Boolean, is this a shape uncertainty?
sep_yrs: Boolean, should this nuisance be combined across the different years or not?
corr: Boolean, are the N bins correlated?
"""


#Globals
year = config.datacard["year"]
year_id = config.datacard["year_key"].index(year)
sig_type = config.sig["type"]
nbins = config.datacard["nbins"]

debugging = True



"""
Small functions
"""

def interp_pickle_triple(nn):
    """ Given nuisance name (ex. "tk_reco_eff"), make up+dn locations """
    loc_dict = ns_conf.pickle_triple_prefixes[nn]
    loc_base = loc_dict["base"]
    return loc_base + loc_dict["up"], loc_base + loc_dict["dn"]


def make_anticorr_bkg(val, dp=4, in_is_b1=True):
    """
    Anti-correlate bins 1, and 2+3
    -INPUTS-
    val: value, in the standard form 1+x where x is fractional uncertainty (e.g. 1.1 for 10%)
    dp: if not None, will truncate everything to this many decimal points
    in_is_b1: does the input represent b1 or b2/b3?
    """
    if in_is_b1: out_arr = val * np.ones(nbins)
    else: out_arr = 1/val * np.ones(nbins)

    out_arr[1:] = 1/out_arr[1:]
    if dp is not None:
        out_arr = np.round(out_arr, decimals=int(dp))
    return out_arr






"""
Nominal Corrections: SIGNAL
"""

""" # Removed code
def get_nominal_reco_effi_sig(siginfo, debug_mode=False):

    nominals = 0.85 * np.ones(nbins)

    return nominals
"""






"""
SIGNAL Nuisances
"""

def get_mc_stat(nuis_name, siginfo, debug_mode=False):
    nuis = sth.NuisanceInfo(nuis_name, 1.2, make_updn=False, sep_yrs=True, corr=False, nuis_type="GammaN", nbins=siginfo.nbins, ana_spec=True)
    return [nuis]



def get_reco_effi(nuis_name, siginfo, debug_mode=False):
    pickle_locs = interp_pickle_triple(nuis_name)

    up_ntab = sth.NuisanceTable(proc="VH", pickle_loc=pickle_locs[0]) # FIXME as of right now, only VH exists
    # up_ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=pickle_locs[0])
    up_arr = up_ntab.get_point_from_fn(siginfo.fn.replace(siginfo.proc, "VH"))
    if up_arr is None: up_arr = [1.0, 1.0, 1.0] # Needed because there's only VH, stupid fix
    dn_ntab = sth.NuisanceTable(proc="VH", pickle_loc=pickle_locs[1])
    # dn_ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=pickle_locs[1])
    dn_arr = dn_ntab.get_point_from_fn(siginfo.fn.replace(siginfo.proc, "VH"))
    if dn_arr is None: dn_arr = [1.0, 1.0, 1.0] # Stupid patch

    # nominals = get_nominal_reco_effi_sig(siginfo, debug_mode=debug_mode) # That's if up/down numbers are absolute corrections (not current assumption)
    # up_lnN = np.round(up_arr/nominals, decimals=4)
    # dn_lnN = np.round(dn_arr/nominals, decimals=4)
    # if np.array_equal(np.array(up_arr), np.ones(nbins)) and np.array_equal(np.array(dn_arr), np.ones(nbins)): return []

    up_nuis = sth.NuisanceInfo(nuis_name, up_arr, make_updn=False, sep_yrs=False, corr=True, nuis_type="special", nbins=siginfo.nbins, ana_spec=True, extra_info=["updn_pair", "up"])
    dn_nuis = sth.NuisanceInfo(nuis_name, dn_arr, make_updn=False, sep_yrs=False, corr=True, nuis_type="special", nbins=siginfo.nbins, ana_spec=True, extra_info=["updn_pair", "dn"])

    if debug_mode: print "Identified trk-reco fractional uncertainties:", up_arr, dn_arr
    
    return [up_nuis, dn_nuis]



def get_vtx_reco_TM(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name]) # Get pickle
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode: print "Identified TM fractional uncertainty:", frac_unc
    if frac_unc is None:
        print "Warning: value not sensible. Write fake value"
        frac_unc = 1.0
        #nuis_name += "_PointNotFound"
    if True: frac_unc = np.round(frac_unc, 7) # Because sometimes I get 1.xxx0000000001
    
    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=True)]



def get_pileup(nuis_name, siginfo, debug_mode=False):

    # Shape up/down uncertainty
    nuis = sth.NuisanceInfo(nuis_name, [1.03, 1.04, 1.06], make_updn=False, sep_yrs=False, corr=True, nbins=siginfo.nbins)
    
    # Used to be a shape+dummy
    # nuis = sth.NuisanceInfo("fake_fact_"+nuis_name, 1.2, make_updn=True, sep_yrs=False, corr=True, nuis_type="shape", nbins=siginfo.nbins, ana_spec=False)
    
    return [nuis]



def get_int_lumi(nuis_name, siginfo, debug_mode=False):

    lumi_components = sb_conf.lumi_lit_corrs

    if year in ["20161", "20162"]: year_tosearch = "2016"
    else: year_tosearch = year

    out_ls = []

    for comp_name in sorted(lumi_components.keys()):
        val = lumi_components[comp_name][year_tosearch]
        if val is None:
            continue
        nuis = sth.NuisanceInfo(comp_name, val, make_updn=False, sep_yrs=False, corr=True, nbins=siginfo.nbins, add_era_tags=False)
        out_ls.append(nuis)

    #frac_unc = sb_conf.lumi_uncs[year] #nuis = sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=True, corr=True, nbins=siginfo.nbins) #sth.NuisanceInfo("lumi_17", 1.01, make_updn=False, sep_yrs=False, corr=True, nuis_type="special", nbins=siginfo.nbins, extra_info=["anti-lnN"]) # If you want something anti-correlated

    return out_ls



def get_lep_effi(nuis_name, siginfo, debug_mode=False):

    # Electron
    nuis_e_id = sth.NuisanceInfo(nuis_name+"e_id", 1+0.01, make_updn=False, sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=False)

    # Muon - not implemented

    return [nuis_e_id]



def get_trig_JESR_btag(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name]) # Get pickle
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode: print "Identified b-tag fractional uncertainty:", frac_unc
    if not np.isfinite(frac_unc):
        print "Warning: value not sensible. Skipping value."
        return []
    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=True)]



def get_calo_inef(nuis_name, siginfo, debug_mode=False):

    frac_unc = 0
    if ("2016" in siginfo.year) and (siginfo.return_mass_as_int()<=300) and (siginfo.return_lifetime_in_unit(unit="mm")>=10):
        frac_unc = 0.05
    else:
        frac_unc = 0.01
    
    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True)]






"""
BACKGROUND Nuisances
"""

def get_bkg_jet_ang(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.06), make_updn=False, sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]



def get_bkg_vtx_arbi(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.37), make_updn=False, sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]



def get_bkg_vtx_refi(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.1), make_updn=False, sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]



"""
def get_bkg_sum_dbvc(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo("fake-bkg", 1.10, make_updn=False, sep_yrs=True, corr=True, nbins=nbins, ana_spec=True)]
"""
    


def get_bkg_pileup(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.0001, make_updn=False, sep_yrs=False, corr=True, nbins=nbins)]



def get_bkg_sig_cont(nuis_name, debug_mode=False):
    up_nuis = sth.NuisanceInfo(nuis_name, 1.05, make_updn=False, sep_yrs=False, corr=True, nuis_type="special", nbins=nbins, ana_spec=True, extra_info=["updn_pair", "up"])
    dn_nuis = sth.NuisanceInfo(nuis_name, 1.00, make_updn=False, sep_yrs=False, corr=True, nuis_type="special", nbins=nbins, ana_spec=True, extra_info=["updn_pair", "dn"])

    return [up_nuis, dn_nuis]



def get_bkg_bkg_norm(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.15, make_updn=False, sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]



def get_bkg_n2v_unc(nuis_name, debug_mode=False):
    frac_unc = sb_conf.n2v_uncs[sig_type][year_id] / sb_conf.template_norms["n2v"][sig_type][year_id]

    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=True, corr=True, nbins=nbins, ana_spec=True)]


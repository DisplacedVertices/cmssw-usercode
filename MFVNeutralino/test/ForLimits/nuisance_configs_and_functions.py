from __future__ import absolute_import
import numpy as np

import helper_PyStorage_objects as sth

import nuisance_configs as ns_conf # dictionaries to make this ad-hoc code work
import uncerts_trigger as trig_unc # Python dictionaries
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
SIGNAL Nuisances
"""

def get_mc_stat(nuis_name, siginfo, debug_mode=False):
    nuis = sth.NuisanceInfo(nuis_name, 1.2, make_updn=False, sep_yrs=True, corr=False, nuis_type="GammaN", nbins=siginfo.nbins, ana_spec=True)
    return [nuis]



def get_reco_effi(nuis_name, siginfo, debug_mode=False):
    # FIXME This is Alec's study
    nuis = sth.NuisanceInfo("fake-shape", 1.2, make_updn=True, sep_yrs=True, corr=True, nuis_type="shape", nbins=siginfo.nbins, ana_spec=True) # Dummy
    return [nuis]



def get_vtx_reco_TM(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name]) # Get pickle
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode: print "Identified TM fractional uncertainty:", frac_unc
    if not np.isfinite(frac_unc):
        print "Warning: value not sensible. Skipping value."
        return []
    
    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=True, corr=False, nbins=siginfo.nbins, ana_spec=True)]



def get_pileup(nuis_name, siginfo, debug_mode=False):
    nuis = sth.NuisanceInfo(nuis_name, 1.02, make_updn=False, sep_yrs=True, corr=False, nbins=siginfo.nbins) #FIXME need shape
    return [nuis]



def get_int_lumi(nuis_name, siginfo, debug_mode=False):
    # FIXME this is a dummy
    return [sth.NuisanceInfo("lumi", 1.01, make_updn=False, sep_yrs=True, corr=True, nbins=siginfo.nbins),
            sth.NuisanceInfo("lumi_17", 1.01, make_updn=False, sep_yrs=False, corr=True, nuis_type="special", nbins=siginfo.nbins, extra_info=["anti-lnN"])
        ]



def get_lep_effi(nuis_name, siginfo, debug_mode=False):
    # FIXME
    return []



def get_trig_JESR_btag(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name]) # Get pickle
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode: print "Identified b-tag fractional uncertainty:", frac_unc
    if not np.isfinite(frac_unc):
        print "Warning: value not sensible. Skipping value."
        return []
    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=True, corr=False, nbins=siginfo.nbins, ana_spec=True)]



def get_calo_inef(nuis_name, siginfo, debug_mode=False):

    frac_unc = 0
    if ("2016" in siginfo.year) and (siginfo.return_mass_as_int()<=300) and (siginfo.return_lifetime_in_unit(unit="mm")>=10):
        frac_unc = 0.05
    else:
        frac_unc = 0.01
    
    return [sth.NuisanceInfo(nuis_name, 1+frac_unc, make_updn=False, sep_yrs=True, corr=False, nbins=siginfo.nbins, ana_spec=True)]






"""
BACKGROUND Nuisances
"""

def get_bkg_sum_dbvc(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo("fake-bkg", 1.10, make_updn=False, sep_yrs=True, corr=True, nbins=nbins, ana_spec=True)]



def get_bkg_pileup(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.0001, make_updn=False, sep_yrs=True, corr=True, nbins=nbins)]



def get_bkg_sig_cont(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.05, make_updn=False, sep_yrs=True, corr=True, nbins=nbins, ana_spec=True)]



def get_bkg_bkg_norm(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.15, make_updn=False, sep_yrs=True, corr=False, nbins=nbins, ana_spec=True)]


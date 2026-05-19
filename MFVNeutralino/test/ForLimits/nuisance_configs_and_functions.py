import numpy as np

import helper_PyStorage_objects as sth
import nuisance_configs as ns_conf
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

# Module-level globals -- updated per year via _init_for_year()
year     = config.datacard["year"]
year_id  = config.datacard["year_key"].index(year)
sig_type = config.sig["type"]
nbins    = config.datacard["nbins"]


def _init_for_year(yr):
    global year, year_id, sig_type, nbins
    year     = yr
    year_id  = config.datacard["year_key"].index(yr)
    sig_type = config.sig["type"]
    nbins    = config.datacard["nbins"]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def interp_pickle_triple(nn):
    """Given nuisance name (e.g. 'tk_reco_eff'), return (up_path, dn_path)."""
    loc_dict = ns_conf.pickle_triple_prefixes[nn]
    base = loc_dict["base"]
    return base + loc_dict["up"], base + loc_dict["dn"]


def make_anticorr_bkg(val, dp=4, in_is_b1=True):
    """Anti-correlate bin 1 vs. bins 2+3 for a background nuisance.

    val: 1+x (e.g. 1.1 for 10%).  in_is_b1: whether val is the bin-1 direction.
    """
    out_arr = val * np.ones(nbins) if in_is_b1 else (1.0 / val) * np.ones(nbins)
    out_arr[1:] = 1.0 / out_arr[1:]
    if dp is not None:
        out_arr = np.round(out_arr, decimals=int(dp))
    return out_arr


# ---------------------------------------------------------------------------
# Signal nuisances
# ---------------------------------------------------------------------------

def get_mc_stat(nuis_name, siginfo, debug_mode=False):
    nuis = sth.NuisanceInfo(nuis_name, 1.2, make_updn=False, sep_yrs=True, corr=False,
                            nuis_type="GammaN", nbins=siginfo.nbins, ana_spec=True)
    return [nuis]


def get_reco_effi(nuis_name, siginfo, debug_mode=False):
    """Track reconstruction efficiency uncertainty.

    Currently only VH has a dedicated table; other processes fall back to 1.0
    (which is then filtered out by replace_all_ones in getNuisanceFromSig).
    """
    pickle_locs = interp_pickle_triple(nuis_name)

    # TODO: replace "VH" with siginfo.proc once tables exist for all processes
    up_ntab = sth.NuisanceTable(proc="VH", pickle_loc=pickle_locs[0])
    up_arr  = up_ntab.get_point_from_fn(siginfo.fn.replace(siginfo.proc, "VH"))
    if up_arr is None:
        up_arr = [1.0] * siginfo.nbins

    dn_ntab = sth.NuisanceTable(proc="VH", pickle_loc=pickle_locs[1])
    dn_arr  = dn_ntab.get_point_from_fn(siginfo.fn.replace(siginfo.proc, "VH"))
    if dn_arr is None:
        dn_arr = [1.0] * siginfo.nbins

    if debug_mode:
        print("Identified trk-reco fractional uncertainties:", up_arr, dn_arr)

    up_nuis = sth.NuisanceInfo(nuis_name, up_arr, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins, ana_spec=True,
                               extra_info=["updn_pair", "up"])
    dn_nuis = sth.NuisanceInfo(nuis_name, dn_arr, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins, ana_spec=True,
                               extra_info=["updn_pair", "dn"])
    return [up_nuis, dn_nuis]


def get_vtx_reco_TM(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name],
                             trig_for_pickle=siginfo.trig_type)
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode:
        print("Identified TM fractional uncertainty:", frac_unc)
    if frac_unc is None:
        print("Warning: vtx_reco_TM value not found. Writing fake value.")
        frac_unc = 1.0
    frac_unc = np.round(frac_unc, 7)

    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False, sep_yrs=False, corr=True,
                             nbins=siginfo.nbins, ana_spec=True)]


def get_pileup(nuis_name, siginfo, debug_mode=False):
    if siginfo.trig_type == "lep":
        nuis = sth.NuisanceInfo(nuis_name, [1.03, 1.04, 1.06], make_updn=False,
                                sep_yrs=False, corr=True, nbins=siginfo.nbins)
    elif siginfo.trig_type == "bjet":
        nuis = sth.NuisanceInfo(nuis_name, 1.03, make_updn=False,
                                sep_yrs=False, corr=True, nbins=siginfo.nbins)
    else:
        raise Exception("Could not add pileup")
    return [nuis]


def get_int_lumi(nuis_name, siginfo, debug_mode=False):
    lumi_components = sb_conf.lumi_lit_corrs
    year_tosearch = "2016" if year in ("20161", "20162") else year

    out_ls = []
    for comp_name in sorted(lumi_components):
        val = lumi_components[comp_name][year_tosearch]
        if val is None:
            continue
        nuis = sth.NuisanceInfo(comp_name, val, make_updn=False, sep_yrs=False,
                                corr=True, nbins=siginfo.nbins, add_era_tags=False)
        out_ls.append(nuis)
    return out_ls


def get_lep_effi(nuis_name, siginfo, debug_mode=False):
    """Lepton reconstruction efficiency (electron ID only; muon not yet implemented)."""
    nuis_e_id = sth.NuisanceInfo(nuis_name + "e_id", 1 + 0.01, make_updn=False,
                                 sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=False)
    return [nuis_e_id]


def get_trig_JESR_btag(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name],
                             trig_for_pickle=siginfo.trig_type)
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode:
        print("Identified b-tag fractional uncertainty:", frac_unc)
    if frac_unc is None:
        print("Warning: trig_JESR_btag value not found. Writing arbitrary value.")
        return [sth.NuisanceInfo(nuis_name + "_fake", 1 + 0.1, make_updn=False,
                                 sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=True)]
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=True)]


def get_calo_inef(nuis_name, siginfo, debug_mode=False):
    if ("2016" in siginfo.year and siginfo.return_mass_as_int() <= 300
            and siginfo.return_lifetime_in_unit(unit="mm") >= 10):
        frac_unc = 0.05
    else:
        frac_unc = 0.01
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True)]


# ---------------------------------------------------------------------------
# Background nuisances
# ---------------------------------------------------------------------------

def get_bkg_jet_ang(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.06), make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]


def get_bkg_vtx_arbi(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.37), make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]


def get_bkg_vtx_refi(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.1), make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]


def get_bkg_pileup(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.0001, make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins)]


def get_bkg_sig_cont(nuis_name, debug_mode=False):
    up_nuis = sth.NuisanceInfo(nuis_name, 1.05, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=nbins, ana_spec=True,
                               extra_info=["updn_pair", "up"])
    dn_nuis = sth.NuisanceInfo(nuis_name, 1.00, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=nbins, ana_spec=True,
                               extra_info=["updn_pair", "dn"])
    return [up_nuis, dn_nuis]


def get_bkg_bkg_norm(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.15, make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True)]


def get_bkg_n2v_unc(nuis_name, debug_mode=False):
    frac_unc = sb_conf.n2v_uncs[sig_type][year_id] / sb_conf.template_norms["n2v"][sig_type][year_id]
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=nbins, ana_spec=True)]

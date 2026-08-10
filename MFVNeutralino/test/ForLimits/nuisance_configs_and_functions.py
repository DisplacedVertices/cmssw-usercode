from __future__ import print_function
import numpy as np

import helper_PyStorage_objects as sth
import helper_theory_tables as thytab
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
    """Anti-correlate bin 1 against all the other bins for a background nuisance.

    -INPUTS-
    val: 1+x (e.g. 1.1 for 10%)
    dp: if not None, round everything to this many decimal places
    in_is_b1: whether val is the bin-1 direction or the other-bins direction
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
    """Signal MC stat, gmN per bin per year. Name carries the signal point: gmN's sideband
    count is part of the parameter identity, so shared names make combineCards refuse to merge."""
    point = "%s_tau%s_M%s" % (siginfo.proc, siginfo.lifetime, siginfo.mass)
    nuis = sth.NuisanceInfo(nuis_name + "_" + point, 1.2, make_updn=False, sep_yrs=True,
                            corr=False, nuis_type="GammaN", nbins=siginfo.nbins, ana_spec=True, extrapolate_last=False)
    return [nuis]


def get_reco_effi(nuis_name, siginfo, debug_mode=False):
    """Track reconstruction efficiency uncertainty.

    Bjet channel: flat 5% working placeholder per AN Sec. 6.2.1 (Table 39/40).
    Lep channel: per-bin asymmetric values from dedicated VH scale factor tables.
    """

    if year in ("20161", "20162"):
        up_arr = [1.0, 1.01, 1.04, 1.07]
        dn_arr = [1.0, 0.99, 0.96, 0.90]
    elif year in ("2017", "2018"):
        up_arr = [1.0, 1.01, 1.02, 1.04]
        dn_arr = [1.0, 0.99, 0.95, 0.90]
    else: raise Exception("Year not recognized: " + year)

    up_nuis = sth.NuisanceInfo(nuis_name, up_arr, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins, ana_spec=True,
                               extra_info=["updn_pair", "up"], extrapolate_last=True,
                               owner=siginfo.return_nuis_key())
    dn_nuis = sth.NuisanceInfo(nuis_name, dn_arr, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins, ana_spec=True,
                               extra_info=["updn_pair", "dn"], extrapolate_last=True,
                               owner=siginfo.return_nuis_key())
    return [up_nuis, dn_nuis]


def get_vtx_reco_TM(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name],
                             trig_for_pickle=siginfo.trig_type)
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode:
        print("Identified TM fractional uncertainty:", frac_unc)
    if frac_unc is None:
        print("*" * 90)
        print("*** FABRICATED NUISANCE: vtx_reco_TM not found in the table for %s"
              % siginfo.return_nuis_key())
        print("*** writing a 100% lnN (value 2.0). This point is off the stored grid.")
        print("*" * 90)
        frac_unc = 1.0
    frac_unc = np.round(frac_unc, 7)

    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False, sep_yrs=False, corr=True,
                             nbins=siginfo.nbins, ana_spec=True, extrapolate_last=False)]


def get_pileup(nuis_name, siginfo, debug_mode=False):
    if siginfo.trig_type == "lep":
        # AN Sec 6.2.6 quotes 3%, 4%, 6% on the old 3-bin binning; the 4th bin is extrapolated
        nuis = sth.NuisanceInfo(nuis_name, [1.03, 1.04, 1.06, 1.06], make_updn=False,
                                sep_yrs=False, corr=True, nbins=siginfo.nbins,
                                extrapolate_last=True, owner=siginfo.return_nuis_key())
    elif siginfo.trig_type == "bjet":
        nuis = sth.NuisanceInfo(nuis_name, 1.03, make_updn=False,
                                sep_yrs=False, corr=True, nbins=siginfo.nbins, extrapolate_last=False)
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
                                corr=True, nbins=siginfo.nbins, add_era_tags=False, extrapolate_last=False)
        out_ls.append(nuis)
    return out_ls


def get_lep_effi(nuis_name, siginfo, debug_mode=False):
    """Lepton reconstruction efficiency (electron ID only; muon not yet implemented)."""
    nuis_e_id = sth.NuisanceInfo(nuis_name + "e_id", 1 + 0.01, make_updn=False,
                                 sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=False, extrapolate_last=False)
    return [nuis_e_id]


def get_trig_JESR_btag(nuis_name, siginfo, debug_mode=False):
    ntab = sth.NuisanceTable(proc=siginfo.proc, pickle_loc=ns_conf.pickle_prefixes[nuis_name],
                             trig_for_pickle=siginfo.trig_type)
    frac_unc = ntab.get_point_from_fn(siginfo, overrides={"yr": ns_conf.year_remaps[nuis_name][siginfo.year]})

    if debug_mode:
        print("Identified b-tag fractional uncertainty:", frac_unc)
    if frac_unc is None:
        print("*" * 90)
        print("*** FABRICATED NUISANCE: trig_JESR_btag not found in the table for %s"
              % siginfo.return_nuis_key())
        print("*** writing an arbitrary 10%% lnN under the name %s_fake." % nuis_name)
        print("*" * 90)
        return [sth.NuisanceInfo(nuis_name + "_fake", 1 + 0.1, make_updn=False,
                                 sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True, extrapolate_last=False)]
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True, extrapolate_last=False)]


def get_calo_inef(nuis_name, siginfo, debug_mode=False):
    if ("2016" in siginfo.year and siginfo.return_mass_as_int() <= 300
            and siginfo.return_lifetime_in_unit(unit="mm") >= 10):
        frac_unc = 0.05
    else:
        frac_unc = 0.01
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True, extrapolate_last=False)]


def get_qcd_scale_ren_ggH(nuis_name, siginfo, debug_mode=False):
    """QCD renormalization scale theory uncertainty for ggH (2%, year- and bin-correlated)."""
    if "ggH" not in siginfo.proc:
        raise Exception("QCDscale_ren_ggH is a ggH-only uncertainty, got " + siginfo.proc)

    return [sth.NuisanceInfo(nuis_name, 1.02, make_updn=False, sep_yrs=False, corr=True,
                             nbins=siginfo.nbins, ana_spec=False, add_era_tags=False, extrapolate_last=False)]


def get_qcd_scale_fac_VH(nuis_name, siginfo, debug_mode=False):
    """Factorization scale shape uncertainty for VH (ZH/WH+/WH-), year-correlated.

    Per-bin kappas from the CSV, all four bins; only low-stats bins are forced to 1.0.
    Missing signal points fall back to kappa=1.0 (no systematic applied).
    """
    table  = thytab.get_fac_scale_VH_table()
    mass   = siginfo.return_mass_as_int()
    ctau   = int(siginfo.return_lifetime_in_unit(unit="um"))
    result = table.get((mass, ctau, year))

    if result is None:
        if debug_mode:
            print("QCDscale_fac_VH: no entry for mass=%d ctau=%d year=%s; using 1.0" % (
                mass, ctau, year))
        kup = [1.0] * siginfo.nbins
        kdn = [1.0] * siginfo.nbins
    else:
        kup = list(result[0])[:siginfo.nbins]
        kdn = list(result[1])[:siginfo.nbins]
        while len(kup) < siginfo.nbins:
            kup.append(1.0)
            kdn.append(1.0)

    if debug_mode:
        print("QCDscale_fac_VH: mass=%d ctau=%d year=%s kup=%s kdn=%s" % (
            mass, ctau, year, kup, kdn))

    up_nuis = sth.NuisanceInfo(nuis_name, kup, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins,
                               ana_spec=False, add_era_tags=False,
                               extra_info=["updn_pair", "up"], extrapolate_last=False)
    dn_nuis = sth.NuisanceInfo(nuis_name, kdn, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins,
                               ana_spec=False, add_era_tags=False,
                               extra_info=["updn_pair", "dn"], extrapolate_last=False)
    return [up_nuis, dn_nuis]


# ---------------------------------------------------------------------------
# Background nuisances
# ---------------------------------------------------------------------------

def get_bkg_jet_ang(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.06), make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True, extrapolate_last=False)]


def get_bkg_vtx_arbi(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.37), make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True, extrapolate_last=False)]


def get_bkg_vtx_refi(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, make_anticorr_bkg(1.1), make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True, extrapolate_last=False)]


def get_bkg_pileup(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.0001, make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, extrapolate_last=False)]


def get_bkg_sig_cont(nuis_name, debug_mode=False):
    up_nuis = sth.NuisanceInfo(nuis_name, 1.05, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=nbins, ana_spec=True,
                               extra_info=["updn_pair", "up"], extrapolate_last=False)
    dn_nuis = sth.NuisanceInfo(nuis_name, 1.00, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=nbins, ana_spec=True,
                               extra_info=["updn_pair", "dn"], extrapolate_last=False)
    return [up_nuis, dn_nuis]


def get_bkg_bkg_norm(nuis_name, debug_mode=False):
    return [sth.NuisanceInfo(nuis_name, 1.15, make_updn=False,
                             sep_yrs=False, corr=True, nbins=nbins, ana_spec=True, extrapolate_last=False)]


def get_bkg_n2v_unc(nuis_name, debug_mode=False):
    frac_unc = sb_conf.n2v_uncs[sig_type][year_id] / sb_conf.template_norms["n2v"][sig_type][year_id]
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=nbins, ana_spec=True, extrapolate_last=False)]

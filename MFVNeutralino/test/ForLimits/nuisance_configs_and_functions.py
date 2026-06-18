from __future__ import print_function
import csv as _csv
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

    Bjet channel: flat 5% working placeholder per AN Sec. 6.2.1 (Table 39/40).
    Lep channel: per-bin asymmetric values from dedicated VH scale factor tables.
    """
    if siginfo.trig_type == "bjet":
        # AN working placeholder: flat 5% symmetric lnN for all bjet signals
        if debug_mode:
            print("tk_reco_eff: using flat 5% placeholder for bjet signal")
        return [sth.NuisanceInfo(nuis_name, [1.05] * siginfo.nbins, make_updn=False,
                                 sep_yrs=False, corr=True, nbins=siginfo.nbins, ana_spec=True)]

    # Lep channel: per-bin asymmetric values from VH scale factor tables
    pickle_locs = interp_pickle_triple(nuis_name)

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
        nuis = sth.NuisanceInfo(nuis_name, [1.03, 1.04, 1.06, 1.06], make_updn=False,
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
                                 sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True)]
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True)]


def get_calo_inef(nuis_name, siginfo, debug_mode=False):
    if ("2016" in siginfo.year and siginfo.return_mass_as_int() <= 300
            and siginfo.return_lifetime_in_unit(unit="mm") >= 10):
        frac_unc = 0.05
    else:
        frac_unc = 0.01
    return [sth.NuisanceInfo(nuis_name, 1 + frac_unc, make_updn=False,
                             sep_yrs=True, corr=True, nbins=siginfo.nbins, ana_spec=True)]


def get_qcd_scale_ren_ggH(nuis_name, siginfo, debug_mode=False):
    """QCD renormalization scale theory uncertainty for ggH (2%, year- and bin-correlated)."""
    return [sth.NuisanceInfo(nuis_name, 1.02, make_updn=False, sep_yrs=False, corr=True,
                             nbins=siginfo.nbins, ana_spec=False, add_era_tags=False)]


def _load_fac_scale_VH_table(csv_path):
    """Parse fac_scale_shape_bins.csv into yield-weighted VH kappas.

    Returns {(mass_gev, ctau_um, year): ([kup_b0..b3], [kdn_b0..b3])}.
    ggZH -> 1.0 (negligible fac-scale dep.).
    Low-stats bins (flags_bin{i}='low_bin') -> kappa=1.0, weight=0.
    """
    NBINS_CSV = 4
    NBINS_ALL = 4

    raw = {}
    with open(csv_path) as f:
        for r in _csv.DictReader(f):
            key = (int(r['mass_gev']), int(r['ctau_um']), r['year'])
            entry = {}
            for b in range(NBINS_CSV):
                if r['flags_bin%d' % b] == 'ok':
                    entry[b] = (float(r['kappa_up_bin%d' % b]),
                                float(r['kappa_dn_bin%d' % b]),
                                int(r['n_bin%d' % b]))
                else:
                    entry[b] = (1.0, 1.0, 0)
            raw.setdefault(key, {})[r['stype']] = entry

    table = {}
    for key, stypes_d in raw.items():
        kup, kdn = [], []
        for b in range(NBINS_ALL):
            if b >= NBINS_CSV:
                kup.append(1.0)
                kdn.append(1.0)
                continue
            total_n = sum_ku = sum_kd = 0.0
            for st in ('ZH', 'WplusH', 'WminusH'):
                ku, kd, n = stypes_d.get(st, {}).get(b, (1.0, 1.0, 0))
                sum_ku += ku * n
                sum_kd += kd * n
                total_n += n
            if total_n > 0:
                kup.append(sum_ku / total_n)
                kdn.append(sum_kd / total_n)
            else:
                kup.append(1.0)
                kdn.append(1.0)
        table[key] = (kup, kdn)
    return table


_fac_scale_VH_table = None


def _get_fac_scale_VH_table():
    global _fac_scale_VH_table
    if _fac_scale_VH_table is None:
        _fac_scale_VH_table = _load_fac_scale_VH_table(ns_conf.fac_scale_VH_csv_path)
    return _fac_scale_VH_table


def get_qcd_scale_fac_VH(nuis_name, siginfo, debug_mode=False):
    """Factorization scale shape uncertainty for VH (ZH/WH+/WH-), year-correlated.

    Per-bin kappas from CSV; bin 3 and ggZH use kappa=1.0; low-stats bins use kappa=1.0.
    Missing signal points fall back to kappa=1.0 (no systematic applied).
    """
    table  = _get_fac_scale_VH_table()
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
                               extra_info=["updn_pair", "up"])
    dn_nuis = sth.NuisanceInfo(nuis_name, kdn, make_updn=False, sep_yrs=False, corr=True,
                               nuis_type="special", nbins=siginfo.nbins,
                               ana_spec=False, add_era_tags=False,
                               extra_info=["updn_pair", "dn"])
    return [up_nuis, dn_nuis]


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

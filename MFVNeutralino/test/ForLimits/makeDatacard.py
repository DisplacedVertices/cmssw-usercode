from __future__ import print_function
import ROOT
import numpy as np

import script_configs as config
import nuisance_configs as ns_conf
import helper_PyStorage_objects as sth

"""
Naming conventions (Note: apparently if I put template as an input, the function refuses to change template, idk why)
    return_XX : it will give something back, append to template
    add_XX: overwrite template with the return value
    replace_XX: like add
    write_XX: overwrite template (apparently this can't be done)

The only stuff that are hard-coded are:
-Sig and bkg are called 0 and 1
-Sig and bkg are written in this order
"""

# Hard codes
n_proc = 2

# Module-level globals -- updated per year via _init_for_year()
year     = config.datacard["year"]
year_id  = config.datacard["year_key"].index(year)
nbins    = config.datacard["nbins"]
bins     = np.array(config.datacard["bins"])
sig_type = config.sig["type"]

year_to_tag = config.datacard["year_to_tag"]
year_tag    = year_to_tag[year]


def _init_for_year(yr):
    global year, year_id, nbins, bins, sig_type, year_to_tag, year_tag
    year     = yr
    year_id  = config.datacard["year_key"].index(yr)
    nbins    = config.datacard["nbins"]
    bins     = np.array(config.datacard["bins"])
    sig_type = config.sig["type"]
    year_to_tag = config.datacard["year_to_tag"]
    year_tag = year_to_tag[yr]


# ---------------------------------------------------------------------------
# Short helpers
# ---------------------------------------------------------------------------

def pad(some_str, n, align_left=True):
    """Pad any given string to n characters (does not truncate); always adds one space."""
    if len(some_str) >= n - 1:
        return (some_str + " ") if align_left else (" " + some_str)
    elif align_left:
        return some_str + (n - len(some_str)) * " "
    else:
        return (n - len(some_str)) * " " + some_str


# Name helpers reference year_tag as a global -- picked up at call time
sig_nm = lambda sid: "  " + "sig" + year_tag + sid
bkg_nm = lambda: "   " + "bkg" + year_tag
b_nm   = lambda bn: "    " + "b" + year_tag + bn


def return_sep():
    return "        "


def make_nuis_dcnm(nuis, siggrp, force_no_CADItag=False):
    """Return the datacard name(s) for a nuisance.

    Correlated -> single string; un-correlated -> list of per-bin strings.

    -If analysis-specific, tag with CADI (unless forced not to). Due to shape-processing
     conventions, force_no_CADItag currently suppresses the era tags too.
    -If separate years, tag with year_tag, else with the Run2 key
    -If separate bins (==corr/uncorr), tag b1, b2 etc
    """
    nuis_rootname = nuis.nuis_name
    if not force_no_CADItag:
        if nuis.add_anaID:
            nuis_rootname = ns_conf.nuis_names["CMS-CADI-tag"] + nuis_rootname
        if nuis.add_era_tags:
            nuis_rootname = nuis_rootname + "_"
            if nuis.sep_yrs:
                nuis_rootname += year_tag
            else:
                nuis_rootname += ns_conf.nuis_names["Run2-key"]

    if nuis.corr is True:
        return nuis_rootname
    elif nuis.corr is False:
        return [nuis_rootname + "b" + str(i + 1) for i in range(nbins)]
    else:
        raise Exception("Unable to interpret nuisance for name->datacard conversion:", nuis.nuis_name)


def return_newline():
    return """
________
"""


def turn_info_to_line(ns_name, ns_type, strls, write_sig):
    """Build one datacard line string.

    -INPUTS-
    ns_name, ns_type: str
    strls: list of anything that becomes str
    write_sig: Boolean. If True the signal columns are written first, else the background ones
    """
    if len(strls) != nbins:
        raise Exception("Bad line input.")
    new_line = "\n"
    nuis_seg = ""
    dash = pad("-", 7, False)

    for i in range(nbins):
        nuis_seg += dash if strls[i] is None else pad(str(strls[i]), 7, False)

    new_line += pad(ns_name, 30) + pad(ns_type, 5)
    dash_tag = "DASH%d" % nbins
    if write_sig is True:
        new_line += nuis_seg + return_sep() + dash_tag
    elif write_sig is False:
        new_line += dash_tag + return_sep() + nuis_seg
    else:
        raise Exception("Specify whether to write signal or bkg")
    return new_line


def turn_info_to_nlines(ns_names, ns_type, strls, write_sig):
    """Build per-bin datacard lines (un-correlated nuisances).

    -INPUTS-
    ns_names: list-like of str, one name per bin
    ns_type: str
    strls: list of anything that becomes str
    write_sig: Boolean
    """
    if len(strls) != nbins or len(ns_names) != nbins:
        raise Exception("Bad line input.")
    new_lines = ""
    for i in range(nbins):
        in_strls = [None if j != i else strls[i] for j in range(nbins)]
        new_lines += turn_info_to_line(ns_names[i], ns_type, in_strls, write_sig)
    return new_lines


def return_no_dashes(template):
    new_template = template
    for d in range(nbins + 1):
        new_template = new_template.replace("DASH%i" % d, d * pad("-", 7, False))
    return new_template


# ---------------------------------------------------------------------------
# Long functions
# ---------------------------------------------------------------------------

def add_ijkmax(template, nuis_ls, nuis_bkg_ls, siggrp):
    new_template = template + "\nimax " + str(nbins) + "\njmax 1\nkmax "

    k_ct = 0
    for nuis in nuis_ls + nuis_bkg_ls:
        if nuis.nuis_type == "special":
            if nuis.extra_info[0] == "updn_pair":
                if nuis.extra_info[1] == "dn":
                    continue
        if nuis.corr is True:
            k_ct += 1
        elif nuis.corr is False:
            k_ct += nbins
        else:
            print("Warning: unable to count k due to bad nuisance object:", nuis.nuis_name)

    new_template += str(k_ct)
    return new_template


def add_observations(template, f, siggrp, sig_id):
    new_template = template + pad("bin", 12)
    for i in range(nbins):
        new_template += b_nm(str(i))

    new_template += "\n" + pad("observation", 12)
    h_obs = ROOT.TH1D(f.Get("h_observed_%s" % year))
    for i in range(nbins):
        new_template += pad(str(int(h_obs.GetBinContent(i + 1))), 7, False)
    h_obs.Delete()
    return new_template


def add_central_vals(template, f, sig_norm_ls, siggrp, sig_id):
    """Build the bin/process/rate block; fills sig_norm_ls in place for Gamma-N.

    -INPUTS-
    sig_norm_ls: list (probably empty), will store extracted signal values for Gamma-N
    """
    new_template = template + pad("bin", 12)
    for j in range(n_proc):
        for i in range(nbins):
            new_template += b_nm(str(i))
        if j != n_proc - 1:
            new_template += return_sep()

    new_template += "\n" + pad("process", 12) + nbins * sig_nm(sig_id) + return_sep() + nbins * bkg_nm()
    new_template += "\n" + pad("process", 12) + nbins * pad("0", 7, False) + return_sep() + nbins * pad("1", 7, False)

    h_sig = f.Get(sig_nm(sig_id).replace(" ", ""))
    h_bkg = f.Get(bkg_nm().replace(" ", ""))
    to_write = [h_sig, h_bkg]

    new_template += "\n" + pad("rate", 12)
    for j in range(n_proc):
        for i in range(nbins):
            new_template += pad(str(to_write[j].GetBinContent(i + 1)), 3, False)
            if j == 0:
                sig_norm_ls.append(to_write[j].GetBinContent(i + 1))
        if j != n_proc - 1:
            new_template += return_sep()

    h_sig.Delete()
    h_bkg.Delete()
    return new_template, sig_norm_ls


def return_lnN_corr(f, ns_ls, siggrp, write_sig):
    new_lines = ""
    for nuis in ns_ls:
        try:
            if nuis.nuis_type != "lnN":
                continue
            if nuis.corr is not True:
                continue
        except Exception:
            raise Exception("Failure: Nuisance object not complete")
        dc_name = make_nuis_dcnm(nuis, siggrp)
        new_lines += turn_info_to_line(dc_name, "lnN", nuis.nuis_val, write_sig)
    new_lines += "\n"
    return new_lines


def return_lnN_uncorr(f, ns_ls, siggrp, write_sig):
    new_lines = ""
    for nuis in ns_ls:
        try:
            if nuis.nuis_type != "lnN":
                continue
            if nuis.corr is not False:
                continue
        except Exception:
            raise Exception("Failure: Nuisance object not complete")
        dc_names = make_nuis_dcnm(nuis, siggrp)
        new_lines += turn_info_to_nlines(dc_names, "lnN", nuis.nuis_val, write_sig)
    new_lines += "\n"
    return new_lines


def return_shape_lines(f, ns_ls, siggrp, sig_id, write_sig=True):
    """Write shape systematics as lnN lines using Up/Down histogram ratios."""
    new_lines = ""
    for nuis in ns_ls:
        if nuis.nuis_type != "shape":
            continue

        dc_name = make_nuis_dcnm(nuis, siggrp)
        process_htag = (sig_nm(sig_id) if write_sig else bkg_nm()).replace(" ", "")

        hname_up = process_htag + "_" + dc_name + "Up"
        hname_dn = process_htag + "_" + dc_name + "Down"

        h_central  = f.Get(process_htag)
        h_shape_up = f.Get(hname_up)
        h_shape_dn = f.Get(hname_dn)

        strls = []
        for i in range(nbins):
            try:
                strls.append(
                    str(h_shape_dn.GetBinContent(i + 1) / h_central.GetBinContent(i + 1))
                    + "/" +
                    str(h_shape_up.GetBinContent(i + 1) / h_central.GetBinContent(i + 1))
                )
            except Exception:
                strls.append("1.0/1.0")
                print("Warning: division by 0 in up/down variations. Filling 1.0 for",
                      siggrp.fn, "bin", i)

        new_lines += turn_info_to_line(dc_name, "lnN", strls, write_sig)

    new_lines += "\n"
    return new_lines


def return_special_lines(f, ns_ls, sig_norm_ls, siggrp, sig_id, write_sig=True):
    """Handle GammaN, updn_pair, and anti-lnN nuisance types. Any new ad-hoc nuisance
    types get handled here.

    -INPUTS-
    sig_norm_ls: list of floats, extracted during the get-signal stage
    """
    new_lines = ""

    for nuis in ns_ls:
        try:
            if nuis.nuis_type in ("lnN", "shape"):
                continue
        except Exception:
            raise Exception("Failure: Nuisance object not complete")

        if nuis.nuis_type == "GammaN":
            if not write_sig:
                raise Exception("GammaN not implemented for background")

            dc_names = make_nuis_dcnm(nuis, siggrp)
            sig_cts_hname = "h_sig%s_ngen_perbin_%s" % (sig_id, year)
            h_sig_cts = f.Get(sig_cts_hname)

            # Precompute per-event weight fallback (AN formula):
            # w = Lumi x XSection / Generated_MC_Events_Pre-Cuts
            # Used when a bin has zero unweighted events.
            _h_ngen     = f.Get("h_sig%s_ngen_total_%s"    % (sig_id, year))
            _h_sigyield = f.Get("h_sig%s_sigyield_total_%s" % (sig_id, year))
            _ngen_total     = _h_ngen.GetBinContent(1)     if _h_ngen     else 0.0
            _sigyield_total = _h_sigyield.GetBinContent(1) if _h_sigyield else 0.0
            _w_precut = (_sigyield_total / _ngen_total) if _ngen_total > 0 else 0.0

            for i in range(nbins):
                strls = []
                for j in range(nbins):
                    if j != i:
                        strls.append(None)
                    else:
                        count = h_sig_cts.GetBinContent(j + 1)
                        if count > 0:
                            kappa = sig_norm_ls[j] / count
                        else:
                            # Fall back to pre-cut weight estimate per AN:
                            # w = Lumi x XSection / Generated_MC_Events_Pre-Cuts
                            kappa = _w_precut
                        strls.append(kappa)
                new_lines += turn_info_to_line(
                    dc_names[i],
                    "gmN " + pad(str(int(h_sig_cts.GetBinContent(i + 1))), 5),
                    strls, write_sig
                )
            continue

        elif nuis.nuis_type == "special":
            if nuis.extra_info[0] == "updn_pair":
                if nuis.extra_info[1] == "up":  # skip down
                    pair_found = False
                    for n2 in ns_ls:
                        if (n2.nuis_name == nuis.nuis_name and
                                n2.nuis_type == nuis.nuis_type and
                                n2.extra_info[1] == "dn"):
                            npair = n2
                            pair_found = True
                            break
                    if not pair_found:
                        raise Exception("updn_pair UP has no corresponding DOWN")

                    strls = [str(npair.nuis_val[i]) + "/" + str(nuis.nuis_val[i])
                             for i in range(nbins)]
                    if nuis.corr is True:
                        new_lines += turn_info_to_line(make_nuis_dcnm(nuis, siggrp), "lnN", strls, write_sig)
                    else:
                        new_lines += turn_info_to_nlines(make_nuis_dcnm(nuis, siggrp), "lnN", strls, write_sig)
                elif nuis.extra_info[1] != "dn":
                    raise Exception("Bad extra_info field, use up or dn")

            if nuis.extra_info[0] == "anti-lnN":
                if nuis.corr is not True:
                    raise Exception("Anti-correlated lnN does not support un-correlated bins")
                dc_name = make_nuis_dcnm(nuis, siggrp)
                strls = [str(nuis.nuis_val[i]) + "/" + str(1 / nuis.nuis_val[i])
                         for i in range(nbins)]
                new_lines += turn_info_to_line(dc_name, "lnN", strls, write_sig)

        else:
            print("Warning: nuisance", nuis.nuis_name, "has not been interpreted as a datacard line")
            if write_sig:
                print("  Generated when evaluating signal")
            else:
                print("  Generated when evaluating background")
            continue

    new_lines += "\n"
    return new_lines


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def make_datacard(f, nuis_ls, nuis_bkg_ls, siggrp, sig_id, debug_mode=False):
    """Write a combine .txt datacard to disk for one signal hypothesis.

    -INPUTS-
    nuis_ls: list of nuisance objects, for signal
    nuis_bkg_ls: list of nuisance objects, for background
    siggrp: SigGrp object storing information about the signal MiniTree
    sig_id: string, the integer indexing the signal
    debug_mode: Bool, whether to print debug statements
    """
    sig_name = "sig" + year_tag + sig_id
    if debug_mode:
        print("\nSearching for signal named", sig_name)

    h_sig_tot = f.Get(sig_nm(sig_id).replace(" ", ""))
    template = (
        "# sample id in ROOT file " + sig_id + "\n"
        "# filename = " + siggrp.fn + "\n"
        "# total sig rate = " + "{:.4e}".format(h_sig_tot.Integral())
    )

    template = add_ijkmax(template=template, nuis_ls=nuis_ls, nuis_bkg_ls=nuis_bkg_ls, siggrp=siggrp)
    template += return_newline()

    template = add_observations(template=template, f=f, siggrp=siggrp, sig_id=sig_id)
    template += return_newline()

    sig_norm_ls = []
    template, sig_norm_ls = add_central_vals(template=template, f=f, sig_norm_ls=sig_norm_ls,
                                              siggrp=siggrp, sig_id=sig_id)
    template += return_newline()

    # Signal nuisances
    template += return_lnN_corr(f=f, ns_ls=nuis_ls, siggrp=siggrp, write_sig=True)
    template += return_lnN_uncorr(f=f, ns_ls=nuis_ls, siggrp=siggrp, write_sig=True)
    template += return_shape_lines(f=f, ns_ls=nuis_ls, siggrp=siggrp, sig_id=sig_id, write_sig=True)
    template += return_special_lines(f=f, ns_ls=nuis_ls, sig_norm_ls=sig_norm_ls,
                                     siggrp=siggrp, sig_id=sig_id, write_sig=True)

    # Background nuisances
    template += return_lnN_corr(f=f, ns_ls=nuis_bkg_ls, siggrp=siggrp, write_sig=False)
    template += return_lnN_uncorr(f=f, ns_ls=nuis_bkg_ls, siggrp=siggrp, write_sig=False)
    template += return_special_lines(f=f, ns_ls=nuis_bkg_ls, sig_norm_ls=sig_norm_ls,
                                     siggrp=siggrp, sig_id=sig_id, write_sig=False)

    template = return_no_dashes(template)

    if debug_mode:
        print("Printing DATACARD:\n")
        print(template)

    dc_dict   = config.datacard_out_loc
    out_dc_fn = (dc_dict[sig_type]["out_folder"] + dc_dict["out_fn_prefix"]
                 + siggrp.trig_type + "_" + siggrp.return_nuis_key())
    if config.debug_settings["scale_bkg_fake"]:
        out_dc_fn += "_fakebkg"
    out_dc_fn += dc_dict["out_fn_suffix"]

    if debug_mode:
        print("Writing datacard to:", out_dc_fn)
    with open(out_dc_fn, "w") as datacard:
        datacard.write(template)

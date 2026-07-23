from __future__ import print_function
import argparse
import os
import sys
from glob import glob

import ROOT
import numpy as np

from JMTucker.Tools.ROOTTools import to_TH1D, move_overflow_into_last_bin

import script_configs as config
import sig_and_bkg_configs as sb_conf
import getNuisanceFromSig as getns
import makeDatacard as mkdat
import nuisance_configs_and_functions as nsfc
import helper_PyStorage_objects as sth
import helper_ROOT_functions as ROOThelper
from makeDatacard import make_nuis_dcnm as mk_dcnm


# ---------------------------------------------------------------------------
# CLI arguments -- override limits_config.yaml at runtime
# ---------------------------------------------------------------------------
def _parse_args():
    p = argparse.ArgumentParser(description="Build limits input ROOT file and datacards")
    p.add_argument("--minitree-dir",     required=True,
                   help="Folder holding the signal MiniTrees for this channel")
    p.add_argument("--bkg-template-dir", required=True,
                   help="Folder holding the background templates for this channel")
    p.add_argument("--out-dir",          required=True,
                   help="Base output folder; LimitsInput and Datacard subfolders are made under it")
    p.add_argument("--year",    default=None, help="Year to process: 20161/20162/2017/2018/all")
    p.add_argument("--channel", default=None, choices=["lep", "bjet"], help="Trigger channel")
    p.add_argument("--debug",   action="store_true", default=None, help="Verbose output")
    p.add_argument("--no-debug", dest="debug", action="store_false")
    return p.parse_args()


def _apply_args(args):
    """Push CLI overrides back into config dicts so the rest of the code is unchanged."""
    config.set_paths(minitree_dir=args.minitree_dir,
                     bkg_template_dir=args.bkg_template_dir,
                     out_dir=args.out_dir)
    if args.year and args.year != "all":
        config.datacard["year"] = args.year
    if args.channel:
        config.sig["type"] = args.channel
    if args.debug is not None:
        config.debug_settings["enabled"] = args.debug


# ---------------------------------------------------------------------------
# Module-level globals (set per-year run inside run_one_year)
# ---------------------------------------------------------------------------
debug         = None
sig_type      = None
year          = None
year_id       = None
year_tag      = None
nbins         = None
bins          = None
print_mapping = True


def _init_globals(yr):
    global debug, sig_type, year, year_id, year_tag, nbins, bins
    if yr not in config.datacard["year_key"]:
        raise ValueError("year %s not in year_key %s" % (yr, config.datacard["year_key"]))
    debug    = config.debug_settings["enabled"]
    sig_type = config.sig["type"]
    year     = yr
    year_id  = config.datacard["year_key"].index(yr)
    year_tag = config.datacard["year_to_tag"][yr]
    nbins    = config.datacard["nbins"]
    bins     = np.array(config.datacard["bins"])
    mkdat._init_for_year(yr)
    nsfc._init_for_year(yr)


# ---------------------------------------------------------------------------
# Config sanity check
# ---------------------------------------------------------------------------
def check_config(yr):
    if yr not in config.datacard["year_key"]:
        raise ValueError("year %s not in year_key" % yr)
    if len(config.datacard["bins"]) != config.datacard["nbins"] + 1:
        raise ValueError("nbins must equal len(bins)-1")
    if config.sig["type"] not in ("lep", "bjet"):
        raise ValueError("channel must be 'lep' or 'bjet'")
    if len(config.obs[yr]) != config.datacard["nbins"]:
        raise ValueError("len(observations[year]) must equal nbins")
    if config.debug_settings["scale_bkg_fake"]:
        print("WARNING: scale_bkg_fake is True -- background will be artificially scaled")
    if config.debug_settings["scale_sig_fake"]:
        print("WARNING: scale_sig_fake is True -- signal will be artificially scaled")


# ---------------------------------------------------------------------------
# Background
# ---------------------------------------------------------------------------
def make_bkg(f):
    """
    Write: lumi, observations, rebinned sum_dBV. Nuisance parameters are added elsewhere.

    -INPUTS-
    f: ROOT file to write into
    """
    bkg_fn = os.path.join(
        config.bkg[sig_type]["folder"],
        config.bkg[sig_type]["fn"].format(year)
    )
    if debug:
        print("Opening bkg file:", bkg_fn)
    bkg_f = ROOT.TFile.Open(bkg_fn)

    new_bkg_hs = []

    h_int_lumi = ROOT.TH1D("h_int_lumi_%s" % year, "", 1, 0, 1)
    h_int_lumi.SetBinContent(1, sb_conf.template_norms["lumi"][sig_type][year_id])
    if debug:
        print("Lumi:", sb_conf.template_norms["lumi"][sig_type][year_id])
    new_bkg_hs.append(h_int_lumi)

    h_observed = ROOT.TH1D("h_observed_%s" % year, "", nbins, bins)
    for i, v in enumerate(config.obs[year]):
        h_observed.SetBinContent(i+1, v)
        if debug:
            print("  observed bin %d = %d" % (i, v))
    new_bkg_hs.append(h_observed)

    # Full Run 2 MC background -- shape normalized to per-year n2v from sig_and_bkg_configs.py
    h_bkg_sumdbv = to_TH1D(bkg_f.Get("h_c1v_sumdbv_w_errorbars"), "h_bkg_sumdbv_%s" % year)
    scale_num = sb_conf.template_norms["n2v"][sig_type][year_id]
    scale_den = h_bkg_sumdbv.Integral()
    h_bkg_sumdbv.Scale(scale_num / scale_den)
    if debug:
        print("Bkg Sum_dBV rescaled %.3g -> %.3g" % (scale_den, scale_num))

    if config.debug_settings["scale_bkg_fake"]:
        h_bkg_sumdbv.Scale(config.debug_settings["bkg_fake_sf"])
        print("WARNING: scaled bkg by fake factor", config.debug_settings["bkg_fake_sf"])

    h_bkg_sumdbv_rebin = h_bkg_sumdbv.Rebin(nbins, "bkg" + year_tag, bins)
    move_overflow_into_last_bin(h_bkg_sumdbv_rebin)
    new_bkg_hs.append(h_bkg_sumdbv_rebin)

    f.cd()
    for h in new_bkg_hs:
        h.SetTitle("")
        h.Write()
        if debug:
            print("  wrote:", h.GetName())

    print("BACKGROUND processing complete")


# ---------------------------------------------------------------------------
# Signal
# ---------------------------------------------------------------------------
def make_sigs(f, sig_nums, sig_scales, sig_fake_corrs):
    """
    Write: signal (rebinned sumdbv), ngen-per-bin, sumw, ngen total, sigyield total.

    -INPUTS-
    f: ROOT file to write into
    sig_nums: dictionary. Stores {SigGrp object : str}, the string index of each signal
    sig_scales: dictionary. Stores {SigGrp object : scalings from MiniTree sumw -> signal yield}
    sig_fake_corrs: dictionary. Stores {SigGrp object : fake scale factor or None}

    -OUTPUTS-
    f will store new histograms; sig_nums, sig_scales and sig_fake_corrs will be added to
    """
    sig_fn_syntax = config.sig[sig_type]["folder"] + config.sig[sig_type]["file_key"]
    candidate_files = sorted(glob(sig_fn_syntax))
    sig_id = 0
    built_clusters = set()
    wrong_channel = 0   # samples found that belong to the other trigger channel

    for cand in candidate_files:
        cand_id = os.path.basename(cand)
        if cand_id.startswith("minitree"):
            cand_id = os.path.basename(os.path.dirname(cand))
        if cand_id.find(year) == -1:
            continue
        generated_siggrp = False
        try:
            siginfo = sth.SignalROOTInfo(cand, root_exists=True, nbins=nbins)
            in_cluster = False
            for sc, members in config.sig["sig_grps"].items():
                if siginfo.proc in members:
                    in_cluster = True
                    # Trigger on whichever member is seen first, not only members[0], so a
                    # missing first member cannot make the whole cluster disappear silently.
                    cluster_key = cand.replace(siginfo.proc, sc)
                    if cluster_key in built_clusters:
                        break
                    sig_str_ls = [cand.replace(siginfo.proc, p) for p in members]
                    missing = [s for s in sig_str_ls if not os.path.exists(s)]
                    if (missing and len(missing) == len(members) - 1
                            and siginfo.proc in config.sig["sig_grp_wide_members"]):
                        # A wide-grid member sitting on its own: ggZH is generated at 12
                        # lifetimes where ZH and W+-H only exist at 6, so this is not a broken
                        # cluster, it is simply not a point where the cluster exists. Any other
                        # member alone falls through to the raise below.
                        print("Not a %s point, only %s exists here, skipping: %s"
                              % (sc, siginfo.proc, siginfo.return_nuis_key()))
                        break
                    if missing:
                        raise Exception(
                            "Incomplete %s cluster for %s. A partial cluster is not a valid "
                            "signal. Missing:\n  %s" % (sc, siginfo.return_nuis_key(),
                                                        "\n  ".join(missing)))
                    print("Found cluster", sc, ":", sig_str_ls)
                    siggrp = sth.SigRInf_Grp(sig_str_ls, root_exists=True, nbins=nbins, overwrite_proc=sc)
                    built_clusters.add(cluster_key)
                    generated_siggrp = True
                    break
            if not in_cluster:
                siggrp = sth.SigRInf_Grp([cand], root_exists=True, nbins=nbins, overwrite_proc=None)
                generated_siggrp = True
        except ValueError as e:
            if str(e) == "No Samples.py entry":
                print("Signal not in Samples.py, skipping:", os.path.basename(cand))
            else:
                raise
        if not generated_siggrp:
            continue
        if siggrp.trig_type != sig_type:
            wrong_channel += 1
            continue
        if debug:
            print("Queued signal #%d: %s (%s)" % (sig_id, os.path.basename(cand), siggrp.trig_type))
        sig_nums[siggrp] = str(sig_id)
        sig_id += 1
        siggrp.print_diagnostics()

    # A folder for the other channel still yields a few cards, because ttH sits in both the
    # lep and bjet lists and falls back to the configured channel. Catch that here rather than
    # writing a handful of cards built from the wrong MiniTrees. Only a genuine mismatch is an
    # error -- a year with no MiniTrees at all is normal and just gets skipped.
    if wrong_channel > len(sig_nums):
        raise Exception(
            "--minitree-dir does not look like a %s folder: %d %s signals queued but %d samples "
            "belong to the other channel.\n  %s"
            % (sig_type, len(sig_nums), sig_type, wrong_channel, config.sig[sig_type]["folder"]))

    if not sig_nums:
        print("No %s signals for year %s in %s, skipping this year"
              % (sig_type, year, config.sig[sig_type]["folder"]))
        return

    if print_mapping:
        print("\nSignal mapping:")
        for k, v in sig_nums.items():
            print("  %s : %s" % (k.fn, v))

    n = lambda sid, x: "h_sig%s_%s_%s" % (sid, x, year)

    for siggrp, sig_id in sig_nums.items():
        if debug:
            print("\nProcessing cluster:", siggrp.fn)

        sumw         = 0.0
        ngen         = 0
        sum_sigyield = 0.0
        scales = []

        r_f_corr = None  # "r fake correction", debug only
        if config.debug_settings["scale_sig_fake"]:
            fake_cfg = config.debug_settings["sig_fake_sf"][sig_type]
            r_f_corr = fake_cfg["overrides"].get(siggrp.proc, fake_cfg["default"])
        if r_f_corr is not None:
            print("WARNING: scaling signal", siggrp.proc, "by fake factor", r_f_corr)
        sig_fake_corrs[siggrp] = r_f_corr

        ROOT.TH1.AddDirectory(1)
        h_sumdbv_tot    = ROOT.TH1D(n(sig_id, "sumdbv"),       "", 800, 0, 8)
        h_sumdbv_nw_tot = ROOT.TH1D(n(sig_id, "sumdbv") + "_nw", "", 800, 0, 8)  # No-weight version

        for sig in siggrp.sig_ls:
            if debug:
                print("  sub-sig:", sig.fn)
            t = ROOT.TChain("mfvMiniTree/t")
            t.Add(sig.full_fn)

            this_sumw      = sig.get_sumw()
            this_ngen      = sig.get_ngen()
            this_xsec      = sig.get_xsec()
            this_sigyield  = this_xsec * sb_conf.template_norms["lumi"][sig.trig_type][year_id]
            this_scale     = this_sigyield / this_sumw
            scales.append(this_scale)
            if debug:
                print("  xsec=%.3g  sumw=%.3g  yield=%.3g  scale=%.3g" % (
                    this_xsec, this_sumw, this_sigyield, this_scale))

            ROOT.TH1.AddDirectory(1)
            h_child    = ROOT.TH1D(n(sig_id, "child_sumdbv"),       "", 800, 0, 8)
            h_child_nw = ROOT.TH1D(n(sig_id, "child_sumdbv") + "_nw", "", 800, 0, 8)

            t.Draw("sumdbv>>%s" % n(sig_id, "child_sumdbv"),       "weight*(nvtx>=2)")
            t.Draw("sumdbv>>%s" % (n(sig_id, "child_sumdbv") + "_nw"), "1.0*(nvtx>=2)")

            ROOT.TH1.AddDirectory(0)
            h_child.SetDirectory(0)
            h_child_nw.SetDirectory(0)
            h_child.Scale(this_scale)

            h_sumdbv_tot.Add(h_child)
            h_sumdbv_nw_tot.Add(h_child_nw)

            sumw         += this_sumw
            ngen         += this_ngen
            sum_sigyield += this_sigyield
            t.Reset()
            h_child    = ROOT.TH1D()
            h_child_nw = ROOT.TH1D()

        sig_scales[siggrp] = scales

        h_sig = h_sumdbv_tot.Rebin(nbins, "sig" + year_tag + sig_id, bins)
        move_overflow_into_last_bin(h_sig)

        h_sig_nw = h_sumdbv_nw_tot.Rebin(nbins, n(sig_id, "ngen_perbin"), bins)
        move_overflow_into_last_bin(h_sig_nw)

        if r_f_corr is not None:
            h_sig.Scale(float(r_f_corr))

        for i in range(1, h_sig.GetNbinsX() + 1):
            if h_sig.GetBinContent(i) < 0:
                print("*" * 30)
                print("CLAMPING NEGATIVE WEIGHT FOR %s (bin %d, %g)"
                      % (siggrp.return_nuis_key(), i, h_sig.GetBinContent(i)))
                print("*" * 30)
                h_sig.SetBinContent(i, 0.0)

        h_sumw_hist     = ROOT.TH1D(n(sig_id, "sumw"),         "", 1, 0, 1)
        h_ngen_hist     = ROOT.TH1D(n(sig_id, "ngen_total"),   "", 1, 0, 1)
        h_sigyield_hist = ROOT.TH1D(n(sig_id, "sigyield_total"), "", 1, 0, 1)
        h_sumw_hist.SetBinContent(1, sumw)
        h_ngen_hist.SetBinContent(1, ngen)
        # sigyield carries the same fake scaling as h_sig, so that the zero-count Gamma-N
        # fallback in makeDatacard (w = sigyield_total/ngen_total) stays consistent with the
        # scaled rates instead of being 1/r_f_corr times too big.
        h_sigyield_hist.SetBinContent(
            1, sum_sigyield if r_f_corr is None else sum_sigyield * float(r_f_corr))

        f.cd()
        for h in [h_sig, h_sig_nw, h_sumw_hist, h_ngen_hist, h_sigyield_hist]:
            h.SetTitle(siggrp.proc + "_" + year)
            h.Write()
            if debug:
                print("  wrote:", h.GetName())

    print("SIGNAL processing complete")


# ---------------------------------------------------------------------------
# Shape systematics (up/down histograms)
# ---------------------------------------------------------------------------
def write_sig_updown(f, nuis_ls, siggrp, sig_scales, sig_fake_corrs, sig_id):
    """
    Given a list of nuisances and a signal tag, write the up/down histograms for every
    shape nuisance (non-shape nuisances are ignored).

    -INPUTS-
    f: ROOT file to write into
    nuis_ls: list of Nuisance objects
    siggrp: SigGrp object
    sig_scales: {SigGrp object : scales}, scale := MiniTree sumw -> signal yield
    sig_fake_corrs: {SigGrp object : fake scale factor or None}
    sig_id: string, the integer indexing the signal
    """
    scales = sig_scales[siggrp]
    if debug:
        print("\nShape systematics for:", siggrp.fn, "scales:", scales)

    r_f_corr = sig_fake_corrs[siggrp]

    for nuis in nuis_ls:
        if not nuis.make_updn:
            continue

        nname      = mk_dcnm(nuis, siggrp)
        nname_dict = mk_dcnm(nuis, siggrp, force_no_CADItag=True)

        hname_up = "sig" + year_tag + sig_id + "_" + nname + "Up"
        hname_dn = "sig" + year_tag + sig_id + "_" + nname + "Down"

        ROOT.TH1.AddDirectory(1)
        h_up_tot = ROOT.TH1D(hname_up + "_orig", "", 800, 0, 8)
        h_dn_tot = ROOT.TH1D(hname_dn + "_orig", "", 800, 0, 8)

        for i, sig in enumerate(siggrp.sig_ls):
            t = ROOT.TChain("mfvMiniTree/t")
            t.Add(sig.full_fn)

            ROOT.TH1.AddDirectory(1)
            h_up = ROOT.TH1D(hname_up + "_child_orig", "", 800, 0, 8)
            h_dn = ROOT.TH1D(hname_dn + "_child_orig", "", 800, 0, 8)

            wt_up, wt_dn = sb_conf.updn_wt_dict[nname_dict]
            t.Draw("sumdbv>>%s" % (hname_up + "_child_orig"),
                   "weight*(nvtx>=2)".replace("weight", wt_up))
            t.Draw("sumdbv>>%s" % (hname_dn + "_child_orig"),
                   "weight*(nvtx>=2)".replace("weight", wt_dn))

            h_up.Scale(scales[i])
            h_dn.Scale(scales[i])
            h_up_tot.Add(h_up)
            h_dn_tot.Add(h_dn)

            t.Reset()
            h_up = ROOT.TH1D()
            h_dn = ROOT.TH1D()

        ROOT.TH1.AddDirectory(0)
        h_sig_up = h_up_tot.Rebin(nbins, hname_up, bins)
        h_sig_dn = h_dn_tot.Rebin(nbins, hname_dn, bins)

        for h in [h_sig_up, h_sig_dn]:
            move_overflow_into_last_bin(h)
            if r_f_corr is not None:
                h.Scale(float(r_f_corr))
            h.SetDirectory(0)

        f.cd()
        for h in [h_sig_up, h_sig_dn]:
            h.SetTitle(siggrp.proc + "_" + year)
            h.Write()
            if debug:
                print("  wrote:", h.GetName())

        h_up_tot = ROOT.TH1D()
        h_dn_tot = ROOT.TH1D()
        h_sig_up = ROOT.TH1D()
        h_sig_dn = ROOT.TH1D()


# ---------------------------------------------------------------------------
# Main pipeline for one year
# ---------------------------------------------------------------------------
def run_one_year(yr):
    _init_globals(yr)
    check_config(yr)
    config.make_out_dirs(sig_type)

    if debug:
        print("\n=== Year: %s  Channel: %s ===" % (yr, sig_type))

    out_fn = config.output[sig_type]["out_folder"] + config.output["out_fn"]
    out_fn += "_%s_%s" % (sig_type, yr)
    if config.debug_settings["scale_bkg_fake"]:
        out_fn += "_fakebkg"
    out_fn += ".root"

    if debug:
        print("Output ROOT file:", out_fn)

    ROOT.TH1.AddDirectory(0)
    f = ROOT.TFile(out_fn, "recreate")

    if debug:
        print("\n--- Background ---")
    make_bkg(f)

    sig_nums   = {}  # signal obj to number dictionary
    sig_scales = {}  # store scalings for signals, preventing repeated calculations
    sig_fake_corrs = {}  # debug-only fake scalings, None unless scale_sig_fake is on

    if debug:
        print("\n--- Signal ---")
    make_sigs(f, sig_nums, sig_scales, sig_fake_corrs)

    if debug:
        print("\n--- Background nuisances ---")
    nuis_bkg_ls = []
    getns.get_nuis_frombkg(nuis_bkg_ls, debug_mode=debug)

    if debug:
        print("\n--- Signal nuisances + datacards ---")
    for siggrp, s_id in sig_nums.items():
        nuis_ls = []
        getns.get_nuis_fromsig(siggrp, nuis_ls, debug_mode=debug)
        write_sig_updown(f=f, nuis_ls=nuis_ls, siggrp=siggrp, sig_scales=sig_scales,
                         sig_fake_corrs=sig_fake_corrs, sig_id=s_id)
        mkdat.make_datacard(f=f, nuis_ls=nuis_ls, nuis_bkg_ls=nuis_bkg_ls,
                            siggrp=siggrp, sig_id=s_id, debug_mode=debug)

    f.Close()
    print("Done: %s  year=%s" % (sig_type, yr))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    args = _parse_args()
    _apply_args(args)

    years_to_run = config.datacard["year_key"] if (args.year == "all") else [config.datacard["year"]]

    for yr in years_to_run:
        run_one_year(yr)

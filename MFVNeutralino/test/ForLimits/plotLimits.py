#!/usr/bin/env python3
"""
Plot 95% CL upper limits on sigma x B^2 [fb] (SUSY) or BR(H->SS) (Higgs).

Reads CombineOutput/<sig_id>/higgsCombine<sig_id>.AsymptoticLimits.mH120.root
for all available hypotheses and produces per-process plots.

Output (in LimitPlots/):
  <proc>_1D.pdf                         -- ctau on x, one curve per mass
  <proc>_1D_vsmass.pdf                  -- mass on x, all ctau values overlaid
  <proc>_1D_vsmass_<c1>_vs_<c2>.pdf    -- mass on x, one plot per adjacent ctau pair
  <proc>_2D.pdf                         -- ctau vs mass 2D color map + r=1 exclusion contour
  <proc>_1D_hepcomp_M<m1>vsM<m2>.pdf   -- ctau on x, Low-HT vs High-HT (HepData) per mass pair
  <proc>_1D_hepcomp_vsmass_<c1>vs<c2>.pdf  -- mass on x, Low-HT vs High-HT per ctau pair

HepData reference (ins1861146, old high-HT displaced vertex analysis):
  Only used for comparison 1D plots (never shown on 2D plots).
  Load from hepdata_ins1861146.json if present.
  Template: {"mfv_neu": {"ctau_mm": [c1,...], "mass_gev": [m1,...],
                          "obs": [[r_c1m1, r_c1m2,...], [r_c2m1,...],...] }}
  where obs[i][j] = observed limit at ctau_mm[i], mass_gev[j].

Usage
  python3 plotLimits.py [--subset VH,mfv_neu] [--out-dir LimitPlots]
"""
import os
import sys
import json
import argparse
import numpy as np

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

try:
    import mplhep as hep
    hep.style.use("CMS")
    _HAS_MPLHEP = True
except ImportError:
    _HAS_MPLHEP = False

try:
    from scipy.interpolate import RectBivariateSpline
    _HAS_SCIPY = True
except ImportError:
    _HAS_SCIPY = False
    print("Warning: scipy not available; 2D plots will show grid points only")

HERE         = os.path.dirname(os.path.abspath(__file__))
COMBINE_OUT  = os.path.join(HERE, "CombineOutput")
HEPDATA_JSON = os.path.join(HERE, "hepdata_ins1861146.json")
PLOT_DIR     = os.path.join(HERE, "LimitPlots")
_ONE2TWO     = os.path.join(HERE, "..", "One2Two")

# Theory XS CSV files (SUSY XS WG, NNLO_approx+NNLL) used to convert HepData
# from r = σ×B²/σ_theory (how it is stored) to σ×B² in fb (our r units, σ_ref=1fb).
_HEPDATA_THEORY_CSV = {
    "mfv_neu":          os.path.join(_ONE2TWO, "gluglu.csv"),
    "mfv_stopdbardbar": os.path.join(_ONE2TWO, "stopstop.csv"),
    "mfv_stopbbarbbar": os.path.join(_ONE2TWO, "stopstop.csv"),
}

# Additional theory curves drawn on top of the primary one (keyed by process).
# For mfv_neu: EWK Higgsino N2N1 (Ñ₂χ̃₁⁰, aNNLO-NNLL, fully degenerate, 13 TeV).
# Only N2N1 is relevant: both final-state particles are neutral, matching the
# neutral LLP produced in the gluino signal MC. C1C1/N2C1 involve charginos
# which are themselves long-lived in the degenerate limit (different topology).
_EXTRA_THEORY_CSV = {
    "mfv_neu": os.path.join(_ONE2TWO, "higgsino_N2N1.csv"),
}


PROC_LABELS = {
    "VH":                  r"WH + ZH (incl. gg),  H$\to$SS$\to$dddd",
    "ggZHToSSTobbbb":      r"ggZH,  H$\to$SS$\to$bbbb",
    "ggHToSSTodddd":       r"ggH,  H$\to$SS$\to$dddd",
    "ttHToLLPs_bbbb":      r"ttH,  H$\to$SS$\to$bbbb",
    "ttHToLLPs_dddd":      r"ttH,  H$\to$SS$\to$dddd",
    "mfv_neu":             r"RPV SUSY,  $\tilde{g}\to qqq$",
    "mfv_stopdbardbar":    r"RPV SUSY,  $\tilde{t}\to\bar{d}\bar{d}$",
    "mfv_stopbbarbbar":    r"RPV SUSY,  $\tilde{t}\to\bar{b}\bar{b}$",
}

_SUSY_PROCS = {"mfv_neu", "mfv_stopdbardbar", "mfv_stopbbarbbar"}

# Fixed 2D colorbar scale (vmin, vref, vmax) in fb, keyed by process.
# vref is the neutral-color pivot (white on RdBu_r) and the colorbar reference line.
# For SUSY: pivot near the expected exclusion boundary (~1-100 fb for M~1-2 TeV).
# Falls back to automatic geometric-mean computation for unspecified processes.
_2D_VSCALE = {
    "mfv_neu":          (0.1,   10.0,  1e5),
    "mfv_stopdbardbar": (0.1,   10.0,  1e5),
    "mfv_stopbbarbbar": (0.1,   10.0,  1e5),
    # Higgs: pivot at SM benchmark BR=1%; range covers 0.1%-100% (well beyond any limit)
    "VH":               (1e-3,  0.01,  1.0),
    "ggZHToSSTobbbb":   (1e-3,  0.01,  1.0),
    "ggHToSSTodddd":    (1e-3,  0.01,  1.0),
    "ttHToLLPs_bbbb":   (1e-3,  0.01,  1.0),
    "ttHToLLPs_dddd":   (1e-3,  0.01,  1.0),
}

# BR(H→SS) benchmark used as datacard normalization and as reference line on plots.
_BR_HSS = 0.01


def _sig_scale_fb(proc, mass=None):
    """Scale factor to convert Combine r to physical units.

    SUSY: σ_ref = 1 fb → r = σ×B² [fb] → return 1.0.
    H→SS: σ_ref = σ_SM_H × BR(H→SS=1%) [× filter_eff, which cancels].
          r = σ(H)×BR(H→SS) / (σ_SM × 0.01), so BR(H→SS) = r × 0.01.
          σ_SM cancels regardless of production mode → return _BR_HSS for all Higgs.
    """
    if proc in _SUSY_PROCS:
        return 1.0
    return _BR_HSS


_COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628"]

_RUN2_LUMI = r"137.9 fb$^{-1}$ (13 TeV)"

# Per-process normalization footnote shown in the plot annotation box.
_PROC_NORM_NOTES = {}


# ---------------------------------------------------------------------------
# Parsing / I/O
# ---------------------------------------------------------------------------

def ctau_to_mm(s):
    """'300um' -> 0.3,  '1mm' -> 1.0,  '10mm' -> 10.0"""
    if s.endswith("um"):
        return float(s[:-2]) * 1e-3
    if s.endswith("mm"):
        return float(s[:-2])
    if s.endswith("cm"):
        return float(s[:-2]) * 10.0
    return float(s)


def parse_sig_id(sig_id):
    """'VH_tau1mm_M15' -> ('VH', '1mm', '15')"""
    parts = sig_id.split("_tau")
    if len(parts) != 2:
        return None, None, None
    proc = parts[0]
    sub  = parts[1].split("_", 1)
    if len(sub) < 2:
        return None, None, None
    ctau = sub[0]
    mass = sub[1].lstrip("M").lstrip("0") or "0"
    return proc, ctau, mass


def read_limits(sig_id):
    """Return {key: r_value} or None.  Keys: obs, exp, dn1, up1, dn2, up2."""
    fn = os.path.join(COMBINE_OUT, sig_id,
                      "higgsCombine%s.AsymptoticLimits.mH120.root" % sig_id)
    if not os.path.exists(fn):
        return None
    try:
        f = ROOT.TFile.Open(fn)
        if not f or f.IsZombie():
            return None
        t = f.Get("limit")
        if not t:
            f.Close()
            return None
        quant_map = {
            -1.0:  "obs",
            0.025: "dn2",
            0.16:  "dn1",
            0.5:   "exp",
            0.84:  "up1",
            0.975: "up2",
        }
        result = {}
        for _ in t:
            q = round(float(t.quantileExpected), 3)
            for qref, key in quant_map.items():
                if abs(q - qref) < 0.01:
                    result[key] = float(t.limit)
        f.Close()
        return result if "exp" in result else None
    except Exception as exc:
        print("Could not read %s: %s" % (fn, exc))
        return None


def collect_all():
    """Return {proc -> {mass_str -> {ctau_mm_float -> {obs/exp/...}}}}"""
    data = {}
    if not os.path.isdir(COMBINE_OUT):
        return data
    for sig_id in sorted(os.listdir(COMBINE_OUT)):
        if not os.path.isdir(os.path.join(COMBINE_OUT, sig_id)):
            continue
        proc, ctau_str, mass = parse_sig_id(sig_id)
        if proc is None:
            continue
        ctau_mm = ctau_to_mm(ctau_str)
        if ctau_mm <= 0:
            continue  # skip prompt (ctau=0) signals -- not meaningful for dv limits
        lims = read_limits(sig_id)
        if lims is None:
            continue
        data.setdefault(proc, {}).setdefault(mass, {})[ctau_mm] = lims
    return data


def _load_theory_xsec_csv(csv_path):
    """Return (mass_arr, xsec_fb_arr) from a SUSY XS WG CSV (cols: mass_GeV, xs_pb, unc_pct)."""
    rows    = [eval(l.strip()) for l in open(csv_path) if l.strip()]
    masses  = np.array([r[0] for r in rows], dtype=float)
    xsec_fb = np.array([r[1] for r in rows], dtype=float) * 1000.0  # pb -> fb
    return masses, xsec_fb


def _interp_theory_xsec_fb(mass_gev, masses, xsec_fb):
    """Log-log interpolation/extrapolation of theory XS in fb at mass_gev."""
    lm  = np.log(masses)
    lxs = np.log(xsec_fb)
    return float(np.exp(np.interp(np.log(float(mass_gev)), lm, lxs)))


def _hepdata_r_to_sigxb2_fb(hd_proc, csv_path):
    """Convert HepData obs from r=σ×B²/σ_theory to σ×B² in fb using the theory XS CSV."""
    masses_csv, xsec_fb_csv = _load_theory_xsec_csv(csv_path)
    hd_masses = hd_proc["mass_gev"]
    obs_raw   = np.array(hd_proc["obs"])  # shape: (n_ctau, n_mass)
    xs_col    = np.array([_interp_theory_xsec_fb(m, masses_csv, xsec_fb_csv)
                           for m in hd_masses])
    obs_fb = obs_raw * xs_col[np.newaxis, :]  # broadcast over ctau axis
    return {
        "ctau_mm":  hd_proc["ctau_mm"],
        "mass_gev": hd_proc["mass_gev"],
        "obs":      obs_fb.tolist(),
    }


def load_hepdata():
    """Load HepData JSON and convert SUSY proc obs from r to σ×B² in fb."""
    if not os.path.exists(HEPDATA_JSON):
        return {}
    with open(HEPDATA_JSON) as fh:
        raw = json.load(fh)
    out = {}
    for proc, hd_proc in raw.items():
        csv_path = _HEPDATA_THEORY_CSV.get(proc)
        if csv_path and os.path.exists(csv_path):
            out[proc] = _hepdata_r_to_sigxb2_fb(hd_proc, csv_path)
        elif csv_path:
            print("Warning: theory XS CSV not found for %s; HepData comparison skipped" % proc)
        else:
            out[proc] = hd_proc
    return out


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def _format_ctau(ctau_mm):
    """Format a ctau float for labels and filenames, e.g. 0.3 -> '0.3mm'."""
    if ctau_mm < 1.0:
        s = "%.3g" % ctau_mm
    else:
        s = "%.4g" % ctau_mm
    return s + "mm"


def _pair_list(items):
    """Non-overlapping adjacent pairs from a sorted list: (0,1), (2,3), ..."""
    return list(zip(items[0::2], items[1::2]))


def _invert_mass_data(mass_data):
    """Return {ctau_mm -> {mass_str -> limits}} from the standard mass-keyed dict."""
    ctau_data = {}
    for mass, cdict in mass_data.items():
        for ctau, lims in cdict.items():
            ctau_data.setdefault(ctau, {})[mass] = lims
    return ctau_data


def _sorted_masses(mass_data):
    return sorted(mass_data.keys(), key=lambda m: int(m) if m.isdigit() else 0)


def _hepdata_slice_at_mass(hd, mass_gev):
    """Interpolate HepData in mass; return (ctau_arr, r_arr) or (None, None)."""
    hd_ctaus  = np.array(hd["ctau_mm"])
    hd_masses = np.array(hd["mass_gev"])
    hd_obs    = np.array(hd["obs"])   # shape: (n_ctau, n_mass)
    if mass_gev < hd_masses[0] or mass_gev > hd_masses[-1]:
        return None, None
    r = np.array([np.interp(mass_gev, hd_masses, hd_obs[i, :])
                  for i in range(len(hd_ctaus))])
    return hd_ctaus, r


def _hepdata_slice_at_ctau(hd, ctau_mm):
    """Interpolate HepData in log(ctau); return (mass_arr, r_arr) or (None, None).

    ctau grids are log-spaced, so interpolation must be done in log space to avoid
    large biases between grid points (e.g. between 1 mm and 10 mm).
    """
    hd_ctaus  = np.array(hd["ctau_mm"])
    hd_masses = np.array(hd["mass_gev"])
    hd_obs    = np.array(hd["obs"])   # shape: (n_ctau, n_mass)
    if ctau_mm < hd_ctaus[0] or ctau_mm > hd_ctaus[-1]:
        return None, None
    log_ctaus = np.log(hd_ctaus)
    r = np.array([np.interp(np.log(ctau_mm), log_ctaus, hd_obs[:, j])
                  for j in range(len(hd_masses))])
    return hd_masses, r


def _draw_ref_curve_vsmass(ax, proc):
    """Draw theory/benchmark reference curves vs mass. Returns True if anything drawn."""
    if proc in _SUSY_PROCS:
        csv_path = _HEPDATA_THEORY_CSV.get(proc)
        if not csv_path or not os.path.exists(csv_path):
            return False
        masses_csv, xsec_fb_csv = _load_theory_xsec_csv(csv_path)
        label = r"$\tilde{g}\tilde{g}$ NLO+NNLL" if proc == "mfv_neu" else r"Theory $\sigma\mathcal{B}^{2}$"
        ax.plot(masses_csv, xsec_fb_csv, color="black", lw=1.5, ls="--",
                label=label, zorder=3)
        extra_path = _EXTRA_THEORY_CSV.get(proc)
        if extra_path and os.path.exists(extra_path):
            em, exs = _load_theory_xsec_csv(extra_path)
            ax.plot(em, exs, color="dimgray", lw=1.5, ls=":",
                    label=r"$\tilde{\chi}^{0}_{1}\tilde{\chi}^{0}_{2}$ aNNLO-NNLL", zorder=3)
        return True
    # Higgs: reference line at BR benchmark
    if proc not in _SUSY_PROCS:
        ax.axhline(_BR_HSS, color="black", lw=1.5, ls="--",
                   label=r"$\mathcal{B}(H{\to}SS) = 1\%$", zorder=3)
        return True
    return False


def _draw_ref_lines_ctau(ax, proc, masses_sorted, color_list):
    """Draw theory/benchmark reference lines on ctau plots. Returns True if anything drawn."""
    if proc in _SUSY_PROCS:
        return False  # theory curve shown on vsmass plots; per-mass lines clutter ctau plots
    # Higgs: single benchmark line at BR = 1%
    ax.axhline(_BR_HSS, color="black", lw=1.5, ls="--",
               label=r"$\mathcal{B}(H{\to}SS) = 1\%$", zorder=3)
    return True


def _annotate_proc(ax, proc):
    _proc_label = PROC_LABELS.get(proc, proc)
    _norm = _PROC_NORM_NOTES.get(proc, "")
    _annot = _proc_label + ("\n" + _norm if _norm else "")
    ax.text(0.0, -0.13, _annot,
            transform=ax.transAxes, fontsize=10, ha="left", va="top", clip_on=False)


def _ylabel(proc):
    if proc in _SUSY_PROCS:
        return r"95% CL upper limit on $\sigma\mathcal{B}^{2}$ [fb]"
    return r"95% CL upper limit on $\mathcal{B}(H{\to}SS)$"


def _mass_xlabel(proc):
    if proc == "mfv_neu":
        return r"Neutralino mass [GeV]"
    return "Mass [GeV]"


def _cms_label(ax):
    if _HAS_MPLHEP:
        hep.cms.label("Preliminary", data=False, ax=ax, fontsize=12, rlabel=_RUN2_LUMI)


def _save(fig, out_fn):
    plt.tight_layout()
    fig.savefig(out_fn, bbox_inches="tight")
    plt.close(fig)
    print("  -> %s" % out_fn)


# ---------------------------------------------------------------------------
# 1D: ctau on x-axis, one curve per mass  (original plot)
# ---------------------------------------------------------------------------

def plot_1d(proc, mass_data, out_dir, hepdata):
    fig, ax = plt.subplots(figsize=(8, 6))

    masses = _sorted_masses(mass_data)

    for i, mass in enumerate(masses):
        scale  = _sig_scale_fb(proc, mass)
        cdict  = mass_data[mass]
        ctaus  = sorted(cdict.keys())
        if not ctaus:
            continue
        exp    = [cdict[c]["exp"]                       * scale for c in ctaus]
        dn1    = [cdict[c]["dn1"]                       * scale for c in ctaus]
        up1    = [cdict[c]["up1"]                       * scale for c in ctaus]
        dn2    = [cdict[c].get("dn2", cdict[c]["dn1"]) * scale for c in ctaus]
        up2    = [cdict[c].get("up2", cdict[c]["up1"]) * scale for c in ctaus]

        col = _COLORS[i % len(_COLORS)]
        ax.fill_between(ctaus, dn2, up2, alpha=0.15, color=col, edgecolor="none")
        ax.fill_between(ctaus, dn1, up1, alpha=0.35, color=col, edgecolor="none")
        ax.plot(ctaus, exp, color=col, lw=2, ls="--",
                label="m = %s GeV (exp)" % mass)

        if "obs" in cdict[ctaus[0]]:
            obs = [cdict[c]["obs"] * scale for c in ctaus]
            ax.plot(ctaus, obs, color=col, lw=2, ls="-",
                    label="m = %s GeV (obs)" % mass)

    if not _draw_ref_lines_ctau(ax, proc, masses, _COLORS):
        pass
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel(_ylabel(proc))
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    _cms_label(ax)
    _annotate_proc(ax, proc)
    _save(fig, os.path.join(out_dir, "%s_1D.pdf" % proc))


# ---------------------------------------------------------------------------
# 1D: mass on x-axis, ctau as overlaid lines — all ctau in one plot
# ---------------------------------------------------------------------------

def plot_1d_vs_mass_all(proc, mass_data, out_dir):
    ctau_data    = _invert_mass_data(mass_data)
    ctaus_sorted = sorted(ctau_data.keys())

    fig, ax = plt.subplots(figsize=(8, 6))

    for i, ctau in enumerate(ctaus_sorted):
        mdict     = ctau_data[ctau]
        masses    = _sorted_masses(mdict)
        mass_vals = [int(m) for m in masses]
        scales    = [_sig_scale_fb(proc, m) for m in masses]

        exp  = [mdict[m]["exp"]                       * s for m, s in zip(masses, scales)]
        dn1  = [mdict[m]["dn1"]                       * s for m, s in zip(masses, scales)]
        up1  = [mdict[m]["up1"]                       * s for m, s in zip(masses, scales)]
        dn2  = [mdict[m].get("dn2", mdict[m]["dn1"]) * s for m, s in zip(masses, scales)]
        up2  = [mdict[m].get("up2", mdict[m]["up1"]) * s for m, s in zip(masses, scales)]

        col = _COLORS[i % len(_COLORS)]
        lbl = _format_ctau(ctau)
        ax.fill_between(mass_vals, dn2, up2, alpha=0.15, color=col, edgecolor="none")
        ax.fill_between(mass_vals, dn1, up1, alpha=0.35, color=col, edgecolor="none")
        ax.plot(mass_vals, exp, color=col, lw=2, ls="--",
                label=r"$c\tau$ = %s (exp)" % lbl)

        has_obs = "obs" in mdict[masses[0]]
        if has_obs:
            obs = [mdict[m]["obs"] * s for m, s in zip(masses, scales)]
            ax.plot(mass_vals, obs, color=col, lw=2, ls="-",
                    label=r"$c\tau$ = %s (obs)" % lbl)

    if not _draw_ref_curve_vsmass(ax, proc):
        pass
    ax.set_yscale("log")
    ax.set_xlabel(_mass_xlabel(proc))
    ax.set_ylabel(_ylabel(proc))
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    _cms_label(ax)
    _annotate_proc(ax, proc)
    _save(fig, os.path.join(out_dir, "%s_1D_vsmass.pdf" % proc))


# ---------------------------------------------------------------------------
# 1D: mass on x-axis, one plot per adjacent ctau pair  (+ optional HepData)
# ---------------------------------------------------------------------------

def _draw_lowht_pair(ax, proc, ctau_data, c1, c2):
    """Draw Low-HT exp+bands+obs for two ctau values, scaled to σ×B² [fb]."""
    for i, ctau in enumerate([c1, c2]):
        mdict     = ctau_data[ctau]
        masses    = _sorted_masses(mdict)
        mass_vals = [int(m) for m in masses]
        scales    = [_sig_scale_fb(proc, m) for m in masses]
        exp  = [mdict[m]["exp"]                       * s for m, s in zip(masses, scales)]
        dn1  = [mdict[m]["dn1"]                       * s for m, s in zip(masses, scales)]
        up1  = [mdict[m]["up1"]                       * s for m, s in zip(masses, scales)]
        dn2  = [mdict[m].get("dn2", mdict[m]["dn1"]) * s for m, s in zip(masses, scales)]
        up2  = [mdict[m].get("up2", mdict[m]["up1"]) * s for m, s in zip(masses, scales)]
        col = _COLORS[i]
        lbl = _format_ctau(ctau)
        ax.fill_between(mass_vals, dn2, up2, alpha=0.15, color=col, edgecolor="none")
        ax.fill_between(mass_vals, dn1, up1, alpha=0.35, color=col, edgecolor="none")
        ax.plot(mass_vals, exp, color=col, lw=2, ls="--",
                label=r"$c\tau$ = %s  Low-HT exp." % lbl)
        if "obs" in mdict[masses[0]]:
            obs = [mdict[m]["obs"] * s for m, s in zip(masses, scales)]
            ax.plot(mass_vals, obs, color=col, lw=2, ls="-",
                    label=r"$c\tau$ = %s  Low-HT obs." % lbl)


def _draw_hepdata_pair(ax, hd, c1, c2):
    """Overlay High-HT (HepData EXO-19-013) obs lines for two ctau values."""
    for i, ctau in enumerate([c1, c2]):
        hd_masses_sl, hd_r_sl = _hepdata_slice_at_ctau(hd, ctau)
        if hd_masses_sl is None:
            continue
        # Mask out zero/non-positive entries (JSON stores 0 for very strong exclusions)
        hd_masses_sl = np.array(hd_masses_sl)
        hd_r_sl      = np.array(hd_r_sl)
        keep = hd_r_sl > 0
        if not np.any(keep):
            continue
        col = _COLORS[i + 2]
        lbl = _format_ctau(ctau)
        ax.plot(hd_masses_sl[keep], hd_r_sl[keep], color=col, lw=2, ls="-",
                label=r"$c\tau$ = %s  High-HT obs. (EXO-19-013)" % lbl)


def plot_1d_vs_mass_pairs(proc, mass_data, out_dir, hepdata=None):
    ctau_data    = _invert_mass_data(mass_data)
    ctaus_sorted = sorted(ctau_data.keys())
    pairs        = _pair_list(ctaus_sorted)
    hd           = hepdata.get(proc) if hepdata else None

    for c1, c2 in pairs:
        fig, ax = plt.subplots(figsize=(8, 6))
        _draw_lowht_pair(ax, proc, ctau_data, c1, c2)
        if hd:
            _draw_hepdata_pair(ax, hd, c1, c2)
        if not _draw_ref_curve_vsmass(ax, proc):
            pass
        ax.set_yscale("log")
        ax.set_xlabel(_mass_xlabel(proc))
        ax.set_ylabel(_ylabel(proc))
        ax.legend(fontsize=9)
        ax.grid(True, which="both", ls=":", alpha=0.4)
        _cms_label(ax)
        _annotate_proc(ax, proc)
        tag = "%s_vs_%s" % (_format_ctau(c1), _format_ctau(c2))
        _save(fig, os.path.join(out_dir, "%s_1D_vsmass_%s.pdf" % (proc, tag)))


# ---------------------------------------------------------------------------
# 1D: mass on x-axis, two user-specified ctau values
# ---------------------------------------------------------------------------

def plot_1d_vs_mass_ctau_pair(proc, mass_data, out_dir, c1_mm, c2_mm, hepdata=None):
    """One plot with exactly two ctau values (specified in mm) overlaid."""
    ctau_data = _invert_mass_data(mass_data)
    available = sorted(ctau_data.keys())
    def _nearest(target):
        return min(available, key=lambda c: abs(c - target))
    c1 = _nearest(c1_mm)
    c2 = _nearest(c2_mm)
    if c1 == c2:
        print("  Skipping specific pair for %s: c1=c2=%s" % (proc, c1))
        return
    hd = hepdata.get(proc) if hepdata else None

    fig, ax = plt.subplots(figsize=(8, 6))
    _draw_lowht_pair(ax, proc, ctau_data, c1, c2)
    if hd:
        _draw_hepdata_pair(ax, hd, c1, c2)
    if not _draw_ref_curve_vsmass(ax, proc):
        pass
    ax.set_yscale("log")
    ax.set_xlabel(_mass_xlabel(proc))
    ax.set_ylabel(_ylabel(proc))
    ax.legend(fontsize=9)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    _cms_label(ax)
    _annotate_proc(ax, proc)
    tag = "%s_vs_%s" % (_format_ctau(c1), _format_ctau(c2))
    _save(fig, os.path.join(out_dir, "%s_1D_vsmass_%s.pdf" % (proc, tag)))


# ---------------------------------------------------------------------------
# 2D: ctau vs mass color map + r=1 contour  (no HepData overlay)
# ---------------------------------------------------------------------------

def _excl_thresholds_2d(proc, masses, mass_vals, theory_csv=None):
    """Return σ×B² [fb] exclusion threshold per mass column for the 2D contour.

    For SUSY: threshold = σ_theory_NLO(mass) from CSV. The r=1 Combine contour
    marks σ×B²=1 fb (arbitrary σ_ref), NOT the theory exclusion boundary.
    For H→SS: threshold = σ_ref_fb(proc, mass) = σ_SM × BR(1%) × filter_eff,
    so r=1 Combine contour IS the SM exclusion boundary — no correction needed.
    theory_csv overrides the default CSV for SUSY (used for EWK variant plots).
    """
    if proc in _SUSY_PROCS:
        csv_path = theory_csv if theory_csv is not None else _HEPDATA_THEORY_CSV.get(proc)
        if csv_path and os.path.exists(csv_path):
            masses_csv, xsec_fb_csv = _load_theory_xsec_csv(csv_path)
            return np.array([_interp_theory_xsec_fb(m, masses_csv, xsec_fb_csv)
                             for m in mass_vals])
    return np.array([_sig_scale_fb(proc, m) for m in masses])


def _interp_grid(log_ctaus, mass_vals, grid, fine_lct, fine_mass):
    if not _HAS_SCIPY:
        return None
    g = grid.copy()
    if np.all(np.isnan(g)):
        return None
    # fill missing cells with a large cap so contour at r=1 can still be drawn
    cap = max(200.0, float(np.nanmax(g)) * 2.0)
    g[np.isnan(g) | (g <= 0)] = cap
    sp = RectBivariateSpline(log_ctaus, mass_vals, np.log10(g), kx=1, ky=1)
    return 10.0 ** sp(fine_lct, fine_mass)


def plot_2d(proc, mass_data, out_dir, hepdata, theory_csv=None, fname_suffix=""):
    masses    = _sorted_masses(mass_data)

    # Build a rectangular grid (NaN for missing cells, capped in _interp_grid).
    # SUSY: drop masses with >1 missing ctau (e.g. M3000 hit wall time, only 2 jobs done).
    # Higgs: only 3 mass points total so keep any mass with >=2 valid ctau.
    # Use the union of all ctau values so no mass is excluded for lacking a corner point;
    # missing (ctau, mass) cells are left as NaN and capped to "not excluded" during interpolation.
    ctau_counts = {m: len(mass_data[m]) for m in masses}
    max_n       = max(ctau_counts.values())
    min_n       = max(3, max_n - 1) if proc in _SUSY_PROCS else 2
    masses      = [m for m in masses if ctau_counts[m] >= min_n]
    ctaus_all   = sorted(set.union(*[set(mass_data[m].keys()) for m in masses]))

    if len(masses) < 2 or len(ctaus_all) < 2:
        print("  Skipping 2D for %s: need at least 2x2 grid" % proc)
        return

    mass_vals = np.array([int(m) for m in masses], dtype=float)
    ctau_vals = np.array(ctaus_all, dtype=float)

    grid_exp = np.full((len(ctau_vals), len(mass_vals)), np.nan)
    grid_obs = np.full((len(ctau_vals), len(mass_vals)), np.nan)

    for j, mass in enumerate(masses):
        for i, ctau in enumerate(ctau_vals):
            if ctau in mass_data[mass]:
                ent = mass_data[mass][ctau]
                grid_exp[i, j] = ent["exp"]
                if "obs" in ent:
                    grid_obs[i, j] = ent["obs"]

    log_ctaus = np.log10(ctau_vals)
    # Extend 0.7 decades left of the first data point so the contour closes
    log_ctau_lo = log_ctaus[0] - 0.7
    fine_lct  = np.linspace(log_ctau_lo, log_ctaus[-1], 200)
    fine_mass = np.linspace(mass_vals[0],  mass_vals[-1],  200)
    fine_ctau = 10.0 ** fine_lct

    fine_exp = _interp_grid(log_ctaus, mass_vals, grid_exp, fine_lct, fine_mass)
    fine_obs = _interp_grid(log_ctaus, mass_vals, grid_obs, fine_lct, fine_mass)

    # Per-mass scale factors: σ_ref [fb] used in the datacard for each mass column.
    # For SUSY scale=1, so the raw Combine r grid is already in σ×B² [fb].
    scales     = np.array([_sig_scale_fb(proc, m) for m in masses])
    scale_fine = np.interp(fine_mass, mass_vals, scales)

    # Scaled grids for the colour map (σ×B² [fb]).
    grid_exp_s = grid_exp * scales[np.newaxis, :]
    grid_obs_s = grid_obs * scales[np.newaxis, :]
    fine_exp_s = fine_exp * scale_fine[np.newaxis, :] if fine_exp is not None else None
    fine_obs_s = fine_obs * scale_fine[np.newaxis, :] if fine_obs is not None else None

    # Exclusion threshold per mass: σ×B² [fb] value at which r=1 boundary is physical.
    # For SUSY this is σ_theory_NLO(mass); for H→SS it equals σ_ref_fb (= scales).
    thresholds  = _excl_thresholds_2d(proc, masses, mass_vals, theory_csv=theory_csv)
    thresh_fine = np.interp(fine_mass, mass_vals, thresholds)

    # Ratio grids: σ×B²_limit / threshold. Contour at 1.0 = genuine exclusion boundary.
    ratio_exp = grid_exp_s / thresholds[np.newaxis, :]
    ratio_obs = grid_obs_s / thresholds[np.newaxis, :]
    fine_ratio_exp = _interp_grid(log_ctaus, mass_vals, ratio_exp, fine_lct, fine_mass)
    fine_ratio_obs = _interp_grid(log_ctaus, mass_vals, ratio_obs, fine_lct, fine_mass)

    # Colormap: SUSY uses ratio = σ×B²_limit / σ_theory (pivot=1 = exclusion boundary).
    # Higgs uses absolute BR limit (pivot at benchmark BR=1%).
    if proc in _SUSY_PROCS:
        cmap_data_exp = fine_ratio_exp
        cmap_data_obs = fine_ratio_obs
        vmin, vref, vmax = 0.01, 1.0, 100.0
        cbar_label = r"$\sigma\mathcal{B}^{2}\ /\ \sigma_\mathrm{theory}$"
    else:
        cmap_data_exp = fine_exp_s
        cmap_data_obs = fine_obs_s
        vmin, vref, vmax = _2D_VSCALE.get(proc, (None, None, None))
        if vref is None:
            vref = float(np.exp(np.mean(np.log(thresholds[thresholds > 0]))))
            vmin, vmax = vref * 0.05, vref * 200.0
        cbar_label = _ylabel(proc)

    fig, ax = plt.subplots(figsize=(9, 6))

    n_half = 30
    levels = np.concatenate([
        np.logspace(np.log10(vmin), np.log10(vref), n_half + 1)[:-1],
        np.logspace(np.log10(vref), np.log10(vmax), n_half + 1),
    ])
    norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
    cmap = plt.get_cmap("RdBu_r")   # blue=excluded (ratio<1), red=not excluded

    _all_nice = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,
                 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
                 10000, 20000, 50000, 100000]
    _nice_ticks = [t for t in _all_nice if vmin <= t <= vmax]

    if cmap_data_exp is not None:
        cf = ax.contourf(fine_ctau, fine_mass, cmap_data_exp.T,
                         levels=levels, norm=norm, cmap=cmap, extend="both")
        cbar = plt.colorbar(cf, ax=ax, pad=0.02)
        cbar.set_label(cbar_label)
        cbar.set_ticks(_nice_ticks)
        cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
        cbar.ax.axhline(y=vref, color="black", lw=1.0, ls="--")

        # Exclusion contours on the ratio grid (= 1.0 where limit = theory/SM benchmark)
        ax.contour(fine_ctau, fine_mass, fine_ratio_exp.T, levels=[1.0],
                   colors=["black"], linewidths=[2.5], linestyles=["dashed"])
        ax.plot([], [], color="black", lw=2.5, ls="--", label="Exp. excl.")

        if fine_ratio_obs is not None:
            ax.contour(fine_ctau, fine_mass, fine_ratio_obs.T, levels=[1.0],
                       colors=["black"], linewidths=[2.5], linestyles=["solid"])
            ax.plot([], [], color="black", lw=2.5, ls="-", label="Obs. excl.")
    else:
        grid_cmap = ratio_exp if proc in _SUSY_PROCS else grid_exp_s
        xs, ys, cs = [], [], []
        for j, mass in enumerate(masses):
            for i, ctau in enumerate(ctau_vals):
                if not np.isnan(grid_cmap[i, j]):
                    xs.append(ctau)
                    ys.append(mass_vals[j])
                    cs.append(np.clip(grid_cmap[i, j], vmin, vmax))
        if xs:
            sc = ax.scatter(xs, ys, c=cs, s=300, zorder=5,
                            norm=norm, cmap=cmap,
                            edgecolors="black", linewidths=0.5)
            cbar = plt.colorbar(sc, ax=ax, pad=0.02)
            cbar.set_label(cbar_label)
            cbar.set_ticks(_nice_ticks)
            cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
            cbar.ax.axhline(y=vref, color="black", lw=1.0, ls="--")

    for j, mass in enumerate(masses):
        for i, ctau in enumerate(ctau_vals):
            ax.scatter(ctau, mass_vals[j], color="black", s=20, zorder=6)

    y_pad = max(3.0, (mass_vals[-1] - mass_vals[0]) * 0.08)
    ax.set_ylim(mass_vals[0] - y_pad, mass_vals[-1] + y_pad)
    ax.set_xscale("log")
    ax.set_xlim(10.0 ** log_ctau_lo, 10.0 ** (log_ctaus[-1] + 0.25))
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel("Mass [GeV]")
    ax.legend(fontsize=11, loc="upper right", framealpha=0.92, edgecolor="0.7")
    ax.grid(True, which="both", ls=":", alpha=0.3)
    _cms_label(ax)
    _annotate_proc(ax, proc)
    _save(fig, os.path.join(out_dir, "%s_2D%s.pdf" % (proc, fname_suffix)))




# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    global COMBINE_OUT
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir",     default=PLOT_DIR)
    ap.add_argument("--combine-out", default=COMBINE_OUT)
    ap.add_argument("--subset",      default=None,
                    help="Comma-separated process names to plot")
    args = ap.parse_args()

    COMBINE_OUT = args.combine_out

    if not os.path.isdir(COMBINE_OUT):
        print("CombineOutput not found: %s" % COMBINE_OUT)
        sys.exit(1)

    os.makedirs(args.out_dir, exist_ok=True)

    subset  = set(args.subset.split(",")) if args.subset else None
    hepdata = load_hepdata()
    if hepdata:
        print("Loaded HepData reference for: %s" % ", ".join(sorted(hepdata)))
    else:
        print("No HepData reference found at %s (comparison plots skipped)" % HEPDATA_JSON)

    data = collect_all()
    if not data:
        print("No limit results found in %s" % COMBINE_OUT)
        sys.exit(0)

    # ggZH is always grouped into VH; never plot it standalone
    _skip_procs = {"ggZHToSSTodddd", "ggZHToSSTobbbb"}

    for proc in sorted(data):
        if proc in _skip_procs:
            continue
        if subset and proc not in subset:
            continue
        n_masses = len(data[proc])
        n_pts    = sum(len(v) for v in data[proc].values())
        print("\n%s:  %d masses,  %d total hypotheses" % (proc, n_masses, n_pts))

        plot_1d(proc, data[proc], args.out_dir, hepdata)
        plot_1d_vs_mass_all(proc, data[proc], args.out_dir)
        plot_1d_vs_mass_pairs(proc, data[proc], args.out_dir, hepdata)
        if proc in ("ggHToSSTodddd", "VH"):
            plot_1d_vs_mass_ctau_pair(proc, data[proc], args.out_dir, 1.0, 10.0)
        plot_2d(proc, data[proc], args.out_dir, hepdata)
        if proc == "mfv_neu" and "mfv_neu" in _EXTRA_THEORY_CSV:
            plot_2d(proc, data[proc], args.out_dir, hepdata,
                    theory_csv=_EXTRA_THEORY_CSV["mfv_neu"],
                    fname_suffix="_ewk")

    print("\nDone. Plots saved to %s" % args.out_dir)


if __name__ == "__main__":
    main()

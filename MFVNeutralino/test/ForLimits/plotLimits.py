#!/usr/bin/env python3
"""
Plot 95% CL upper limits on sigma x B^2 [fb] (SUSY) or BR(H->SS) (Higgs).

Reads CombineOutput/<sig_id>/higgsCombine<sig_id>.HybridNew.mH120.root
(falls back to AsymptoticLimits if HybridNew output is absent)
for all available hypotheses and produces per-process plots.

Output (in LimitPlots/):
  <proc>_1D.pdf                         -- ctau on x, one curve per mass
  <proc>_1D_vsmass.pdf                  -- mass on x, all ctau values overlaid
  <proc>_1D_vsmass_<c1>_vs_<c2>.pdf    -- mass on x, one plot per adjacent ctau pair
  <proc>_2D.pdf                         -- ctau vs mass 2D color map + r=1 exclusion contour
  higgs_overlay_<4d|4b>_M<m>.pdf        -- ctau on x, one curve per Higgs production mode (each fitted on its own)
  *_published.pdf                       -- with --published-dir: the overlays and 2D maps with published
                                           observed limits from other analyses drawn on them
  <proc>_1D_hepcomp_M<m1>vsM<m2>.pdf   -- ctau on x, Low-HT vs High-HT (HepData) per mass pair
  <proc>_1D_hepcomp_vsmass_<c1>vs<c2>.pdf  -- mass on x, Low-HT vs High-HT per ctau pair

HepData reference (ins1861146, old high-HT displaced vertex analysis):
  Only used for comparison 1D plots (never shown on 2D plots).
  Load from hepdata_ins1861146.json if present.
  Template: {"mfv_neu": {"ctau_mm": [c1,...], "mass_gev": [m1,...],
                          "obs": [[r_c1m1, r_c1m2,...], [r_c2m1,...],...] }}
  where obs[i][j] = observed limit at ctau_mm[i], mass_gev[j].

Usage
  python3 plotLimits.py [--subset VHToSSTodddd,mfv_neu] [--out-dir LimitPlots]
"""
import os
import re
import sys
import csv
import json
import tarfile
import argparse
import numpy as np

import ROOT
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.patheffects as patheffects
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.legend_handler import HandlerLine2D
import contourpy

try:
    import mplhep as hep
    hep.style.use("CMS")
    _HAS_MPLHEP = True
except ImportError:
    _HAS_MPLHEP = False

plt.rcParams.update({
    "axes.labelsize":  13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
})

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

# Extra theory curves drawn on top (per process). For mfv_neu: EWK Higgsino N2N1
# (aNNLO-NNLL, 13 TeV) -- both final-state particles are neutral, matching the gluino LLP.
_EXTRA_THEORY_CSV = {
    "mfv_neu": os.path.join(_ONE2TWO, "higgsino_N2N1.csv"),
}

# Per theory CSV: (key of its twiki line in xsec_info.txt, process symbol, perturbative order).
_XSEC_INFO = os.path.join(_ONE2TWO, "xsec_info.txt")
_THEORY = {
    "gluglu.csv":        ("gluinos",     r"\tilde{g}\tilde{g}",                     r"NNLO$_\mathrm{approx}$+NNLL"),
    "stopstop.csv":      ("stops",       r"\tilde{t}\bar{\tilde{t}}",                r"NNLO$_\mathrm{approx}$+NNLL"),
    "higgsino_N2N1.csv": ("neutralinos", r"\tilde{\chi}^{0}_{1}\tilde{\chi}^{0}_{2}", r"aNNLO+NNLL, higgsino-like"),
}


_HSS_4D = r"H$\to$SS$\to$d$\bar{\mathrm{d}}$d$\bar{\mathrm{d}}$"
_HSS_4B = r"H$\to$SS$\to$b$\bar{\mathrm{b}}$b$\bar{\mathrm{b}}$"
PROC_LABELS = {
    "VHToSSTodddd":        r"WH + ZH (incl. gg),  " + _HSS_4D,
    "ggZHToSSTobbbb":      r"ggZH,  " + _HSS_4B,
    "VHToSSTobbbb":        r"WH + ZH (incl. gg),  " + _HSS_4B,
    "ggHToSSTodddd":       r"ggH,  " + _HSS_4D,
    "ggHToSSTobbbb":       r"ggH,  " + _HSS_4B,
    "ttHToSSTo4b_lep":     r"ttH (lepton-triggered),  " + _HSS_4B,
    "ttHToSSTo4d_lep":     r"ttH (lepton-triggered),  " + _HSS_4D,
    "ttHToSSTo4b_bjet":    r"ttH (displacement-triggered),  " + _HSS_4B,
    "ttHToSSTo4d_bjet":    r"ttH (displacement-triggered),  " + _HSS_4D,
    "VBFHToSSTo4b":        r"VBF H,  " + _HSS_4B,
    "VBFHToSSTo4d":        r"VBF H,  " + _HSS_4D,
    "mfv_neu":             r"RPV SUSY,  $\tilde{g}\to tbs$",
    "mfv_stopdbardbar":    r"RPV SUSY,  $\tilde{t}\to\bar{d}\bar{d}$",
    "mfv_stopbbarbbar":    r"RPV SUSY,  $\tilde{t}\to\bar{b}\bar{b}$",
}

_SUSY_PROCS = {"mfv_neu", "mfv_stopdbardbar", "mfv_stopbbarbbar"}
_EWK_LABEL = r"RPV SUSY,  $\tilde{\chi}^{0}_{1}\tilde{\chi}^{0}_{2}$,  $\tilde{\chi}^{0}\to tbs$"

# (vmin, vref, vmax) in fb for the 2D color scale; vref is the white pivot on RdBu_r.
# Unspecified processes fall back to geometric-mean auto-scaling.
_2D_VSCALE = {
    # Higgs: pivot at SM benchmark BR=1%; range covers 0.1%-100% (well beyond any limit)
    "VHToSSTodddd":     (1e-3,  0.01,  1.0),
    "ggZHToSSTobbbb":   (1e-3,  0.01,  1.0),
    "ggHToSSTodddd":    (1e-3,  0.01,  1.0),
    "ggHToSSTobbbb":    (1e-3,  0.01,  1.0),
    "VHToSSTobbbb":     (1e-3,  0.01,  1.0),
    "ttHToSSTo4b_lep":  (1e-3,  0.01,  1.0),
    "ttHToSSTo4d_lep":  (1e-3,  0.01,  1.0),
    "ttHToSSTo4b_bjet": (1e-3,  0.01,  1.0),
    "ttHToSSTo4d_bjet": (1e-3,  0.01,  1.0),
    "VBFHToSSTo4b":     (1e-3,  0.01,  1.0),
    "VBFHToSSTo4d":     (1e-3,  0.01,  1.0),
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
_RUN2_LUMI_DISP_TRIG = r"127.8 fb$^{-1}$ (13 TeV)"
_LUMI_2016 = r"36.3 fb$^{-1}$ (13 TeV)"
_DISP_TRIG_PROCS = {"ggHToSSTodddd", "ggHToSSTobbbb", "ttHToSSTo4b_bjet", "ttHToSSTo4d_bjet", "mfv_neu", "mfv_stopdbardbar", "mfv_stopbbarbbar"}
_2016_ONLY_PROCS = {"VBFHToSSTo4b", "VBFHToSSTo4d"}
_TABLE_ONLY_MODELS = {"ttHToSSTo2b2d", "ttHToSSTo4s", "VBFHToSSTo2b2d", "VBFHToSSTo4s"}

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
    """'VHToSSTodddd_tau1mm_M15' -> ('VHToSSTodddd', '1mm', '15')"""
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
    method_found = None
    fn = None
    for method in ("HybridNew", "AsymptoticLimits"):
        # HybridNew jobs run with -s 1234, which appends the seed to the filename.
        for suffix in (".mH120.1234.root", ".mH120.root"):
            candidate = os.path.join(COMBINE_OUT, sig_id,
                                     "higgsCombine%s.%s%s" % (sig_id, method, suffix))
            if os.path.exists(candidate):
                fn = candidate
                method_found = method
                break
        if fn:
            break
    if fn is None:
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
        # -t -1 (Asimov) puts the result in quantileExpected=-1 ("obs" slot) -- remap to "exp".
        if method_found == "HybridNew" and "obs" in result and "exp" not in result:
            result["exp"] = result.pop("obs")
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


def _load_theory_unc_frac(csv_path):
    rows = [eval(l.strip()) for l in open(csv_path) if l.strip()]
    return np.array([r[2] for r in rows], dtype=float) / 100.0


def _interp_theory_xsec_fb(mass_gev, masses, xsec_fb):
    """Log-log interpolation of theory XS in fb at mass_gev."""
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

def _format_ctau(ctau_mm, sep=""):
    """Format a ctau float for labels and filenames, e.g. 0.3 -> '0.3mm' (sep=" " gives '0.3 mm')."""
    if ctau_mm < 1.0:
        s = "%.3g" % ctau_mm
    else:
        s = "%.4g" % ctau_mm
    return s + sep + "mm"


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


def _theory_curve(csv_path, xlim=None):
    """(mass, σ [fb], fractional unc) from a theory CSV, cut to xlim [GeV] if given."""
    masses, xsec_fb = _load_theory_xsec_csv(csv_path)
    unc = _load_theory_unc_frac(csv_path)
    if xlim is None:
        return masses, xsec_fb, unc
    keep = (masses >= xlim[0]) & (masses <= xlim[1])
    return masses[keep], xsec_fb[keep], unc[keep]


def _draw_ref_curve_vsmass(ax, proc, xlim=None):
    """Draw theory/benchmark reference curves vs mass. Returns True if anything drawn."""
    if proc in _SUSY_PROCS:
        csv_path = _HEPDATA_THEORY_CSV.get(proc)
        if not csv_path or not os.path.exists(csv_path):
            return False
        masses_csv, xsec_fb_csv, unc = _theory_curve(csv_path, xlim)
        label = r"$\sigma_\mathrm{theory}(%s)$" % _theory_symbol(csv_path)
        ax.fill_between(masses_csv, xsec_fb_csv * (1 - unc), xsec_fb_csv * (1 + unc),
                        color="black", alpha=0.15, lw=0, zorder=2)
        ax.plot(masses_csv, xsec_fb_csv, color="black", lw=1.5, ls="--",
                label=label, zorder=3)
        _theory_footnote(ax, csv_path)
        extra_path = _EXTRA_THEORY_CSV.get(proc)
        if extra_path and os.path.exists(extra_path):
            em, exs, eunc = _theory_curve(extra_path, xlim)
            ax.fill_between(em, exs * (1 - eunc), exs * (1 + eunc),
                            color="dimgray", alpha=0.15, lw=0, zorder=2)
            ax.plot(em, exs, color="dimgray", lw=1.5, ls=":",
                    label=r"$\sigma_\mathrm{theory}(%s)$" % _theory_symbol(extra_path), zorder=3)
            _theory_footnote(ax, extra_path, row=1)
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


def _theory_url(csv_path):
    key = _THEORY[os.path.basename(csv_path)][0]
    for line in open(_XSEC_INFO):
        if line.startswith(key + ":"):
            return line.split()[1]
    return None


def _theory_symbol(csv_path):
    return _THEORY[os.path.basename(csv_path)][1]


def _theory_footnote(ax, csv_path, row=0):
    """Clickable footnote (in the PDF) naming the theory cross section and linking its twiki."""
    _, sym, order = _THEORY[os.path.basename(csv_path)]
    ax.text(0.0, -0.20 - 0.05 * row,
            r"$\sigma_\mathrm{theory}(%s)$: %s, PDF4LHC21, $\mathcal{B} = 100\%%$ "
            r"(LHC SUSY Cross Section WG twiki)" % (sym, order),
            transform=ax.transAxes, fontsize=9, ha="left", va="top", clip_on=False,
            color="#1f4e9c", url=_theory_url(csv_path))


def _excl_label(proc, csv_path=None):
    if proc in _SUSY_PROCS:
        return r"Expected exclusion: $\sigma\mathcal{B}^{2} = \sigma_\mathrm{theory}(%s)$" % _theory_symbol(csv_path)
    return r"Expected exclusion at $\mathcal{B}(H{\to}SS) = 1\%$"


def _mass_label(proc, mass):
    if proc in _SUSY_PROCS:
        return "m = %s GeV" % mass
    return r"$m_{S}$ = %s GeV" % mass


def _annotate_proc(ax, proc, label=None):
    _proc_label = label or PROC_LABELS.get(proc, proc)
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


def _cms_label(ax, proc):
    if _HAS_MPLHEP:
        if proc in _2016_ONLY_PROCS:
            rlabel = _LUMI_2016
        elif proc in _DISP_TRIG_PROCS:
            rlabel = _RUN2_LUMI_DISP_TRIG
        else:
            rlabel = _RUN2_LUMI
        hep.cms.label("Preliminary", data=False, ax=ax, fontsize=12, rlabel=rlabel)


def _band(lims_list, key, fallback_key=None):
    """Return list of limit values for `key` if ALL entries have it, else None."""
    vals = [l.get(key) if fallback_key is None else l.get(key, l.get(fallback_key))
            for l in lims_list]
    return vals if all(v is not None for v in vals) else None


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
        lims_c = [cdict[c] for c in ctaus]
        exp    = [l["exp"] * scale for l in lims_c]

        col = _COLORS[i % len(_COLORS)]
        ax.plot(ctaus, exp, color=col, lw=2, ls="--", marker="o", ms=5,
                label=_mass_label(proc, mass))

        _obs_raw = _band(lims_c, "obs")
        if _obs_raw:
            obs = [v * scale for v in _obs_raw]
            ax.plot(ctaus, obs, color=col, lw=2, ls="-",
                    label=_mass_label(proc, mass) + " (observed)")

    if not _draw_ref_lines_ctau(ax, proc, masses, _COLORS):
        pass
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel(_ylabel(proc))
    ax.legend(fontsize=9, ncol=2, title="Expected limits (blinded)", title_fontsize=9)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    _cms_label(ax, proc)
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

        lims_m = [mdict[m] for m in masses]
        exp  = [l["exp"] * s for l, s in zip(lims_m, scales)]

        col = _COLORS[i % len(_COLORS)]
        lbl = _format_ctau(ctau, " ")
        ax.plot(mass_vals, exp, color=col, lw=2, ls="--", marker="o", ms=5,
                label=r"$c\tau$ = %s" % lbl)

        _obs_raw = _band(lims_m, "obs")
        if _obs_raw:
            obs = [v * s for v, s in zip(_obs_raw, scales)]
            ax.plot(mass_vals, obs, color=col, lw=2, ls="-",
                    label=r"$c\tau$ = %s (observed)" % lbl)

    xlim = None
    if proc in _SUSY_PROCS:
        all_masses = [int(m) for m in _sorted_masses(mass_data)]
        xlim = (all_masses[0] - 100, all_masses[-1] + 100)
        ax.set_xlim(*xlim)
    if not _draw_ref_curve_vsmass(ax, proc, xlim):
        pass
    ax.set_yscale("log")
    ax.set_xlabel(_mass_xlabel(proc))
    ax.set_ylabel(_ylabel(proc))
    ax.legend(fontsize=9, ncol=2, title="Expected limits (blinded)", title_fontsize=9)
    ax.grid(True, which="both", ls=":", alpha=0.4)
    _cms_label(ax, proc)
    _annotate_proc(ax, proc)
    _save(fig, os.path.join(out_dir, "%s_1D_vsmass.pdf" % proc))


# ---------------------------------------------------------------------------
# 1D: mass on x-axis, one plot per adjacent ctau pair  (+ optional HepData)
# ---------------------------------------------------------------------------

def _draw_lowht_pair(ax, proc, ctau_data, c1, c2):
    """Draw Low-HT exp+obs for two ctau values, scaled to σ×B² [fb]."""
    for i, ctau in enumerate([c1, c2]):
        mdict     = ctau_data[ctau]
        masses    = _sorted_masses(mdict)
        mass_vals = [int(m) for m in masses]
        scales    = [_sig_scale_fb(proc, m) for m in masses]
        lims_m = [mdict[m] for m in masses]
        exp  = [l["exp"] * s for l, s in zip(lims_m, scales)]
        col = _COLORS[i]
        lbl = _format_ctau(ctau, " ")
        ax.plot(mass_vals, exp, color=col, lw=2, ls="--", marker="o", ms=5,
                label=r"$c\tau$ = %s, Low-HT expected" % lbl)
        _obs_raw = _band(lims_m, "obs")
        if _obs_raw:
            obs = [v * s for v, s in zip(_obs_raw, scales)]
            ax.plot(mass_vals, obs, color=col, lw=2, ls="-",
                    label=r"$c\tau$ = %s, Low-HT observed" % lbl)


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
        lbl = _format_ctau(ctau, " ")
        ax.plot(hd_masses_sl[keep], hd_r_sl[keep], color=col, lw=2, ls="-",
                label=r"$c\tau$ = %s, High-HT observed (EXO-19-013)" % lbl)


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
        _cms_label(ax, proc)
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
    _cms_label(ax, proc)
    _annotate_proc(ax, proc)
    tag = "%s_vs_%s" % (_format_ctau(c1), _format_ctau(c2))
    _save(fig, os.path.join(out_dir, "%s_1D_vsmass_%s.pdf" % (proc, tag)))


# ---------------------------------------------------------------------------
# 2D: ctau vs mass color map + r=1 contour  (no HepData overlay)
# ---------------------------------------------------------------------------

def _excl_thresholds_2d(proc, masses, mass_vals, theory_csv=None):
    """Per-mass σ×B² [fb] threshold where r=1 is the physical exclusion boundary.
    SUSY: σ_theory from CSV. H→SS: σ_ref_fb (_sig_scale_fb), so r=1 = SM boundary.
    theory_csv overrides the SUSY default (for EWK variant plots).
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
    # Interpolate interior NaN holes along ctau per mass column before capping edges
    x_all = np.arange(g.shape[0])
    for j in range(g.shape[1]):
        col = g[:, j]
        valid = ~np.isnan(col)
        if valid.sum() >= 2 and not valid.all():
            g[:, j] = np.interp(x_all, x_all[valid], col[valid])
    # fill remaining edge NaNs with a large cap so contour at r=1 can still be drawn
    cap = max(200.0, float(np.nanmax(g)) * 2.0)
    g[np.isnan(g) | (g <= 0)] = cap
    sp = RectBivariateSpline(log_ctaus, mass_vals, np.log10(g), kx=1, ky=1)
    return 10.0 ** sp(fine_lct, fine_mass)


def _color_scale(proc, grid_fb, thresholds):
    """(vmin, vref, vmax, cmap, levels) for the 2D colour map of the limit in physical units.
    SUSY: sequential map over the decades spanned by the limits. H→SS: RdBu_r with the white
    pivot at the BR benchmark.
    """
    if proc in _SUSY_PROCS:
        v = grid_fb[np.isfinite(grid_fb) & (grid_fb > 0)]
        vmin = 10.0 ** np.floor(np.log10(v.min()))
        vmax = 10.0 ** np.ceil(np.log10(v.max()))
        return vmin, None, vmax, plt.get_cmap("viridis"), np.logspace(np.log10(vmin), np.log10(vmax), 61)
    vmin, vref, vmax = _2D_VSCALE.get(proc, (None, None, None))
    if vref is None:
        vref = float(np.exp(np.mean(np.log(thresholds[thresholds > 0]))))
        vmin, vmax = vref * 0.05, vref * 200.0
    levels = np.concatenate([np.logspace(np.log10(vmin), np.log10(vref), 31)[:-1],
                             np.logspace(np.log10(vref), np.log10(vmax), 31)])
    return vmin, vref, vmax, plt.get_cmap("RdBu_r"), levels


def plot_2d(proc, mass_data, out_dir, hepdata, theory_csv=None, fname_suffix="", published=None):
    masses    = _sorted_masses(mass_data)

    # Rectangular grid with NaN for missing cells (capped to "not excluded" in _interp_grid).
    # min_n: drop masses with too few valid ctau points (SUSY needs 3+, Higgs 2+).
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
    log_ctau_lo = log_ctaus[0]
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
    # For SUSY this is σ_theory(mass); for H→SS it equals σ_ref_fb (= scales).
    thresholds  = _excl_thresholds_2d(proc, masses, mass_vals, theory_csv=theory_csv)
    thresh_fine = np.interp(fine_mass, mass_vals, thresholds)

    # Ratio grids: σ×B²_limit / threshold. Contour at 1.0 = genuine exclusion boundary.
    ratio_exp = grid_exp_s / thresholds[np.newaxis, :]
    ratio_obs = grid_obs_s / thresholds[np.newaxis, :]
    fine_ratio_exp = _interp_grid(log_ctaus, mass_vals, ratio_exp, fine_lct, fine_mass)
    fine_ratio_obs = _interp_grid(log_ctaus, mass_vals, ratio_obs, fine_lct, fine_mass)

    cmap_data_exp = fine_exp_s
    cmap_data_obs = fine_obs_s
    vmin, vref, vmax, cmap, levels = _color_scale(proc, grid_exp_s, thresholds)
    cbar_label = _ylabel(proc)

    fig, ax = plt.subplots(figsize=(9, 6))
    if published:
        ax.set_facecolor(_OUTSIDE_FC)

    norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)

    _all_nice = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,
                 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
                 10000, 20000, 50000, 100000]
    _nice_ticks = [t for t in _all_nice if vmin <= t <= vmax]

    if cmap_data_exp is not None:
        cf = ax.contourf(fine_ctau, fine_mass, cmap_data_exp.T,
                         levels=levels, norm=norm, cmap=cmap, extend="both")
        cf.set_edgecolor("face")
        cbar = plt.colorbar(cf, ax=ax, pad=0.02)
        cbar.set_label(cbar_label, fontsize=11)
        cbar.set_ticks(_nice_ticks)
        cbar.minorticks_off()
        cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
        if vref is not None:
            cbar.ax.axhline(y=vref, color="black", lw=1.0, ls="--")

        # Exclusion contours on the ratio grid (= 1.0 where limit = theory/SM benchmark)
        ax.contour(fine_ctau, fine_mass, fine_ratio_exp.T, levels=[1.0],
                   colors=["black"], linewidths=[2.5], linestyles=["dashed"], zorder=5)
        ax.plot([], [], color="black", lw=2.5, ls="--",
                label=_excl_label(proc, theory_csv or _HEPDATA_THEORY_CSV.get(proc)))

        if fine_ratio_obs is not None:
            ax.contour(fine_ctau, fine_mass, fine_ratio_obs.T, levels=[1.0],
                       colors=["black"], linewidths=[2.5], linestyles=["solid"], zorder=5)
            ax.plot([], [], color="black", lw=2.5, ls="-", label="Obs. excl.")
    else:
        grid_cmap = grid_exp_s
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
            cbar.set_label(cbar_label, fontsize=11)
            cbar.set_ticks(_nice_ticks)
            cbar.minorticks_off()
            cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
            if vref is not None:
                cbar.ax.axhline(y=vref, color="black", lw=1.0, ls="--")

    for j, mass in enumerate(masses):
        for i, ctau in enumerate(ctau_vals):
            if not np.isnan(grid_exp[i, j]):
                ax.scatter(ctau, mass_vals[j], color="black", s=20, zorder=6)

    y_pad = max(3.0, (mass_vals[-1] - mass_vals[0]) * 0.08)
    ax.set_xscale("log")
    x_hi = 10.0 ** (log_ctaus[-1] + 0.25)
    y_lo, y_top = mass_vals[0] - y_pad, mass_vals[-1]
    n_pub = 0
    if published:
        ax.add_patch(Rectangle((ctau_vals[0], mass_vals[0]), ctau_vals[-1] - ctau_vals[0],
                               mass_vals[-1] - mass_vals[0], fill=False, edgecolor="#303030", lw=1.2, zorder=3))
        if proc in _SUSY_PROCS:
            n_pub = _draw_pub_lines(ax, "EXO-19-013", [published["susy"][_PUB_SUSY_CURVE[proc + fname_suffix]]])
        else:
            n_pub = _draw_published_2d(ax, "4d" if ("dddd" in proc or "4d" in proc) else "4b", published)
        x_hi = _nice_ceil(max(x_hi, 10.0 ** (np.log10(ax.dataLim.x1) + 0.25)))
        y_lo = min(y_lo, ax.dataLim.y0 - y_pad)
        y_top = max(y_top, ax.dataLim.y1)
    ax.set_xlim(10.0 ** log_ctau_lo, x_hi)
    ax.set_ylim(y_lo, y_top + (2.5 + 0.8 * n_pub) * y_pad)
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel("Mass [GeV]")
    if published:
        leg = ax.legend(fontsize=9, loc="upper right", handlelength=4.0, borderaxespad=1.5,
                        ncol=2 if proc in _SUSY_PROCS else 1, columnspacing=1.5, frameon=True,
                        framealpha=1.0, facecolor=_OUTSIDE_FC, edgecolor=_OUTSIDE_FC)
    else:
        ax.legend(fontsize=11, loc="upper right", framealpha=0.92, edgecolor="0.7")
    ax.grid(True, which="both", ls=":", alpha=0.3)
    _cms_label(ax, proc)
    _annotate_proc(ax, proc, _EWK_LABEL if fname_suffix == "_ewk" else None)
    if proc in _SUSY_PROCS:
        _theory_footnote(ax, theory_csv or _HEPDATA_THEORY_CSV.get(proc))
    if published:
        _fit_legend_top(ax, leg, y_top)
    _save(fig, os.path.join(out_dir, "%s_2D%s%s.pdf" % (proc, fname_suffix, "_published" if published else "")))




# ---------------------------------------------------------------------------
# Method comparison: collect both HybridNew and AsymptoticLimits per signal
# ---------------------------------------------------------------------------

_HN_COLOR = "#2166ac"   # blue  — HybridNew
_AS_COLOR = "#d6604d"   # red   — AsymptoticLimits


def read_limits_method(sig_id, method):
    """Read limits for a specific method without priority fallback."""
    for suffix in (".mH120.1234.root", ".mH120.root"):
        fn = os.path.join(COMBINE_OUT, sig_id,
                          "higgsCombine%s.%s%s" % (sig_id, method, suffix))
        if os.path.exists(fn):
            break
    else:
        return None
    try:
        f = ROOT.TFile.Open(fn)
        if not f or f.IsZombie():
            return None
        t = f.Get("limit")
        if not t:
            f.Close()
            return None
        quant_map = {-1.0: "obs", 0.025: "dn2", 0.16: "dn1",
                     0.5: "exp", 0.84: "up1", 0.975: "up2"}
        result = {}
        for _ in t:
            q = round(float(t.quantileExpected), 3)
            for qref, key in quant_map.items():
                if abs(q - qref) < 0.01:
                    result[key] = float(t.limit)
        f.Close()
        if method == "HybridNew" and "obs" in result and "exp" not in result:
            result["exp"] = result.pop("obs")
        return result if "exp" in result else None
    except Exception as exc:
        print("Could not read %s %s: %s" % (sig_id, method, exc))
        return None


def write_limits_table(proc, mass_data_m, out_dir):
    scale = _sig_scale_fb(proc)
    out_fn = os.path.join(out_dir, "%s_limits.txt" % proc)
    with open(out_fn, "w") as fh:
        fh.write("# %s: 95%% CL expected upper limit on B(H->SS)\n" % proc)
        fh.write("# mass_GeV ctau_mm asymptotic_exp asymptotic_-1sigma asymptotic_+1sigma hybridnew_exp\n")
        for mass in sorted(mass_data_m, key=float):
            for ctau in sorted(mass_data_m[mass]):
                a = mass_data_m[mass][ctau].get("AsymptoticLimits", {})
                h = mass_data_m[mass][ctau].get("HybridNew", {})
                vals = [a.get("exp"), a.get("dn1"), a.get("up1"), h.get("exp")]
                fh.write("%s %g %s\n" % (mass, ctau, " ".join(
                    "%.4g" % (v * scale) if v is not None else "nan" for v in vals)))
    print("Wrote %s" % out_fn)


def collect_all_methods():
    """Return {proc -> {mass_str -> {ctau_mm -> {method: lims}}}}"""
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
            continue
        methods = {}
        for method in ("HybridNew", "AsymptoticLimits"):
            lims = read_limits_method(sig_id, method)
            if lims is not None:
                methods[method] = lims
        if not methods:
            continue
        data.setdefault(proc, {}).setdefault(mass, {})[ctau_mm] = methods
    return data


# ---------------------------------------------------------------------------
# Comparison 1D: one plot per ctau, HybridNew median vs Asymptotic median+bands
# ---------------------------------------------------------------------------

def plot_comparison_1d_per_ctau(proc, mass_data_m, out_dir, hepdata=None):
    """Per-ctau 1D vs mass: HybridNew median (blue) + Asymptotic median+bands (red)."""
    # Invert to {ctau -> {mass -> {method -> lims}}}
    ctau_data = {}
    for mass, cdict in mass_data_m.items():
        for ctau, mdict in cdict.items():
            ctau_data.setdefault(ctau, {})[mass] = mdict

    hd = hepdata.get(proc) if hepdata else None

    for ctau in sorted(ctau_data.keys()):
        mdict     = ctau_data[ctau]
        masses    = _sorted_masses(mdict)
        if not masses:
            continue
        mass_vals = [int(m) for m in masses]
        scales    = [_sig_scale_fb(proc, m) for m in masses]

        fig, ax = plt.subplots(figsize=(8, 6))
        drew = False

        # AsymptoticLimits: median + ±1σ/2σ bands
        as_idx  = [i for i, m in enumerate(masses) if "AsymptoticLimits" in mdict[m]]
        if as_idx:
            as_mv   = [mass_vals[i] for i in as_idx]
            as_sc   = [scales[i]    for i in as_idx]
            as_lims = [mdict[masses[i]]["AsymptoticLimits"] for i in as_idx]
            as_exp  = [l["exp"] * s for l, s in zip(as_lims, as_sc)]
            as_dn1  = [l["dn1"] * s for l, s in zip(as_lims, as_sc)] if all("dn1" in l for l in as_lims) else None
            as_up1  = [l["up1"] * s for l, s in zip(as_lims, as_sc)] if all("up1" in l for l in as_lims) else None
            as_dn2  = [l.get("dn2", l["dn1"]) * s for l, s in zip(as_lims, as_sc)] if as_dn1 else None
            as_up2  = [l.get("up2", l["up1"]) * s for l, s in zip(as_lims, as_sc)] if as_up1 else None
            if as_dn2 and as_up2:
                ax.fill_between(as_mv, as_dn2, as_up2, alpha=0.15, color=_AS_COLOR, edgecolor="none")
            if as_dn1 and as_up1:
                ax.fill_between(as_mv, as_dn1, as_up1, alpha=0.35, color=_AS_COLOR, edgecolor="none")
            ax.plot(as_mv, as_exp, color=_AS_COLOR, lw=2, ls="--", label="Asymptotic exp.", zorder=4)
            drew = True

        # HybridNew: median only (solid, marker at missing points)
        hn_idx  = [i for i, m in enumerate(masses) if "HybridNew" in mdict[m]]
        if hn_idx:
            hn_mv   = [mass_vals[i] for i in hn_idx]
            hn_sc   = [scales[i]    for i in hn_idx]
            hn_lims = [mdict[masses[i]]["HybridNew"] for i in hn_idx]
            hn_exp  = [l["exp"] * s for l, s in zip(hn_lims, hn_sc)]
            ax.plot(hn_mv, hn_exp, color=_HN_COLOR, lw=2.5, ls="-",
                    marker="o", ms=5, label="HybridNew exp.", zorder=5)
            drew = True

        # HepData reference (EXO-19-013), where available for this ctau
        if hd is not None:
            hd_masses_sl, hd_r_sl = _hepdata_slice_at_ctau(hd, ctau)
            if hd_masses_sl is not None:
                hd_masses_sl = np.array(hd_masses_sl)
                hd_r_sl      = np.array(hd_r_sl)
                keep = hd_r_sl > 0
                if np.any(keep):
                    ax.plot(hd_masses_sl[keep], hd_r_sl[keep], color="black", lw=1.5, ls="-",
                            label="High-HT obs. (EXO-19-013)", zorder=3)
                    drew = True

        if not drew:
            plt.close(fig)
            continue

        _draw_ref_curve_vsmass(ax, proc)
        ax.set_yscale("log")
        ax.set_xlabel(_mass_xlabel(proc))
        ax.set_ylabel(_ylabel(proc))
        ax.set_title(r"$c\tau = %s$" % _format_ctau(ctau), fontsize=12)
        ax.legend(fontsize=10)
        ax.grid(True, which="both", ls=":", alpha=0.4)
        _cms_label(ax, proc)
        _annotate_proc(ax, proc)
        ctau_tag = _format_ctau(ctau).replace(".", "p")
        _save(fig, os.path.join(out_dir, "%s_compare_%s.pdf" % (proc, ctau_tag)))


# ---------------------------------------------------------------------------
# Comparison 2D: color map + HybridNew contour + Asymptotic contour
# ---------------------------------------------------------------------------

def plot_comparison_2d(proc, mass_data_m, out_dir, hepdata, theory_csv=None, fname_suffix=""):
    """2D comparison: HybridNew color map with both exclusion contours overlaid."""
    masses = _sorted_masses(mass_data_m)
    ctau_counts = {m: len(mass_data_m[m]) for m in masses}
    max_n  = max(ctau_counts.values())
    min_n  = max(3, max_n - 1) if proc in _SUSY_PROCS else 2
    masses = [m for m in masses if ctau_counts[m] >= min_n]
    ctaus_all = sorted(set.union(*[set(mass_data_m[m].keys()) for m in masses]))

    if len(masses) < 2 or len(ctaus_all) < 2:
        print("  Skipping comparison 2D for %s: need at least 2x2 grid" % proc)
        return

    mass_vals  = np.array([int(m) for m in masses], dtype=float)
    ctau_vals  = np.array(ctaus_all, dtype=float)
    scales     = np.array([_sig_scale_fb(proc, m) for m in masses])
    thresholds = _excl_thresholds_2d(proc, masses, mass_vals, theory_csv=theory_csv)

    grid_hn = np.full((len(ctau_vals), len(mass_vals)), np.nan)
    grid_as = np.full((len(ctau_vals), len(mass_vals)), np.nan)

    for j, mass in enumerate(masses):
        for i, ctau in enumerate(ctau_vals):
            if ctau not in mass_data_m[mass]:
                continue
            entry = mass_data_m[mass][ctau]
            if "HybridNew" in entry:
                grid_hn[i, j] = entry["HybridNew"]["exp"]
            if "AsymptoticLimits" in entry:
                grid_as[i, j] = entry["AsymptoticLimits"]["exp"]

    grid_hn_s = grid_hn * scales[np.newaxis, :]
    grid_as_s = grid_as * scales[np.newaxis, :]

    # Color map: HybridNew where available, fill Asymptotic for missing cells
    grid_cmap = np.where(np.isnan(grid_hn_s), grid_as_s, grid_hn_s)

    ratio_hn = grid_hn_s / thresholds[np.newaxis, :]
    ratio_as = grid_as_s / thresholds[np.newaxis, :]
    vmin, vref, vmax, cmap, levels = _color_scale(proc, grid_cmap, thresholds)
    cbar_label = _ylabel(proc) + "  [HybridNew]"

    log_ctaus   = np.log10(ctau_vals)
    log_ctau_lo = log_ctaus[0]
    fine_lct    = np.linspace(log_ctau_lo, log_ctaus[-1], 200)
    fine_mass   = np.linspace(mass_vals[0], mass_vals[-1], 200)
    fine_ctau   = 10.0 ** fine_lct

    fine_cmap    = _interp_grid(log_ctaus, mass_vals, grid_cmap, fine_lct, fine_mass)
    fine_ratio_hn = _interp_grid(log_ctaus, mass_vals, ratio_hn,   fine_lct, fine_mass)
    fine_ratio_as = _interp_grid(log_ctaus, mass_vals, ratio_as,   fine_lct, fine_mass)

    norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
    _all_nice = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5,
                 1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
                 10000, 20000, 50000, 100000]
    _nice_ticks = [t for t in _all_nice if vmin <= t <= vmax]

    fig, ax = plt.subplots(figsize=(9, 6))

    if fine_cmap is not None:
        cf = ax.contourf(fine_ctau, fine_mass, fine_cmap.T,
                         levels=levels, norm=norm, cmap=cmap, extend="both")
        cf.set_edgecolor("face")
        cbar = plt.colorbar(cf, ax=ax, pad=0.02)
        cbar.set_label(cbar_label, fontsize=11)
        cbar.set_ticks(_nice_ticks)
        cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
        if vref is not None:
            cbar.ax.axhline(y=vref, color="black", lw=1.0, ls="--")

    if fine_ratio_hn is not None:
        ax.contour(fine_ctau, fine_mass, fine_ratio_hn.T, levels=[1.0],
                   colors=[_HN_COLOR], linewidths=[2.5], linestyles=["solid"])
        ax.plot([], [], color=_HN_COLOR, lw=2.5, ls="-", label="Expected exclusion (HybridNew)")

    if fine_ratio_as is not None:
        ax.contour(fine_ctau, fine_mass, fine_ratio_as.T, levels=[1.0],
                   colors=[_AS_COLOR], linewidths=[2.0], linestyles=["dashed"])
        ax.plot([], [], color=_AS_COLOR, lw=2.0, ls="--", label="Expected exclusion (asymptotic)")

    for j, mass in enumerate(masses):
        for i, ctau in enumerate(ctau_vals):
            if not np.isnan(grid_cmap[i, j]):
                ax.scatter(ctau, mass_vals[j], color="black", s=20, zorder=6)

    y_pad = max(3.0, (mass_vals[-1] - mass_vals[0]) * 0.08)
    ax.set_ylim(mass_vals[0] - y_pad, mass_vals[-1] + 3.5 * y_pad)
    ax.set_xscale("log")
    ax.set_xlim(10.0 ** log_ctau_lo, 10.0 ** (log_ctaus[-1] + 0.25))
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel("Mass [GeV]")
    ax.legend(fontsize=11, loc="upper right", framealpha=0.92, edgecolor="0.7")
    ax.grid(True, which="both", ls=":", alpha=0.3)
    _cms_label(ax, proc)
    _annotate_proc(ax, proc, _EWK_LABEL if fname_suffix == "_ewk" else None)
    if proc in _SUSY_PROCS:
        _theory_footnote(ax, theory_csv or _HEPDATA_THEORY_CSV.get(proc))
    _save(fig, os.path.join(out_dir, "%s_2D_compare%s.pdf" % (proc, fname_suffix)))


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Higgs: every production mode overlaid (each fitted on its own), ctau on x
# ---------------------------------------------------------------------------

_OVERLAY_FINAL_STATES = {
    "4d": ("dddd", "4d", r"S$\to$d$\bar{\mathrm{d}}$"),
    "4b": ("bbbb", "4b", r"S$\to$b$\bar{\mathrm{b}}$"),
}
_OVERLAY_MODES = [
    ("VHToSSTo%s",       False, "VH (lepton)"),
    ("ggHToSSTo%s",      False, "ggH (displacement)"),
    ("ttHToSSTo%s_lep",  True,  "ttH (lepton)"),
    ("ttHToSSTo%s_bjet", True,  "ttH (displacement)"),
    ("VBFHToSSTo%s",     True,  "VBF (displacement, 2016 only)"),
]
_OVERLAY_EXTRAS_M55 = [
    ("ttHToSSTo2b2d_lep",  2, "D", r"ttH (lepton), mixed b$\bar{\mathrm{b}}$/d$\bar{\mathrm{d}}$"),
    ("ttHToSSTo2b2d_bjet", 3, "D", r"ttH (displacement), mixed b$\bar{\mathrm{b}}$/d$\bar{\mathrm{d}}$"),
    ("VBFHToSSTo2b2d",     4, "D", r"VBF (displacement), mixed b$\bar{\mathrm{b}}$/d$\bar{\mathrm{d}}$"),
    ("ttHToSSTo4s_lep",    2, "s", r"ttH (lepton), S$\to$s$\bar{\mathrm{s}}$"),
    ("ttHToSSTo4s_bjet",   3, "s", r"ttH (displacement), S$\to$s$\bar{\mathrm{s}}$"),
    ("VBFHToSSTo4s",       4, "s", r"VBF (displacement), S$\to$s$\bar{\mathrm{s}}$"),
]


_PUB_STYLE = {
    "EXO-19-021": ("CMS Displaced Jets, ggH, 13 TeV (obs.)", "-"),
    "EXO-23-013": ("CMS Displaced Jets, ggH, 13.6 TeV (obs.)", (0, (4.0, 1.5, 1.0, 1.5))),
    "ATLAS":      ("ATLAS Inner Detector DVs, VH+VBF, $m_{s}$ = 16 GeV (obs.)", (0, (0.01, 2.2))),
    "EXO-19-013": ("CMS High-HT Tracker DVs, 13 TeV (obs.)", "-"),
}
_PUB_COLOR_2D = {"EXO-19-021": "#ff3cff", "EXO-23-013": "#ffd60a", "ATLAS": "#18e0ff", "EXO-19-013": "#ff8c1a"}
_PUB_SUSY_CURVE = {"mfv_neu": "gluino", "mfv_neu_ewk": "neutralino", "mfv_stopdbardbar": "stop"}
_OUTSIDE_FC = "#e0e0e0"
_PUB_OVERLAY_PANELS = {
    ("4d", "55"): [("EXO-19-021", 55), ("EXO-23-013", 55)],
    ("4d", "40"): [("EXO-19-021", 40), ("EXO-23-013", 40)],
    ("4d", "15"): [("EXO-23-013", 15), ("ATLAS", 16)],
    ("4b", "55"): [("EXO-23-013", 55)],
    ("4b", "40"): [("EXO-23-013", 40)],
    ("4b", "15"): [("EXO-23-013", 15)],
}


def _read_hepdata_blocks(text):
    """[(header, rows)] for each table in a HEPData CSV export."""
    blocks = []
    for chunk in text.replace("\r", "").split("\n\n"):
        lines = [l for l in chunk.splitlines() if l.strip() and not l.startswith("#")]
        if lines:
            blocks.append((lines[0], [[float(x) for x in l.split(",")] for l in lines[1:]]))
    return blocks


def _tar_text(tar_path, name):
    with tarfile.open(tar_path) as tf:
        member = [m for m in tf.getmembers() if os.path.basename(m.name) == name][0]
        return tf.extractfile(member).read().decode()


def load_published(pub_dir):
    """Published observed limits from the overlay handoff folder:
    {"4d"/"4b": {name: {m_S: (ctau_mm, B)}}, "contours": {"4d"/"4b": {name: (ctau_mm, m_S)}},
     "susy": {"neutralino"/"gluino"/"stop": (ctau_mm, excluded mass in GeV)}}. "contours" holds an
    analysis's own published B(H->SS) = 1% exclusion in the (ctau, m_S) plane, used on the 2D maps
    instead of a rebuilt one; "susy" holds the EXO-19-013 observed mass-lifetime exclusion curves."""
    out = {"4d": {}, "4b": {}, "contours": {"4d": {}, "4b": {}}}
    tar = os.path.join(pub_dir, "hepdata", "HEPData-ins2829524-v2-csv.tar.gz")
    for fs, name, contour in (("4b", "Figure4a.csv", "Figure6a.csv"), ("4d", "Figure4b.csv", "Figure6b.csv")):
        out[fs]["EXO-23-013"] = {}
        for header, rows in _read_hepdata_blocks(_tar_text(tar, name)):
            if "observed" in header:
                pts = [r for r in rows if not np.isnan(r[1])]
                out[fs]["EXO-23-013"][int(re.search(r"=(\d+)~", header).group(1))] = tuple(np.array(pts).T)
        rows = [r for h, r in _read_hepdata_blocks(_tar_text(tar, contour)) if "observed" in h][0]
        out["contours"][fs]["EXO-23-013"] = tuple(np.array(rows).T)
    rows = list(csv.DictReader(open(os.path.join(pub_dir, "digitized", "EXO-19-021_Fig8a_SToDD.csv"))))
    out["4d"]["EXO-19-021"] = {}
    for m in set(int(r["m_S_GeV"]) for r in rows):
        pts = sorted((float(r["ctau_mm"]), float(r["B"])) for r in rows
                     if int(r["m_S_GeV"]) == m and r["limit"] == "observed")
        out["4d"]["EXO-19-021"][m] = tuple(np.array(pts).T)
    rows = csv.DictReader(open(os.path.join(pub_dir, "digitized", "ATLAS_2403.15332_4u_ms16_AuxTable1.csv")))
    out["4d"]["ATLAS"] = {16: tuple(np.array(sorted((float(r["ctau_mm"]), float(r["B"])) for r in rows)).T)}
    tar = os.path.join(pub_dir, "hepdata", "HEPData-ins1861146-v3-csv.tar.gz")
    out["susy"] = {}
    for key, name in (("neutralino", "Figure7a(left),neutralinoexclusioncurve.csv"),
                      ("gluino", "Figure7a(left),gluinoexclusioncurve.csv"),
                      ("stop", "Figure7b(right),topsquarkexclusioncurve.csv")):
        rows = np.array([r for h, r in _read_hepdata_blocks(_tar_text(tar, name)) if "Observed" in h][0])
        out["susy"][key] = (rows[:, 0], rows[:, 1])
    return out


def _cut_curve(ctau, b, xlim):
    """A published (ctau, B) curve restricted to the axis ctau range, ending on the axis edges."""
    lc, lb = np.log10(ctau), np.log10(b)
    lo, hi = np.log10(xlim)
    x = np.union1d(lc[(lc >= lo) & (lc <= hi)], [e for e in (lo, hi) if lc[0] < e < lc[-1]])
    return 10.0 ** x, 10.0 ** np.interp(x, lc, lb)


def _pub_kw(name, on_map):
    """Line settings of a published curve: black on the 1D overlays, a bright colour with a black
    edge on the 2D maps so it reads on every heatmap colour."""
    ls = _PUB_STYLE[name][1]
    cap = "round" if name == "ATLAS" else "butt"
    lw = 2.4 if (name == "ATLAS" or not on_map) else 1.8
    kw = dict(ls=ls, lw=lw, dash_capstyle=cap, solid_capstyle=cap)
    if on_map:
        kw.update(color=_PUB_COLOR_2D[name], zorder=4,
                  path_effects=[patheffects.withStroke(linewidth=lw + 1.2, foreground="black", capstyle=cap)])
    else:
        kw.update(color="black", zorder=1.9)
    return kw


def _draw_pub_lines(ax, name, lines):
    """Draw the (ctau, mass) pieces of a published curve in its map style and add its legend entry
    if anything is drawn. Returns 1 or 0."""
    kw = _pub_kw(name, True)
    for x, y in lines:
        ax.plot(x, y, **kw)
    if lines:
        ax.plot([], [], label=_PUB_STYLE[name][0], **kw)
    return 1 if lines else 0


def _excluded_window(ctau, b):
    """(lo, hi) ctau where a single-mass curve is at or below B(H->SS) = 1%, log-log interpolated
    at the crossings; None if it never is."""
    lc, lb = np.log10(ctau), np.log10(b) - np.log10(_BR_HSS)
    inside = np.where(lb <= 1e-9)[0]
    if not inside.size:
        return None
    i0, i1 = inside[0], inside[-1]
    lo = lc[i0] if i0 == 0 else lc[i0 - 1] + (0.0 - lb[i0 - 1]) / (lb[i0] - lb[i0 - 1]) * (lc[i0] - lc[i0 - 1])
    hi = lc[i1] if i1 == len(lc) - 1 else lc[i1] + (0.0 - lb[i1]) / (lb[i1 + 1] - lb[i1]) * (lc[i1 + 1] - lc[i1])
    return 10.0 ** lo, 10.0 ** hi


def _draw_published_2d(ax, fs, published):
    """B(H->SS) = 1% exclusion of each published analysis: its own published contour when it has one;
    otherwise a contour built across its m_S curves (log-bilinear, as for our map) between the lowest
    and highest m_S that exclude B = 1% anywhere, with B = 100% outside each curve's own ctau range so
    the contour closes where its data end; or the excluded ctau window when it has a single m_S.
    Returns the number drawn."""
    level = np.log10(_BR_HSS)
    n_drawn = 0
    for name in [n for n in ("EXO-19-021", "EXO-23-013", "ATLAS") if n in published[fs]]:
        if name in published["contours"][fs]:
            n_drawn += _draw_pub_lines(ax, name, [published["contours"][fs][name]])
            continue
        curves = published[fs][name]
        excl = [m for m in sorted(curves) if np.min(curves[m][1]) <= _BR_HSS * (1 + 1e-9)]
        masses = [m for m in sorted(curves) if excl and excl[0] <= m <= excl[-1]]
        if not masses:
            continue
        if len(masses) == 1:
            ctau, b = curves[masses[0]]
            lo, hi = _excluded_window(ctau, b)
            lines = [(np.array([lo, hi]), np.array([masses[0]] * 2, dtype=float))]
        else:
            edges = np.log10([curves[m][0][i] for m in masses for i in (0, -1)])
            lct = np.union1d(np.linspace(edges.min() - 0.02, edges.max() + 0.02, 400),
                             np.concatenate([edges - 1e-6, edges]))
            rows = []
            for m in masses:
                lc, lb = np.log10(curves[m][0]), np.log10(curves[m][1])
                rows.append(np.where((lct >= lc[0]) & (lct <= lc[-1]), np.interp(lct, lc, lb), 0.0))
            fm = np.linspace(masses[0], masses[-1], 200)
            grid = np.array([np.interp(fm, masses, col) for col in np.array(rows).T])
            segs = contourpy.contour_generator(lct, fm, grid.T, line_type="Separate").lines(level)
            lines = [(10.0 ** s[:, 0], s[:, 1]) for s in segs]
        n_drawn += _draw_pub_lines(ax, name, lines)
    return n_drawn


def _nice_ceil(x):
    e = 10.0 ** np.floor(np.log10(x))
    return next(f * e for f in (1, 2, 3, 5, 10) if f * e >= x * (1 - 1e-9))


def _fit_legend_top(ax, leg, y_data_top, gap=0.035):
    """Raise the y-axis top until the legend's bottom edge clears y_data_top."""
    for _ in range(2):
        plt.tight_layout()
        ax.figure.canvas.draw()
        y0 = leg.get_window_extent().transformed(ax.transAxes.inverted()).y0
        lo, hi = ax.get_ylim()
        ax.set_ylim(lo, max(hi, lo + (y_data_top - lo) / (y0 - gap)))


class _RowLine(HandlerLine2D):
    """Legend line or marker drawn at a fixed height above the label baseline, so rows of equal
    height line up across columns."""
    def create_artists(self, legend, orig_handle, xdescent, ydescent, width, height, fontsize, trans):
        artists = HandlerLine2D.create_artists(self, legend, orig_handle, xdescent, ydescent, width, height,
                                               fontsize, trans)
        for a in artists:
            a.set_ydata(np.full(len(a.get_xdata()), 0.36 * fontsize))
        return artists


_OVERLAY_LEGEND_KW = dict(fontsize=7.5, handlelength=3.5, handleheight=2.4, labelspacing=0.05, columnspacing=0.8,
                          handletextpad=0.45, borderpad=0.4, borderaxespad=0.0, frameon=False,
                          title_fontproperties={"size": 8.5, "weight": "bold"}, alignment="center",
                          handler_map={Line2D: _RowLine()})


def _overlay_legends(fig, ax, ours, points, pubs, ref, loc):
    """Our curves (1% line on their last row) and the M55 points under one title, the published
    curves under another, placed side by side as one block at the top of the axes."""
    nrows = max(len(ours) + 1, len(points))
    cols = [ours + [Line2D([], [], ls="none") for _ in range(nrows - 1 - len(ours))] + [ref]]
    if points:
        cols.append(points + [Line2D([], [], ls="none") for _ in range(nrows - len(points))])
    handles = [h for c in cols for h in c]
    l1 = ax.legend(handles, [h.get_label() for h in handles], ncol=len(cols), title="Expected limits (blinded)",
                   loc="upper left", **_OVERLAY_LEGEND_KW)
    ax.add_artist(l1)
    l2 = ax.legend(pubs, [p.get_label() for p in pubs], title="Published (observed)", loc="upper left",
                   **_OVERLAY_LEGEND_KW)
    r = fig.canvas.get_renderer()
    w1, w2 = [l.get_window_extent(r).transformed(ax.transAxes.inverted()).width for l in (l1, l2)]
    x0 = {"upper left": 0.02, "upper center": 0.5 - (w1 + w2) / 2.0, "upper right": 0.98 - w1 - w2}[loc]
    l1.set_bbox_to_anchor((x0, 0.964), transform=ax.transAxes)
    l2.set_bbox_to_anchor((x0 + w1, 0.964), transform=ax.transAxes)
    return [l1, l2]


def _overlay_top(fig, ax, legends, lines, lo, margin_pt=6.0):
    """Smallest y top of the log axis that keeps every data line below the legend block."""
    r = fig.canvas.get_renderer()
    boxes = [l.get_window_extent(r).transformed(ax.transAxes.inverted()) for l in legends]
    x0, x1, y0 = min(b.x0 for b in boxes), max(b.x1 for b in boxes), min(b.y0 for b in boxes)
    bb = ax.get_window_extent(r)
    mx, my = margin_pt * fig.dpi / 72.0 / bb.width, margin_pt * fig.dpi / 72.0 / bb.height
    lxlo, lxhi = np.log10(ax.get_xlim())
    lxa, lxb = lxlo + (x0 - mx) * (lxhi - lxlo), lxlo + (x1 + mx) * (lxhi - lxlo)
    ys = []
    for line in lines:
        lx, ly = np.log10(np.asarray(line.get_xdata(), float)), np.log10(np.asarray(line.get_ydata(), float))
        ys += list(ly[(lx >= lxa) & (lx <= lxb)])
        if line.get_linestyle() not in ("None", "none", "", " ") and len(lx) > 1:
            ys += [np.interp(e, lx, ly) for e in (lxa, lxb) if lx[0] <= e <= lx[-1]]
    if not ys:
        return lo
    llo = np.log10(lo)
    return 10.0 ** (llo + (max(ys) - llo) / (y0 - my))


def _place_overlay_legends(fig, ax, ours, points, pubs, ref):
    """Put the legend block where it needs the least headroom, then raise the y top so no data
    sit under it."""
    lines = ours + points + pubs
    lo, hi = ax.get_ylim()
    hi = max(hi, 10.0 ** (max(np.log10(np.asarray(l.get_ydata(), float)).max() for l in lines) + 0.25))
    fig.tight_layout()
    best = None
    for loc in ("upper center", "upper right", "upper left"):
        legs = _overlay_legends(fig, ax, ours, points, pubs, ref, loc)
        top = _overlay_top(fig, ax, legs, lines, lo)
        for l in legs:
            l.remove()
        ax.legend_ = None
        if best is None or np.log10(top) < np.log10(best[1]) - 0.02:
            best = (loc, top)
    legs = _overlay_legends(fig, ax, ours, points, pubs, ref, best[0])
    for _ in range(3):
        ax.set_ylim(lo, max(hi, _overlay_top(fig, ax, legs, lines, lo)))
        fig.tight_layout()


def plot_higgs_overlay(data, out_dir, published=None):
    all_ctaus = []
    for long_tag, short_tag, _ in _OVERLAY_FINAL_STATES.values():
        for pattern, use_short, _ in _OVERLAY_MODES:
            for cdict in data.get(pattern % (short_tag if use_short else long_tag), {}).values():
                all_ctaus += list(cdict)
    if not all_ctaus:
        return
    xlim = (min(all_ctaus) / 1.5, max(all_ctaus) * 1.5)
    for fs, (long_tag, short_tag, fs_label) in sorted(_OVERLAY_FINAL_STATES.items()):
        for mass in ("15", "40", "55"):
            fig, ax = plt.subplots(figsize=(8, 6))
            ours, points = [], []
            for j, (pattern, use_short, label) in enumerate(_OVERLAY_MODES):
                cdict = data.get(pattern % (short_tag if use_short else long_tag), {}).get(mass)
                if not cdict:
                    continue
                ctaus = sorted(cdict)
                ours += ax.plot(ctaus, [cdict[c]["exp"] * _BR_HSS for c in ctaus], color=_COLORS[j],
                                lw=2, ls="--", marker="o", ms=5, label=label)
            if not ours:
                plt.close(fig)
                continue
            if mass == "55":
                for proc, j, marker, label in _OVERLAY_EXTRAS_M55:
                    cdict = data.get(proc, {}).get(mass)
                    if not cdict:
                        continue
                    ctaus = sorted(cdict)
                    points += ax.plot(ctaus, [cdict[c]["exp"] * _BR_HSS for c in ctaus], ls="none", marker=marker,
                                      ms=7, markerfacecolor="none", markeredgecolor=_COLORS[j], markeredgewidth=1.5,
                                      label=label)
            ref = ax.axhline(_BR_HSS, color="0.5" if published else "black", lw=1.5, ls="--",
                             label=r"$\mathcal{B}(H{\to}SS) = 1\%$", zorder=1.8 if published else 3)
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlim(*xlim)
            ax.set_xlabel(r"$c\tau$ [mm]")
            ax.set_ylabel(r"95% CL upper limit on $\mathcal{B}(H{\to}SS)$")
            pubs = []
            if published:
                for name, m in _PUB_OVERLAY_PANELS[(fs, mass)]:
                    ctau, b = published[fs][name][m]
                    pubs += ax.plot(*_cut_curve(ctau, b, xlim), label=_PUB_STYLE[name][0], **_pub_kw(name, False))
            else:
                ax.legend(fontsize=8, ncol=2, title="Expected limits (blinded)", title_fontsize=9)
            ax.grid(True, which="both", ls=":", alpha=0.4)
            if _HAS_MPLHEP:
                hep.cms.label("Preliminary", data=False, ax=ax, fontsize=12,
                              rlabel=r"36.3$-$137.9 fb$^{-1}$ (13 TeV)")
            ax.text(0.0, -0.13, r"H$\to$SS, %s, $m_{S}$ = %s GeV (no combination)" % (fs_label, mass),
                    transform=ax.transAxes, fontsize=10, ha="left", va="top", clip_on=False)
            if published:
                _place_overlay_legends(fig, ax, ours, points, pubs, ref)
            _save(fig, os.path.join(out_dir, "higgs_overlay_%s_M%s%s.pdf"
                                    % (fs, mass, "_published" if published else "")))


def main():
    global COMBINE_OUT
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out-dir",        default=PLOT_DIR)
    ap.add_argument("--combine-out",    default=COMBINE_OUT)
    ap.add_argument("--subset",         default=None,
                    help="Comma-separated process names to plot")
    ap.add_argument("--comparison-dir", default=None,
                    help="If set, write HybridNew vs Asymptotic comparison plots here")
    ap.add_argument("--published-dir", default=None,
                    help="Folder with the published limits (hepdata/, digitized/); if set, also write the "
                         "*_published plots with them overlaid")
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
    published = load_published(args.published_dir) if args.published_dir else None

    # ggZH is always grouped into VH; never plot it standalone
    _skip_procs = {"ggZHToSSTodddd", "ggZHToSSTobbbb"}

    table_data = collect_all_methods()
    for proc in sorted(data):
        if proc in _skip_procs:
            continue
        if subset and proc not in subset:
            continue
        if proc.split("_")[0] in _TABLE_ONLY_MODELS:
            write_limits_table(proc, table_data.get(proc, {}), args.out_dir)
            continue
        n_masses = len(data[proc])
        n_pts    = sum(len(v) for v in data[proc].values())
        print("\n%s:  %d masses,  %d total hypotheses" % (proc, n_masses, n_pts))

        plot_1d(proc, data[proc], args.out_dir, hepdata)
        plot_1d_vs_mass_all(proc, data[proc], args.out_dir)
        plot_1d_vs_mass_pairs(proc, data[proc], args.out_dir, hepdata)
        if proc in ("ggHToSSTodddd", "VHToSSTodddd"):
            plot_1d_vs_mass_ctau_pair(proc, data[proc], args.out_dir, 1.0, 10.0)
        plot_2d(proc, data[proc], args.out_dir, hepdata)
        if published and (proc not in _SUSY_PROCS or proc in _PUB_SUSY_CURVE):
            plot_2d(proc, data[proc], args.out_dir, hepdata, published=published)
        if proc == "mfv_neu" and "mfv_neu" in _EXTRA_THEORY_CSV:
            plot_2d(proc, data[proc], args.out_dir, hepdata,
                    theory_csv=_EXTRA_THEORY_CSV["mfv_neu"],
                    fname_suffix="_ewk")
            if published:
                plot_2d(proc, data[proc], args.out_dir, hepdata,
                        theory_csv=_EXTRA_THEORY_CSV["mfv_neu"],
                        fname_suffix="_ewk", published=published)

    plot_higgs_overlay(data, args.out_dir)
    if published:
        plot_higgs_overlay(data, args.out_dir, published)

    print("\nDone. Plots saved to %s" % args.out_dir)

    if args.comparison_dir:
        os.makedirs(args.comparison_dir, exist_ok=True)
        print("\n--- Generating HybridNew vs Asymptotic comparison plots ---")
        data_m = collect_all_methods()
        for proc in sorted(data_m):
            if proc in _skip_procs or proc.split("_")[0] in _TABLE_ONLY_MODELS:
                continue
            if subset and proc not in subset:
                continue
            n_pts = sum(len(v) for v in data_m[proc].values())
            print("\n%s:  %d hypotheses" % (proc, n_pts))
            plot_comparison_1d_per_ctau(proc, data_m[proc], args.comparison_dir, hepdata)
            plot_comparison_2d(proc, data_m[proc], args.comparison_dir, hepdata)
            if proc == "mfv_neu" and "mfv_neu" in _EXTRA_THEORY_CSV:
                plot_comparison_2d(proc, data_m[proc], args.comparison_dir, hepdata,
                                   theory_csv=_EXTRA_THEORY_CSV["mfv_neu"],
                                   fname_suffix="_ewk")
        print("\nComparison plots saved to %s" % args.comparison_dir)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Plot 95% CL upper limits on signal strength r = sigma/sigma_theory.

Reads CombineOutput/<sig_id>/higgsCombine<sig_id>.AsymptoticLimits.mH120.root
for all available hypotheses and produces per-process plots.

Output (in LimitPlots/):
  <proc>_1D.pdf  -- ctau [mm] vs r upper limit, one curve per mass
  <proc>_2D.pdf  -- ctau vs mass 2D color map + r=1 exclusion contour

HepData reference (ins1861146, old high-HT displaced vertex analysis):
  Only shown for SUSY signals.  Load from hepdata_ins1861146.json if present.
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

HEPDATA_PROCS = {"mfv_neu", "mfv_stopdbardbar", "mfv_stopbbarbbar"}

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

_COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#a65628"]

_RUN2_LUMI = r"137.9 fb$^{-1}$ (13 TeV)"

# Per-process normalization footnote shown in the plot annotation box.
# H->SS processes: BR(H->SS)=1% is folded into xsec.
# ggH additionally has a mass-dependent gen-level filter efficiency in xsec.
_NORM_NOTE = r"$\sigma \times \mathcal{B}(H{\to}SS)=1\%$"
_NORM_NOTE_FILTER = r"$\sigma \times \mathcal{B}(H{\to}SS)=1\%$, gen. filter eff."
_PROC_NORM_NOTES = {
    "VH":             _NORM_NOTE,
    "ggZHToSSTobbbb": _NORM_NOTE,
    "ggHToSSTodddd":  _NORM_NOTE_FILTER,
    "ttHToLLPs_bbbb": _NORM_NOTE,
    "ttHToLLPs_dddd": _NORM_NOTE,
}


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


def load_hepdata():
    if not os.path.exists(HEPDATA_JSON):
        return {}
    with open(HEPDATA_JSON) as fh:
        return json.load(fh)


def plot_1d(proc, mass_data, out_dir, hepdata):
    fig, ax = plt.subplots(figsize=(8, 6))

    masses = sorted(mass_data.keys(), key=lambda m: int(m) if m.isdigit() else 0)

    for i, mass in enumerate(masses):
        cdict  = mass_data[mass]
        ctaus  = sorted(cdict.keys())
        if not ctaus:
            continue
        exp    = [cdict[c]["exp"]                        for c in ctaus]
        dn1    = [cdict[c]["dn1"]                        for c in ctaus]
        up1    = [cdict[c]["up1"]                        for c in ctaus]
        dn2    = [cdict[c].get("dn2", cdict[c]["dn1"])  for c in ctaus]
        up2    = [cdict[c].get("up2", cdict[c]["up1"])  for c in ctaus]

        col = _COLORS[i % len(_COLORS)]
        ax.fill_between(ctaus, dn2, up2, alpha=0.15, color=col, edgecolor="none")
        ax.fill_between(ctaus, dn1, up1, alpha=0.35, color=col, edgecolor="none")
        ax.plot(ctaus, exp, color=col, lw=2, ls="--",
                label="m = %s GeV (exp)" % mass)

        if "obs" in cdict[ctaus[0]]:
            obs = [cdict[c]["obs"] for c in ctaus]
            ax.plot(ctaus, obs, color=col, lw=2, ls="-",
                    label="m = %s GeV (obs)" % mass)

    ax.axhline(1.0, color="black", lw=1.2, ls=":", zorder=3)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel("95% CL upper limit on $r$")
    ax.legend(fontsize=9, ncol=2)
    ax.grid(True, which="both", ls=":", alpha=0.4)

    if _HAS_MPLHEP:
        hep.cms.label("Preliminary", data=False, ax=ax, fontsize=12,
                      rlabel=_RUN2_LUMI)

    _proc_label = PROC_LABELS.get(proc, proc)
    _norm = _PROC_NORM_NOTES.get(proc, "")
    _annot = _proc_label + ("\n" + _norm if _norm else "")
    ax.text(0.0, -0.13, _annot,
            transform=ax.transAxes, fontsize=10, ha="left", va="top",
            clip_on=False)

    plt.tight_layout()
    out_fn = os.path.join(out_dir, "%s_1D.pdf" % proc)
    fig.savefig(out_fn, bbox_inches="tight")
    plt.close(fig)
    print("  1D -> %s" % out_fn)


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


def plot_2d(proc, mass_data, out_dir, hepdata):
    masses    = sorted(mass_data.keys(), key=lambda m: int(m) if m.isdigit() else 0)
    ctaus_all = sorted(set(c for md in mass_data.values() for c in md.keys()))

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

    fig, ax = plt.subplots(figsize=(9, 6))

    # Diverging log-scale colormap centred at r=1: blue=excluded, red=not excluded
    vmin, vmax = 0.05, 200.0
    n_half = 30
    levels = np.concatenate([
        np.logspace(np.log10(vmin), 0, n_half + 1)[:-1],
        np.logspace(0, np.log10(vmax), n_half + 1),
    ])
    norm = mcolors.LogNorm(vmin=vmin, vmax=vmax)
    cmap = plt.get_cmap("RdBu_r")   # blue=low r (excluded), red=high r (not excluded)

    _nice_ticks = [t for t in [0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50, 100, 200]
                   if vmin <= t <= vmax]

    if fine_exp is not None:
        cf = ax.contourf(fine_ctau, fine_mass, fine_exp.T,
                         levels=levels, norm=norm, cmap=cmap, extend="both")
        cbar = plt.colorbar(cf, ax=ax, pad=0.02)
        cbar.set_label("95% CL upper limit on $r$")
        cbar.set_ticks(_nice_ticks)
        cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
        cbar.ax.axhline(y=1.0, color="black", lw=1.0, ls="--")

        # expected: dashed; observed: solid  (CMS convention)
        ax.contour(fine_ctau, fine_mass, fine_exp.T, levels=[1.0],
                   colors=["black"], linewidths=[2.5], linestyles=["dashed"])
        ax.plot([], [], color="black", lw=2.5, ls="--", label="Exp. excl. ($r=1$)")

        if fine_obs is not None:
            ax.contour(fine_ctau, fine_mass, fine_obs.T, levels=[1.0],
                       colors=["black"], linewidths=[2.5], linestyles=["solid"])
            ax.plot([], [], color="black", lw=2.5, ls="-", label="Obs. excl. ($r=1$)")
    else:
        xs, ys, cs = [], [], []
        for j, mass in enumerate(masses):
            for i, ctau in enumerate(ctau_vals):
                if not np.isnan(grid_exp[i, j]):
                    xs.append(ctau)
                    ys.append(mass_vals[j])
                    cs.append(np.clip(grid_exp[i, j], vmin, vmax))
        if xs:
            sc = ax.scatter(xs, ys, c=cs, s=300, zorder=5,
                            norm=norm, cmap=cmap,
                            edgecolors="black", linewidths=0.5)
            cbar = plt.colorbar(sc, ax=ax, pad=0.02)
            cbar.set_label("95% CL upper limit on $r$")
            cbar.set_ticks(_nice_ticks)
            cbar.set_ticklabels(["%g" % t for t in _nice_ticks])
            cbar.ax.axhline(y=1.0, color="black", lw=1.0, ls="--")

    for j, mass in enumerate(masses):
        for i, ctau in enumerate(ctau_vals):
            ax.scatter(ctau, mass_vals[j], color="black", s=20, zorder=6)

    if proc in HEPDATA_PROCS and proc in hepdata:
        hd = hepdata[proc]
        hd_ctaus  = np.array(hd["ctau_mm"], dtype=float)
        hd_masses = np.array(hd["mass_gev"], dtype=float)
        hd_obs    = np.array(hd["obs"],      dtype=float)
        if _HAS_SCIPY and len(hd_ctaus) >= 2 and len(hd_masses) >= 2:
            hd_fine_lct  = np.linspace(np.log10(hd_ctaus[0]),
                                       np.log10(hd_ctaus[-1]), 200)
            hd_fine_mass = np.linspace(hd_masses[0], hd_masses[-1], 200)
            sp_hd = RectBivariateSpline(np.log10(hd_ctaus), hd_masses,
                                        np.log10(hd_obs + 1e-9), kx=1, ky=1)
            hd_fine_obs = 10.0 ** sp_hd(hd_fine_lct, hd_fine_mass)
            ax.contour(10.0 ** hd_fine_lct, hd_fine_mass, hd_fine_obs.T,
                       levels=[1.0], colors=["gray"],
                       linewidths=[2.0], linestyles=["dotted"])
            ax.plot([], [], color="gray", lw=2.0, ls="dotted",
                    label="CMS-EXO-19-013 obs.")

    # y-axis: for SUSY+HepData extend to 2500 GeV so the old exclusion line
    # is visible; otherwise auto-scale.
    y_pad = max(3.0, (mass_vals[-1] - mass_vals[0]) * 0.08)
    if proc in HEPDATA_PROCS and proc in hepdata:
        y_top = max(mass_vals[-1] + y_pad, 2500.)
    else:
        y_top = mass_vals[-1] + y_pad
    ax.set_ylim(mass_vals[0] - y_pad, y_top)

    ax.set_xscale("log")
    # x-axis: extend left to show exclusion closure, right with small padding
    ax.set_xlim(10.0 ** log_ctau_lo, 10.0 ** (log_ctaus[-1] + 0.25))
    ax.set_xlabel(r"$c\tau$ [mm]")
    ax.set_ylabel("Mass [GeV]")
    ax.legend(fontsize=11, loc="upper right", framealpha=0.92, edgecolor="0.7")
    ax.grid(True, which="both", ls=":", alpha=0.3)

    if _HAS_MPLHEP:
        hep.cms.label("Preliminary", data=False, ax=ax, fontsize=12,
                      rlabel=_RUN2_LUMI)

    _proc_label = PROC_LABELS.get(proc, proc)
    _norm = _PROC_NORM_NOTES.get(proc, "")
    _annot = _proc_label + ("\n" + _norm if _norm else "")
    ax.text(0.0, -0.13, _annot,
            transform=ax.transAxes, fontsize=10, ha="left", va="top",
            clip_on=False)

    plt.tight_layout()
    out_fn = os.path.join(out_dir, "%s_2D.pdf" % proc)
    fig.savefig(out_fn, bbox_inches="tight")
    plt.close(fig)
    print("  2D -> %s" % out_fn)


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
        print("No HepData reference found at %s (skipping overlay)" % HEPDATA_JSON)

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
        plot_2d(proc, data[proc], args.out_dir, hepdata)

    print("\nDone. Plots saved to %s" % args.out_dir)


if __name__ == "__main__":
    main()

"""
Discovery boundary scan: [0, 0.1, 0.4, x, 4.0]

For each x, computes:
  - B_tail(x): integrated background in [x, 4.0] from the Run2 template
  - S_tail(x): absolute expected signal events in [x, 4.0] at r=1

B_tail(x) is the p-value for observing >= 1 event given background-only.
Z = sqrt(2) * erfinv(1 - 2*B_tail) is the equivalent sigma.
S_tail(x) = total_run2_yield * (counts_above_x / counts_total) from MiniTree TTrees.

Usage:
  python3 discovery_scan.py    # runs and plots (LCG dev3)
"""
import os, sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SIGNAL_POINTS, YEARS
from fast_study_datacards import (BKG_FILES, MINI_BASE, N2V, YEAR_IDX,
                                   VH_PROCS, get_sig_files, get_sig_shape,
                                   parse_ref_yield)

HERE = os.path.dirname(os.path.abspath(__file__))

SCAN_VALS = [round(i * 0.1, 1) for i in range(5, 40)]   # 0.5..3.9
UPPER     = 4.0

# Signals to show — pick representative ones from each channel
PLOT_SIGS = [
    ("ggHToSSTodddd_tau1mm_M55",  "bjet", "forestgreen",   r"ggH $\tau$=1mm $M$=55"),
    ("ggHToSSTodddd_tau1mm_M40",  "bjet", "limegreen",     r"ggH $\tau$=1mm $M$=40"),
    ("VH_tau1mm_M55",             "lep",  "royalblue",     r"VH $\tau$=1mm $M$=55"),
    ("VH_tau10mm_M55",            "lep",  "tomato",        r"VH $\tau$=10mm $M$=55"),
]


def get_bkg_tail(ch, x):
    """Integrated Run2 background in [x, 4.0] from the 200-bin template."""
    import ROOT
    f = ROOT.TFile(BKG_FILES[ch])
    h = f.Get("h_c1v_sumdbv_w_errorbars")
    total = h.Integral()
    n2v_run2 = sum(N2V[ch])
    scale = n2v_run2 / total
    nbins = h.GetNbinsX()
    tail = 0.0
    for i in range(1, nbins + 2):   # +2 to include overflow
        if h.GetBinLowEdge(i) >= x:
            tail += h.GetBinContent(i) * scale
    f.Close()
    return tail


def get_sig_fraction(sig_id, ch, x):
    """Fraction of Run2 signal events with sumdbv >= x (from MiniTree TTrees)."""
    import ROOT
    counts_above = 0.0
    counts_total = 0.0
    for year in YEARS:
        files = get_sig_files(sig_id, ch, year)
        for fn in files:
            f = ROOT.TFile(fn)
            t = f.Get("mfvMiniTree/t")
            n_above = t.Draw("sumdbv", "nvtx>=2 && sumdbv>=%f" % x, "goff")
            n_total = t.Draw("sumdbv", "nvtx>=2", "goff")
            counts_above += max(n_above, 0)
            counts_total += max(n_total, 0)
            f.Close()
    if counts_total == 0:
        return None
    return counts_above / counts_total


def get_total_sig_yield(sig_id, ch):
    """Total Run2 expected signal yield at r=1, summed over all years."""
    total = 0.0
    for year in YEARS:
        try:
            total += parse_ref_yield(sig_id, ch, year)
        except (FileNotFoundError, RuntimeError):
            pass
    return total


def main():
    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
        ROOT.gErrorIgnoreLevel = ROOT.kError
    except ImportError:
        print("ERROR: ROOT not available"); sys.exit(1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from scipy.special import erfinv

    xs = SCAN_VALS

    # --- compute background tails ---
    print("Computing background tails...")
    bkg = {}
    for ch in ("bjet", "lep"):
        bkg[ch] = [get_bkg_tail(ch, x) for x in xs]
        print("  %s done" % ch)

    # --- compute absolute signal yields in tail ---
    print("Computing signal tails...")
    sig_yields = {}
    for sig_id, ch, color, label in PLOT_SIGS:
        print("  %s..." % sig_id)
        total_yield = get_total_sig_yield(sig_id, ch)
        print("    Run2 total yield = %.4f" % total_yield)
        fracs = [get_sig_fraction(sig_id, ch, x) for x in xs]
        sig_yields[sig_id] = [total_yield * f if f is not None else None for f in fracs]

    # --- plot ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, ch, title, ch_sigs in [
        (axes[0], "bjet", "Bjet channel",    [s for s in PLOT_SIGS if s[1]=="bjet"]),
        (axes[1], "lep",  "Lepton channel",  [s for s in PLOT_SIGS if s[1]=="lep"]),
    ]:
        ax2 = ax.twinx()

        # background tail (left axis, log scale)
        ax.semilogy(xs, bkg[ch], "k-", lw=2.5, label="Bkg tail B(x,4)")
        ax.axhline(1.35e-3, color="gray",  ls="--", lw=1.2, label=r"3$\sigma$ threshold")
        ax.axhline(2.87e-7, color="black", ls="--", lw=1.2, label=r"5$\sigma$ threshold")

        # mark where background crosses 1e-3
        for i in range(len(xs)-1):
            if bkg[ch][i] >= 1e-3 > bkg[ch][i+1]:
                ax.axvline(xs[i+1], color="orange", ls=":", lw=1.5,
                           label="B < 1e-3 @ %.1f cm" % xs[i+1])
                break

        ax.set_ylabel("Background in [x, 4.0] cm  (= p-value for 1 obs. event)", fontsize=10)
        ax.set_ylim(1e-8, 1.0)

        # absolute signal yields (right axis, log scale)
        ax2.axhline(1.0, color="dimgray", ls=":", lw=1.2, label="1 event")
        for sig_id, _, color, label in ch_sigs:
            yvals = sig_yields.get(sig_id, [])
            valid_x = [x for x, y in zip(xs, yvals) if y is not None and y > 0]
            valid_y = [y for y in yvals if y is not None and y > 0]
            if valid_y:
                ax2.semilogy(valid_x, valid_y, "o--", color=color, lw=1.5, ms=4,
                             label=label + " (sig. events)")

        ax2.set_ylabel("Expected signal events in [x, 4.0]  (r=1)", fontsize=10)
        ax2.set_ylim(1e-4, 1e2)
        ax2.yaxis.set_tick_params(labelsize=9)

        ax.set_xlabel("4th boundary x (cm)", fontsize=11)
        ax.set_title(title, fontsize=12)
        ax.set_xticks(xs[::2])
        ax.set_xticklabels(["%.1f" % v for v in xs[::2]], fontsize=8)

        # combined legend
        lines1, labs1 = ax.get_legend_handles_labels()
        lines2, labs2 = ax2.get_legend_handles_labels()
        ax.legend(lines1 + lines2, labs1 + labs2, fontsize=8, framealpha=0.85,
                  loc="upper right")
        ax.grid(alpha=0.3)

    fig.suptitle(r"Discovery scan — background tail & expected signal events vs 4th boundary x in [0, 0.1, 0.4, $x$, 4.0] cm",
                 fontsize=11)
    fig.tight_layout()

    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "discovery_scan.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)


if __name__ == "__main__":
    main()

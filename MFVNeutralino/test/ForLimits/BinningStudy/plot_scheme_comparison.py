"""
Plot expected 95% CL UL on r for each signal point, across all binning schemes.
One panel per signal. Nominal scheme highlighted with a dashed reference line.

Usage:
  source LCG dev3 setup
  python3 plot_scheme_comparison.py
Output: scheme_comparison.pdf / .png
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SCHEMES
from collect_results import collect, SIG_LABELS

HERE = os.path.dirname(os.path.abspath(__file__))

# Short scheme labels for the x-axis
SHORT_LABELS = {
    "old_binning":   "[0,.08,.16,4]",
    "2bin":          "[0,1.6,4]",
    "3bin_nom":      "[0,.8,1.6,4]",
    "3bin_v1":       "[0,.4,1.6,4]",
    "3bin_v2":       "[0,.8,2.5,4]",
    "3bin_v3":       "[0,1,2,4]",
    "3bin_v4":       "[0,.5,1,4]",
    "4bin_v1":       "[0,.4,.8,\n1.6,4]",
    "4bin_v2":       "[0,.8,1.2,\n1.6,4]",
    "3bin_412":      "[0,.4,1.2,4]",
    "4bin_412_25":   "[0,.4,1.2,\n2.5,4]",
    "3bin_420":      "[0,.4,2,4]",
    "4bin_nom_30":   "[0,.8,1.6,\n3,4]",
    "4bin_516_30":   "[0,.5,1.6,\n3,4]",
    "3bin_520":      "[0,.5,2,4]",
    "3bin_104":      "[0,.1,.4,4]",
    "4bin_104_200":  "[0,.1,.4,\n2,4]",
    "4bin_104_250":  "[0,.1,.4,\n2.5,4]",
}

# Short signal labels for panel titles
SIG_SHORT = {
    "VH_tau1mm_M55":                     "VH  τ=1mm  M=55  (lep)",
    "VH_tau10mm_M55":                    "VH  τ=10mm M=55  (lep)",
    "VH_tau1mm_M40":                     "VH  τ=1mm  M=40  (lep)",
    "VH_tau1mm_M15":                     "VH  τ=1mm  M=15  (lep)",
    "ggHToSSTodddd_tau1mm_M55":          "ggH τ=1mm  M=55  (bjet)",
    "ggHToSSTodddd_tau1mm_M40":          "ggH τ=1mm  M=40  (bjet)",
    "mfv_stopdbardbar_tau001000um_M0200":"stop τ=1mm  M=200 (bjet)",
    "mfv_stopdbardbar_tau000300um_M0400":"stop τ=0.3mm M=400 (bjet)",
    "mfv_neu_tau001000um_M0400":         "neu  τ=1mm  M=400 (bjet)",
}

ALL_SCHEMES = [
    "old_binning","2bin","3bin_nom","3bin_v1","3bin_v2","3bin_v3","3bin_v4",
    "4bin_v1","4bin_v2","3bin_412",
    "4bin_412_25","3bin_420","4bin_nom_30","4bin_516_30","3bin_520",
    "3bin_104","4bin_104_200","4bin_104_250",
]


def main():
    results = collect()

    sigs    = list(SIG_LABELS.keys())
    schemes = [s for s in ALL_SCHEMES if s in results]
    xs      = np.arange(len(schemes))

    # Color by number of bins; nominal gets its own color
    NBINS_COLOR = {2: "#88CCEE", 3: "#DDCC77", 4: "#CC6677"}
    NOM_COLOR   = "#222222"
    def scheme_color(s):
        if s == "3bin_nom":
            return NOM_COLOR
        nbins = SCHEMES[s].get("nbins", SCHEMES[s].get("bjet_nbins", 3))
        return NBINS_COLOR.get(nbins, "#999999")
    colors = [scheme_color(s) for s in schemes]

    fig, axes = plt.subplots(3, 3, figsize=(18, 13))
    axes = axes.flatten()

    for ax, sig_id in zip(axes, sigs):
        uls = []
        for s in schemes:
            v = results.get(s, {}).get(sig_id, {}).get("al")
            uls.append(v)

        nom_ul = results.get("3bin_nom", {}).get(sig_id, {}).get("al")

        # Bar chart
        for i, (x, ul, c) in enumerate(zip(xs, uls, colors)):
            if ul is None:
                continue
            is_nom = (schemes[i] == "3bin_nom")
            ax.bar(x, ul, color=c, alpha=0.90, width=0.75,
                   linewidth=1.5 if is_nom else 0.5,
                   edgecolor="black")

        # Nominal reference line
        if nom_ul is not None:
            ax.axhline(nom_ul, color="black", linestyle="--", linewidth=1.0, alpha=0.6)

        ax.set_title(SIG_SHORT[sig_id], fontsize=10)
        ax.set_ylabel("Exp. 95% CL UL on r", fontsize=8)
        ax.set_xticks(xs)
        ax.set_xticklabels([SHORT_LABELS.get(s, s) for s in schemes],
                           fontsize=6.5, rotation=30, ha="right")
        ax.yaxis.set_tick_params(labelsize=8)

        # Y-range: just above the max bar, starting near zero
        vals = [v for v in uls if v is not None]
        if vals:
            ymax = max(vals) * 1.12
            ymin = min(vals) * 0.88
            ax.set_ylim(ymin, ymax)

        ax.grid(axis="y", alpha=0.3)

    # Legend
    legend_handles = [
        mpatches.Patch(color=NOM_COLOR,   label="Nominal [0,0.8,1.6,4]"),
        mpatches.Patch(color="#88CCEE",   label="2-bin"),
        mpatches.Patch(color="#DDCC77",   label="3-bin alternatives"),
        mpatches.Patch(color="#CC6677",   label="4-bin alternatives"),
    ]
    fig.legend(handles=legend_handles, loc="upper center", ncol=4,
               fontsize=9, bbox_to_anchor=(0.5, 1.01))

    fig.suptitle("Expected 95% CL UL on r — binning scheme comparison (stat-only, Asimov)",
                 fontsize=11, y=1.04)
    fig.tight_layout()

    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "scheme_comparison.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)


if __name__ == "__main__":
    main()

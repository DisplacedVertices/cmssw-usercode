"""
Scheme comparison plot for the three new signal points added in round 2:
  VH tau=1mm M=40 (lep), VH tau=1mm M=15 (lep), ggH tau=1mm M=40 (bjet)

Usage:
  source LCG dev3 setup
  python3 plot_new_signals.py
Output: new_signals_comparison.pdf / .png
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SCHEMES
from collect_results import collect

HERE = os.path.dirname(os.path.abspath(__file__))

SHORT_LABELS = {
    "old_binning": "[0,.08,.16,4]",
    "2bin":        "[0,1.6,4]",
    "3bin_nom":    "[0,.8,1.6,4]",
    "3bin_v1":     "[0,.4,1.6,4]",
    "3bin_v2":     "[0,.8,2.5,4]",
    "3bin_v3":     "[0,1,2,4]",
    "3bin_v4":     "[0,.5,1,4]",
    "4bin_v1":     "[0,.4,.8,\n1.6,4]",
    "4bin_v2":     "[0,.8,1.2,\n1.6,4]",
    "3bin_412":    "[0,.4,1.2,4]",
    "4bin_412_25": "[0,.4,1.2,\n2.5,4]",
    "3bin_420":    "[0,.4,2,4]",
    "4bin_nom_30": "[0,.8,1.6,\n3,4]",
    "4bin_516_30": "[0,.5,1.6,\n3,4]",
    "3bin_520":    "[0,.5,2,4]",
    "3bin_104":    "[0,.1,.4,4]",
    "4bin_104_200": "[0,.1,.4,\n2,4]",
    "4bin_104_250": "[0,.1,.4,\n2.5,4]",
}

NEW_SIGS = [
    ("ggHToSSTodddd_tau1mm_M40", "ggH  τ=1mm  M=40  (bjet)"),
    ("VH_tau1mm_M40",            "VH   τ=1mm  M=40  (lep)"),
    ("VH_tau1mm_M15",            "VH   τ=1mm  M=15  (lep)"),
]

ALL_SCHEMES = [
    "old_binning","2bin","3bin_nom","3bin_v1","3bin_v2","3bin_v3","3bin_v4",
    "4bin_v1","4bin_v2","3bin_412",
    "4bin_412_25","3bin_420","4bin_nom_30","4bin_516_30","3bin_520",
    "3bin_104","4bin_104_200","4bin_104_250",
]

NBINS_COLOR = {2: "#88CCEE", 3: "#DDCC77", 4: "#CC6677"}
NOM_COLOR   = "#222222"

def scheme_color(s):
    if s == "3bin_nom":
        return NOM_COLOR
    nbins = SCHEMES[s].get("nbins", SCHEMES[s].get("bjet_nbins", 3))
    return NBINS_COLOR.get(nbins, "#999999")


def main():
    results = collect()
    schemes = [s for s in ALL_SCHEMES if s in results]
    xs      = np.arange(len(schemes))
    colors  = [scheme_color(s) for s in schemes]

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    for ax, (sig_id, title) in zip(axes, NEW_SIGS):
        uls = [results.get(s, {}).get(sig_id, {}).get("al") for s in schemes]
        nom_ul = results.get("3bin_nom", {}).get(sig_id, {}).get("al")

        for i, (x, ul, c) in enumerate(zip(xs, uls, colors)):
            if ul is None:
                continue
            is_nom = (schemes[i] == "3bin_nom")
            ax.bar(x, ul, color=c, alpha=0.90, width=0.75,
                   linewidth=1.5 if is_nom else 0.5,
                   edgecolor="black")

        if nom_ul is not None:
            ax.axhline(nom_ul, color="black", linestyle="--", linewidth=1.0, alpha=0.6)

        ax.set_title(title, fontsize=11)
        ax.set_ylabel("Exp. 95% CL UL on r", fontsize=9)
        ax.set_xticks(xs)
        ax.set_xticklabels([SHORT_LABELS.get(s, s) for s in schemes],
                           fontsize=6.5, rotation=30, ha="right")
        ax.yaxis.set_tick_params(labelsize=9)

        vals = [v for v in uls if v is not None]
        if vals:
            ax.set_ylim(min(vals) * 0.88, max(vals) * 1.12)

        ax.grid(axis="y", alpha=0.3)

    legend_handles = [
        mpatches.Patch(color=NOM_COLOR,  label="Nominal [0,0.8,1.6,4]"),
        mpatches.Patch(color="#88CCEE",  label="2-bin"),
        mpatches.Patch(color="#DDCC77",  label="3-bin alternatives"),
        mpatches.Patch(color="#CC6677",  label="4-bin alternatives"),
    ]
    fig.legend(handles=legend_handles, loc="upper center", ncol=4,
               fontsize=9, bbox_to_anchor=(0.5, 1.02))

    fig.suptitle("Expected 95% CL UL on r — new signal points (stat-only, Asimov)",
                 fontsize=11, y=1.06)
    fig.tight_layout()

    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "new_signals_comparison.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)


if __name__ == "__main__":
    main()

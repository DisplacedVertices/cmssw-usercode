"""
Compare stat-only vs with-systematics expected UL for 3bin_nom, 3bin_v1, 3bin_412.
Bar chart: grouped pairs (stat-only, with-systs) per scheme per signal.
Output: syst_comparison.pdf / .png
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collect_results import collect, SIG_LABELS

HERE     = os.path.dirname(os.path.abspath(__file__))
OUT_SYST = os.path.join(HERE, "combine_output_systs")

SCHEMES_SYST = ["3bin_nom", "3bin_v1", "3bin_412"]
SCHEME_LABELS = {
    "3bin_nom": "nom\n[0,.8,1.6,4]",
    "3bin_v1":  "v1\n[0,.4,1.6,4]",
    "3bin_412": "412\n[0,.4,1.2,4]",
}
SIG_SHORT = {
    "VH_tau1mm_M55":                     "VH  τ=1mm  M=55 (lep)",
    "VH_tau10mm_M55":                    "VH  τ=10mm M=55 (lep)",
    "ggHToSSTodddd_tau1mm_M55":          "ggH  τ=1mm  M=55 (bjet)",
    "mfv_stopdbardbar_tau001000um_M0200":"stop τ=1mm  M=200 (bjet)",
    "mfv_stopdbardbar_tau000300um_M0400":"stop τ=0.3mm M=400 (bjet)",
    "mfv_neu_tau001000um_M0400":         "neu  τ=1mm  M=400 (bjet)",
}


def collect_systs():
    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
    except ImportError:
        print("ERROR: ROOT not available"); sys.exit(1)

    results = {}
    for scheme in SCHEMES_SYST:
        results[scheme] = {}
        for sig_id in SIG_LABELS:
            work = os.path.join(OUT_SYST, scheme, sig_id)
            if not os.path.isdir(work):
                continue
            pattern = "higgsCombinesysts_%s_%s.AsymptoticLimits" % (scheme, sig_id)
            for fn in os.listdir(work):
                if fn.startswith(pattern) and fn.endswith(".root"):
                    f = ROOT.TFile(os.path.join(work, fn))
                    t = f.Get("limit")
                    for ev in t:
                        if abs(ev.quantileExpected - 0.5) < 0.01:
                            results[scheme][sig_id] = float(ev.limit)
                            break
                    f.Close()
                    break
    return results


def main():
    stat_results  = collect()   # from collect_results.py
    syst_results  = collect_systs()

    sigs    = list(SIG_LABELS.keys())
    schemes = SCHEMES_SYST

    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    axes = axes.flatten()

    bar_w  = 0.35
    xs_stat = np.arange(len(schemes))
    xs_syst = xs_stat + bar_w

    for ax, sig_id in zip(axes, sigs):
        stat_uls = [stat_results.get(s, {}).get(sig_id, {}).get("al") for s in schemes]
        syst_uls = [syst_results.get(s, {}).get(sig_id) for s in schemes]

        for i, (xu, xs_, u_stat, u_syst) in enumerate(
                zip(xs_stat, xs_syst, stat_uls, syst_uls)):
            if u_stat is not None:
                ax.bar(xu, u_stat, bar_w, color="#4477AA", alpha=0.85,
                       edgecolor="black", linewidth=0.5)
            if u_syst is not None:
                ax.bar(xs_, u_syst, bar_w, color="#CC6677", alpha=0.85,
                       edgecolor="black", linewidth=0.5)

        ax.set_title(SIG_SHORT[sig_id], fontsize=9)
        ax.set_ylabel("Exp. 95% CL UL on r", fontsize=8)
        ax.set_xticks(xs_stat + bar_w / 2)
        ax.set_xticklabels([SCHEME_LABELS[s] for s in schemes], fontsize=9)
        ax.yaxis.set_tick_params(labelsize=8)
        ax.grid(axis="y", alpha=0.3)

        vals = [v for v in stat_uls + syst_uls if v is not None]
        if vals:
            ax.set_ylim(min(vals) * 0.85, max(vals) * 1.15)

    legend_handles = [
        mpatches.Patch(color="#4477AA", label="Stat-only"),
        mpatches.Patch(color="#CC6677", label="With systematics"),
    ]
    fig.legend(handles=legend_handles, loc="upper center", ncol=2,
               fontsize=10, bbox_to_anchor=(0.5, 1.01))
    fig.suptitle("Exp. 95% CL UL on r — stat-only vs with-systematics (Asimov)",
                 fontsize=11, y=1.04)
    fig.tight_layout()

    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "syst_comparison.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)


if __name__ == "__main__":
    main()

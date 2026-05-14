# Plot normalized background and signal shapes from 3bin_nom datacards.
# Reads yields from text datacards (no ROOT); sums all 4 years.
# Run after generate_variants_el7.py and strip_systs.py have produced
# BinningStudy/datacards/3bin_nom/.

import os, re
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

HERE     = os.path.dirname(os.path.abspath(__file__))
DC_BASE  = os.path.join(HERE, "datacards", "3bin_nom")

# Nominal 3-bin edges (mm/sigma)
BIN_EDGES = [0.0, 0.8, 1.6, 4.0]
BIN_CTRS  = [0.4, 1.2, 2.8]

YEARS = ["20161", "20162", "2017", "2018"]


def read_yields(channel, sig_id):
    """Return (bkg_yields, sig_yields) summed over all years as numpy arrays."""
    bkg_total = None
    sig_total = None
    for yr in YEARS:
        path = os.path.join(DC_BASE, channel,
                            "Datacard_%s_%s_%s_statonly.txt" % (channel, sig_id, yr))
        if not os.path.exists(path):
            continue
        with open(path) as f:
            lines = f.readlines()
        rate_lines = [l for l in lines if l.startswith("rate")]
        if len(rate_lines) < 1:
            continue
        vals = list(map(float, rate_lines[0].split()[1:]))
        nbins = len(vals) // 2
        # makeDatacard.py writes signal first, then background in the rate line
        sig = np.array(vals[:nbins])
        bkg = np.array(vals[nbins:])
        if bkg_total is None:
            bkg_total = bkg.copy()
            sig_total = sig.copy()
        else:
            bkg_total += bkg
            sig_total += sig
    return bkg_total, sig_total


def plot_channel(ax, channel, signals, colors, labels, title):
    """Plot background + signals for one channel."""
    first_bkg = None
    for sig_id, color, label in zip(signals, colors, labels):
        bkg, sig = read_yields(channel, sig_id)
        if bkg is None:
            print("WARNING: no data for %s / %s" % (channel, sig_id))
            continue
        if first_bkg is None:
            first_bkg = bkg

        # Normalize signal to unit area
        sig_norm = sig / sig.sum() if sig.sum() > 0 else sig

        # Plot as step histogram
        ax.step(BIN_EDGES[:-1] + [BIN_EDGES[-1]],
                list(sig_norm) + [0],
                where='post', color=color, lw=2, label=label)

    # Background (use last read, they should all be the same shape)
    if first_bkg is not None:
        bkg_norm = first_bkg / first_bkg.sum() if first_bkg.sum() > 0 else first_bkg
        ax.step(BIN_EDGES[:-1] + [BIN_EDGES[-1]],
                list(bkg_norm) + [0],
                where='post', color='black', lw=2.5, ls='--', label='Background')

    # Bin boundary lines
    for edge in BIN_EDGES[1:-1]:
        ax.axvline(edge, color='gray', lw=1.5, ls=':', alpha=0.8)

    # Bin edge labels at top (use axes fraction coordinates)
    for i, (lo, hi) in enumerate(zip(BIN_EDGES[:-1], BIN_EDGES[1:])):
        hi_str = "%.1f" % hi if hi < 3.5 else r"$\infty$"
        x_frac = (BIN_CTRS[i] - BIN_EDGES[0]) / (BIN_EDGES[-1] - BIN_EDGES[0])
        ax.text(x_frac, 1.01, "[%.1f, %s]" % (lo, hi_str),
                ha='center', va='bottom', fontsize=8, color='gray',
                transform=ax.transAxes)

    ax.set_xlim(BIN_EDGES[0], BIN_EDGES[-1])
    ax.set_ylim(bottom=0)
    ax.set_xlabel(r"Displacement significance $\sigma_{sv}$ (mm/$\sigma$)", fontsize=11)
    ax.set_ylabel("Normalized yield (arb.)", fontsize=11)
    ax.set_title(title, fontsize=12)
    ax.legend(fontsize=9, loc='upper right')
    ax.set_xticks(BIN_EDGES)
    ax.tick_params(axis='both', labelsize=9)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle(
        "Background template and signal shapes -- nominal 3-bin scheme\n"
        "Dashed vertical lines: bin boundaries at 0.8 and 1.6 $\\sigma_{sv}$",
        fontsize=11
    )

    # Bjet channel: use signals with contrasting lifetime shapes
    plot_channel(
        axes[0],
        channel="bjet",
        signals=[
            "mfv_neu_tau001000um_M0400",
            "mfv_stopdbardbar_tau000300um_M0400",
        ],
        colors=["royalblue", "tomato"],
        labels=[
            r"$\tilde{g}\tilde{g}$, $\tau=1$ mm, $M=400$ GeV",
            r"$\tilde{t}\tilde{t}^*$, $\tau=0.3$ mm, $M=400$ GeV",
        ],
        title="Bjet channel (displaced jet + b-tag trigger)",
    )

    # Lepton channel
    plot_channel(
        axes[1],
        channel="lep",
        signals=[
            "VH_tau1mm_M55",
            "VH_tau10mm_M55",
        ],
        colors=["royalblue", "tomato"],
        labels=[
            r"VH $\to$ SS, $\tau=1$ mm, $m_S=55$ GeV",
            r"VH $\to$ SS, $\tau=10$ mm, $m_S=55$ GeV",
        ],
        title="Lepton channel (lepton trigger)",
    )

    plt.tight_layout()
    out = os.path.join(HERE, "background_templates.pdf")
    fig.savefig(out, bbox_inches="tight")
    print("Saved: %s" % out)

    out_png = os.path.join(HERE, "background_templates.png")
    fig.savefig(out_png, bbox_inches="tight", dpi=150)
    print("Saved: %s" % out_png)


if __name__ == "__main__":
    main()

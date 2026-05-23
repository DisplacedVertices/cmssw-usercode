# Background and signal shapes in sumdbv, yield-normalized.
# Background: h_c1v_sumdbv_w_errorbars scaled to Run2 n2v (expected background events).
# Signal: weighted by XS x lumi x eff (weight branch), summed over all years.
# Requires PyROOT (LCG dev3 or cmsenv).

import os, glob
import ROOT
ROOT.gROOT.SetBatch(True)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE     = os.path.dirname(os.path.abspath(__file__))
FORLIM   = os.path.dirname(HERE)
BKG_BASE = os.path.join(FORLIM, "BackgroundTemplates")

LEP_MINI  = "/uscms/home/gdecastr/nobackup/crabdirs/MiniTree_tag001Lepm_VH"
BJET_MINI = "/uscms/home/gdecastr/nobackup/crabdirs/MiniTree_tag001BvetoLHTm_bjet"

NOMINAL_EDGES = [0.0, 0.8, 1.6, 4.0]
YEARS         = ["20161", "20162", "2017", "2018"]
REBIN         = 8      # 200 -> 25 bins, width 0.16 cm
NBINS_DISP    = 25
XMAX          = 4.0

# Run2 total expected background (sum over years), from sig_and_bkg_configs.py
N2V_RUN2 = {
    "bjet": 0.258 + 0.062 + 0.078 + 0.122,   # = 0.520
    "lep":  0.001 + 0.012 + 0.002 + 0.034,   # = 0.049
}


def get_fine_bkg(channel, tag):
    """Rebin background histogram and scale to Run2 n2v yield.
    Returns (edges, counts) where counts are in expected events per display bin."""
    path = os.path.join(BKG_BASE, channel,
                        "2v_from_jets_run2_5track_default_%s.root" % tag)
    f = ROOT.TFile(path)
    h = f.Get("h_c1v_sumdbv_w_errorbars")
    h.SetDirectory(0)
    h_rb = h.Rebin(REBIN)
    nb       = h_rb.GetNbinsX()
    edges    = np.array([h_rb.GetBinLowEdge(i+1) for i in range(nb)]
                        + [h_rb.GetBinLowEdge(nb+1)])
    contents = np.array([h_rb.GetBinContent(i+1) for i in range(nb)])
    f.Close()
    total = contents.sum()
    if total > 0:
        contents = contents / total * N2V_RUN2[channel]
    return edges, contents


def get_fine_sig_shape(mini_dirs_by_year):
    """Fill sumdbv histogram (unweighted, nvtx>=2 selection).
    Returns (edges, counts_normalized) normalized to unit area — shape only."""
    edges  = np.linspace(0.0, XMAX, NBINS_DISP + 1)
    counts = np.zeros(NBINS_DISP)
    for pattern in mini_dirs_by_year:
        for fn in glob.glob(pattern):
            f = ROOT.TFile(fn)
            t = f.Get("mfvMiniTree/t")
            n = t.Draw("sumdbv", "1.0*(nvtx>=2)", "goff")
            if n > 0:
                vals = np.frombuffer(t.GetV1(), dtype=np.float64, count=n).copy()
                c, _ = np.histogram(vals, bins=edges)
                counts += c
            f.Close()
    bin_w = edges[1] - edges[0]
    total = (counts * bin_w).sum()
    if total > 0:
        counts = counts / total
    return edges, counts


def get_sig_run2_yield(sig_id, ch):
    """Sum expected signal events across all 4 years from 3bin_nom stat-only datacards."""
    total = 0.0
    for year in YEARS:
        dc = os.path.join(HERE, "datacards", "3bin_nom", ch,
                          "Datacard_%s_%s_%s_statonly.txt" % (ch, sig_id, year))
        if not os.path.exists(dc):
            continue
        for line in open(dc):
            if line.startswith("rate"):
                vals = list(map(float, line.split()[1:]))
                nbins = len(vals) // 2
                total += sum(vals[:nbins])
                break
    return total


def plot_channel(ax, channel, tag, signals, title):
    # signals: list of (label, color, glob_patterns, sig_id)
    edges, bkg = get_fine_bkg(channel, tag)

    # Pre-compute signal yields for y_ceil
    sig_counts = []
    for label, color, patterns, sig_id in signals:
        _, shape = get_fine_sig_shape(patterns)
        run2_yield = get_sig_run2_yield(sig_id, channel)
        bin_w = edges[1] - edges[0]
        counts = shape * run2_yield * bin_w   # events per display bin
        sig_counts.append((label, color, counts))

    nonzero = bkg[bkg > 0]
    y_floor = nonzero.min() * 0.10 if len(nonzero) else 1e-6
    y_ceil  = max(bkg.max(), max(c.max() for _, _, c in sig_counts)) * 5.0

    bkg_disp = np.where(bkg > 0, bkg, y_floor)
    ax.fill_between(edges[:-1], bkg_disp, y2=y_floor,
                    step="post", alpha=0.20, color="#444444")
    ax.step(edges[:-1], bkg_disp, where="post",
            color="#222222", lw=1.8, label="Background")

    for label, color, counts in sig_counts:
        sig_disp = np.where(counts > 0, counts, y_floor)
        ax.step(edges[:-1], sig_disp, where="post", color=color, lw=2.2, label=label)

    for edge in NOMINAL_EDGES[1:-1]:
        ax.axvline(edge, color="black", lw=1.8, ls="--", zorder=5)

    nom_labels = [r"[0.0, 0.8)", r"[0.8, 1.6)", r"[1.6, $\infty$)"]
    nom_ctrs   = [0.4, 1.2, 2.8]
    for ctr, lbl in zip(nom_ctrs, nom_labels):
        ax.text(ctr / XMAX, 1.01, lbl, ha="center", va="bottom",
                fontsize=9, color="black", transform=ax.transAxes)

    ax.set_yscale("log")
    ax.set_xlim(0.0, XMAX)
    ax.set_ylim(y_floor, y_ceil)
    ax.set_xlabel(r"sumdbv (cm)", fontsize=12)
    ax.set_ylabel(r"Expected events / 0.16 cm bin (Run 2)", fontsize=11)
    ax.set_title(title, fontsize=13, pad=14)
    ax.set_xticks([0.0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 2.8, 3.2, 3.6, 4.0])
    ax.tick_params(axis="both", labelsize=10)
    ax.legend(fontsize=10, loc="upper right", framealpha=0.85)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    fig.suptitle("Nominal sumdbv bin boundaries", fontsize=13)

    def bjet_patterns(proc, tau, mass):
        return ["%s/condor_%s_%s_%s_%s/minitree_0.root" % (BJET_MINI, proc, tau, mass, yr)
                for yr in YEARS]

    VH_PROCS = ["ZHToSSTodddd", "WminusHToSSTodddd", "WplusHToSSTodddd", "ggZHToSSTodddd"]

    def lep_vh_patterns(tau, mass):
        return ["%s/condor_%s_%s_%s_%s/minitree_0.root" % (LEP_MINI, proc, tau, mass, yr)
                for proc in VH_PROCS for yr in YEARS]

    plot_channel(
        axes[0], "bjet", "ULV30BvetoLHTm",
        signals=[
            (r"$\tilde{g}\tilde{g}$, $\tau=1$ mm, $M=400$ GeV",
             "royalblue", bjet_patterns("mfv_neu", "tau001000um", "M0400"),
             "mfv_neu_tau001000um_M0400"),
            (r"$\tilde{t}\tilde{t}^*$, $\tau=0.3$ mm, $M=400$ GeV",
             "tomato", bjet_patterns("mfv_stopdbardbar", "tau000300um", "M0400"),
             "mfv_stopdbardbar_tau000300um_M0400"),
            (r"ggH $\to$ SS, $\tau=1$ mm, $m_S=55$ GeV",
             "forestgreen", bjet_patterns("ggHToSSTodddd", "tau1mm", "M55"),
             "ggHToSSTodddd_tau1mm_M55"),
        ],
        title="Bjet channel",
    )

    plot_channel(
        axes[1], "lep", "ULV30Lepm",
        signals=[
            (r"VH $\to$ SS, $\tau=1$ mm, $m_S=55$ GeV",
             "royalblue", lep_vh_patterns("tau1mm", "M55"),
             "VH_tau1mm_M55"),
            (r"VH $\to$ SS, $\tau=10$ mm, $m_S=55$ GeV",
             "tomato", lep_vh_patterns("tau10mm", "M55"),
             "VH_tau10mm_M55"),
        ],
        title="Lepton channel",
    )

    plt.tight_layout()
    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "background_templates.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)


if __name__ == "__main__":
    main()

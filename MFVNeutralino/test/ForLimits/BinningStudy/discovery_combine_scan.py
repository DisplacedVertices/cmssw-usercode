"""
Combine-based expected discovery significance scan.

For each (signal, x), builds a single-bin [x, 4.0] datacard with
  bkg = B_tail(x), sig = S_tail(x)
and runs:
  combine -M Significance -t -1 --expectSignal 1
to get Z_exp: the expected significance if the signal is present at r=1.

This is the proper discovery-power metric — it combines signal efficiency
and background suppression into one number via the profile likelihood Asimov.

Usage (from CMSSW environment with combine in PATH):
  python3 discovery_combine_scan.py
"""
import os, sys, subprocess, tempfile, shutil, re
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import YEARS
from fast_study_datacards import (BKG_FILES, N2V, get_sig_files, parse_ref_yield)

HERE = os.path.dirname(os.path.abspath(__file__))
SCAN_VALS = [round(i * 0.1, 1) for i in range(5, 40)]   # 0.5..3.9

PLOT_SIGS = [
    ("ggHToSSTodddd_tau1mm_M55",  "bjet", "forestgreen", r"ggH $\tau$=1mm $M$=55"),
    ("ggHToSSTodddd_tau1mm_M40",  "bjet", "limegreen",   r"ggH $\tau$=1mm $M$=40"),
    ("VH_tau1mm_M55",             "lep",  "royalblue",   r"VH $\tau$=1mm $M$=55"),
    ("VH_tau10mm_M55",            "lep",  "tomato",      r"VH $\tau$=10mm $M$=55"),
]


def get_bkg_tail(ch, x):
    import ROOT
    f = ROOT.TFile(BKG_FILES[ch])
    h = f.Get("h_c1v_sumdbv_w_errorbars")
    total = h.Integral()
    scale = sum(N2V[ch]) / total
    nbins = h.GetNbinsX()
    tail = 0.0
    for i in range(1, nbins + 2):
        if h.GetBinLowEdge(i) >= x:
            tail += h.GetBinContent(i) * scale
    f.Close()
    return tail


def get_sig_tail(sig_id, ch, x):
    """Returns (s_tail, n_mc_above). n_mc_above=0 means unusable."""
    import ROOT
    counts_above = 0.0
    counts_total = 0.0
    for year in YEARS:
        for fn in get_sig_files(sig_id, ch, year):
            f = ROOT.TFile(fn)
            t = f.Get("mfvMiniTree/t")
            counts_above += max(t.Draw("sumdbv", "nvtx>=2 && sumdbv>=%f" % x, "goff"), 0)
            counts_total += max(t.Draw("sumdbv", "nvtx>=2", "goff"), 0)
            f.Close()
    if counts_total == 0:
        return 0.0, 0
    total_yield = sum(parse_ref_yield(sig_id, ch, yr) for yr in YEARS)
    s_tail = total_yield * (counts_above / counts_total)
    return s_tail, int(counts_above)


def make_datacard(path, b_tail, s_tail):
    """Stat-only single-bin datacard. Observation is -1: Asimov used by combine -t -1."""
    with open(path, "w") as f:
        f.write("imax 1\njmax 1\nkmax 0\n")
        f.write("-" * 40 + "\n")
        f.write("bin         tail\n")
        f.write("observation -1\n")
        f.write("-" * 40 + "\n")
        f.write("bin         tail         tail\n")
        f.write("process     sig          bkg\n")
        f.write("process     0            1\n")
        f.write("rate        %.8g         %.8g\n" % (s_tail, b_tail))


def run_significance(dc_path, workdir):
    """Run combine -M Significance on Asimov (s+b) with r=1, return Z_exp or None."""
    tag = os.path.splitext(os.path.basename(dc_path))[0]
    cmd = ["combine", "-M", "Significance", "-t", "-1", "--expectSignal", "1",
           "-n", tag, dc_path]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           cwd=workdir, timeout=60)
        for line in r.stdout.splitlines():
            m = re.search(r"Significance:\s+([\d.eE+\-nan]+)", line)
            if m:
                val = m.group(1)
                return float(val) if val != "nan" else None
    except Exception:
        pass
    return None



def main():
    if shutil.which("combine") is None:
        print("ERROR: combine not in PATH — source CMSSW environment first.")
        sys.exit(1)

    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
        ROOT.gErrorIgnoreLevel = ROOT.kError
    except ImportError:
        print("ERROR: ROOT not available"); sys.exit(1)

    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    xs = SCAN_VALS
    workdir = tempfile.mkdtemp(prefix="disc_comb_")
    print("Tempdir:", workdir)

    print("Computing background tails...")
    bkg = {ch: [get_bkg_tail(ch, x) for x in xs] for ch in ("bjet", "lep")}

    # --- Combine expected significance scan ---
    combine_results = {}   # sig_id -> list of (x, Z_exp)
    for sig_id, ch, color, label in PLOT_SIGS:
        print("\n%s (%s)..." % (sig_id, ch))
        pts = []
        for x, b in zip(xs, bkg[ch]):
            s_tail, n_mc = get_sig_tail(sig_id, ch, x)
            if n_mc < 1 or s_tail <= 0:
                pts.append((x, None))
                continue
            dc = os.path.join(workdir, "dc_%s_%03d.txt" % (sig_id.replace("_","")[:12], round(x*10)))
            make_datacard(dc, b, s_tail)
            z = run_significance(dc, workdir)
            print("  x=%.1f  B=%.3e  S=%.4f  Z_exp=%s" % (
                x, b, s_tail, "%.2f" % z if z is not None else "fail"))
            pts.append((x, z))
        combine_results[sig_id] = pts

    # --- plot ---
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    for ax, ch, title in [
        (axes[0], "bjet", "Bjet channel"),
        (axes[1], "lep",  "Lepton channel"),
    ]:
        ch_sigs = [(sid, c, col, lab) for sid, c, col, lab in PLOT_SIGS if c == ch]

        for sig_id, _, color, label in ch_sigs:
            pts = combine_results[sig_id]
            vx = [x for x, z in pts if z is not None]
            vz = [z for _, z in pts if z is not None]
            if vz:
                ax.plot(vx, vz, "o-", color=color, lw=1.8, ms=4, label=label)

        ax.axhline(3.0, color="gray",  ls="--", lw=1.2, label=r"3$\sigma$")
        ax.axhline(5.0, color="black", ls="--", lw=1.2, label=r"5$\sigma$")

        ax.set_xlabel("4th boundary x (cm)", fontsize=11)
        ax.set_ylabel(r"Expected $Z_{\rm exp}$ (sigma, Asimov $r$=1)", fontsize=10)
        ax.set_title(title, fontsize=12)
        ax.set_ylim(0, 12)
        ax.set_xticks(xs[::2])
        ax.set_xticklabels(["%.1f" % v for v in xs[::2]], fontsize=8)
        ax.legend(fontsize=9, loc="upper right", framealpha=0.85)
        ax.grid(alpha=0.3)

    fig.suptitle(r"Expected discovery significance vs 4th boundary x in [0, 0.1, 0.4, $x$, 4.0] cm  (single tail bin, stat-only)",
                 fontsize=11)
    fig.tight_layout()

    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "discovery_combine_scan.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)

    shutil.rmtree(workdir)


if __name__ == "__main__":
    main()

"""
2-bin boundary scan: [0, x, 4.0]
  Fine:   x = 0.01..0.10 in steps of 0.01
  Coarse: x = 0.20..3.90 in steps of 0.10

Usage:
  python3 boundary_scan_2bin.py gen     # generate datacards (LCG dev3 or cmsenv)
  python3 boundary_scan_2bin.py run     # run combine (cmsenv)
  python3 boundary_scan_2bin.py plot    # make plot (LCG dev3)
  python3 boundary_scan_2bin.py         # all three
"""
import os, sys, subprocess
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SIGNAL_POINTS, YEARS
from fast_study_datacards import run_scheme, parse_ref_yield, write_datacard

HERE     = os.path.dirname(os.path.abspath(__file__))
DC_BASE  = os.path.join(HERE, "datacards")
OUT_BASE = os.path.join(HERE, "combine_output")

FINE_VALS   = [round(i * 0.01, 2) for i in range(1, 11)]   # 0.01..0.10
COARSE_VALS = [round(i * 0.1, 1)  for i in range(2, 40)]   # 0.20..3.90
SCAN_VALS   = FINE_VALS + COARSE_VALS
UPPER       = 4.0

SIG_CHANNEL = {sp[0]: sp[1] for sp in SIGNAL_POINTS}


def scheme_name(x):
    return "scan2b_%03d" % round(x * 100)

def scheme_bins(x):
    return [0., x, UPPER]


# ---- generation -------------------------------------------------------

def gen_all():
    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
    except ImportError:
        print("ERROR: ROOT not available"); sys.exit(1)

    for x in SCAN_VALS:
        name = scheme_name(x)
        dc_check = os.path.join(DC_BASE, name)
        if os.path.isdir(dc_check):
            print("SKIP %s (datacards exist)" % name)
            continue
        bins = scheme_bins(x)
        print("\n=== scan2b x=%.2f  %s ===" % (x, bins))
        info = {"bins": bins, "nbins": len(bins) - 1}
        run_scheme(name, info)
    print("\nGeneration done.")


# ---- combine ----------------------------------------------------------

def run_all():
    for x in SCAN_VALS:
        name = scheme_name(x)
        dc_dir = os.path.join(DC_BASE, name)
        if not os.path.isdir(dc_dir):
            print("SKIP %s (no datacards)" % name)
            continue
        for sig_id, ch in SIGNAL_POINTS:
            _run_one(name, sig_id, ch)
    print("\nCombine done.")


def _run_one(scheme, sig_id, ch):
    work = os.path.join(OUT_BASE, scheme, sig_id)
    os.makedirs(work, exist_ok=True)

    card_args = []
    for yr in YEARS:
        p = os.path.join(DC_BASE, scheme, ch,
                         "Datacard_%s_%s_%s_statonly.txt" % (ch, sig_id, yr))
        if not os.path.exists(p):
            print("  SKIP (missing card): %s/%s" % (scheme, sig_id))
            return
        card_args.append("%s_%s=%s" % (ch, yr, p))

    combined = os.path.join(work, "combined_%s.txt" % sig_id)
    r = subprocess.run(["combineCards.py"] + card_args,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("  combineCards FAILED: %s/%s" % (scheme, sig_id))
        return
    with open(combined, "w") as fh:
        fh.write(r.stdout)

    subprocess.run(
        ["combine", "-M", "AsymptoticLimits",
         "--name", "%s_%s" % (scheme, sig_id),
         combined, "--expectSignal", "0", "-v", "0"],
        cwd=work, capture_output=True)


# ---- collect results --------------------------------------------------

def collect():
    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
    except ImportError:
        print("ERROR: ROOT not available"); sys.exit(1)

    results = {}   # x -> sig_id -> expected_median_UL
    for x in SCAN_VALS:
        name = scheme_name(x)
        out_dir = os.path.join(OUT_BASE, name)
        if not os.path.isdir(out_dir):
            continue
        results[x] = {}
        for sig_id, ch in SIGNAL_POINTS:
            work = os.path.join(out_dir, sig_id)
            pattern = "higgsCombine%s_%s.AsymptoticLimits" % (name, sig_id)
            ul = None
            for fn in (os.listdir(work) if os.path.isdir(work) else []):
                if fn.startswith(pattern) and fn.endswith(".root"):
                    f = ROOT.TFile(os.path.join(work, fn))
                    t = f.Get("limit")
                    try:
                        for ev in t:
                            if abs(ev.quantileExpected - 0.5) < 0.01:
                                ul = float(ev.limit)
                                break
                    except TypeError:
                        print("  WARN: unreadable file %s" % fn)
                    f.Close()
                    break
            results[x][sig_id] = ul
    return results


# ---- plot -------------------------------------------------------------

def plot(results):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    sigs = [sp[0] for sp in SIGNAL_POINTS]

    SIG_LABELS = {
        "VH_tau1mm_M55":                      r"VH $\tau$=1mm  $M$=55  (lep)",
        "VH_tau10mm_M55":                     r"VH $\tau$=10mm $M$=55  (lep)",
        "VH_tau1mm_M40":                      r"VH $\tau$=1mm  $M$=40  (lep)",
        "VH_tau1mm_M15":                      r"VH $\tau$=1mm  $M$=15  (lep)",
        "ggHToSSTodddd_tau1mm_M55":           r"ggH $\tau$=1mm  $M$=55  (bjet)",
        "ggHToSSTodddd_tau1mm_M40":           r"ggH $\tau$=1mm  $M$=40  (bjet)",
        "mfv_stopdbardbar_tau001000um_M0200": r"stop $\tau$=1mm  $M$=200 (bjet)",
        "mfv_stopdbardbar_tau000300um_M0400": r"stop $\tau$=0.3mm $M$=400 (bjet)",
        "mfv_neu_tau001000um_M0400":          r"neu  $\tau$=1mm  $M$=400 (bjet)",
    }
    COLORS = ["royalblue","tomato","cornflowerblue","skyblue",
              "forestgreen","limegreen","darkorange","purple","saddlebrown"]

    xs = sorted(results.keys())
    # x-ticks: all fine points + every other coarse point
    tick_xs = [x for x in xs if x <= 0.10 or abs(round(x * 10) % 2) < 0.01]

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))

    for ax, sig_ids, title in [
        (axes[0], [s for s in sigs if SIG_CHANNEL[s] == "bjet"], "Bjet channel"),
        (axes[1], [s for s in sigs if SIG_CHANNEL[s] == "lep"],  "Lepton channel"),
    ]:
        for sig_id, color in zip(sig_ids, COLORS):
            lbl = SIG_LABELS.get(sig_id, sig_id)
            uls = [results.get(x, {}).get(sig_id) for x in xs]
            valid_x  = [x for x, u in zip(xs, uls) if u is not None]
            valid_ul = [u for u in uls if u is not None]
            if not valid_ul:
                continue
            ax.plot(valid_x, valid_ul, "o-", color=color, lw=1.8, ms=4,
                    label=lbl)

        ax.set_xlabel("Boundary x (cm)", fontsize=12)
        ax.set_ylabel("Exp. 95% CL UL on r", fontsize=11)
        ax.set_title(title, fontsize=12)
        ax.set_xticks(tick_xs)
        ax.set_xticklabels(["%.2f" % v for v in tick_xs], rotation=45, ha="right", fontsize=7)
        ax.legend(fontsize=8, framealpha=0.85)
        ax.grid(alpha=0.3)

    fig.suptitle(r"Expected UL vs boundary — scheme [0, $x$, 4.0] cm (2-bin)",
                 fontsize=12)
    fig.tight_layout()

    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "boundary_scan_2bin.%s" % ext)
        fig.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)


# ---- main -------------------------------------------------------------

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("gen", "all"):
        gen_all()
    if mode in ("run", "all"):
        run_all()
    if mode in ("plot", "all"):
        results = collect()
        plot(results)


if __name__ == "__main__":
    main()

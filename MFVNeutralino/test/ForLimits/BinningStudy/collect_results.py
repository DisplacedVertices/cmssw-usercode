# Usage:  python collect_results.py
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SCHEMES

try:
    import ROOT
    ROOT.gROOT.SetBatch(True)
    HAS_ROOT = True
except ImportError:
    HAS_ROOT = False

HERE     = os.path.dirname(os.path.abspath(__file__))
OUT_BASE = os.path.join(HERE, "combine_output")

SCHEMES_ORDER = list(SCHEMES.keys())
SCHEME_LABELS = {k: v["label"] for k, v in SCHEMES.items()}

SIG_LABELS = {
    "VH_tau1mm_M55":                      "VH  tau=1mm  M=55  (lep)",
    "VH_tau10mm_M55":                     "VH  tau=10mm M=55  (lep)",
    "VH_tau1mm_M40":                      "VH  tau=1mm  M=40  (lep)",
    "VH_tau1mm_M15":                      "VH  tau=1mm  M=15  (lep)",
    "ggHToSSTodddd_tau1mm_M55":           "ggH tau=1mm  M=55  (bjet)",
    "ggHToSSTodddd_tau1mm_M40":           "ggH tau=1mm  M=40  (bjet)",
    "mfv_stopdbardbar_tau001000um_M0200": "stop tau=1mm  M=200 (bjet)",
    "mfv_stopdbardbar_tau000300um_M0400": "stop tau=0.3mm M=400 (bjet)",
    "mfv_neu_tau001000um_M0400":          "neu  tau=1mm  M=400 (bjet)",
}


def read_grid_sigma_r(path):
    """Return sigma_r from MultiDimFit --algo grid output.

    Reads the NLL profile, finds the best-fit r, then interpolates the
    crossings of deltaNLL = 0.5 on each side to get the 68% CI.
    Returns the average half-width as sigma_r, or None on failure.
    """
    if not HAS_ROOT or not os.path.exists(path):
        return None
    f = ROOT.TFile.Open(path)
    if not f or f.IsZombie():
        return None
    t = f.Get("limit")
    if not t or t.GetEntries() < 3:
        f.Close()
        return None

    pts = sorted((ev.r, ev.deltaNLL) for ev in t)
    f.Close()

    best_r, best_dnll = min(pts, key=lambda x: x[1])

    # Shift so minimum is at 0
    pts = [(r, d - best_dnll) for r, d in pts]

    # Interpolate 68% crossing (deltaNLL = 0.5) on each side
    def interp_crossing(pairs):
        for i in range(len(pairs) - 1):
            r0, d0 = pairs[i]
            r1, d1 = pairs[i+1]
            if d0 <= 0.5 <= d1 and abs(d1 - d0) > 1e-10:
                return r0 + (0.5 - d0) * (r1 - r0) / (d1 - d0)
        return None

    # left side: scan outward from best_r downward
    left  = sorted([(r, d) for r, d in pts if r <= best_r], reverse=True)
    # right side: scan outward from best_r upward
    right = sorted([(r, d) for r, d in pts if r >= best_r])

    lo = interp_crossing(left)
    hi = interp_crossing(right)

    if lo is None or hi is None:
        return None
    return 0.5 * (hi - lo)


def read_asymptotic(path):
    """Return expected 95% CL UL (median quantile) or None."""
    if not HAS_ROOT or not os.path.exists(path):
        return None
    f = ROOT.TFile.Open(path)
    if not f or f.IsZombie():
        return None
    t = f.Get("limit")
    if not t:
        f.Close()
        return None
    exp = None
    for ev in t:
        if abs(ev.quantileExpected - 0.5) < 0.01:
            exp = ev.limit
            break
    f.Close()
    return exp


def collect():
    results = {}  # [scheme][sig] = {"sigma_r": ..., "exp_ul": ...}
    for scheme in SCHEMES_ORDER:
        scheme_dir = os.path.join(OUT_BASE, scheme)
        if not os.path.isdir(scheme_dir):
            continue
        results[scheme] = {}
        for sig_id in SIG_LABELS:
            sig_dir = os.path.join(scheme_dir, sig_id)
            # MultiDimFit grid scan
            grid_pat = os.path.join(sig_dir,
                "higgsCombine%s_%s.MultiDimFit.mH120.root" % (scheme, sig_id))
            sr = read_grid_sigma_r(grid_pat)
            # AsymptoticLimits
            al_pat = os.path.join(sig_dir,
                "higgsCombine%s_%s.AsymptoticLimits.mH120.root" % (scheme, sig_id))
            al = read_asymptotic(al_pat)
            results[scheme][sig_id] = {"sigma_r": sr, "al": al}
    return results


def print_table(results, metric, title):
    print("\n" + "="*80)
    print(title)
    print("="*80)

    sigs    = list(SIG_LABELS.keys())
    schemes = [s for s in SCHEMES_ORDER if s in results]

    print("%-26s" % "Scheme", end="")
    for s in sigs:
        lbl = SIG_LABELS[s].split("(")[0].strip()[:18]
        print("  %-18s" % lbl, end="")
    print()
    print("-" * (26 + 20 * len(sigs)))

    for scheme in schemes:
        print("%-26s" % SCHEME_LABELS.get(scheme, scheme), end="")
        for sig in sigs:
            d = results[scheme].get(sig, {})
            if metric == "sigma_r":
                sr = d.get("sigma_r")
                val = "%6.4f" % sr if sr is not None else "  --  "
            else:
                al = d.get("al")
                val = "%6.3f" % al if al is not None else "  --  "
            print("  %-18s" % val, end="")
        print()


def main():
    results = collect()
    if not results:
        print("No results found in %s" % OUT_BASE)
        sys.exit(1)

    print_table(results, "sigma_r",
                "sigma_r  (68% CI half-width on r, Asimov injection r=1, stat-only)")
    print_table(results, "exp_ul",
                "Expected 95% CL upper limit on r  (stat-only)")


if __name__ == "__main__":
    main()

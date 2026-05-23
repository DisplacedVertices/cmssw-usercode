"""
Cross-check: compare fast_study_datacards.py yields vs the original
3bin_nom datacards produced by the full makeLimitsInputROOT.py pipeline.

Prints a table of (original, fast, % diff) for signal and background
yields in each bin for each year / signal point.

Usage:
  source LCG dev3 setup
  python3 check_fast_vs_original.py
"""
import os, sys, re
import numpy as np

try:
    import ROOT
    ROOT.gROOT.SetBatch(True)
except ImportError:
    print("ERROR: ROOT not available"); sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SCHEMES, SIGNAL_POINTS, YEARS
from fast_study_datacards import (
    parse_ref_yield, get_bkg_yields, get_sig_files, get_sig_shape
)

HERE     = os.path.dirname(os.path.abspath(__file__))
NOM_BINS = SCHEMES["3bin_nom"]["bins"]


def parse_original_rates(sig_id, ch, year):
    """Return (sig_yields, bkg_yields) lists from original 3bin_nom stat-only card."""
    dc = os.path.join(HERE, "datacards", "3bin_nom", ch,
                      "Datacard_%s_%s_%s_statonly.txt" % (ch, sig_id, year))
    for line in open(dc):
        if line.startswith("rate"):
            vals = list(map(float, line.split()[1:]))
            n = len(vals) // 2
            return vals[:n], vals[n:]
    raise RuntimeError("No rate line in %s" % dc)


def recompute_fast(sig_id, ch, year):
    """Recompute yields the same way fast_study_datacards.py would."""
    bins      = NOM_BINS
    ref_yield = parse_ref_yield(sig_id, ch, year)
    files     = get_sig_files(sig_id, ch, year)
    shape     = get_sig_shape(files, bins)
    sig_ylds  = [s * ref_yield for s in shape]
    bkg_ylds  = get_bkg_yields(ch, year, bins)
    return sig_ylds, bkg_ylds


def pct(a, b):
    if abs(b) < 1e-12:
        return "  n/a " if abs(a) < 1e-12 else " +inf%"
    return "%+6.2f%%" % (100.0 * (a - b) / b)


print("%-42s  %-5s  %-25s  %-25s  %s" % (
    "signal / year", "bin", "original (full pipeline)", "fast (recomputed)", "diff"))
print("-" * 115)

max_sig_diff = 0.0
max_bkg_diff = 0.0

for sig_id, ch in SIGNAL_POINTS:
    for year in YEARS:
        try:
            orig_sig, orig_bkg = parse_original_rates(sig_id, ch, year)
            fast_sig, fast_bkg = recompute_fast(sig_id, ch, year)
        except Exception as e:
            print("  SKIP %s %s: %s" % (sig_id, year, e))
            continue

        label = "%s / %s" % (sig_id[-20:], year)
        for i in range(len(orig_sig)):
            d_sig = abs(fast_sig[i] - orig_sig[i]) / orig_sig[i] * 100 if orig_sig[i] > 1e-12 else 0
            d_bkg = abs(fast_bkg[i] - orig_bkg[i]) / orig_bkg[i] * 100 if orig_bkg[i] > 1e-12 else 0
            max_sig_diff = max(max_sig_diff, d_sig)
            max_bkg_diff = max(max_bkg_diff, d_bkg)
            print("%-42s  bin%d  sig: %9.4f vs %9.4f %s   bkg: %9.5f vs %9.5f %s" % (
                label if i == 0 else "", i,
                orig_sig[i], fast_sig[i], pct(fast_sig[i], orig_sig[i]),
                orig_bkg[i], fast_bkg[i], pct(fast_bkg[i], orig_bkg[i])))

print()
print("Max signal diff: %.3f%%   Max background diff: %.3f%%" % (max_sig_diff, max_bkg_diff))

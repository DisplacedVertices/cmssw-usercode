"""
Fast datacard generator for binning study schemes.

Instead of re-running makeLimitsInputROOT.py (processes all 120+ signals),
this reads only the 6 study signals:
  - Background: rebin 200-bin BackgroundTemplates histogram to new boundaries
  - Signal shape: fill histogram from MiniTree TTree (sumdbv, nvtx>=2)
  - Signal normalization: read from existing 3bin_nom stat-only datacards

Requires: PyROOT (source LCG dev3 or cmsenv with ROOT)

Usage:
  python3 fast_study_datacards.py                  # all new schemes
  python3 fast_study_datacards.py 3bin_split 3bin_412
"""
from __future__ import print_function
import os, sys, re, glob
import numpy as np

try:
    import ROOT
    ROOT.gROOT.SetBatch(True)
except ImportError:
    print("ERROR: ROOT not available. Source LCG dev3 or cmsenv.")
    sys.exit(1)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from binning_schemes import SCHEMES, SIGNAL_POINTS, YEARS

# ---------------------------------------------------------------------------
HERE    = os.path.dirname(os.path.abspath(__file__))
FORLIM  = os.path.dirname(HERE)

BKG_FILES = {
    "lep":  os.path.join(FORLIM, "BackgroundTemplates/lep/2v_from_jets_run2_5track_default_ULV30Lepm.root"),
    "bjet": os.path.join(FORLIM, "BackgroundTemplates/bjet/2v_from_jets_run2_5track_default_ULV30BvetoLHTm.root"),
}

MINI_BASE = {
    "lep":  "/uscms/home/gdecastr/nobackup/crabdirs/MiniTree_tag001Lepm_VH",
    "bjet": "/uscms/home/gdecastr/nobackup/crabdirs/MiniTree_tag001BvetoLHTm_bjet",
}

N2V = {
    "lep":  [0.001, 0.012, 0.002, 0.034],
    "bjet": [0.258, 0.062, 0.078, 0.122],
}
YEAR_IDX = {y: i for i, y in enumerate(YEARS)}

# VH: sum of 4 production modes (dddd final state only)
VH_PROCS = ["ZHToSSTodddd", "WminusHToSSTodddd", "WplusHToSSTodddd", "ggZHToSSTodddd"]

# Ref scheme to borrow signal normalization from
REF_SCHEME = "3bin_nom"


# Main Datacards/ directory (fall back for signals not yet in BinningStudy/datacards/)
MAIN_DATACARDS = os.path.join(FORLIM, "Datacards")


# ---------------------------------------------------------------------------
def parse_ref_yield(sig_id, ch, year):
    """Sum of per-bin signal rates from a reference datacard.

    Tries BinningStudy/datacards/3bin_nom first (stat-only), then falls back
    to the main ForLimits/Datacards/ directory (full systematics — only the
    rate line is read so systematics don't matter here).
    """
    candidates = [
        os.path.join(HERE, "datacards", REF_SCHEME, ch,
                     "Datacard_%s_%s_%s_statonly.txt" % (ch, sig_id, year)),
        os.path.join(MAIN_DATACARDS, ch,
                     "Datacard_%s_%s_%s.txt" % (ch, sig_id, year)),
    ]
    for dc in candidates:
        if not os.path.exists(dc):
            continue
        for line in open(dc):
            if line.startswith("rate"):
                vals = list(map(float, line.split()[1:]))
                nbins_ref = len(vals) // 2
                return sum(vals[:nbins_ref])
        raise RuntimeError("No rate line in %s" % dc)
    raise FileNotFoundError("No ref datacard found for %s/%s/%s" % (sig_id, ch, year))


def get_bkg_yields(ch, year, bins):
    """Rebin the 200-bin background histogram to `bins`, return per-bin yields."""
    f = ROOT.TFile.Open(BKG_FILES[ch])
    h200 = f.Get("h_c1v_sumdbv_w_errorbars")
    h200.SetDirectory(0)
    f.Close()
    nbins = len(bins) - 1
    arr   = np.array(bins, dtype=np.float64)
    h     = h200.Rebin(nbins, "bkg_tmp", arr)
    # last bin absorbs overflow (sumdbv > 4 is negligible but keep consistent)
    last = h.GetBinContent(nbins) + h.GetBinContent(nbins + 1)
    h.SetBinContent(nbins, last)
    total = h.Integral()
    scale = N2V[ch][YEAR_IDX[year]] / total if total > 0 else 0.0
    # floor at 1e-9 to avoid combine segfault on zero-background bins
    return [max(h.GetBinContent(i+1) * scale, 1e-9) for i in range(nbins)]


def get_sig_files(sig_id, ch, year):
    """Return list of minitree paths for this signal."""
    base = MINI_BASE[ch]
    if sig_id.startswith("VH_"):
        # Decode tau/mass from sig_id: VH_tau1mm_M55 → tau1mm, M55
        m = re.match(r"VH_(tau\S+)_(M\d+)$", sig_id)
        tau, mass = m.group(1), m.group(2)
        paths = []
        for proc in VH_PROCS:
            p = os.path.join(base, "condor_%s_%s_%s_%s" % (proc, tau, mass, year), "minitree_0.root")
            if os.path.exists(p):
                paths.append(p)
        return paths
    else:
        p = os.path.join(base, "condor_%s_%s" % (sig_id, year), "minitree_0.root")
        return [p] if os.path.exists(p) else []


def get_sig_shape(files, bins):
    """Fill sumdbv histogram (nvtx>=2) from list of ROOT files, normalize to 1."""
    nbins = len(bins) - 1
    counts = np.zeros(nbins)
    edges  = np.array(bins)
    for fn in files:
        f = ROOT.TFile(fn)
        t = f.Get("mfvMiniTree/t")
        n = t.Draw("sumdbv", "1.0*(nvtx>=2)", "goff")
        if n > 0:
            vals = np.frombuffer(t.GetV1(), dtype=np.float64, count=n).copy()
            c, _ = np.histogram(vals, bins=edges)
            counts += c
        f.Close()
    total = counts.sum()
    return counts / total if total > 0 else counts


def write_datacard(path, ch, sig_id, year, sig_yields, bkg_yields):
    nbins = len(sig_yields)
    yr_tag = {"20161": "2016pre", "20162": "2016post", "2017": "2017", "2018": "2018"}.get(year, year)
    bin_names    = " ".join("b%s%d" % (year, i) for i in range(nbins))
    sig_proc     = "sig%s" % year
    bkg_proc     = "bkg%s" % yr_tag

    sig_rate = " ".join("%.10g" % v for v in sig_yields)
    bkg_rate = " ".join("%.10g" % v for v in bkg_yields)

    obs_line = " ".join("0" for _ in range(nbins))

    with open(path, "w") as fh:
        fh.write("imax %d\n" % nbins)
        fh.write("jmax 1\n")
        fh.write("kmax 0  number of nuisance parameters\n")
        fh.write("________\n")
        fh.write("bin             %s\n" % bin_names)
        fh.write("observation       %s\n" % obs_line)
        fh.write("________\n")
        fh.write("bin             %s            %s\n" % (bin_names, bin_names))
        fh.write("process       %s           %s\n" % (
            "  ".join([sig_proc] * nbins),
            "  ".join([bkg_proc] * nbins)))
        fh.write("process           %s              %s\n" % (
            "  ".join(["0"] * nbins),
            "  ".join(["1"] * nbins)))
        fh.write("rate         %s         %s\n" % (sig_rate, bkg_rate))


def run_scheme(scheme_name, scheme_info):
    is_split = "lep_bins" in scheme_info

    for sig_id, ch in SIGNAL_POINTS:
        if is_split:
            bins = scheme_info["%s_bins" % ch]
        else:
            bins = scheme_info["bins"]
        nbins = len(bins) - 1

        dc_dir = os.path.join(HERE, "datacards", scheme_name, ch)
        if not os.path.exists(dc_dir):
            os.makedirs(dc_dir)

        for year in YEARS:
            dc_path = os.path.join(dc_dir, "Datacard_%s_%s_%s_statonly.txt" % (ch, sig_id, year))

            try:
                ref_yield = parse_ref_yield(sig_id, ch, year)
            except (FileNotFoundError, RuntimeError) as e:
                print("  SKIP %s/%s/%s: %s" % (scheme_name, sig_id, year, e))
                continue

            files = get_sig_files(sig_id, ch, year)
            if not files:
                print("  SKIP %s/%s/%s: no MiniTree files" % (scheme_name, sig_id, year))
                continue

            shape    = get_sig_shape(files, bins)
            sig_ylds = [s * ref_yield for s in shape]
            bkg_ylds = get_bkg_yields(ch, year, bins)

            write_datacard(dc_path, ch, sig_id, year, sig_ylds, bkg_ylds)
            print("  wrote %s" % os.path.relpath(dc_path, HERE))


def main():
    schemes_to_run = sys.argv[1:] if len(sys.argv) > 1 else sorted(SCHEMES.keys())
    for name in schemes_to_run:
        if name not in SCHEMES:
            print("Unknown scheme:", name)
            continue
        print("\n=== Scheme:", name, "===")
        run_scheme(name, SCHEMES[name])
    print("\nDone.")


if __name__ == "__main__":
    main()

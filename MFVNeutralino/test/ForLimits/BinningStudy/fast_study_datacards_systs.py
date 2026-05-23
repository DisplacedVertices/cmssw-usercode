"""
Generate with-systematics datacards for a subset of binning schemes,
by porting nuisances from the original 3bin_nom full-pipeline cards.

Supports schemes: 3bin_nom, 3bin_v1, 3bin_412 (add others as needed).

Nuisance porting rules:
  lnN uniform (lumi, vtx_reco, calo_ineff, disp_trig): copy as-is, repeat for new nbins.
  lnN bin-dependent (pileup, tk_reco_eff): assign original bin whose range most
    overlaps the new bin (conservative approximation — these are small systematics).
  gmN (signal MC stats): recompute N from unweighted TTree counts per new bin;
    coefficient = ref_yield / total_MC_count (constant across bins).

Usage:
  source LCG dev3 or cmsenv
  python3 fast_study_datacards_systs.py              # all three schemes
  python3 fast_study_datacards_systs.py 3bin_nom     # single scheme
"""
from __future__ import print_function
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
    get_bkg_yields, get_sig_files, parse_ref_yield, YEAR_IDX
)

HERE      = os.path.dirname(os.path.abspath(__file__))
FORLIM    = os.path.dirname(HERE)
ORIG_DC   = os.path.join(FORLIM, "Datacards")   # full-syst nominal cards
NOM_BINS  = SCHEMES["3bin_nom"]["bins"]

SCHEMES_WITH_SYSTS = ["3bin_nom", "3bin_v1", "3bin_412"]


# ---------------------------------------------------------------------------

def get_sig_counts(files, bins):
    """Return (counts_per_bin, total) — unweighted, for gmN computation."""
    nbins  = len(bins) - 1
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
    return counts, counts.sum()


def _orig_bin_for(new_lo, new_hi, orig_bins):
    """Return the index of the original bin that most overlaps [new_lo, new_hi]."""
    best_k, best_overlap = 0, 0.0
    for k in range(len(orig_bins) - 1):
        lo_k, hi_k = orig_bins[k], orig_bins[k + 1]
        overlap = max(0.0, min(new_hi, hi_k) - max(new_lo, lo_k))
        if overlap > best_overlap:
            best_overlap, best_k = overlap, k
    return best_k


def parse_original_nuisances(dc_path):
    """Parse a full-syst datacard, return (nbins, nuisance_lines_raw)."""
    nbins = None
    nuisance_lines = []
    for line in open(dc_path):
        line = line.rstrip()
        if line.startswith("imax"):
            nbins = int(line.split()[1])
        if (line.startswith("CMS_") or line.startswith("lumi_")) and len(line) > 5:
            nuisance_lines.append(line)
    return nbins, nuisance_lines


def port_nuisances(nuisance_lines, orig_nbins, orig_bins, new_nbins, new_bins,
                   new_sig_counts, total_mc, ref_yield):
    """
    Convert original nuisance lines to new binning.
    Returns list of (name, type, sig_vals_list, bkg_dashes_list, extra)
    where extra = gmN_N for gmN, None for lnN.
    """
    ported = []
    for line in nuisance_lines:
        parts = line.split()
        if len(parts) < 2 + 2 * orig_nbins:
            continue
        name  = parts[0]
        ntype = parts[1]

        if ntype == "lnN":
            sig_orig = parts[2 : 2 + orig_nbins]
            # check if any value is not '-'
            active = [v for v in sig_orig if v != "-"]
            if not active:
                continue

            # check if uniform
            uniform = len(set(active)) == 1

            new_sig_vals = []
            for j in range(new_nbins):
                if uniform:
                    new_sig_vals.append(active[0])
                else:
                    k = _orig_bin_for(new_bins[j], new_bins[j + 1], orig_bins)
                    new_sig_vals.append(sig_orig[k])

            ported.append((name, "lnN", new_sig_vals, None))

        elif ntype == "gmN":
            # original gmN: one nuisance controls one bin
            # find which original bin is controlled
            coeffs = parts[3 : 3 + orig_nbins]
            try:
                active_orig_bin = next(i for i, c in enumerate(coeffs) if c != "-")
            except StopIteration:
                continue

            # Emit one gmN nuisance per new bin
            coeff = ref_yield / total_mc if total_mc > 0 else 0.0
            for j in range(new_nbins):
                n_j   = int(new_sig_counts[j])
                nname = re.sub(r"b\d+$", "nb%d" % j, name)
                ported.append((nname, "gmN", j, n_j, coeff))

    # deduplicate gmN entries (we'll get one set per original gmN line; keep first)
    seen_gmN = set()
    deduped  = []
    for entry in ported:
        if entry[1] == "gmN":
            key = entry[2]   # new bin index
            if key in seen_gmN:
                continue
            seen_gmN.add(key)
        deduped.append(entry)
    return deduped


def write_datacard_with_systs(path, ch, sig_id, year, sig_yields, bkg_yields,
                               new_bins, nuisances):
    nbins   = len(sig_yields)
    yr_tag  = {"20161":"2016pre","20162":"2016post","2017":"2017","2018":"2018"}.get(year,year)
    bin_names = " ".join("b%s%d" % (year, i) for i in range(nbins))
    sig_proc  = "sig%s" % year
    bkg_proc  = "bkg%s" % yr_tag
    obs       = " ".join("0" for _ in range(nbins))
    sig_rate  = " ".join("%.10g" % v for v in sig_yields)
    bkg_rate  = " ".join("%.10g" % max(v, 1e-9) for v in bkg_yields)

    kmax = len([e for e in nuisances if e[1] == "lnN"]) + nbins  # lnN + gmN per bin

    with open(path, "w") as fh:
        fh.write("imax %d\n" % nbins)
        fh.write("jmax 1\n")
        fh.write("kmax %d\n" % kmax)
        fh.write("________\n")
        fh.write("bin             %s\n" % bin_names)
        fh.write("observation       %s\n" % obs)
        fh.write("________\n")
        fh.write("bin             %s            %s\n" % (bin_names, bin_names))
        fh.write("process       %s           %s\n" % (
            "  ".join([sig_proc] * nbins), "  ".join([bkg_proc] * nbins)))
        fh.write("process           %s              %s\n" % (
            "  ".join(["0"] * nbins), "  ".join(["1"] * nbins)))
        fh.write("rate         %s         %s\n" % (sig_rate, bkg_rate))
        fh.write("________\n\n")

        gmN_written = set()
        for entry in nuisances:
            if entry[1] == "lnN":
                name, _, sig_vals, _ = entry
                dashes = "  ".join(["-"] * nbins)
                fh.write("%-50s lnN   %s              %s\n" % (
                    name, "  ".join(sig_vals), dashes))
            elif entry[1] == "gmN":
                name, _, j, N_j, coeff = entry
                if j in gmN_written:
                    continue
                gmN_written.add(j)
                sig_cols = ["  -"] * nbins
                sig_cols[j] = " %.10g" % coeff
                bkg_cols = ["-"] * nbins
                fh.write("%-50s gmN %d   %s              %s\n" % (
                    name, N_j, "  ".join(sig_cols), "  ".join(bkg_cols)))


def run_scheme_systs(scheme_name, bins):
    nbins    = len(bins) - 1
    orig_bins = NOM_BINS

    for sig_id, ch in SIGNAL_POINTS:
        dc_dir = os.path.join(HERE, "datacards_systs", scheme_name, ch)
        os.makedirs(dc_dir, exist_ok=True)

        for year in YEARS:
            dc_path = os.path.join(dc_dir,
                "Datacard_%s_%s_%s_withsysts.txt" % (ch, sig_id, year))

            orig_dc = os.path.join(ORIG_DC, ch,
                "Datacard_%s_%s_%s.txt" % (ch, sig_id, year))
            if not os.path.exists(orig_dc):
                print("  SKIP (no orig card): %s/%s/%s" % (scheme_name, sig_id, year))
                continue

            try:
                ref_yield = parse_ref_yield(sig_id, ch, year)
            except Exception as e:
                print("  SKIP: %s" % e)
                continue

            files = get_sig_files(sig_id, ch, year)
            if not files:
                print("  SKIP (no MiniTree): %s/%s/%s" % (scheme_name, sig_id, year))
                continue

            sig_counts, total_mc = get_sig_counts(files, bins)
            shape     = sig_counts / total_mc if total_mc > 0 else sig_counts
            sig_ylds  = [float(s * ref_yield) for s in shape]
            bkg_ylds  = get_bkg_yields(ch, year, bins)

            orig_nbins, nuis_lines = parse_original_nuisances(orig_dc)
            nuisances = port_nuisances(
                nuis_lines, orig_nbins, orig_bins, nbins, bins,
                sig_counts, total_mc, ref_yield)

            write_datacard_with_systs(
                dc_path, ch, sig_id, year, sig_ylds, bkg_ylds, bins, nuisances)
            print("  wrote %s" % os.path.relpath(dc_path, HERE))


def main():
    targets = sys.argv[1:] if len(sys.argv) > 1 else SCHEMES_WITH_SYSTS
    for name in targets:
        if name not in SCHEMES:
            print("Unknown scheme:", name); continue
        print("\n=== Scheme:", name, "===")
        run_scheme_systs(name, SCHEMES[name]["bins"])
    print("\nDone.")


if __name__ == "__main__":
    main()

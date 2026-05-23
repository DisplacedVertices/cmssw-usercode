"""
HybridNew scheme comparison + validation.

Produces two plots:
  1. hybridnew_schemes.pdf  — same format as scheme_comparison.pdf but HybridNew limits
                              (all 18 named schemes, 9 signals)
  2. hybridnew_validation.pdf — HybridNew vs Asymptotic side-by-side for 5 key schemes

Uses the same condor pattern as submitCombine.py:
  - text2workspace.py run on submit node (needs cmsenv)
  - combine binary shipped via combine_env.tar.gz
  - CMSSW 14.1.0 from CVMFS on worker

Usage:
  source cmsenv first, then:
  python3 hybridnew_validation.py submit   # build workspaces + submit condor jobs
  python3 hybridnew_validation.py check    # count finished jobs
  python3 hybridnew_validation.py collect  # make plots (needs LCG dev3)
"""
import os, sys, subprocess, glob
import numpy as np

HERE    = os.path.dirname(os.path.abspath(__file__))
OUTBASE = os.path.join(HERE, "combine_output")
CONDDIR = os.path.join(HERE, "condor_hybridnew")

COMBINE_TARBALL = os.environ.get(
    "COMBINE_TARBALL",
    "/uscms_data/d3/gdecastr/work/combine_env.tar.gz",
)
CVMFS_CMSSW14 = "/cvmfs/cms.cern.ch/el9_amd64_gcc12/cms/cmssw/CMSSW_14_1_0/src"

NTOYS = 20000  # --fork 2 → 20000 effective toys, ~3x noise reduction vs 2000
SEED  = 1234   # fixed seed → predictable output filename

# All 18 named comparison schemes (same order as scheme_comparison.pdf)
ALL_SCHEMES = [
    "old_binning", "2bin", "3bin_nom", "3bin_v1", "3bin_v2", "3bin_v3", "3bin_v4",
    "4bin_v1", "4bin_v2", "3bin_412",
    "4bin_412_25", "3bin_420", "4bin_nom_30", "4bin_516_30", "3bin_520",
    "3bin_104", "4bin_104_200", "4bin_104_250",
]

# 5 key schemes for the HybridNew vs Asymptotic validation plot
VALIDATION_SCHEMES = ["2bin", "old_binning", "3bin_nom", "3bin_104", "4bin_104_200"]

SHORT_LABELS = {
    "old_binning":   "[0,.08,.16,4]",
    "2bin":          "[0,1.6,4]",
    "3bin_nom":      "[0,.8,1.6,4]",
    "3bin_v1":       "[0,.4,1.6,4]",
    "3bin_v2":       "[0,.8,2.5,4]",
    "3bin_v3":       "[0,1,2,4]",
    "3bin_v4":       "[0,.5,1,4]",
    "4bin_v1":       "[0,.4,.8,\n1.6,4]",
    "4bin_v2":       "[0,.8,1.2,\n1.6,4]",
    "3bin_412":      "[0,.4,1.2,4]",
    "4bin_412_25":   "[0,.4,1.2,\n2.5,4]",
    "3bin_420":      "[0,.4,2,4]",
    "4bin_nom_30":   "[0,.8,1.6,\n3,4]",
    "4bin_516_30":   "[0,.5,1.6,\n3,4]",
    "3bin_520":      "[0,.5,2,4]",
    "3bin_104":      "[0,.1,.4,4]",
    "4bin_104_200":  "[0,.1,.4,\n2,4]",
    "4bin_104_250":  "[0,.1,.4,\n2.5,4]",
}

SIG_SHORT = {
    "VH_tau1mm_M55":                     "VH  τ=1mm  M=55  (lep)",
    "VH_tau10mm_M55":                    "VH  τ=10mm M=55  (lep)",
    "VH_tau1mm_M40":                     "VH  τ=1mm  M=40  (lep)",
    "VH_tau1mm_M15":                     "VH  τ=1mm  M=15  (lep)",
    "ggHToSSTodddd_tau1mm_M55":          "ggH τ=1mm  M=55  (bjet)",
    "ggHToSSTodddd_tau1mm_M40":          "ggH τ=1mm  M=40  (bjet)",
    "mfv_stopdbardbar_tau001000um_M0200": "stop τ=1mm  M=200 (bjet)",
    "mfv_stopdbardbar_tau000300um_M0400": "stop τ=0.3mm M=400 (bjet)",
    "mfv_neu_tau001000um_M0400":          "neu  τ=1mm  M=400 (bjet)",
}

# Color scheme matching scheme_comparison.pdf
NOM_COLOR = "#222222"
NBINS_COLOR = {2: "#88CCEE", 3: "#DDCC77", 4: "#CC6677"}
NBINS = {
    "old_binning": 3, "2bin": 2, "3bin_nom": 3, "3bin_v1": 3, "3bin_v2": 3,
    "3bin_v3": 3, "3bin_v4": 3, "4bin_v1": 4, "4bin_v2": 4, "3bin_412": 3,
    "4bin_412_25": 4, "3bin_420": 3, "4bin_nom_30": 4, "4bin_516_30": 4,
    "3bin_520": 3, "3bin_104": 3, "4bin_104_200": 4, "4bin_104_250": 4,
}

def scheme_color(s):
    if s == "3bin_nom":
        return NOM_COLOR
    return NBINS_COLOR.get(NBINS.get(s, 3), "#999999")


def get_jobs(schemes=None):
    """Return list of (scheme, sig_id, datacard_path)."""
    if schemes is None:
        schemes = ALL_SCHEMES
    jobs = []
    for scheme in schemes:
        scheme_dir = os.path.join(OUTBASE, scheme)
        if not os.path.isdir(scheme_dir):
            continue
        for sig_dir in sorted(os.listdir(scheme_dir)):
            dc = os.path.join(scheme_dir, sig_dir, "combined_%s.txt" % sig_dir)
            if os.path.exists(dc):
                jobs.append((scheme, sig_dir, dc))
    return jobs


def hybridnew_outfile(tag):
    return "higgsCombine%s.HybridNew.mH120.%d.root" % (tag, SEED)


def submit():
    import shutil
    os.makedirs(CONDDIR, exist_ok=True)

    if not os.path.exists(COMBINE_TARBALL):
        print("ERROR: combine tarball not found: %s" % COMBINE_TARBALL)
        sys.exit(1)
    if not shutil.which("text2workspace.py"):
        print("ERROR: text2workspace.py not in PATH — source cmsenv first")
        sys.exit(1)

    jobs = get_jobs()
    print("Found %d jobs across %d schemes" % (len(jobs), len(ALL_SCHEMES)))

    n_submitted = 0
    n_skipped = 0
    for scheme, sig_id, dc_path in jobs:
        tag      = "%s_%s" % (scheme, sig_id)
        work_dir = os.path.dirname(dc_path)
        out_root = os.path.join(work_dir, hybridnew_outfile(tag))

        # Skip if output already exists
        if os.path.exists(out_root):
            n_skipped += 1
            continue

        job_dir = os.path.join(CONDDIR, tag)
        os.makedirs(job_dir, exist_ok=True)

        # Pre-convert datacard to workspace on submit node
        ws = os.path.join(work_dir, "workspace_%s.root" % tag)
        if not os.path.exists(ws):
            ret = subprocess.call(
                "text2workspace.py %s -m 125 -o %s" % (dc_path, ws), shell=True)
            if ret != 0:
                print("WARNING: text2workspace.py failed for %s -- skipping" % tag)
                continue

        sh = os.path.join(job_dir, "run.sh")
        with open(sh, "w") as f:
            f.write("#!/bin/bash\nset -e\n")
            f.write("source /cvmfs/cms.cern.ch/cmsset_default.sh\n")
            f.write("cd %s\n" % CVMFS_CMSSW14)
            f.write("eval $(scramv1 runtime -sh)\n")
            f.write("cd /srv\n")
            f.write("tar xf combine_env.tar.gz\n")
            f.write("export PATH=/srv/combine_env/bin:$PATH\n")
            f.write("export LD_LIBRARY_PATH=/srv/combine_env/lib:$LD_LIBRARY_PATH\n")
            f.write("echo '=== HybridNew: %s ==='\n" % tag)
            f.write("combine -M HybridNew --frequentist --testStat LHC \\\n")
            f.write("  -T %d --fork 2 -t -1 -s %d \\\n" % (NTOYS, SEED))
            f.write("  --name %s \\\n" % tag)
            f.write("  workspace_%s.root -v 0\n" % tag)
            f.write("echo '=== Done: %s ==='\n" % tag)
        os.chmod(sh, 0o755)

        jdl = os.path.join(job_dir, "submit.jdl")
        with open(jdl, "w") as f:
            f.write("universe                = vanilla\n")
            f.write("executable              = %s\n" % sh)
            f.write("initialdir              = %s\n" % work_dir)
            f.write("output                  = %s/job.out\n" % job_dir)
            f.write("error                   = %s/job.err\n" % job_dir)
            f.write("log                     = %s/job.log\n" % job_dir)
            f.write("request_cpus            = 2\n")
            f.write("request_memory          = 3000MB\n")
            f.write('+DesiredOS              = "EL9"\n')
            f.write("should_transfer_files   = YES\n")
            f.write("when_to_transfer_output = ON_EXIT\n")
            f.write("transfer_input_files    = %s,%s\n" % (COMBINE_TARBALL, ws))
            f.write("transfer_output_files   = %s\n" % hybridnew_outfile(tag))
            f.write("queue 1\n")

        ret = subprocess.call("condor_submit " + jdl, shell=True)
        if ret == 0:
            n_submitted += 1
        else:
            print("WARNING: condor_submit failed for %s" % tag)

    print("\n%d submitted, %d already done (skipped)" % (n_submitted, n_skipped))


def check():
    subprocess.call("condor_q", shell=True)
    jobs = get_jobs()
    done, missing = 0, []
    for scheme, sig_id, dc_path in jobs:
        tag  = "%s_%s" % (scheme, sig_id)
        root = os.path.join(os.path.dirname(dc_path), hybridnew_outfile(tag))
        if os.path.exists(root):
            done += 1
        else:
            missing.append("%s/%s" % (scheme, sig_id))
    print("\n%d / %d jobs have output" % (done, len(jobs)))
    if missing:
        print("Missing:", missing[:10], "..." if len(missing) > 10 else "")


def read_hybridnew(scheme, sig_id, dc_path):
    """Read HybridNew expected limit. Returns float or None."""
    import ROOT
    tag  = "%s_%s" % (scheme, sig_id)
    root = os.path.join(os.path.dirname(dc_path), hybridnew_outfile(tag))
    if not os.path.exists(root):
        files = glob.glob(os.path.join(os.path.dirname(dc_path),
                          "higgsCombine%s.HybridNew.mH120.*.root" % tag))
        if not files:
            return None
        root = files[0]
    f = ROOT.TFile(root)
    t = f.Get("limit")
    if not t or t.GetEntries() == 0:
        f.Close()
        return None
    t.GetEntry(0)
    val = float(t.limit)
    f.Close()
    return val


def read_asymptotic(scheme, sig_id, dc_path):
    """Read Asymptotic median expected limit. Returns float or None."""
    import ROOT
    root = os.path.join(os.path.dirname(dc_path),
                        "higgsCombine%s_%s.AsymptoticLimits.mH120.root" % (scheme, sig_id))
    if not os.path.exists(root):
        return None
    f = ROOT.TFile(root)
    t = f.Get("limit")
    if not t:
        f.Close()
        return None
    for _ in t:
        if abs(t.quantileExpected - 0.5) < 0.01:
            val = float(t.limit)
            f.Close()
            return val
    f.Close()
    return None


def collect():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    try:
        import ROOT
        ROOT.gROOT.SetBatch(True)
        ROOT.gErrorIgnoreLevel = ROOT.kError
    except ImportError:
        print("ERROR: ROOT not available"); sys.exit(1)

    jobs     = get_jobs()
    all_jobs = get_jobs(ALL_SCHEMES)
    sig_ids  = sorted(set(s for _, s, _ in all_jobs))

    # Build lookup: scheme -> sig_id -> (hyb, asy)
    data = {s: {} for s in ALL_SCHEMES}
    for scheme, sig_id, dc_path in all_jobs:
        h = read_hybridnew(scheme, sig_id, dc_path)
        a = read_asymptotic(scheme, sig_id, dc_path)
        data[scheme][sig_id] = (h, a)
        if h is not None and a is not None:
            print("  %-20s %-40s  Asymp=%.3f  HybNew=%.3f  ratio=%.3f" % (
                scheme, sig_id, a, h, h/a))

    # ------------------------------------------------------------------ #
    # Plot 1: HybridNew scheme comparison — same style as scheme_comparison.pdf
    # ------------------------------------------------------------------ #
    schemes_present = [s for s in ALL_SCHEMES
                       if any(data[s].get(si, (None,))[0] is not None for si in sig_ids)]
    xs = np.arange(len(schemes_present))
    colors = [scheme_color(s) for s in schemes_present]

    fig1, axes1 = plt.subplots(3, 3, figsize=(18, 13))
    axes1 = axes1.flatten()

    for ax, sig_id in zip(axes1, sig_ids):
        nom_val = data.get("3bin_nom", {}).get(sig_id, (None,))[0]
        for i, (s, c) in enumerate(zip(schemes_present, colors)):
            v = data[s].get(sig_id, (None,))[0]
            if v is None:
                continue
            ax.bar(i, v, color=c, alpha=0.90, width=0.75,
                   linewidth=1.5 if s == "3bin_nom" else 0.5,
                   edgecolor="black")
        if nom_val is not None:
            ax.axhline(nom_val, color="black", linestyle="--", linewidth=1.0, alpha=0.6)

        ax.set_title(SIG_SHORT.get(sig_id, sig_id), fontsize=10)
        ax.set_ylabel("Exp. 95% CL UL on r", fontsize=8)
        ax.set_xticks(xs)
        ax.set_xticklabels([SHORT_LABELS.get(s, s) for s in schemes_present],
                           fontsize=6.5, rotation=30, ha="right")
        ax.yaxis.set_tick_params(labelsize=8)
        vals = [data[s].get(sig_id, (None,))[0] for s in schemes_present]
        vals = [v for v in vals if v is not None]
        if vals:
            ax.set_ylim(min(vals) * 0.88, max(vals) * 1.12)
        ax.grid(axis="y", alpha=0.3)

    legend_handles = [
        mpatches.Patch(color=NOM_COLOR,  label="Nominal [0,0.8,1.6,4]"),
        mpatches.Patch(color="#88CCEE",  label="2-bin"),
        mpatches.Patch(color="#DDCC77",  label="3-bin alternatives"),
        mpatches.Patch(color="#CC6677",  label="4-bin alternatives"),
    ]
    fig1.legend(handles=legend_handles, loc="upper center", ncol=4,
                fontsize=9, bbox_to_anchor=(0.5, 1.01))
    fig1.suptitle("Expected 95%% CL UL on r — HybridNew scheme comparison (frequentist, T=%d\xd72, Asimov)" % NTOYS,
                  fontsize=11, y=1.04)
    fig1.tight_layout()
    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "hybridnew_schemes.%s" % ext)
        fig1.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)
    plt.close(fig1)

    # ------------------------------------------------------------------ #
    # Plot 2: HybridNew vs Asymptotic for 5 key validation schemes        #
    # ------------------------------------------------------------------ #
    val_schemes_present = [s for s in VALIDATION_SCHEMES
                           if any(data[s].get(si, (None,))[0] is not None for si in sig_ids)]
    val_xs = np.arange(len(val_schemes_present))

    fig2, axes2 = plt.subplots(3, 3, figsize=(16, 12))
    axes2 = axes2.flatten()

    for ax, sig_id in zip(axes2, sig_ids):
        asy_vals = [data[s].get(sig_id, (None, None))[1] for s in val_schemes_present]
        hyb_vals = [data[s].get(sig_id, (None, None))[0] for s in val_schemes_present]

        for i, (a, h) in enumerate(zip(asy_vals, hyb_vals)):
            if a is not None:
                ax.bar(i - 0.2, a, 0.35, color="#4477AA", alpha=0.8,
                       label="Asymptotic" if i == 0 else "")
            if h is not None:
                ax.bar(i + 0.2, h, 0.35, color="#EE6677", alpha=0.8,
                       label="HybridNew" if i == 0 else "")

        ax.set_title(SIG_SHORT.get(sig_id, sig_id), fontsize=9)
        ax.set_ylabel("Exp. 95% CL UL on r", fontsize=8)
        ax.set_xticks(val_xs)
        ax.set_xticklabels([SHORT_LABELS.get(s, s) for s in val_schemes_present],
                           fontsize=8, rotation=15, ha="right")
        ax.legend(fontsize=7)
        ax.grid(axis="y", alpha=0.3)

    fig2.suptitle("AsymptoticLimits vs HybridNew (-t -1, T=%d\xd72) — key schemes" % NTOYS,
                  fontsize=11)
    fig2.tight_layout()
    for ext in ("pdf", "png"):
        out = os.path.join(HERE, "hybridnew_validation.%s" % ext)
        fig2.savefig(out, bbox_inches="tight", dpi=150)
        print("Saved:", out)
    plt.close(fig2)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "submit":
        submit()
    elif cmd == "collect":
        collect()
    elif cmd == "check":
        check()
    else:
        print(__doc__)

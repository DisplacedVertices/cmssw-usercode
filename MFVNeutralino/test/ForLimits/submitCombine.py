#!/usr/bin/env python
"""
Discover all signal datacards under ForLimits/Datacards/, group them by
(proc, ctau, mass), and submit one Condor job per hypothesis that:
  1. combineCards.py -- merges per-year/per-channel cards into one Run-2 card
  2. combine -M AsymptoticLimits -- 95% CL expected/observed limits
  3. combine -M FitDiagnostics   -- best-fit signal strength + s+b shapes

Prerequisites
  - makeLimitsInputROOT.py must have been run for all years + channels so that
    Datacards/{lep,bjet}/Datacard_*.txt files exist.
  - CMSSW_14_1_0_pre4 + Combine must be installed.  Set CMSSW_14_BASE below.
    To install from scratch (run outside apptainer, on LPC EL9 node):
        cmsrel CMSSW_14_1_0_pre4
        cd CMSSW_14_1_0_pre4/src && cmsenv
        git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
        scram b -j8

Usage
  python submitCombine.py                       # all signals
  python submitCombine.py --subset VH,mfv_neu  # selected processes
  python submitCombine.py --dry-run             # list jobs without submitting
"""
import os
import sys
import glob
import stat
import argparse
import subprocess

# =============================================================================
# --- SET THIS AFTER INSTALLING CMSSW_14_1_0_pre4 ----------------------------
CMSSW_14_BASE = "/uscms/home/gdecastr/nobackup/work/CMSSW_14_1_0_pre4"
# =============================================================================

HERE         = os.path.dirname(os.path.abspath(__file__))
DATACARD_DIR = os.path.join(HERE, "Datacards")
COMBINE_OUT  = os.path.join(HERE, "CombineOutput")
CONDOR_DIR   = os.path.join(HERE, "CombineCondor")

YEARS    = ("20161", "20162", "2017", "2018")
CHANNELS = ("lep", "bjet")

# ---------------------------------------------------------------------------
# Per-job shell script
# ---------------------------------------------------------------------------
_JOB_SH = """\
#!/bin/bash
set -e
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {cmssw_src}
eval $(scramv1 runtime -sh)
mkdir -p {work_dir}
cd {work_dir}

echo "=== combineCards: {sig_id} ==="
combineCards.py {card_args} > combined_{sig_id}.txt

echo "=== AsymptoticLimits ==="
combine -M AsymptoticLimits \\
    --name {sig_id} \\
    combined_{sig_id}.txt \\
    -v 1

echo "=== FitDiagnostics ==="
combine -M FitDiagnostics \\
    --name {sig_id} \\
    combined_{sig_id}.txt \\
    --saveShapes --saveWithUncertainties \\
    -v 1

echo "=== Done: {sig_id} ==="
"""

# ---------------------------------------------------------------------------
# Condor JDL
# ---------------------------------------------------------------------------
_JDL = """\
universe                = vanilla
executable              = {job_sh}
output                  = {log_pfx}.out
error                   = {log_pfx}.err
log                     = {log_pfx}.log
request_cpus            = 1
request_memory          = 2000MB
+DesiredOS              = "EL9"
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_output_files   = ""
queue 1
"""


def _makedirs(path):
    if not os.path.exists(path):
        os.makedirs(path)


def find_hypotheses():
    """Return {sig_base: {ch_year: card_path}} for every available datacard.

    sig_base = "<proc>_tau<ctau>_M<mass>"  (no year suffix).
    ch_year  = "lep_2018", "bjet_20161", etc.
    """
    hyps = {}
    for ch in CHANNELS:
        ch_dir = os.path.join(DATACARD_DIR, ch)
        if not os.path.isdir(ch_dir):
            continue
        prefix = "Datacard_%s_" % ch
        for fn in sorted(glob.glob(os.path.join(ch_dir, prefix + "*.txt"))):
            bn   = os.path.basename(fn).replace(".txt", "")
            rest = bn[len(prefix):]          # "VH_tau1mm_M15_2018"
            parts = rest.rsplit("_", 1)
            if len(parts) != 2:
                continue
            sig_base, year = parts
            if year not in YEARS:
                continue
            hyps.setdefault(sig_base, {})
            hyps[sig_base]["%s_%s" % (ch, year)] = fn
    return hyps


def _write_job(sig_id, cards, dry_run):
    work_dir   = os.path.join(COMBINE_OUT, sig_id)
    condor_dir = os.path.join(CONDOR_DIR,  sig_id)
    _makedirs(work_dir)
    _makedirs(condor_dir)

    card_args  = " ".join("%s=%s" % (k, v) for k, v in sorted(cards.items()))
    cmssw_src  = os.path.join(CMSSW_14_BASE, "src")

    job_sh = os.path.join(condor_dir, "run.sh")
    with open(job_sh, "w") as fh:
        fh.write(_JOB_SH.format(
            cmssw_src = cmssw_src,
            work_dir  = work_dir,
            card_args = card_args,
            sig_id    = sig_id,
        ))
    os.chmod(job_sh, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    log_pfx = os.path.join(condor_dir, "job")
    jdl_fn  = os.path.join(condor_dir, "submit.jdl")
    with open(jdl_fn, "w") as fh:
        fh.write(_JDL.format(job_sh=job_sh, log_pfx=log_pfx))

    if not dry_run:
        ret = subprocess.call("condor_submit " + jdl_fn, shell=True)
        if ret != 0:
            print("WARNING: condor_submit returned %d for %s" % (ret, sig_id))
    else:
        print("  [dry-run] %s  (%d cards: %s)" % (sig_id, len(cards), ", ".join(sorted(cards))))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--subset",  default=None,
                    help="Comma-separated process names to include, e.g. VH,mfv_neu")
    ap.add_argument("--dry-run", action="store_true",
                    help="Write job files but do not call condor_submit")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Skip hypotheses that already have AsymptoticLimits output")
    args = ap.parse_args()

    if "CHANGEME" in CMSSW_14_BASE and not args.dry_run:
        print("ERROR: set CMSSW_14_BASE in submitCombine.py before submitting.")
        sys.exit(1)

    subset = set(args.subset.split(",")) if args.subset else None
    hyps   = find_hypotheses()

    if not hyps:
        print("No datacards found under %s" % DATACARD_DIR)
        sys.exit(1)

    n = 0
    n_skip = 0
    for sig_id in sorted(hyps):
        proc = sig_id.split("_tau")[0]
        if subset and proc not in subset:
            continue
        if args.skip_existing:
            out_fn = os.path.join(COMBINE_OUT, sig_id,
                                  "higgsCombine%s.AsymptoticLimits.mH120.root" % sig_id)
            if os.path.exists(out_fn):
                n_skip += 1
                continue
        _write_job(sig_id, hyps[sig_id], args.dry_run)
        n += 1

    if n_skip:
        print("Skipped %d already-completed hypotheses (--skip-existing)" % n_skip)

    status = "queued (dry-run, job files written)" if args.dry_run else "submitted to Condor"
    print("\n%d hypotheses %s" % (n, status))


if __name__ == "__main__":
    main()

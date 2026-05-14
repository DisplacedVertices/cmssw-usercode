#!/usr/bin/env python
"""
Discover all signal datacards under ForLimits/Datacards/, group them by
(proc, ctau, mass), and submit one Condor job per hypothesis that runs:
  1. combine -M AsymptoticLimits -- 95% CL expected/observed limits
  2. combine -M FitDiagnostics   -- best-fit signal strength + s+b shapes

Cards are merged locally by combineCards.py before submission (requires the
CMSSW_14_1_0_pre4 environment to be active when running this script).
The combine binary and libHiggsAnalysisCombinedLimit.so are shipped via
transfer_input_files so worker nodes do not need /uscms/home or /uscms_data.

Prerequisites
  - makeLimitsInputROOT.py must have been run for all years + channels so that
    Datacards/{lep,bjet}/Datacard_*.txt files exist.
  - Run this script with CMSSW_14_1_0_pre4 + Combine sourced (cmsenv).
    combineCards.py and the combine binary must be in PATH.
    To install from scratch (on LPC EL9 node, outside apptainer):
        cmsrel CMSSW_14_1_0_pre4
        cd CMSSW_14_1_0_pre4/src && cmsenv
        git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
        scram b -j8

Usage
  python submitCombine.py                       # all signals
  python submitCombine.py --subset VH,mfv_neu  # selected processes
  python submitCombine.py --dry-run             # list jobs without submitting
  python submitCombine.py --skip-existing       # skip already-completed jobs
"""
import os
import sys
import glob
import stat
import argparse
import subprocess

HERE         = os.path.dirname(os.path.abspath(__file__))
DATACARD_DIR = os.path.join(HERE, "Datacards")
COMBINE_OUT  = os.path.join(HERE, "CombineOutput")
CONDOR_DIR   = os.path.join(HERE, "CombineCondor")

# Tarball of user-built Combine files: binary, library, .pcm/.rootmap.
# Expected at $CMSSW_BASE/../combine_env.tar.gz (one level above the CMSSW installation).
# Override by setting the COMBINE_TARBALL environment variable.
COMBINE_TARBALL  = os.environ.get(
    "COMBINE_TARBALL",
    os.path.join(os.path.dirname(os.environ.get("CMSSW_BASE", "")), "combine_env.tar.gz"),
)
# CMSSW_14_1_0 (final release) is in CVMFS and has the same ABI as pre4.
# Worker nodes only bind /cvmfs, so we set up the environment from there.
CVMFS_CMSSW14    = "/cvmfs/cms.cern.ch/el9_amd64_gcc12/cms/cmssw/CMSSW_14_1_0/src"

YEARS    = ("20161", "20162", "2017", "2018")
CHANNELS = ("lep", "bjet")

# ---------------------------------------------------------------------------
# Per-job shell script
# Cards are pre-merged locally; this script only runs combine.
# CMSSW_14_1_0 from CVMFS sets up ROOT/RooFit; the shipped .so provides Combine.
# ---------------------------------------------------------------------------
_JOB_SH = """\
#!/bin/bash
set -e
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {cvmfs_cmssw14}
eval $(scramv1 runtime -sh)
cd /srv
tar xf combine_env.tar.gz
export PATH=/srv/combine_env/bin:$PATH
export LD_LIBRARY_PATH=/srv/combine_env/lib:$LD_LIBRARY_PATH

echo "=== AsymptoticLimits: {sig_id} ==="
combine -M AsymptoticLimits \\
    --name {sig_id} \\
    workspace_{sig_id}.root \\
    -v 1

# FitDiagnostics is best-effort; failure does not abort the job.
set +e
echo "=== FitDiagnostics: {sig_id} ==="
combine -M FitDiagnostics \\
    --name {sig_id} \\
    workspace_{sig_id}.root \\
    --saveShapes --saveWithUncertainties \\
    -v 1
FD_STATUS=$?
set -e
if [ $FD_STATUS -ne 0 ]; then
    echo "WARNING: FitDiagnostics failed (status $FD_STATUS) -- AsymptoticLimits result is still valid"
fi

echo "=== Done: {sig_id} ==="
"""

# ---------------------------------------------------------------------------
# Condor JDL
# transfer_input_files ships combine + the one user-built .so + the merged card.
# initialdir directs returned output files straight into CombineOutput/sig_id/.
# ---------------------------------------------------------------------------
_JDL = """\
universe                = vanilla
executable              = {job_sh}
initialdir              = {work_dir}
output                  = {log_pfx}.out
error                   = {log_pfx}.err
log                     = {log_pfx}.log
request_cpus            = 1
request_memory          = 2000MB
+DesiredOS              = "EL9"
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = {combine_tarball},{workspace}
transfer_output_files   = higgsCombine{sig_id}.AsymptoticLimits.mH120.root
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

    # Pre-merge cards locally (runs on submit node where NFS is available).
    card_args     = " ".join("%s=%s" % (k, v) for k, v in sorted(cards.items()))
    combined_card = os.path.join(condor_dir, "combined_%s.txt" % sig_id)
    workspace     = os.path.join(condor_dir, "workspace_%s.root" % sig_id)
    if not dry_run:
        ret = subprocess.call("combineCards.py %s > %s" % (card_args, combined_card), shell=True)
        if ret != 0:
            print("WARNING: combineCards.py failed for %s -- skipping" % sig_id)
            return False
        # Convert to RooStats workspace locally (requires CMSSW_14_1_0_pre4 Python).
        # Worker nodes run combine on the workspace in pure C++ -- no Python needed there.
        ret = subprocess.call(
            "text2workspace.py %s -m 125 -o %s" % (combined_card, workspace), shell=True)
        if ret != 0:
            print("WARNING: text2workspace.py failed for %s -- skipping" % sig_id)
            return False

    job_sh = os.path.join(condor_dir, "run.sh")
    with open(job_sh, "w") as fh:
        fh.write(_JOB_SH.format(
            cvmfs_cmssw14 = CVMFS_CMSSW14,
            sig_id        = sig_id,
        ))
    os.chmod(job_sh, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    log_pfx = os.path.join(condor_dir, "job")
    jdl_fn  = os.path.join(condor_dir, "submit.jdl")
    with open(jdl_fn, "w") as fh:
        fh.write(_JDL.format(
            job_sh          = job_sh,
            work_dir        = work_dir,
            log_pfx         = log_pfx,
            combine_tarball = COMBINE_TARBALL,
            workspace       = workspace,
            sig_id          = sig_id,
        ))

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

    if not args.dry_run:
        for path in (COMBINE_TARBALL, CVMFS_CMSSW14):
            if not os.path.exists(path):
                print("ERROR: required path not found: %s" % path)
                sys.exit(1)
        import shutil
        for tool in ("combineCards.py", "text2workspace.py"):
            if not shutil.which(tool):
                print("ERROR: %s not in PATH -- source CMSSW_14_1_0_pre4 cmsenv first" % tool)
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
        if _write_job(sig_id, hyps[sig_id], args.dry_run) is not False:
            n += 1

    if n_skip:
        print("Skipped %d already-completed hypotheses (--skip-existing)" % n_skip)

    status = "queued (dry-run, job files written)" if args.dry_run else "submitted to Condor"
    print("\n%d hypotheses %s" % (n, status))


if __name__ == "__main__":
    main()

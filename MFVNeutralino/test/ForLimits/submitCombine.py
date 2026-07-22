#!/usr/bin/env python
"""
Discover all signal datacards under <out-dir>/Datacards_<tag>/, group them by
(proc, ctau, mass), and submit one Condor job per hypothesis that runs:
  1. combine -M AsymptoticLimits -- 95% CL expected/observed limits
  2. combine -M FitDiagnostics   -- best-fit signal strength + s+b shapes

Cards are merged locally by combineCards.py before submission (requires the
CMSSW_14_1_0_pre4 environment to be active when running this script).
The combine binary and libHiggsAnalysisCombinedLimit.so are shipped via
transfer_input_files so worker nodes do not need /uscms/home or /uscms_data.

Prerequisites
  - makeLimitsInputROOT.py must have been run for all years + channels so that
    Datacards_<tag>/{lep,bjet}/Datacard_*.txt files exist. Pass the same --out-dir
    you gave it, otherwise this reads whatever happens to sit in this directory.
  - Run this script with CMSSW_14_1_0_pre4 + Combine sourced (cmsenv).
    combineCards.py and the combine binary must be in PATH.
    To install from scratch (on LPC EL9 node, outside apptainer):
        cmsrel CMSSW_14_1_0_pre4
        cd CMSSW_14_1_0_pre4/src && cmsenv
        git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
        scram b -j8

Usage
  python submitCombine.py --tag 4bin --out-dir DIR --method asymptotic   # all signals
  python submitCombine.py --tag 4bin --out-dir DIR --subset VH,mfv_neu   # selected processes
  python submitCombine.py --tag 4bin --out-dir DIR --dry-run             # list, don't submit
  python submitCombine.py --tag 4bin --out-dir DIR --skip-existing       # skip completed
  Run asymptotic before hybridnew, it uses the asymptotic result to set rMax.
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

def _apply_tag(tag, base=None):
    """Redirect all I/O directories to tagged variants (e.g. tag='4bin').

    base defaults to this directory, but should be the same --out-dir that was given to
    makeLimitsInputROOT.py, otherwise this reads a different set of datacards than the
    one that was just produced.
    """
    global DATACARD_DIR, COMBINE_OUT, CONDOR_DIR
    if base is None:
        base = HERE
    DATACARD_DIR = os.path.join(base, "Datacards_%s"    % tag)
    COMBINE_OUT  = os.path.join(base, "CombineOutput_%s" % tag)
    CONDOR_DIR   = os.path.join(base, "CombineCondor_%s" % tag)

COMBINE_TARBALL  = os.environ.get(
    "COMBINE_TARBALL",
    "/uscms_data/d3/gdecastr/work/combine_env.tar.gz",
)
# CMSSW_14_1_0 (final release) is in CVMFS and has the same ABI as pre4.
# Worker nodes only bind /cvmfs, so we set up the environment from there.
CVMFS_CMSSW14    = "/cvmfs/cms.cern.ch/el9_amd64_gcc12/cms/cmssw/CMSSW_14_1_0/src"

YEARS    = ("20161", "20162", "2017", "2018")
CHANNELS = ("lep", "bjet")

# ---------------------------------------------------------------------------
# Per-job shell scripts
# ---------------------------------------------------------------------------

# AsymptoticLimits: analytic CLs, fast (~5s), produces bands + median.
# Output: higgsCombine{sig}.AsymptoticLimits.mH120.root + combine.log
_JOB_SH_ASYMPTOTIC = """\
#!/bin/bash
set -e
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {cvmfs_cmssw14}
eval $(scramv1 runtime -sh)
cd /srv
tar xf combine_env.tar.gz
export PATH=/srv/combine_env/bin:$PATH
export LD_LIBRARY_PATH=/srv/combine_env/lib:$LD_LIBRARY_PATH

SIG={sig_id}
echo "=== AsymptoticLimits: $SIG ==="
combine -M AsymptoticLimits workspace_$SIG.root \\
    --name $SIG --run blind -v 0 \\
    2>&1 | tee combine.log
echo "=== Done: $SIG ==="
"""

# HybridNew: single Asimov (-t -1) run; blinded analysis so data = background.
_JOB_SH_HYBRIDNEW = """\
#!/bin/bash
set -e
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd {cvmfs_cmssw14}
eval $(scramv1 runtime -sh)
cd /srv
tar xf combine_env.tar.gz
export PATH=/srv/combine_env/bin:$PATH
export LD_LIBRARY_PATH=/srv/combine_env/lib:$LD_LIBRARY_PATH

SIG={sig_id}
echo "=== HybridNew Asimov expected: $SIG ==="
combine -M HybridNew --frequentist --testStat LHC \\
    -T 20000 --fork 2 -t -1 -s 1234 \\
    --rMax {rmax} \\
    --name $SIG \\
    workspace_$SIG.root -v 0
echo "=== Done: $SIG ==="
"""

# ---------------------------------------------------------------------------
# Condor JDL templates (one per method)
# ---------------------------------------------------------------------------

_JDL_ASYMPTOTIC = """\
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
transfer_output_files   = higgsCombine{sig_id}.AsymptoticLimits.mH120.root,combine.log
queue 1
"""

_JDL_HYBRIDNEW = """\
universe                = vanilla
executable              = {job_sh}
initialdir              = {work_dir}
output                  = {log_pfx}.out
error                   = {log_pfx}.err
log                     = {log_pfx}.log
request_cpus            = 2
request_memory          = 4000MB
+DesiredOS              = "EL9"
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
transfer_input_files    = {combine_tarball},{workspace}
transfer_output_files   = higgsCombine{sig_id}.HybridNew.mH120.1234.root
queue 1
"""

# Keep _JOB_SH / _JDL as aliases for backward compatibility
_JOB_SH = _JOB_SH_HYBRIDNEW
_JDL    = _JDL_HYBRIDNEW


def _read_asymptotic_exp(sig_id):
    """Return median expected limit (quantile=0.5) from AsymptoticLimits ROOT file, or None."""
    root_fn = os.path.join(COMBINE_OUT, sig_id,
                           "higgsCombine%s.AsymptoticLimits.mH120.root" % sig_id)
    if not os.path.exists(root_fn):
        return None
    try:
        import ROOT
        ROOT.PyConfig.IgnoreCommandLineOptions = True
        ROOT.gROOT.SetBatch(True)
        f = ROOT.TFile.Open(root_fn)
        if not f or f.IsZombie():
            return None
        t = f.Get("limit")
        if not t:
            f.Close()
            return None
        for _ in t:
            if abs(float(t.quantileExpected) - 0.5) < 0.01:
                val = float(t.limit)
                f.Close()
                return val
        f.Close()
    except Exception:
        pass
    return None


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


def _write_job(sig_id, cards, dry_run, method="hybridnew"):
    work_dir   = os.path.join(COMBINE_OUT, sig_id)
    condor_dir = os.path.join(CONDOR_DIR,  sig_id)
    _makedirs(work_dir)
    _makedirs(condor_dir)

    # Pre-merge cards and build workspace locally (submit node has NFS access).
    card_args     = " ".join("%s=%s" % (k, v) for k, v in sorted(cards.items()))
    combined_card = os.path.join(condor_dir, "combined_%s.txt" % sig_id)
    workspace     = os.path.join(condor_dir, "workspace_%s.root" % sig_id)
    if not dry_run:
        if not os.path.exists(workspace):
            import shutil
            for tool in ("combineCards.py", "text2workspace.py"):
                if not shutil.which(tool):
                    print("ERROR: %s not in PATH; workspace missing for %s -- skipping" % (tool, sig_id))
                    return False
            ret = subprocess.call("combineCards.py %s > %s" % (card_args, combined_card), shell=True)
            if ret != 0:
                print("WARNING: combineCards.py failed for %s -- skipping" % sig_id)
                return False
            ret = subprocess.call(
                "text2workspace.py %s -m 125 -o %s" % (combined_card, workspace), shell=True)
            if ret != 0:
                print("WARNING: text2workspace.py failed for %s -- skipping" % sig_id)
                return False

    job_sh  = os.path.join(condor_dir, "run.sh")
    log_pfx = os.path.join(condor_dir, "job")
    jdl_fn  = os.path.join(condor_dir, "submit.jdl")

    if method == "asymptotic":
        with open(job_sh, "w") as fh:
            fh.write(_JOB_SH_ASYMPTOTIC.format(
                cvmfs_cmssw14 = CVMFS_CMSSW14,
                sig_id        = sig_id,
            ))
        os.chmod(job_sh, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        with open(jdl_fn, "w") as fh:
            fh.write(_JDL_ASYMPTOTIC.format(
                job_sh          = job_sh,
                work_dir        = work_dir,
                log_pfx         = log_pfx,
                combine_tarball = COMBINE_TARBALL,
                workspace       = workspace,
                sig_id          = sig_id,
            ))
    else:
        asymp_exp = _read_asymptotic_exp(sig_id)
        if asymp_exp and asymp_exp > 0:
            rmax = 10.0 * asymp_exp  # no floor: at r=10*expected, CLs~0 and fork 2 is stable
        else:
            rmax = 20.0  # fallback for signals with no asymptotic log
        with open(job_sh, "w") as fh:
            fh.write(_JOB_SH_HYBRIDNEW.format(
                cvmfs_cmssw14 = CVMFS_CMSSW14,
                sig_id        = sig_id,
                rmax          = rmax,
            ))
        os.chmod(job_sh, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        with open(jdl_fn, "w") as fh:
            fh.write(_JDL_HYBRIDNEW.format(
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
            return False
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
                    help="Skip hypotheses that already have output for the chosen method")
    ap.add_argument("--limit", type=int, default=None,
                    help="Submit at most N jobs (for testing)")
    ap.add_argument("--sig-id", default=None,
                    help="Submit only this exact hypothesis (e.g. mfv_neu_tau001000um_M0400)")
    ap.add_argument("--tag", default=None,
                    help="Redirect I/O to tagged directories, e.g. --tag 4bin uses Datacards_4bin/, CombineOutput_4bin/, CombineCondor_4bin/")
    ap.add_argument("--out-dir", default=None,
                    help="Base folder holding the tagged directories. Give the same --out-dir "
                         "used for makeLimitsInputROOT.py. Defaults to this ForLimits directory.")
    ap.add_argument("--method", default="hybridnew", choices=["hybridnew", "asymptotic"],
                    help="Which combine method to run: hybridnew (default) or asymptotic")
    args = ap.parse_args()

    if args.tag:
        _apply_tag(args.tag, base=args.out_dir)
    elif args.out_dir:
        raise SystemExit("--out-dir only has an effect together with --tag")

    if not os.path.isdir(DATACARD_DIR):
        raise SystemExit("No datacard directory at %s. Point --out-dir at the same base you "
                         "gave makeLimitsInputROOT.py." % DATACARD_DIR)

    if not args.dry_run:
        for path in (COMBINE_TARBALL, CVMFS_CMSSW14):
            if not os.path.exists(path):
                print("ERROR: required path not found: %s" % path)
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
        if args.sig_id and sig_id != args.sig_id:
            continue
        if subset and proc not in subset:
            continue
        if args.skip_existing:
            if args.method == "asymptotic":
                out_fn = os.path.join(COMBINE_OUT, sig_id,
                                      "higgsCombine%s.AsymptoticLimits.mH120.root" % sig_id)
            else:
                out_fn = os.path.join(COMBINE_OUT, sig_id,
                                      "higgsCombine%s.HybridNew.mH120.1234.root" % sig_id)
            if os.path.exists(out_fn):
                n_skip += 1
                continue
        if _write_job(sig_id, hyps[sig_id], args.dry_run, method=args.method) is not False:
            n += 1
        if args.limit and n >= args.limit:
            break

    if n_skip:
        print("Skipped %d already-completed hypotheses (--skip-existing)" % n_skip)

    status = "queued (dry-run, job files written)" if args.dry_run else "submitted to Condor"
    print("\n%d hypotheses %s" % (n, status))


if __name__ == "__main__":
    main()

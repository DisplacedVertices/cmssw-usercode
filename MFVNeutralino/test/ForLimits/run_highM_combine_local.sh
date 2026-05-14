#!/bin/bash
# Run all highM Combine jobs directly on an el9 node (bypasses Condor container issue).
# Usage: bash run_highM_combine_local.sh [nparallel]
#   nparallel: number of simultaneous combine processes (default 8)
set -e

CMSSW14=/uscms/home/gdecastr/nobackup/work/CMSSW_14_1_0_pre4/src
FORLIM=/uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648/src/JMTucker/MFVNeutralino/test/ForLimits
NPAR=${1:-8}

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd "$CMSSW14"
eval $(scramv1 runtime -sh)

run_one() {
    local sig_id="$1"
    local work_dir="$FORLIM/CombineOutput/$sig_id"
    local card_dir_bjet="$FORLIM/Datacards/bjet"
    local out_fn="$work_dir/higgsCombine${sig_id}.AsymptoticLimits.mH120.root"

    if [ -f "$out_fn" ]; then
        echo "SKIP (already done): $sig_id"
        return 0
    fi

    mkdir -p "$work_dir"
    cd "$work_dir"

    # Build combineCards argument from available bjet datacards for this sig_id
    local card_args=""
    for year in 20161 20162 2017 2018; do
        local fn="$card_dir_bjet/Datacard_bjet_${sig_id}_${year}.txt"
        if [ -f "$fn" ]; then
            card_args="$card_args bjet_${year}=$fn"
        fi
    done

    echo "=== $sig_id ==="
    combineCards.py $card_args > "combined_${sig_id}.txt" 2>/dev/null
    combine -M AsymptoticLimits --name "$sig_id" "combined_${sig_id}.txt" -v 1 \
        > "$work_dir/combine.log" 2>&1
    echo "DONE: $sig_id"
}
export -f run_one
export FORLIM

# Collect all highM hypotheses (M1200, M1600, M3000) for the three SUSY processes
SIG_IDS=$(ls "$FORLIM/Datacards/bjet/" \
    | grep -E "Datacard_bjet_(mfv_neu|mfv_stopbbarbbar|mfv_stopdbardbar)_tau.*_M(1[26][0-9][0-9]|3000)_[0-9]" \
    | sed 's/Datacard_bjet_//' \
    | sed 's/_[0-9]\{4,5\}\.txt//' \
    | sort -u)

echo "Running $(echo "$SIG_IDS" | wc -l) hypotheses with $NPAR parallel jobs..."
echo "$SIG_IDS" | xargs -P "$NPAR" -I{} bash -c 'run_one "$@"' _ {}

echo ""
echo "=== All highM Combine jobs complete. ==="

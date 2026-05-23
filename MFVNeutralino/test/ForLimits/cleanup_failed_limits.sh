#!/bin/bash
# Delete output files for jobs that hit "Cannot set higher limit"
# so they can be resubmitted with --skip-existing.
CONDOR=/uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648/src/JMTucker/MFVNeutralino/test/ForLimits/CombineCondor
OUT=/uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648/src/JMTucker/MFVNeutralino/test/ForLimits/CombineOutput

n_del=0; n_keep=0; n_running=0
for d in $CONDOR/*/; do
    sig=$(basename $d)
    log="$d/job.out"
    outf="$OUT/$sig/higgsCombine${sig}.HybridNew.mH120.1234.root"
    [ -f "$log" ] || continue
    if grep -q "=== Done:" "$log" 2>/dev/null; then
        if grep -q "Limit: r <" "$log" 2>/dev/null; then
            n_keep=$((n_keep+1))
        else
            # "Cannot set higher limit" — delete output so it gets resubmitted
            if [ -f "$outf" ]; then
                echo "DEL $sig"
                rm -f "$outf"
                n_del=$((n_del+1))
            fi
        fi
    else
        n_running=$((n_running+1))
    fi
done
echo ""
echo "Kept (good limit):       $n_keep"
echo "Deleted (bad/no limit):  $n_del"
echo "Still running:           $n_running"

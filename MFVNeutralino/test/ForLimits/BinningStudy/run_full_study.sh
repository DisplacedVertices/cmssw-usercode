#!/bin/bash
# Sequential pipeline for the 5 new binning schemes.
# Run as: nohup bash run_full_study.sh > run_full_study.log 2>&1 & echo $! > run_full_study.pid
# Survives SSH disconnect. Check progress: tail -f run_full_study.log

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
NEW_SCHEMES="3bin_split 3bin_split_v2 3bin_412 2bin_split 4bin_split"

echo "[$(date)] === Step 1: Generate datacards (el7 + CMSSW_10_6_48) ==="
/cvmfs/cms.cern.ch/common/cmssw-cc7 -- bash -c "
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  cd /uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648
  eval \$(scramv1 runtime -sh) 2>/dev/null
  cd src/JMTucker/MFVNeutralino/test/ForLimits/BinningStudy
  python generate_variants_el7.py ${NEW_SCHEMES}
"
echo "[$(date)] Step 1 done (exit $?)"

echo "[$(date)] === Step 2: Strip systematics ==="
python3 "${HERE}/strip_systs.py"
echo "[$(date)] Step 2 done"

echo "[$(date)] === Step 3: Run combine (CMSSW_14_1_0_pre4) ==="
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /uscms/home/gdecastr/nobackup/work/CMSSW_14_1_0_pre4/src
eval $(scramv1 runtime -sh) 2>/dev/null
cd "${HERE}"
bash run_combine_study.sh ${NEW_SCHEMES}
echo "[$(date)] Step 3 done"

echo "[$(date)] === Step 4: Collect results ==="
source /cvmfs/sft.cern.ch/lcg/views/dev3/latest/x86_64-el9-gcc13-opt/setup.sh 2>/dev/null || true
python3 "${HERE}/collect_results.py" | tee "${HERE}/results_new_schemes.txt"
echo "[$(date)] === All done ==="

#!/bin/bash
# Condor payload: generate datacards, strip systs, run combine, collect results.
# Runs on el9 batch node; el7 step uses the cmssw-cc7 apptainer wrapper.
# All I/O goes to NFS (/uscms/home mounted via SingularityBind in JDL).

set -e
HERE="/uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648/src/JMTucker/MFVNeutralino/test/ForLimits/BinningStudy"
NEW_SCHEMES="3bin_split 3bin_split_v2 3bin_412 2bin_split 4bin_split"
CMSSW14_SRC="/uscms/home/gdecastr/nobackup/work/CMSSW_14_1_0_pre4/src"

echo "====== Step 1: Generate datacards (el7 container) ======"
/cvmfs/cms.cern.ch/common/cmssw-cc7 -- bash -c "
  source /cvmfs/cms.cern.ch/cmsset_default.sh
  cd /uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648
  eval \$(scramv1 runtime -sh) 2>/dev/null
  cd src/JMTucker/MFVNeutralino/test/ForLimits/BinningStudy
  python generate_variants_el7.py ${NEW_SCHEMES}
"

echo "====== Step 2: Strip systematics ======"
python3 "${HERE}/strip_systs.py"

echo "====== Step 3: Run combine (CMSSW_14_1_0_pre4) ======"
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd "${CMSSW14_SRC}"
eval $(scramv1 runtime -sh) 2>/dev/null
cd "${HERE}"
bash run_combine_study.sh ${NEW_SCHEMES}

echo "====== Step 4: Collect results ======"
source /cvmfs/sft.cern.ch/lcg/views/dev3/latest/x86_64-el9-gcc13-opt/setup.sh 2>/dev/null || true
python3 "${HERE}/collect_results.py" | tee "${HERE}/results_new_schemes.txt"

echo "====== Done ======"

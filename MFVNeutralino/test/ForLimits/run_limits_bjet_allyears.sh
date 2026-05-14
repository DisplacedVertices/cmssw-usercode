#!/bin/bash
# Run makeLimitsInputROOT.py for bjet channel, all 4 years.
# Run inside el7 apptainer with CMSSW_10_6_48 sourced.
# Usage:
#   apptainer exec ... bash run_limits_bjet_allyears.sh
# or interactively inside the apptainer:
#   bash run_limits_bjet_allyears.sh

set -e

CMSSW_SRC=/uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648/src
FORLIMITS=${CMSSW_SRC}/JMTucker/MFVNeutralino/test/ForLimits

echo "=== Setting up CMSSW ==="
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${CMSSW_SRC}
eval $(scramv1 runtime -sh)
echo "CMSSW_BASE=${CMSSW_BASE}"

echo ""
echo "=== Running makeLimitsInputROOT.py (bjet, all years) ==="
cd ${FORLIMITS}
python makeLimitsInputROOT.py --year all --channel bjet

echo ""
echo "=== Done! ==="

#!/bin/bash
# Run makeLimitsInputROOT.py for bjet channel, all 4 years.
# Sets up CMSSW itself, so run it inside the el7 container:
#   /cvmfs/cms.cern.ch/common/cmssw-el7 --bind /uscms_data -- bash run_limits_bjet_allyears.sh ...
#
# Usage:
#   bash run_limits_bjet_allyears.sh <minitree-dir> <bkg-template-dir> <out-dir>
#
# No defaults on purpose. The paths are yours, not mine -- passing them explicitly is what
# stops everyone writing into the same person's ForLimits directory.

set -e

if [ "$#" -ne 3 ]; then
    echo "Usage: bash $0 <minitree-dir> <bkg-template-dir> <out-dir>" >&2
    exit 1
fi

MINITREE_DIR=$1
BKG_TEMPLATE_DIR=$2
OUT_DIR=$3

# CMSSW_10_6_48 checkout that contains this file
FORLIMITS=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
CMSSW_SRC=$(cd "${FORLIMITS}/../../../.." && pwd)

echo "=== Setting up CMSSW ==="
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${CMSSW_SRC}
eval $(scramv1 runtime -sh)
echo "CMSSW_BASE=${CMSSW_BASE}"

echo ""
echo "=== Running makeLimitsInputROOT.py (bjet, all years) ==="
cd ${FORLIMITS}
python makeLimitsInputROOT.py --year all --channel bjet \
    --minitree-dir     ${MINITREE_DIR} \
    --bkg-template-dir ${BKG_TEMPLATE_DIR} \
    --out-dir          ${OUT_DIR}

echo ""
echo "=== Done! ==="

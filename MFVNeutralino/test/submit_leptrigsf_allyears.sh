#!/bin/bash
# Submit histosLepSF.py for all four Run-II years.
# Run this script from inside the CMSSW el7 apptainer after cmsenv.
# It uses $CMSSW_BASE automatically, so works with any CMSSW installation.
#   source /uscms/home/joeyr/setup_cmssw-el7_apptainer.sh
#   cd $CMSSW_BASE/src && cmsenv
#   cd JMTucker/MFVNeutralino/test
#   bash submit_leptrigsf_allyears.sh

set -e

if [ -z "$CMSSW_BASE" ]; then
    echo "ERROR: CMSSW_BASE not set. Run cmsenv first."
    exit 1
fi

YEAR_H=${CMSSW_BASE}/src/JMTucker/Tools/interface/Year.h
CMSSW_SRC=${CMSSW_BASE}/src
SCRIPT_DIR=${CMSSW_BASE}/src/JMTucker/MFVNeutralino/test

for YEAR in 20161 20162 2017 2018; do
    echo "============================================"
    echo "  Year: ${YEAR}"
    echo "============================================"

    # Swap the active year define in Year.h
    # Use [0-9]+ (one-or-more) and $ (end-of-line) so we only match the
    # single-token active-year line and never corrupt MFVNEUTRALINO_YEARS etc.
    sed -i -E "s|^#define MFVNEUTRALINO_[0-9]+$|#define MFVNEUTRALINO_${YEAR}|" ${YEAR_H}
    echo "Year.h set to MFVNEUTRALINO_${YEAR}:"
    grep "^#define MFVNEUTRALINO_[0-9]" ${YEAR_H}

    # Recompile
    cd ${CMSSW_SRC}
    scram b -j8 2>&1 | tail -5

    # Submit
    cd ${SCRIPT_DIR}
    python histosLepSF.py submit
    echo "Submitted year ${YEAR}"
    echo ""
done

echo "All four years submitted."

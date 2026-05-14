#!/bin/bash
# Submit high-M MiniTree condor jobs for all 4 Run 2 years.
# Run inside el7 apptainer with CMSSW_10_6_48.
#
# Usage (inside apptainer with cmsset_default.sh already sourced):
#   bash submit_highM_minitrees_allyears.sh
#
# NtupleCommon.py must already have use_btag_vetoLepHT_triggers = True (it does).
# Year.h is edited automatically; restored to 2018 at the end.

set -e

CMSSW_SRC=/uscms/home/gdecastr/nobackup/work/DVCode/mfv_10648/src
YEAR_H=${CMSSW_SRC}/JMTucker/Tools/interface/Year.h
TEST_DIR=${CMSSW_SRC}/JMTucker/MFVNeutralino/test

echo "=== Setting up CMSSW environment ==="
source /cvmfs/cms.cern.ch/cmsset_default.sh
cd ${CMSSW_SRC}
eval $(scramv1 runtime -sh)

for YEAR in 20161 20162 2017 2018; do
    echo ""
    echo "============================================================"
    echo "  Year: $YEAR"
    echo "============================================================"

    # Set Year.h: replace only the bare define line (no trailing content)
    sed -i "s/^#define MFVNEUTRALINO_[0-9]\{4,5\}$/#define MFVNEUTRALINO_${YEAR}/" ${YEAR_H}
    echo "Year.h set to MFVNEUTRALINO_${YEAR}"
    grep "^#define MFVNEUTRALINO_[0-9]" ${YEAR_H}

    # Rebuild (only files that depend on Year.h are recompiled -- fast)
    cd ${CMSSW_SRC}
    scram b -j8 2>&1 | grep -E "^(Building|Compiling|Linking|ERROR|error:|Warning|scram)" | head -20 || true
    echo "scram b done"

    # Submit
    cd ${TEST_DIR}
    python minitree_signal_bjet_highM.py submit
    echo "Submitted for year $YEAR"
done

# Restore Year.h to 2018 and rebuild once more
echo ""
echo "=== Restoring Year.h to 2018 ==="
sed -i "s/^#define MFVNEUTRALINO_[0-9]\{4,5\}$/#define MFVNEUTRALINO_2018/" ${YEAR_H}
grep "^#define MFVNEUTRALINO_[0-9]" ${YEAR_H}
cd ${CMSSW_SRC}
scram b -j8 2>&1 | grep -E "^(Building|Done|ERROR)" | head -5 || true

echo ""
echo "=== All done! High-M MiniTree jobs submitted for all 4 years. ==="

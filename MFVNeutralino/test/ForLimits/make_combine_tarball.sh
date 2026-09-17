#!/bin/bash
# Build combine_env.tar.gz for shipping to Condor worker nodes.
#
# Run this once after building CMSSW_14_1_0_pre4 + HiggsAnalysis/CombinedLimit.
# The tarball is placed at $CMSSW_BASE/../combine_env.tar.gz (one level above
# the CMSSW installation), which is where submitCombine.py expects it by default.
#
# Prerequisites: source CMSSW_14_1_0_pre4 cmsenv before running this script.
#   source /cvmfs/cms.cern.ch/cmsset_default.sh
#   cd <your CMSSW_14_1_0_pre4>/src && cmsenv && cd -
#   bash make_combine_tarball.sh
set -e

if [ -z "$CMSSW_BASE" ]; then
    echo "ERROR: CMSSW_BASE not set -- source cmsenv first"
    exit 1
fi

ARCH=$(ls "$CMSSW_BASE/bin")
OUT="$(dirname "$CMSSW_BASE")/combine_env.tar.gz"
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

mkdir -p "$TMPDIR/combine_env/bin"
mkdir -p "$TMPDIR/combine_env/lib"
mkdir -p "$TMPDIR/combine_env/python/HiggsAnalysis/CombinedLimit"
mkdir -p "$TMPDIR/combine_env/src/HiggsAnalysis/CombinedLimit/python"

# Binaries
cp "$CMSSW_BASE/bin/$ARCH/combine"              "$TMPDIR/combine_env/bin/"
cp "$CMSSW_BASE/bin/$ARCH/text2workspace.py"    "$TMPDIR/combine_env/bin/"

# Library + ROOT dictionary files
cp "$CMSSW_BASE/lib/$ARCH/libHiggsAnalysisCombinedLimit.so"        "$TMPDIR/combine_env/lib/"
cp "$CMSSW_BASE/lib/$ARCH/HiggsAnalysisCombinedLimit_xr_rdict.pcm" "$TMPDIR/combine_env/lib/"
cp "$CMSSW_BASE/lib/$ARCH/HiggsAnalysisCombinedLimit_xr.rootmap"   "$TMPDIR/combine_env/lib/"

# Python modules (CMSSW src/ layout required by CombinedLimit/__init__.py)
cp "$CMSSW_BASE/src/HiggsAnalysis/CombinedLimit/python/"*.py \
    "$TMPDIR/combine_env/src/HiggsAnalysis/CombinedLimit/python/"

# Python namespace stubs (used at import time to locate the src/ tree)
# The CombinedLimit __init__.py is installed to $CMSSW_BASE/python/ by scram b,
# not in src/ -- it contains the CMSSW path-resolution logic.
cp "$CMSSW_BASE/python/HiggsAnalysis/CombinedLimit/__init__.py" \
    "$TMPDIR/combine_env/python/HiggsAnalysis/CombinedLimit/__init__.py"
echo "# Namespace package" > "$TMPDIR/combine_env/python/HiggsAnalysis/__init__.py"

tar -czf "$OUT" -C "$TMPDIR" combine_env
echo "Written: $OUT ($(du -sh "$OUT" | cut -f1))"

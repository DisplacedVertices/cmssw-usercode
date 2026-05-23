#!/bin/bash
# Run inside CMSSW_14_1_0_pre4 with cmsenv already sourced.
# For each scheme x signal point: combineCards + FitDiagnostics + AsymptoticLimits (stat-only datacards).
set -e

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATACARD_BASE="${HERE}/datacards"
OUT_BASE="${HERE}/combine_output"

YEARS="20161 20162 2017 2018"

declare -A SIG_CHANNEL
SIG_CHANNEL["VH_tau1mm_M55"]="lep"
SIG_CHANNEL["VH_tau10mm_M55"]="lep"
SIG_CHANNEL["VH_tau1mm_M40"]="lep"
SIG_CHANNEL["VH_tau1mm_M15"]="lep"
SIG_CHANNEL["ggHToSSTodddd_tau1mm_M55"]="bjet"
SIG_CHANNEL["ggHToSSTodddd_tau1mm_M40"]="bjet"
SIG_CHANNEL["mfv_stopdbardbar_tau001000um_M0200"]="bjet"
SIG_CHANNEL["mfv_stopdbardbar_tau000300um_M0400"]="bjet"
SIG_CHANNEL["mfv_neu_tau001000um_M0400"]="bjet"

# Optional: pass scheme names as arguments to process only those schemes.
SCHEME_LIST="${@:-$(ls "${DATACARD_BASE}")}"

for SCHEME in ${SCHEME_LIST}; do
    echo ""
    echo "==============================="
    echo "SCHEME: ${SCHEME}"
    echo "==============================="

    for SIG_ID in "${!SIG_CHANNEL[@]}"; do
        CH="${SIG_CHANNEL[$SIG_ID]}"
        WORK_DIR="${OUT_BASE}/${SCHEME}/${SIG_ID}"
        mkdir -p "${WORK_DIR}"
        cd "${WORK_DIR}"

        # Build card_args: one card per year, named <ch>_<year>=<path>
        CARD_ARGS=""
        MISSING=0
        for YR in ${YEARS}; do
            CARD="${DATACARD_BASE}/${SCHEME}/${CH}/Datacard_${CH}_${SIG_ID}_${YR}_statonly.txt"
            if [ ! -f "${CARD}" ]; then
                echo "  SKIP (missing card): ${CARD}"
                MISSING=1
                break
            fi
            CARD_ARGS="${CARD_ARGS} ${CH}_${YR}=${CARD}"
        done
        [ "${MISSING}" -eq 1 ] && continue

        COMBINED="combined_${SIG_ID}.txt"

        echo "  Combining: ${SIG_ID}"
        combineCards.py ${CARD_ARGS} > "${COMBINED}" 2>/dev/null

        echo "  MultiDimFit grid scan (signal injection r=1)"
        combine -M MultiDimFit --algo grid \
            --name "${SCHEME}_${SIG_ID}" \
            "${COMBINED}" \
            -t -1 --expectSignal 1 \
            --rMin 0.5 --rMax 1.5 --points 200 \
            -v 0 2>/dev/null || echo "  WARNING: MultiDimFit failed"

        echo "  AsymptoticLimits (expectSignal=0)"
        combine -M AsymptoticLimits \
            --name "${SCHEME}_${SIG_ID}" \
            "${COMBINED}" \
            --expectSignal 0 \
            -v 0 2>/dev/null || echo "  WARNING: AsymptoticLimits failed"

        cd "${HERE}"
    done
done

echo ""
echo "Combine study complete."

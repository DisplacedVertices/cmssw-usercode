#!/bin/bash
# Run combine (AsymptoticLimits only) on with-systematics datacards.
# Source cmsenv before running.
set -e

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DC_BASE="${HERE}/datacards_systs"
OUT_BASE="${HERE}/combine_output_systs"
YEARS="20161 20162 2017 2018"

declare -A SIG_CHANNEL
SIG_CHANNEL["VH_tau1mm_M55"]="lep"
SIG_CHANNEL["VH_tau10mm_M55"]="lep"
SIG_CHANNEL["ggHToSSTodddd_tau1mm_M55"]="bjet"
SIG_CHANNEL["mfv_stopdbardbar_tau001000um_M0200"]="bjet"
SIG_CHANNEL["mfv_stopdbardbar_tau000300um_M0400"]="bjet"
SIG_CHANNEL["mfv_neu_tau001000um_M0400"]="bjet"

SCHEME_LIST="${@:-$(ls "${DC_BASE}" 2>/dev/null)}"

for SCHEME in ${SCHEME_LIST}; do
    echo ""
    echo "==============================="
    echo "SCHEME (with systs): ${SCHEME}"
    echo "==============================="

    for SIG_ID in "${!SIG_CHANNEL[@]}"; do
        CH="${SIG_CHANNEL[$SIG_ID]}"
        WORK_DIR="${OUT_BASE}/${SCHEME}/${SIG_ID}"
        mkdir -p "${WORK_DIR}"
        cd "${WORK_DIR}"

        CARD_ARGS=""
        MISSING=0
        for YR in ${YEARS}; do
            CARD="${DC_BASE}/${SCHEME}/${CH}/Datacard_${CH}_${SIG_ID}_${YR}_withsysts.txt"
            if [ ! -f "${CARD}" ]; then
                echo "  SKIP (missing card): ${CARD}"
                MISSING=1; break
            fi
            CARD_ARGS="${CARD_ARGS} ${CH}_${YR}=${CARD}"
        done
        [ "${MISSING}" -eq 1 ] && continue

        COMBINED="combined_systs_${SIG_ID}.txt"
        echo "  Combining: ${SIG_ID}"
        combineCards.py ${CARD_ARGS} > "${COMBINED}" 2>/dev/null

        echo "  AsymptoticLimits (with systs)"
        combine -M AsymptoticLimits \
            --name "systs_${SCHEME}_${SIG_ID}" \
            "${COMBINED}" \
            --expectSignal 0 \
            -v 0 2>/dev/null || echo "  WARNING: AsymptoticLimits failed"

        cd "${HERE}"
    done
done

echo ""
echo "Systs study complete."

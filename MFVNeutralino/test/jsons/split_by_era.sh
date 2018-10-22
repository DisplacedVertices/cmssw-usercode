#!/bin/bash

if [[ ! -f ds.txt ]]; then
    echo need ds.txt
    exit 1
fi

while read x; do
    if [[ $x =~ ' ' ]]; then
        year=$(echo $x | cut -d ' ' -f 1)
        era=$(echo $x | cut -d ' ' -f 2)
        x=$(echo $x | cut -d ' ' -f 3)
    else
        year=$(echo $x | sed 's/.*Run\([[:digit:]]\{4\}\).*/\1/')
        era=$(echo $x | sed 's/.*Run\('${year}'.\).*/\1/')
        if [[ $x =~ PromptReco ]]; then
            era=${era}$(echo $x | sed 's/.*PromptReco-v\(.\).*/\1/')
        fi
    fi
    runfn=runs-${era}.txt
    dasgoclient -query "run dataset=$x" > $runfn
    minrun=$(sort -n $runfn | head -1)
    maxrun=$(sort -n $runfn | tail -1)
    echo $year $era $x $minrun $maxrun
    for xx in '' ana_; do
        filterJSON.py --min=$minrun --max=$maxrun ${xx}${year}.json > ${xx}${era}.json
    done
done < ds.txt

#!/bin/bash

if [[ ! -f ds.txt ]]; then
    echo need ds.txt
    exit 1
fi

for x in $(<ds.txt); do
    year=$(echo $x | sed 's/.*Run\([[:digit:]]\{4\}\).*/\1/')
    era=$(echo $x | sed 's/.*Run\('${year}'.\).*/\1/')
    runfn=runs-${era}.txt
    dasgoclient -query "run dataset=$x" > $runfn
    minrun=$(sort -n $runfn | head -1)
    maxrun=$(sort -n $runfn | tail -1)
    echo $era $minrun $maxrun
    for xx in '' ana_; do
        filterJSON.py --min=$minrun --max=$maxrun ${xx}${year}.json > ${xx}${era}.json
    done
done

#!/bin/bash

if [[ ! -f ds.txt ]]; then
    echo need ds.txt
    exit 1
fi

for x in $(<ds.txt); do
    era=$(echo $x | sed 's/.*\(Run2017.\).*/\1/')
    era=${era/Run/}
    runfn=runs-${era}.txt
    dasgoclient_linux -query "run dataset=$x" > $runfn
    runrange=( $(python -c "l = "$(<$runfn)"; print min(l),max(l)") )
    echo $era ${runrange[@]}
    for xx in '' ana_; do
        filterJSON.py --min=${runrange[0]} --max=${runrange[1]} ${xx}2017.json > ${xx}${era}.json
    done
done

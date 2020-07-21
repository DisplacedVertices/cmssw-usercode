#!/bin/bash

for x in "$@"; do
    store=$(cr od "$x" | grep /store)
    nj=$(cr njobs "$x" | grep -v crab)
    for i in $(seq 1 $nj); do
        j=$((i/1000))
        nd=$(printf '%04i' $j )
        echo copy root://cmseos.fnal.gov/$store/$nd/output_${i}.txz to "$x"
#        xrdcp -sf root://cmseos.fnal.gov/$store/$nd/output_${i}.txz "$x"
    done

done

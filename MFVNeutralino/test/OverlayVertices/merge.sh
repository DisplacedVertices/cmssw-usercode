#!/bin/bash

d=$1
if [[ ! -d $d ]]; then
    echo no directory $d
    exit 1
fi

for x in qcdht{10,15,20}00 ttbar; do
    f=$d/${x}.root
    if [[ ! -e $f ]]; then
        echo no file $f
        exit 1
    fi
done

mergeTFileServiceHistograms -w 8.537878,1.093070,0.459715,0.778106 -i $d/qcdht1000.root $d/qcdht1500.root $d/qcdht2000.root $d/ttbar.root -o $d/merge.root 2>&1 | grep -v "Sum of squares of weights structure already created"
exit ${PIPESTATUS[0]}


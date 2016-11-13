#!/bin/bash

function pwarn() { echo -e '\033[36;7m' $@ '\033[m'; }
function pexit() { pwarn $@; echo; exit 1; }

if [[ $# -ne 1 ]]; then
    pexit need dir in argv[1]
fi

d=$1
echo using dir $d
d=$d/outputs
if [[ ! -d $d ]]; then
    pexit $d is not a directory
fi

prefix=$(basename $(ls -1 $d/*_*_*.* | head -1) | cut -d _ -f 1-2)
bname=$(echo $prefix | cut -d _ -f 1)

nlogs=$(ls -1 $d/*.log | wc -l)
if [[ $nlogs -eq 0 ]]; then
    pexit found no log files
else
    echo found $nlogs log files
fi

logsok=1
numsok=()
for i in $(seq 0 $((nlogs-1))); do
    fn=$d/${prefix}_${i}.log
    if [[ ! -e $fn ]]; then
        echo log $i is missing
        logsok=0
        continue
    fi
    grep return\ value $fn > /dev/null
    if [[ $? -ne 0 ]]; then
        echo return value not found in log $i
        grep -i remove $fn
        logsok=0
        continue
    fi
    grep -H return\ value $fn | grep -v 'return value 0'
    if [[ $? -ne 1 ]]; then
        logsok=0
        continue
    fi
    numsok+=($i)
done
if [[ $logsok -ne 1 ]]; then
    pwarn one or more logs missing/bad, expect ${#numsok[@]} root files
else
    echo all logs ok
fi

roots=()
for i in ${numsok[@]}; do
    fn=$d/${bname}_${i}.root
    if [[ ! -e $fn ]]; then
        pwarn root file $i missing
    else
        roots+=($fn)
    fi
done

echo got ${#roots[@]} root files
haddlog=$d/overlay.root.haddlog
hadd $d/overlay.root ${roots[@]} 2>&1 > $haddlog
echo hadd saw $(grep Source\ file $haddlog | tail -1 | cut -d ' ' -f 4 | tr -d :) files
echo

#!/bin/bash

if [ $# -eq 0 ]; then
    echo No arguments supplied
fi

d=$1
echo using dir $d

nlogs=$(ls -1 $d/outputs/*.log | wc -l)
echo found $nlogs log files

grep return\ value $d/outputs/*log | grep -v 'return value 0'
if [ $? -ne 1 ]; then
    echo '\033[36;7m problem with one or more log files \033[m'
    exit 1
else
    echo all logs ok
fi

roots=( $(ls -1v $d/outputs/*root) )
nroots=${#roots[@]}
if [ $nroots -ne $nlogs ]; then
    echo '\033[36;7m number of root files ne nlogs \033[m' $nroots
    exit 1
else
    echo found $nroots root files
fi

last=${roots[$((nroots-1))]}
lastnum=$(echo $last | sed -e 's/.*_//' -e 's/.root//')
if [ $lastnum -ne $((nroots-1)) ]; then
    echo '\033[36;7m problem root files \033[m'
    exit 1
else
    echo root numbers ok
fi

newfn=$d/outputs/overlay.root
hadd.py $newfn ${roots[@]}

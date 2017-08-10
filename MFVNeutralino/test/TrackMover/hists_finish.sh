#!/bin/bash

njobstot=38

if [[ $1 == "check" ]]; then
    njobs=$(grep 'return value' hists.log.* | grep -c 'value 0')
    if [[ $njobs != $njobstot ]]; then
        echo only $njobs done
        exit 1
    else
        echo all $njobstot done
        exit 0
    fi

elif [[ $1 == "cleanup" ]]; then
    tar --remove-files -czf lastlogs.tgz hists.{stdout,stderr,log}.*

elif [[ $1 == "finish" ]]; then
   for x in $2 $3 $4 $5 $6 $7 $8 $9; do # e.g. specify ./hists_finish finish 20 21 22
       echo $x
       mkdir $x
       for y in ${x}_*root; do
           mv $y ${x}/${y/${x}_/}
       done
       cd $x
       #py $CMSSW_BASE/src/JMTucker/MFVNeutralino/test/utilities.py merge_background # not using full bkg samples anymore
       samples merge qcdht1000and1500_hip1p0_mit.root -22300 qcdht*_hip1p0_mit.root
       samples merge qcdht1000and1500.root -16200 qcdht{1000,1500}.root
       hadd qcdht1000and1500_hipplusno.root qcdht1000and1500_hip1p0_mit.root qcdht1000and1500.root
       cd - >/dev/null
       echo
   done
fi

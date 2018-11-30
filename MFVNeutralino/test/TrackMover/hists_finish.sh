#!/bin/bash

njobstot=510

function mergemc {
    allthere=1
    for x in qcdht0700_2017.root qcdht1000_2017.root qcdht1500_2017.root qcdht2000_2017.root ttbarht0600_2017.root ttbarht0800_2017.root ; do
        if [[ ! -e $x ]]; then
            echo mergemc: $x does not exist
            allthere=0
        fi
        if [[ allthere -ne 1 ]]; then
            return 1
        fi
    done
    samples merge qcdht0700_2017.root qcdht1000_2017.root qcdht1500_2017.root qcdht2000_2017.root ttbarht0600_2017.root ttbarht0800_2017.root -41530 background_2017.root
}

function mergedata {
    allthere=1
    for x in JetHT2017{B,C,D,E,F}.root JetHT2018{A,B,D2}.root ; do
        if [[ ! -e $x ]]; then
            echo mergedata: $x does not exist
            allthere=0
        fi
        if [[ allthere -ne 1 ]]; then
            return 1
        fi
    done
    hadd.py JetHT2017.root JetHT2017{B,C,D,E,F}.root
    hadd.py JetHT2018.root JetHT2018{A,B,D2}.root
    hadd.py JetHT2017p8.root JetHT2017.root JetHT2018.root
}

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
    for x in TrackMoverV*.root ; do
        y=$(echo $x | sed 's/TrackMoverV._//' | sed 's@_@XXX@g5' | sed 's@_@/@g' | sed 's/XXX/_/g')
        mkdir -p $(dirname $y)
        mv $x $y
    done
    for d in $(find . -type d -links 2) ; do
        if [[ $(basename $d) != bin ]]; then
            echo $d
            cd $d
            mergemc
            mergedata
            cd - >/dev/null
            echo
        fi
    done

elif [[ $1 == "mergemc" ]]; then
    mergemc

elif [[ $1 == "mergedata" ]]; then
    mergedata

elif [[ $1 == "allthere" ]]; then
    for d in $(find . -type d -links 2) ; do
        for x in qcdht0700_2017.root qcdht1000_2017.root qcdht1500_2017.root qcdht2000_2017.root ttbar_2017.root JetHT2017{B,C,D,E,F}.root ; do
            if [[ ! -e $d/$x ]]; then
                echo $d no $x
            fi
        done
        for x in background_2017.root ; do
            if [[ ! -e $d/$x ]]; then
                echo $d needs mergemc
            fi
        done
    done
fi

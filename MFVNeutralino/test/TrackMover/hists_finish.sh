#!/bin/bash

njobstot=2310

function mergeqcd {
    allthere=1
    for x in qcdht1000.root qcdht1500.root qcdht1000_hip1p0_mit.root qcdht1500_hip1p0_mit.root ; do
        if [[ ! -e $x ]]; then
            echo mergeqcd: $x does not exist
            allthere=0
        fi
        if [[ allthere -ne 1 ]]; then
            return 1
        fi
    done
    samples merge qcdht1000and1500_hip1p0_mit.root -22300 qcdht{1000,1500}_hip1p0_mit.root
    samples merge qcdht1000and1500.root -16200 qcdht{1000,1500}.root
    hadd qcdht1000and1500_hipplusno.root qcdht1000and1500_hip1p0_mit.root qcdht1000and1500.root
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
    rename TrackMoverV3_ '' *.root
    for x in *.root ; do
        y=$(echo $x | sed 's@_@XXX@g4' | sed 's@_@/@g' | sed 's/XXX/_/g')
        mkdir -p $(dirname $y)
        mv $x $y
    done
    for d in $(find . -type d -links 2) ; do
        echo $d
        cd $d
        mergeqcd
        cd - >/dev/null
        echo
    done

elif [[ $1 == "mergeqcd" ]]; then
    mergeqcd

elif [[ $1 == "allthere" ]]; then
    for d in $(find . -type d -links 2) ; do
        for x in qcdht1000.root qcdht1500.root qcdht1000_hip1p0_mit.root qcdht1500_hip1p0_mit.root JetHT2016{B3,C,D,E,F,G,H}.root ; do
            if [[ ! -e $d/$x ]]; then
                echo $d no $x
            fi
        done
        for x in qcdht1000and1500_hip1p0_mit.root qcdht1000and1500.root qcdht1000and1500_hipplusno.root ; do
            if [[ ! -e $d/$x ]]; then
                echo $d needs mergeqcd
            fi
        done
    done

fi
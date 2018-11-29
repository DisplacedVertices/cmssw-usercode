#!/bin/bash

batchdir=$1

if [[ $batchdir == "" ]]; then
    echo must specifiy batchdir
    exit 1
fi

if [[ -e $batchdir ]]; then
    echo $batchdir exists, refusing to clobber
    exit 1
fi

make clean
make -j 4
if [[ $? -ne 0 ]]; then
    echo problem with make
    exit 1
fi

./hists.sh -1
echo -n 'ok? '
read ok

mkdir -p $batchdir
cp -p hists.sh hists.exe hists.jdl $(python -c "from JMTucker.Tools.CMSSWTools import json_path; print json_path('ana_2017p8.json')") $batchdir
cd $batchdir
condor_submit hists.jdl
cd - >/dev/null


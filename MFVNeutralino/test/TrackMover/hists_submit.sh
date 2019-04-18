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

if true; then
    make clean
    make -j 8
    if [[ $? -ne 0 ]]; then
        echo problem with make
        exit 1
    fi
fi

./hists.sh -1
echo -n 'ok? '
read ok

mkdir -p $batchdir/inputs
cmsMakeTarball.py $batchdir/inputs/libs.tgz --no-include-python --no-include-interface
tocp=(
    hists.sh
    hists.exe
    $(python -c "from JMTucker.Tools.CMSSWTools import json_path; print json_path('ana_2017p8.json')")
)
cp -p ${tocp[@]} $batchdir/inputs

cd $batchdir
cat >inputs/hists.jdl <<EOF
universe = vanilla
Executable = inputs/hists.sh
arguments = \$(Process)
Output = hists.stdout.\$(Process)
Error = hists.stderr.\$(Process)
Log = hists.log.\$(Process)
stream_output = false
stream_error  = false
notification  = never
transfer_input_files = inputs/libs.tgz,inputs/hists.exe,inputs/ana_2017p8.json
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
Queue $(inputs/hists.sh -1 | tail -n 1)
EOF
condor_submit inputs/hists.jdl

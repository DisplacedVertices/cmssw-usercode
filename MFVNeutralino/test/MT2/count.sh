#!/bin/bash

inpath=/store/user/tucker/hadded/NtupleV27mmB5
outpath=count

if [[ -e $outpath ]]; then
    ls -l $outpath
    echo ok to rm\?
    read
    rm -r $outpath
fi

mkdir -p $outpath
make count.exe || exit 1

for x in /eos/uscms$inpath/*root; do
    ./count.exe -l -i root://cmseos.fnal.gov/$inpath/$(basename $x) -o $outpath/$(basename $x) 2>&1 | grep -v 'Warning in <TClass::Init>: no dictionary for class ROOT::TIOFeatures is available' &
done

ps aux | grep $(whoami) | grep count.exe
echo -n 'sleeping until finished: '
while ( ps -U $(whoami) | grep count.exe > /dev/null ); do
    sleep 2; echo -n '.'
done

echo -e '\nhadding data and background:'
cd $outpath
for cmd in hadd_data merge_background; do
    python $CMSSW_BASE/src/JMTucker/MFVNeutralino/test/utilities.py $cmd
done
cd -

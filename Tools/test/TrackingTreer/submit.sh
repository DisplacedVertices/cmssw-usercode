#!/bin/sh

wd=$(pwd)
batch=$1
job=$2
out_dir=$3

export SCRAM_ARCH=slc6_amd64_gcc630
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project CMSSW CMSSW_9_4_6_patch1 2>/dev/null >/dev/null
cd CMSSW_9_4_6_patch1/src
eval $(scram ru -sh)
cd $wd

in_fn=$(sed -n "$((job+1))p" ${batch}.txt)
out_fn=${batch}_${job}.root

./hists.exe -i $in_fn -o $out_fn
exit_code=$?
if [[ $exit_code == 0 ]]; then
    xrdcp -s $out_fn root://cmseos.fnal.gov/${out_dir}
fi

rm $out_fn
exit $exit_code

#!/bin/sh

echo script starting on `date`
echo script args: $@
wd=$(pwd)
echo in $wd

batch=$1
job=$2
out_dir=$3
echo batch $batch job $job

source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsrel CMSSW_7_4_15_patch1 2>&1 > /dev/null
cd CMSSW_7_4_15_patch1/src
cmsenv
cd $wd

echo which root
which root

sed -n "$((job+1))p" ${batch}.txt > input.txt
echo input.txt
cat input.txt

out_fn=${batch}_${job}.root

cmd="./hists.exe input.txt $out_fn"
echo $cmd
$cmd
exit_code=$?
if [[ $exit_code == "0" ]]; then
    cmd="xrdcp -s $out_fn root://cmseos.fnal.gov/${out_dir}"
    echo $cmd
    $cmd
fi

rm input.txt
rm $out_fn
exit $exit_code

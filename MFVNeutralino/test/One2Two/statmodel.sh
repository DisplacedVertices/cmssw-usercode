#!/bin/bash

#echo script starting on $(date)

wd=$(pwd)
job=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/slc6_amd64_gcc493/cms/cmssw-patch/CMSSW_7_6_3_patch2/src
eval `scramv1 runtime -sh`
cd $wd

ntracks=$((3+job%3))
oversample_a=(1 2 5 10 20)
oversample=${oversample_a[$((job/3))]}
echo ntracks $ntracks oversample $oversample

out_fn=sm_ntk${ntracks}_os${oversample}

env sm_ntracks=${ntracks} sm_out_fn=${out_fn} sm_oversample=${oversample} ./statmodel.exe 2>&1 > ${out_fn}.log



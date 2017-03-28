#!/bin/bash

#echo script starting on $(date)

wd=$(pwd)
job=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh
cd /cvmfs/cms.cern.ch/slc6_amd64_gcc530/cms/cmssw/CMSSW_8_0_25/src
eval `scramv1 runtime -sh`
cd $wd

ntracks=$((3+job%3))
year_index=$((job/3))
echo ntracks $ntracks year_index $year_index

out_fn=sm_ntk${ntracks}_year${year_index}

env sm_ntracks=${ntracks} sm_out_fn=${out_fn} sm_year_index=${year_index} ./statmodel.exe 2>&1 > ${out_fn}.log

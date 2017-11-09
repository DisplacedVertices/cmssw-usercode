#!/bin/bash

job=$1
test=0
if [[ $job < 0 ]]; then
    job=$((-job))
    test=1
fi

inpathbase=root://cmseos.fnal.gov//store/user/tucker/TrackMoverV6

paths=(
${inpathbase}
)

fns=(
JetHT2016B3.root
JetHT2016C.root
JetHT2016D.root
JetHT2016E.root
JetHT2016F.root
JetHT2016G.root
JetHT2016H.root
qcdht1000.root
qcdht1000_hip1p0_mit.root
qcdht1500.root
qcdht1500_hip1p0_mit.root
)

nsigs=( 4p0 4p1 )
taus=( 100 300 1000 10000 30000 )
nls=( 2 3 )
nbs=( 0 1 2 )

####

npaths=${#paths[@]}
nfns=${#fns[@]}
nnsigs=${#nsigs[@]}
ntaus=${#taus[@]}
nnls=${#nls[@]}
nnbs=${#nbs[@]}
njobs=$((npaths * nfns * nnsigs * ntaus * nnls * nnbs))
echo job $job inpathbase $inpathbase \#paths $npaths \#fns $nfns \#nsigs $nnsigs \#taus $ntaus \#nls $nnls \#nbs $nnbs max jobs $njobs
if [[ $job -ge $njobs ]]; then
    echo problem
    exit 1
fi

ii=$job

path=${paths[$((ii % npaths))]}
ii=$((ii / npaths))
fn=${fns[$((ii % nfns))]}
ii=$((ii / nfns))
nsig=${nsigs[$((ii % nnsigs))]}
ii=$((ii / nnsigs))
tau=${taus[$((ii % ntaus))]}
ii=$((ii / ntaus))
nl=${nls[$((ii % nnls))]}
ii=$((ii / nnls))
nb=${nbs[$((ii % nnbs))]}
ii=$((ii / nnbs))

outfn=$(basename $path)_nsig${nsig}_tau$(printf %05i $tau)um_${nl}${nb}_$(basename $fn .root).root
treepath=mfvMovedTree${nl}${nb}nsig${nsig}btagoldangle0p2/t

echo path $path fn $fn nl $nl nb $nb outfn $outfn treepath $treepath

if [[ $test == 1 ]]; then
    echo test only, possibly modifying hists.jdl and hists_finish.sh
    sed -i -e "s/Queue.*/Queue ${njobs}/" hists.jdl
    sed -i -e "s/^njobstot=.*/njobstot=${njobs}/" hists_finish.sh
    exit 1
fi

export SCRAM_ARCH=slc6_amd64_gcc530
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project CMSSW CMSSW_8_0_25 2>&1
cd CMSSW_8_0_25/src
eval $(scram ru -sh)
cd ../..

cmd="./hists.exe $path/$fn $outfn $treepath $tau"
echo $cmd
eval $cmd 2>&1

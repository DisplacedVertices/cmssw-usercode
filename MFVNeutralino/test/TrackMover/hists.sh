#!/bin/bash

job=$1

fns=(
 JetHT2015.root 
 JetHT2015C.root 
 JetHT2015D.root 
 JetHT2016.root 
 JetHT2016B3.root 
 JetHT2016BCD.root 
 JetHT2016BthruG.root 
 JetHT2016C.root 
 JetHT2016D.root 
 JetHT2016E.root 
 JetHT2016EF.root 
 JetHT2016F.root 
 JetHT2016G.root 
 JetHT2016H.root 
 JetHT2016H2.root 
 JetHT2016H3.root 
 qcdht0500sum.root 
 qcdht0500sum_2015.root 
 qcdht0700sum.root 
 qcdht0700sum_2015.root 
 qcdht1000sum.root 
 qcdht1000sum_2015.root 
 qcdht1500sum.root 
 qcdht1500sum_2015.root 
 qcdht2000sum.root 
 qcdht2000sum_2015.root 
 ttbar.root 
 ttbar_2015.root
 )
nfns=${#fns[@]}

nls=( 2 3 )
nbs=( 0 1 2 )

nnls=${#nls[@]}
nnbs=${#nbs[@]}

echo \#fns $nfns \#nls $nnls \#nbs $nnbs

nmax=$((nfns * nnls * nnbs))
echo job $job, nmax is $nmax
if [[ $job -ge $nmax ]]; then
    echo problem
    exit 1
fi

ifn=$((job % nfns))
fn=${fns[$ifn]}
iz=$((job / nfns))
inl=$((iz / nnbs))
inb=$((iz % nnbs))
nl=${nls[$inl]}
nb=${nbs[$inb]}
z=$nl$nb
outfn=${z}_$fn
echo fn $fn iz $iz inl $inl nl $nl inb $inb nb $nb z $z outfn $outfn

export SCRAM_ARCH=slc6_amd64_gcc530
source /cvmfs/cms.cern.ch/cmsset_default.sh
scram project CMSSW CMSSW_8_0_25 2>&1
cd CMSSW_8_0_25/src
eval $(scram ru -sh)
cd ../..

./hists.exe root://cmseos.fnal.gov//store/user/tucker/TrackMoverV1/$z/$fn $outfn $nl $nb 2>&1

# check with:
#   grep 'return value' hists.log.* | grep -v 'value 0'
# when done:
#   tar --remove-files -czf lastlogs.tgz hists.{stdout,stderr,log}.*
#   for x in 20 21 22 30 31 32 ; do mkdir $x ; for y in ${x}*root; do mv $y $x/${y/${x}_/} ; done ; cd $x ; py $CMSSW_BASE/src/JMTucker/MFVNeutralino/test/utilities.py merge_background ; cd - ; done

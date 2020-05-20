#!/bin/bash

# The combine tarball is made in a locally checked-out combine
# environment so the worker nodes don't have to git clone, etc.
#
# In this CMSSW environment, run
#   cmsMakeTarball.py --standalone dummyarg > ~/tarball.py
#
# Set up combine *on a SL7 machine* following
#   http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
# Directly for this version:
#
#   export SCRAM_ARCH=slc7_amd64_gcc700
#   cmsrel CMSSW_10_2_13
#   cd CMSSW_10_2_13/src
#   cmsenv
#   git clone https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
#   cd HiggsAnalysis/CombinedLimit
#   patch -p1 < path/to/main/cmssw/src/JMTucker/MFVNeutralino/test/One2Two/patchSetHint
#   git fetch origin
#   git checkout v8.0.1
#   scram b clean; scram b
#
# In that same combine environment, make the tarball with:
#   python ~/tarball.py --include-bin combine.tgz
# Copy the tarball to eos, hopefully with a versioned name,
# and update the urls in both submitgrid.py and below.

echo combine script starting at $(date) with args $*

export JOB=$1
export WD=$(pwd)

source steering.sh

echo JOB: ${JOB}
echo ISAMPLE: ${ISAMPLE}
echo XRDCPCOMBINETARBALL: ${XRDCPCOMBINETARBALL}
echo DATACARDARGS: ${DATACARDARGS}
echo SAVETOYS: ${SAVETOYS}
echo EXPECTED: ${EXPECTED}
echo NOSYSTEMATICS: ${NOSYSTEMATICS}
echo GOODNESSOFFIT: ${GOODNESSOFFIT}
 
if [[ ${SAVETOYS} -eq 1 ]]; then
    SAVETOYSPAR="--saveToys"
else
    SAVETOYSPAR=""
fi

#################################a###############################################

eval $(scram unsetenv -sh)

export SCRAM_ARCH=slc7_amd64_gcc700
scram project CMSSW CMSSW_10_2_13 2>&1 >/dev/null
scramexit=$?
if [[ $scramexit -ne 0 ]]; then
    echo problem with scram project $1 $2
    exit $scramexit
fi
cd CMSSW_10_2_13
eval $(scram runtime -sh)

if [[ ${XRDCPCOMBINETARBALL} -eq 0 ]]; then
    mv $WD/combine.tgz .
else
    xrdcp -s root://cmseos.fnal.gov//store/user/tucker/combine.tgz .
fi

tar xf combine.tgz
scram b 2>&1 >/dev/null
hash -r
which combine

cd $WD

{
    echo "========================================================================="
    echo datacard:
    python datacard.py $ISAMPLE $DATACARDARGS > datacard.txt
    awk '{ print "DATACARD: " $0 }' datacard.txt

    hint=$(awk '/hint/ { print $NF }' datacard.txt)
    # don't use -H AsymptoticLimits, at least don't do it for low-efficiency signals, it can lead to way too low limits
    cmd="combine --setTheHint $hint -M MarkovChainMC --noDefaultPrior=0 --tries 20 -b 200 --iteration 100000 datacard.txt"

    if [[ $JOB == 0 ]]; then
        echo "========================================================================="
        echo Observed limit
        eval $cmd
        mv higgsCombine*root observed_${JOB}.root

        if [[ $NOSYSTEMATICS -eq 0 ]]; then
            echo "========================================================================="
            echo Observed limit, no systematics
            eval $cmd -S0
            mv higgsCombine*root observedS0_${JOB}.root
        fi
    else
        # otherwise crab craps its pants
        touch observed_${JOB}.root
        [[ $NOSYSTEMATICS -eq 0 ]] && touch observedS0_${JOB}.root
    fi

    ntoys=100
    seedbase=13068931

    if [[ $EXPECTED -ne 0 ]]; then
        echo "========================================================================="
        echo Expected limits
        eval $cmd --toys $ntoys ${SAVETOYSPAR} -s $((JOB+seedbase))
        mv higgsCombine*root expected_${JOB}.root

        if [[ $NOSYSTEMATICS -eq 0 ]]; then 
            echo "========================================================================="
            echo Expected limits, no systematics
            eval $cmd -S0 --toys $ntoys ${SAVETOYSPAR} -s $((JOB+seedbase))
            mv higgsCombine*root expectedS0_${JOB}.root
        fi
    fi

########################################################################

#   cmd="combine -M GoodnessOfFit --algo=saturated datacard.txt"
#
#   if [[ $JOB == 0 ]]; then
#       echo "========================================================================="
#       echo GoodnessOfFit observed
#       eval $cmd
#       mv higgsCombine*root gof_observed.root
#
#       echo "========================================================================="
#       echo GoodnessOfFit observed, no systematics
#       eval $cmd -S0
#       combine -S0 -M GoodnessOfFit datacard.txt --algo=saturated
#       mv higgsCombine*root gof_S0_observed.root
#   fi
#
#   echo "========================================================================="
#   echo GoodnessOfFit expected
#   eval $cmd --toys $ntoys -s $((JOB+seedbase))
#   mv higgsCombine*root gof_expected_${JOB}.root
#
#   echo "========================================================================="
#   echo GoodnessOfFit expected, no systematics
#   eval $cmd -S0 --toys ntoys -s $((JOB+seedbase))
#   mv higgsCombine*root gof_S0_expected_${JOB}.root

########################################################################

#   cmd="combine -M Significance datacard.txt"
#
#   if [[ $JOB == 0 ]]; then
#       echo "========================================================================="
#       echo Observed significance
#       eval $cmd
#       mv higgsCombine*root signif_observed.root
#       
#       echo "========================================================================="
#       echo Observed significance, no systematics
#       eval $cmd -S0
#       mv higgsCombine*root signif_observed_S0.root
#   fi
#
#   echo "========================================================================="
#   echo Expected significance
#   eval $cmd --toys $ntoys -saveToys -s $((JOB+seedbase))
#   mv higgsCombine*root signif_expected_${JOB}.root
#
#   echo "========================================================================="
#   echo Expected significances, no systematics
#   eval $cmd -S0 --toys $ntoys -saveToys -s $((JOB+seedbase))
#   mv higgsCombine*root signif_expected_S0_${JOB}.root
} 2>&1 | gzip -c > combine_output_${JOB}.txtgz

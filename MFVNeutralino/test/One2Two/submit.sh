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

export WD=$(pwd)

source steering.sh

DOOBSERVED=0
if [[ $JOBENV == condor ]]; then
    REALJOB=$1
    mapfile -t JOBMAP < cs_jobmap
    export JOB=${JOBMAP[$REALJOB]}

    if [[ $JOB == 0 ]]; then
        DOOBSERVED=1
    fi
elif [[ $JOBENV == crab ]]; then
    export JOB=$1
    if [[ $JOB == 1 ]]; then
        DOOBSERVED=1
    fi
else
    echo bad JOBENV $JOBENV
    exit 1
fi

echo JOB: ${JOB}
echo JOBENV: ${JOBENV}
echo TESTONLY: ${TESTONLY}
echo ISAMPLE: ${ISAMPLE}
echo DATACARDARGS: ${DATACARDARGS}
echo SAVETOYS: ${SAVETOYS}
echo EXPECTED: ${EXPECTED}
echo NOSYSTEMATICS: ${NOSYSTEMATICS}
echo GOODNESSOFFIT: ${GOODNESSOFFIT}
echo SIGNIFICANCE: ${SIGNIFICANCE}
 
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

if [[ ${JOBENV} == crab ]]; then
    mv $WD/combine.tgz .
else
    xrdcp -s root://cmseos.fnal.gov//store/user/tucker/combine.tgz .
fi

if [[ ! -f combine.tgz ]]; then
    >&2 echo could not copy combine tarball
    exit 1
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
    if [[ $TESTONLY -eq 1 ]]; then
        touch observed.root expected.root
    else
        # don't use -H AsymptoticLimits, at least don't do it for low-efficiency signals, it can lead to way too low limits
        cmd="combine --setTheHint $hint -M MarkovChainMC --noDefaultPrior=0 --tries 20 -b 200 --iteration 100000 datacard.txt"

        if [[ $DOOBSERVED -eq 1 ]]; then
            echo "========================================================================="
            echo Observed limit
            eval $cmd
            mv higgsCombine*root observed.root

            if [[ $NOSYSTEMATICS -eq 1 ]]; then
                echo "========================================================================="
                echo Observed limit, no systematics
                eval $cmd -S0
                mv higgsCombine*root observedS0.root
            fi
        else
            touch observed.root
            [[ $NOSYSTEMATICS -eq 1 ]] && touch observedS0.root
        fi

        ntoys=100
        seedbase=13068931

        if [[ $EXPECTED -ne 0 ]]; then
            echo "========================================================================="
            echo Expected limits
            eval $cmd --toys $ntoys ${SAVETOYSPAR} -s $((JOB+seedbase))
            mv higgsCombine*root expected.root

            if [[ $NOSYSTEMATICS -eq 1 ]]; then 
                echo "========================================================================="
                echo Expected limits, no systematics
                eval $cmd -S0 --toys $ntoys ${SAVETOYSPAR} -s $((JOB+seedbase))
                mv higgsCombine*root expectedS0.root
            fi
        fi

        if [[ $GOODNESSOFFIT -eq 1 ]]; then
            cmd="combine -M GoodnessOfFit --algo=saturated datacard.txt"
         
            if [[ $DOOBSERVED -eq 1 ]]; then
                echo "========================================================================="
                echo GoodnessOfFit observed
                eval $cmd
                mv higgsCombine*root gof_observed.root

                if [[ $NOSYSTEMATICS -eq 1 ]]; then
                    echo "========================================================================="
                    echo GoodnessOfFit observed, no systematics
                    eval $cmd -S0
                    combine -S0 -M GoodnessOfFit datacard.txt --algo=saturated
                    mv higgsCombine*root gof_S0_observed.root
                fi
            fi

            if [[ $EXPECTED -ne 0 ]]; then
                echo "========================================================================="
                echo GoodnessOfFit expected
                eval $cmd --toys $ntoys -s $((JOB+seedbase))
                mv higgsCombine*root gof_expected.root
         
                if [[ $NOSYSTEMATICS -eq 1 ]]; then
                    echo "========================================================================="
                    echo GoodnessOfFit expected, no systematics
                    eval $cmd -S0 --toys ntoys -s $((JOB+seedbase))
                    mv higgsCombine*root gof_S0_expected.root
                fi
        fi

        if [[ $SIGNIFICANCE -eq 1 ]]; then
            cmd="combine -M Significance datacard.txt"
         
            if [[ $DOOBSERVED -eq 1 ]]; then
                echo "========================================================================="
                echo Observed significance
                eval $cmd
                mv higgsCombine*root signif_observed.root
                
                if [[ $NOSYSTEMATICS -eq 1 ]]; then
                    echo "========================================================================="
                    echo Observed significance, no systematics
                    eval $cmd -S0
                    mv higgsCombine*root signif_S0_observed.root
                fi
            fi
         
            if [[ $EXPECTED -ne 0 ]]; then
                echo "========================================================================="
                echo Expected significance
                eval $cmd --toys $ntoys -s $((JOB+seedbase))
                mv higgsCombine*root signif_expected.root
         
                if [[ $NOSYSTEMATICS -eq 1 ]]; then
                    echo "========================================================================="
                    echo Expected significances, no systematics
                    eval $cmd -S0 --toys $ntoys -s $((JOB+seedbase))
                    mv higgsCombine*root signif_S0_expected.root
                fi
            fi
        fi
    fi
} 2>&1 | gzip -c > combine_output.txtgz

if [[ $JOBENV != crab ]]; then
    for bn in *root combine_output.txtgz; do
        bnnew="${bn%.*}"_${JOB}."${bn##*.}"
        mv -v "$bn" "$bnnew"
    done
fi

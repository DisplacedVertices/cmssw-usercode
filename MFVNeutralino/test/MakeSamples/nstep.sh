#!/bin/bash

for fn in lhe.py gensim.py rawhlt.py reco.py ntuple.py minitree.py; do
    if [[ -e $fn ]]; then
        ./todoify.sh $fn > temp
        mv temp $fn
    fi
done

function afteq { echo $1 | cut -d = -f 2; } # crab scriptArgs requires a =

JOBNUM=$1

source steering.sh

INDIR=$(pwd)
OUTDIR=$(pwd)

echo JOBNUM: ${JOBNUM}
echo MAXEVENTS: ${MAXEVENTS}
echo SALT: ${SALT}
echo USETHISCMSSW: ${USETHISCMSSW}
echo FROMLHE: ${FROMLHE}
echo DUMMYFORHASH: ${DUMMYFORHASH}
echo OUTPUTLEVEL: ${OUTPUTLEVEL}
echo TODO: ${TODO}
echo TODO2: ${TODO2}

################################################################################

function scramproj {
    scram project -n $1 CMSSW CMSSW_$2 >/dev/null 2>&1 
    scramexit=$?
    if [[ $scramexit -ne 0 ]]; then
        echo problem with scram project $1 $2
        exit $scramexit
    fi
    cd $1/src
    eval $(scram runtime -sh)
    cd ../..
}

function exitbanner {
    if [[ -e tempfjr.xml ]]; then
        python fixfjr.py
    fi

    if [[ $1 -ne 0 ]]; then
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      echo @@@@ cmsRun exited $2 step with error code $1 at $(date)
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      exit $1
    fi
}

function lhe {
    cmd="cmsRun lhe.py salt=${SALT} jobnum=${JOBNUM} maxevents=${MAXEVENTS} ${TODO}"
    echo $cmd at $(date) ; eval $cmd 2>&1
}

function gensim {
    cmd="cmsRun -j tempfjr.xml gensim.py fromlhe=${FROMLHE} salt=${SALT} jobnum=${JOBNUM} maxevents=${MAXEVENTS} ${TODO}"
    echo $cmd at $(date) ; eval $cmd 2>&1
}

function rawhlt {
    cmd="cmsRun rawhlt.py salt=${SALT} jobnum=${JOBNUM} premix=${PREMIX} ${TODO2}"
    echo $cmd at $(date) ; eval $cmd 2>&1
}

function reco {
    cmd="cmsRun -j tempfjr.xml reco.py premix=${PREMIX} ${TODO2}"
    echo $cmd at $(date) ; eval $cmd 2>&1
}

################################################################################

if [[ $USETHISCMSSW -ne 1 ]]; then
    eval $(scram unsetenv -sh)
fi

################################################################################

if [[ $FROMLHE -eq 1 ]]; then
    echo
    echo START LHE at $(date)
    if [[ $USETHISCMSSW -eq 1 ]]; then
        lhe
    else
        ( scramproj LHE 7_1_16_patch1 && lhe )
    fi
    exitbanner $? LHE
    echo END LHE at $(date)
fi

################################################################################

echo
echo START GENSIM at $(date)
if [[ $USETHISCMSSW -eq 1 ]]; then
    gensim
else
    ( scramproj GENSIM 7_1_21_patch2 && gensim )
fi
exitbanner $? GENSIM
echo END GENSIM at $(date)

if [[ $OUTPUTLEVEL == "gensim" ]]; then
    echo OUTPUTLEVEL told me to exit
    exit 0
fi

################################################################################

echo
echo START RAWHLT at $(date)
if [[ $USETHISCMSSW -eq 1 ]]; then
    rawhlt
else
    ( scramproj RAWHLT 8_0_21 && rawhlt )
fi
exitbanner $? RAWHLT
echo END RAWHLT at $(date)

################################################################################

echo
echo START RECO at $(date)

if [[ $USETHISCMSSW -ne 1 ]]; then
    cd CMSSW_8_0_25/src
    eval $(scram runtime -sh)
    cd ../..
fi

reco
exitbanner $? RECO
echo END RECO at $(date)

################################################################################

if [[ $OUTPUTLEVEL == "minitree" ]]; then
    echo START NTUPLE+MINITREE at $(date)

    echo "process.source.fileNames = ['file:reco.root']" >> ntuple.py
    echo "process.maxEvents.input = -1" >> ntuple.py
    echo cmsRun ntuple.py
    cmsRun ntuple.py ${TODO2} 2>&1

    EXITCODE=${PIPESTATUS[0]}
    if [ $EXITCODE -eq 0 ]; then
        echo NTUPLE nevents $(edmEventSize -v ntuple.root | grep Events)

        echo "process.source.fileNames = ['file:ntuple.root']" >> minitree.py
        echo "process.maxEvents.input = -1" >> minitree.py
        echo cmsRun minitree.py
        cmsRun -j tempfjr.xml minitree.py ${TODO2} 2>&1
        EXITCODE=${PIPESTATUS[0]}
        python fixfjr.py
        if [ $EXITCODE -eq 0 ]; then
            echo MINITREE nevents $(python -c "import sys; sys.argv.append('-b'); import ROOT; f=ROOT.TFile('minitree.root'); print f.Get('tre33/t').GetEntries(), f.Get('tre44/t').GetEntries(), f.Get('mfvMiniTree/t').GetEntries()")
        fi
    fi

    if [ $EXITCODE -ne 0 ]; then
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      echo @@@@ cmsRun exited NTUPLE+MINITREE step with error code $EXITCODE
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      exit $EXITCODE
    fi

    echo END NTUPLE+MINITREE at $(date)
fi

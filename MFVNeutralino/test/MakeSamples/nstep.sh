#!/bin/bash

for fn in lhe.py gensim.py rawhlt.py reco.py ntuple.py minitree.py; do
    if [[ -e $fn ]]; then
        ./todoify.sh $fn > temp
        mv temp $fn
    fi
done

JOBNUM=$1

source steering.sh

INDIR=$(pwd)
OUTDIR=$(pwd)

echo JOBNUM: ${JOBNUM}
echo MAXEVENTS: ${MAXEVENTS}
echo SALT: ${SALT}
echo USETHISCMSSW: ${USETHISCMSSW}
echo FROMLHE: ${FROMLHE}
echo TRIGFILTER: ${TRIGFILTER}
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

function fixfjr {
    if [[ -e tempfjr.xml ]]; then
        python fixfjr.py
    fi
}

function nevents {
    echo $(edmEventSize -v $1 | grep Events)
}

function exitbanner {
    fixfjr

    if [[ $1 -ne 0 ]]; then
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      echo @@@@ cmsRun exited $2 step with error code $1 at $(date)
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      exit $1
    fi

    echo END $2 at $(date) nevents $(nevents ${2,,}.root)
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
    cmd="cmsRun -j tempfjr.xml rawhlt.py salt=${SALT} jobnum=${JOBNUM} premix=${PREMIX} trigfilter=${TRIGFILTER} ${TODO2}"
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
        eval $(scram unsetenv -sh)
    fi

    scramproj LHE 7_1_16_patch1 && lhe
    exitbanner $? LHE

    if [[ $USETHISCMSSW -eq 1 ]]; then
        cd CMSSW_8_0_25/src
        eval $(scram runtime -sh)
        cd ../..
    fi
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

################################################################################

if [[ $OUTPUTLEVEL == "ntuple" || $OUTPUTLEVEL == "minitree" ]]; then
    echo START NTUPLE\|MINITREE at $(date)

    function doit {
        echo "process.source.fileNames = ['file:$2']" >> $1
        echo "process.maxEvents.input = -1" >> $1
        cmd="cmsRun -j tempfjr.xml $1 ${TODO2}"
        echo $cmd at $(date) ; eval $cmd 2>&1
        exitcode=$?
        fixfjr
        return $exitcode
    }

    doit ntuple.py reco.root ; exitcode=$?

    if [[ $exitcode -eq 0 ]]; then
        echo NTUPLE done at $(date) nevents $(nevents ntuple.root)

        if [[ $OUTPUTLEVEL == "minitree" ]]; then
            doit minitree.py ntuple.root ; exitcode=$?
            if [[ $exitcode -eq 0 ]]; then
                echo MINITREE done at $(date) nevents $(python -c "import sys; sys.argv.append('-b'); import ROOT; f=ROOT.TFile('minitree.root'); print f.Get('mfvMiniTreeNtk3/t').GetEntries(), f.Get('mfvMiniTreeNtk4/t').GetEntries(), f.Get('mfvMiniTree/t').GetEntries()")
            fi
        fi
    fi

    if [[ $exitcode -ne 0 ]]; then
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      echo @@@@ cmsRun exited NTUPLE\|MINITREE step with error code $exitcode at $(date)
      echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
      exit $exitcode
    fi

    echo END NTUPLE\|MINITREE at $(date)
fi

################################################################################

echo recap of events in files:
for fn in lhe gensim rawhlt reco ntuple; do
    fn=${fn}.root
    if [[ -e $fn ]]; then
        echo $(nevents $fn)
    else
        echo no file $fn
    fi
done

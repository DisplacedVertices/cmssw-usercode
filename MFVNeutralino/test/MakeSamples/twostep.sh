#!/bin/bash

echo TWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEP
echo twostep.sh called with args:
echo $*
echo NJob is $NJob
echo MaxEvents is $MaxEvents
echo RUNTIME_AREA is $RUNTIME_AREA
echo
#echo PRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENV
#echo printenv
#printenv
#echo PRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENVPRINTENV
echo
echo start gensimhlt step at `date`
echo

cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml pset.py $1 &>/dev/null
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited gensimhlt step with error code $exit_code
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $exit_code
fi

echo NEV `edmEventSize -v gensimhlt.root | grep Events | head -1`

if [ -f my_reco.py ]; then 
  echo
  echo done with gensimhlt step at `date`, starting reco step
  echo
  cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml my_reco.py
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    echo @@@@ cmsRun exited reco step with error code $exit_code
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    exit $exit_code
  fi

  echo NEV `edmEventSize -v reco.root | grep Events | head -1`
fi


if [ -f my_tkdqm.py ]; then
  echo
  echo done with reco at `date`, starting tkdqm
  echo
  cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml my_tkdqm.py
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    echo @@@@ cmsRun exited tkdqm step with error code $exit_code
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    exit $exit_code
  fi
fi

if [ -f pat.py ]; then
  echo
  echo done with reco at `date`, starting pat step
  echo
  cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml pat.py
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    echo cmsRun exited pat step with error code $exit_code
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    exit $exit_code
  fi

  echo NEV `edmEventSize -v pat.root | grep Events | head -1`
fi

if [ -f ntuple.py ]; then
  echo
  echo done with reco at `date`, starting ntuple step
  echo
  cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml ntuple.py
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    echo cmsRun exited ntuple step with error code $exit_code
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    exit $exit_code
  fi

  echo NEV `edmEventSize -v ntuple.root | grep Events | head -1`
fi

if [ -f minitree.py ]; then
  echo
  echo done with ntuple at `date`, starting minitree step
  echo
  cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml minitree.py
  exit_code=$?
  if [ $exit_code -ne 0 ]; then
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    echo cmsRun exited minitree step with error code $exit_code
    echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    exit $exit_code
  fi

  echo NEV `python -c "import sys; sys.argv.append('-b'); import ROOT; f=ROOT.TFile('minitree.root'); print f.Get('mfvMiniTree/t').GetEntries()"`
fi

echo
echo done at `date`
echo TWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEP

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
cmsRun pset.py $1
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited gensimhlt step with error code $exit_code
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $exit_code
fi
echo
echo done with gensimhlt step at `date`, starting reco step
echo
cmsRun -j $RUNTIME_AREA/crab_fjr_$NJob.xml reco.py
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited reco step with error code $exit_code
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $exit_code
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
fi
echo
echo done at `date`
echo TWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEP

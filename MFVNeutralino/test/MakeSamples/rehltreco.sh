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
echo start rawhlt step at $(date)
echo

cmsRun -j first_fjr.xml PSet.py
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited rawhlt step with error code $exit_code
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $exit_code
fi

echo
echo NEV `edmEventSize -v hlt.root | grep Events | head -1`
echo

echo
echo done with rawhlt step at $(date), starting reco step
echo
cmsRun -j last_fjr.xml reco.py
exit_code=$?
if [ $exit_code -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ cmsRun exited reco step with error code $exit_code
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $exit_code
fi

echo
echo NEV `edmEventSize -v reco.root | grep Events | head -1`
echo

echo
echo done with rawhlt step at $(date), merging FJRs
echo
python merge_fjrs.py
if [ $exit_code -ne 0 ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ merge_fjrs.py exited with error code $exit_code
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $exit_code
fi

echo
echo done with everything at $(date)
echo TWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEPTWOSTEP

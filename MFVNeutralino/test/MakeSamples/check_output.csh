#!/bin/tcsh

set dirs="$argv"
echo $dirs
foreach dir ($dirs)
  echo checking $dir
  pushd ${dir}/res > /dev/null
  set stdouts="*.stdout"
  echo '  number of stdouts:' `echo $stdouts | wc -w`
  echo '  jmtok check'
  grep -L JMTOK $stdouts
  echo '  pythia 8.165 check'
  grep -L "PYTHIA version 8.165" $stdouts
  echo '  pat check'
  grep -L 'Summary Table selectedPatCanddiates' $stdouts
  grep 'Summary Table selectedPatCanddiates' $stdouts | grep -v "events total 50"
  popd > /dev/null
  echo
end

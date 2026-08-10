#!/bin/bash

# be in a scratch dir before you run this

echo -n 'need to debug this before running, did you make a copy first? '
read ok

path="$1"
if [[ ! -d $path ]]; then
    echo usage: cleanup.sh path_to_signal_dirs
    exit 1
fi

echo 'jobs with return not 0:'
grep -L 'return value 0' $path/signal_*/log.0
echo -n 'ok? '
read ok

echo 'jobs with stderr not empty:'
find $path -size +0 -name stderr.0 -exec ls -l {} \;
echo -n 'ok? '
read ok

for x in $path/signal_*/results; do
    grep '^num expected' $x
done | sort -nrk 4 | uniq -c
echo -n 'ok? '
read ok

echo 'gzipping various files and trimming combine_outputs'
for x in $path/signal_*; do
    gzip -v $x/{log.0,stdout.0,run.sh,cs_submit.jdl}
    y=$(basename $x)
    echo $y
    mkdir $y
    gunzip -c $x/combine_output.txt.gz | sed 's/Error in estimating posterior is larger than 20.*/Error in estimating posterior is larger than 20/' | uniq -c | sed 's/      1 //' > $y/combine_output.txt.trimmed
done

echo 'recompressing combine outputs'
tar --remove-files -cJvf combine_outputs.txz signal_*
rm $path/signal_*/combine_output.txt.gz
mv combine_outputs.txz $path

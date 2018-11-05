#!/bin/bash

# be in a scratch dir before you run this

path="$1"
if [[ ! -d $path ]]; then
    echo usage: cleanup.sh path_to_signal_dirs
    exit 1
fi

grep -l 'return value 0' $path/signal_*/log.0 | xargs rm

for x in $path/signal_*; do
    gzip -v $x/log.0
    y=$(basename $x)
    echo $y
    mkdir $y
    gunzip -c $x/combine_output.txt.gz | sed 's/Error in estimating posterior is larger than 20.*/Error in estimating posterior is larger than 20/' | uniq -c | sed 's/      1 //' > $y/combine_output.txt.trimmed
done

tar --remove-files -cJvf combine_outputs.txz signal_*
rm $path/signal_*/combine_output.txt.gz
mv combine_outputs.txz $path

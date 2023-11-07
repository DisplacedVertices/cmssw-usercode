#!/bin/bash

ntk=5
indir=/uscms/home/joeyr/crabdirs/MiniTreeV27darksectorreviewm
outdir=output
files=(
mfv_ZprimetoLLPto4j_tau10mm_M2000_950_2016.root
)
intlumi=$(python -c 'import JMTucker.MFVNeutralino.AnalysisConstants as ac; print ac.int_lumi_2015p6 * ac.scale_factor_2015p6')

########################################################################

if [[ -d $outdir ]]; then
    echo $outdir already exists
    exit 1
fi

mkdir $outdir

make
if [[ $? != 0 ]]; then
    exit 1
fi

outbackgrounds=()
outsignals=()

for x in ${files[@]}; do
    fin=$indir/$x
    fout=$outdir/$x
    if [[ ! -e $fin ]]; then
        echo $fin missing
        exit 1
    fi

    echo $x
    ./looptrees.exe $fin $fout $ntk
    if [[ $? != 0 ]]; then
        echo problem, exit code was $?
        exit 1
    fi

    if [[ $x != mfv* ]]; then
        outbackgrounds+=($fout)
    else
        outsignals+=($fout)
    fi
done

# FIXME NOTE! backgrounds are not currently included, ONLY signals
#samples merge -${intlumi} $outdir/background.root ${outbackgrounds[@]}

echo; echo scaling files, do not rerun merge background or use the h_sums in these files after this
for x in ${outbackgrounds[@]} ${outsignals[@]}; do
    y=$outdir/temp.root
    samples merge -${intlumi} $x $y
    mv $x ${x/.root/.unscaled.root}
    mv $y $x
done

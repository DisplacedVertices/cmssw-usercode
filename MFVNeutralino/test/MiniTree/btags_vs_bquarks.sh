#!/bin/bash

version=OnnormdzULV30Lepm

indir=/eos/user/p/pekotamn/MiniTree${version}
files2017=(
	dyjetstollM10_2017.root
	dyjetstollM50_2017.root
	qcdbctoept015_2017.root
	qcdbctoept020_2017.root
	qcdbctoept030_2017.root
	qcdbctoept080_2017.root
	qcdbctoept170_2017.root
	qcdbctoept250_2017.root
	qcdempt020_2017.root
	qcdempt030_2017.root
	qcdempt050_2017.root
	qcdempt080_2017.root
	qcdempt120_2017.root
	qcdempt170_2017.root
	qcdempt300_2017.root
	qcdpt1000mupt5_2017.root
	qcdpt120mupt5_2017.root
	qcdpt15mupt5_2017.root
	qcdpt170mupt5_2017.root
	qcdpt20mupt5_2017.root
	qcdpt300mupt5_2017.root
	qcdpt30mupt5_2017.root
	qcdpt470mupt5_2017.root
	qcdpt50mupt5_2017.root
	qcdpt600mupt5_2017.root
	qcdpt800mupt5_2017.root
	qcdpt80mupt5_2017.root
	ttbar_2017.root
	wjetstolnu_0j_2017.root
	wjetstolnu_1j_2017.root
	wjetstolnu_2j_2017.root
	ww_2017.root
	wz_2017.root
	zz_2017.root
#    qcdht0200_2017.root
#    qcdht0300_2017.root
#    qcdht0500_2017.root
#    qcdht0700_2017.root
#    qcdht1000_2017.root
#    qcdht1500_2017.root
#    qcdht2000_2017.root
#    ttbar_2017.root
#    ttbarht0600_2017.root
#    ttbarht0800_2017.root
#    ttbarht1200_2017.root
#    ttbarht2500_2017.root
#    mfv_neu_tau000100um_M0800_2017.root
#    mfv_neu_tau000300um_M0800_2017.root
#    mfv_neu_tau001000um_M0800_2017.root
#    mfv_neu_tau010000um_M0800_2017.root
#    mfv_neu_tau030000um_M0800_2017.root
#    mfv_neu_tau100000um_M0800_2017.root
#    mfv_stopdbardbar_tau000100um_M0800_2017.root
#    mfv_stopdbardbar_tau000300um_M0800_2017.root
#    mfv_stopdbardbar_tau001000um_M0800_2017.root
#    mfv_stopdbardbar_tau010000um_M0800_2017.root
#    mfv_stopdbardbar_tau030000um_M0800_2017.root
#    mfv_stopdbardbar_tau100000um_M0800_2017.root
)

files2018=(
	dyjetstollM10_2018.root
	dyjetstollM50_2018.root
	qcdbctoept015_2018.root
	qcdbctoept020_2018.root
	qcdbctoept030_2018.root
	qcdbctoept080_2018.root
	qcdbctoept170_2018.root
	qcdbctoept250_2018.root
	qcdempt015_2018.root
	qcdempt020_2018.root
	qcdempt030_2018.root
	qcdempt050_2018.root
	qcdempt080_2018.root
	qcdempt120_2018.root
	qcdempt170_2018.root
	qcdempt300_2018.root
	qcdmupt15_2018.root
	ttbar_2018.root
	wjetstolnu_0j_2018.root
	wjetstolnu_1j_2018.root
	wjetstolnu_2j_2018.root
	ww_2018.root
	wz_2018.root
	zz_2018.root
#    qcdht0200_2018.root
#    qcdht0300_2018.root
#    qcdht0500_2018.root
#    qcdht0700_2018.root
#    qcdht1000_2018.root
#    qcdht1500_2018.root
#    qcdht2000_2018.root
#    ttbar_2018.root
#    ttbarht0600_2018.root
#    ttbarht0800_2018.root
#    ttbarht1200_2018.root
#    ttbarht2500_2018.root
#    mfv_neu_tau000100um_M0800_2018.root
#    mfv_neu_tau000300um_M0800_2018.root
#    mfv_neu_tau001000um_M0800_2018.root
#    mfv_neu_tau010000um_M0800_2018.root
#    mfv_neu_tau030000um_M0800_2018.root
#    mfv_neu_tau100000um_M0800_2018.root
#    mfv_stopdbardbar_tau000100um_M0800_2018.root
#    mfv_stopdbardbar_tau000300um_M0800_2018.root
#    mfv_stopdbardbar_tau001000um_M0800_2018.root
#    mfv_stopdbardbar_tau010000um_M0800_2018.root
#    mfv_stopdbardbar_tau030000um_M0800_2018.root
#    mfv_stopdbardbar_tau100000um_M0800_2018.root
)

for ntk in 3 4 5 7
do
  for year in 2017 2018
  do
    outdir=output_btags_vs_bquarks_MiniTree${version}_ntk${ntk}_${year}

    if [[ $year -eq 2017 ]]; then
      echo "Year is: $year"
      files=("${files2017[@]}")
    elif [[ $year -eq 2018 ]]; then
      echo "Year is: $year"
      files=("${files2018[@]}")
    else
      echo "Invalid year specified ($year). Exiting."
      exit 1
    fi

    intlumi=$(python -c 'import JMTucker.MFVNeutralino.AnalysisConstants as ac; print ac.int_lumi_'${year}' * ac.scale_factor_'${year})

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
            continue
        fi

        echo $x
        ./btags_vs_bquarks.exe $fin $fout $ntk $year
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

    samples merge -${intlumi} $outdir/background.root ${outbackgrounds[@]}

    echo; echo scaling files, do not rerun merge background or use the h_sums in these files after this
    for x in ${outbackgrounds[@]} ${outsignals[@]}; do
        y=$outdir/temp.root
        samples merge -${intlumi} $x $y
        mv $x ${x/.root/.unscaled.root}
        mv $y $x
    done
  done
done

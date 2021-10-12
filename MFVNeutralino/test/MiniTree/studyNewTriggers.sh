#!/bin/bash

indir=/uscms/home/ali/nobackup/LLP/crabdir/MiniTreeV36METm/
#indir=/uscms/home/joeyr/crabdirs/MiniTreeV27Bm
#indir=/uscms_data/d2/tucker/crab_dirs/MiniTreeV27m

splitSUSY2017=(
    qcdht0200_2017.root
    qcdht0300_2017.root
    qcdht0500_2017.root
    qcdht0700_2017.root
    qcdht1000_2017.root
    qcdht1500_2017.root
    qcdht2000_2017.root
    ttbar_2017.root
    #ttbarht0600_2017.root
    #ttbarht0800_2017.root
    #ttbarht1200_2017.root
    #ttbarht2500_2017.root
    zjetstonunuht0100_2017.root
    zjetstonunuht0200_2017.root
    zjetstonunuht0400_2017.root
    zjetstonunuht0600_2017.root
    zjetstonunuht0800_2017.root
    zjetstonunuht1200_2017.root
    zjetstonunuht2500_2017.root
    wjetstolnu_2017.root
    mfv_splitSUSY_tau000000000um_M2000_1800_2017.root
    mfv_splitSUSY_tau000000000um_M2000_1900_2017.root
    mfv_splitSUSY_tau000000000um_M2400_100_2017.root
    mfv_splitSUSY_tau000000000um_M2400_2300_2017.root
    mfv_splitSUSY_tau000001000um_M2000_1800_2017.root
    mfv_splitSUSY_tau000001000um_M2000_1900_2017.root
    mfv_splitSUSY_tau000001000um_M2400_100_2017.root
    mfv_splitSUSY_tau000001000um_M2400_2300_2017.root
    mfv_splitSUSY_tau000010000um_M2000_1800_2017.root
    mfv_splitSUSY_tau000010000um_M2000_1900_2017.root
    mfv_splitSUSY_tau000010000um_M2400_100_2017.root
    mfv_splitSUSY_tau000010000um_M2400_2300_2017.root
    mfv_splitSUSY_tau000100000um_M2000_1800_2017.root
    mfv_splitSUSY_tau000100000um_M2000_1900_2017.root
    mfv_splitSUSY_tau000100000um_M2400_100_2017.root
    mfv_splitSUSY_tau000100000um_M2400_2300_2017.root
    mfv_splitSUSY_tau001000000um_M2000_1800_2017.root
    mfv_splitSUSY_tau001000000um_M2000_1900_2017.root
    mfv_splitSUSY_tau001000000um_M2400_100_2017.root
    mfv_splitSUSY_tau001000000um_M2400_2300_2017.root
    mfv_splitSUSY_tau010000000um_M2000_1800_2017.root
    mfv_splitSUSY_tau010000000um_M2000_1900_2017.root
    mfv_splitSUSY_tau010000000um_M2400_100_2017.root
    mfv_splitSUSY_tau010000000um_M2400_2300_2017.root
    mfv_splitSUSY_tau100000000um_M2000_1800_2017.root
    mfv_splitSUSY_tau100000000um_M2000_1900_2017.root
    mfv_splitSUSY_tau100000000um_M2400_100_2017.root
    mfv_splitSUSY_tau100000000um_M2400_2300_2017.root
)

files2017=(
    #qcdht0500_2017.root
    qcdht0700_2017.root
    qcdht1000_2017.root
    qcdht1500_2017.root
    qcdht2000_2017.root
    #ttbarht0600_2017.root
    #ttbarht0800_2017.root
    #ttbarht1200_2017.root
    #ttbarht2500_2017.root
    #ttbar_2017.root
    mfv_neu_tau000100um_M0400_2017.root
    mfv_neu_tau000100um_M0600_2017.root
    mfv_neu_tau000100um_M0800_2017.root
    mfv_neu_tau000100um_M1200_2017.root
    mfv_neu_tau000100um_M1600_2017.root
    mfv_neu_tau000100um_M3000_2017.root
    mfv_neu_tau000300um_M0400_2017.root
    mfv_neu_tau000300um_M0600_2017.root
    mfv_neu_tau000300um_M0800_2017.root
    mfv_neu_tau000300um_M1200_2017.root
    mfv_neu_tau000300um_M1600_2017.root
    mfv_neu_tau000300um_M3000_2017.root
    mfv_neu_tau001000um_M0400_2017.root
    mfv_neu_tau001000um_M0600_2017.root
    mfv_neu_tau001000um_M0800_2017.root
    mfv_neu_tau001000um_M1200_2017.root
    mfv_neu_tau001000um_M1600_2017.root
    mfv_neu_tau001000um_M3000_2017.root
    mfv_neu_tau010000um_M0400_2017.root
    mfv_neu_tau010000um_M0600_2017.root
    mfv_neu_tau010000um_M0800_2017.root
    mfv_neu_tau010000um_M1200_2017.root
    mfv_neu_tau010000um_M1600_2017.root
    mfv_neu_tau030000um_M0400_2017.root
    mfv_neu_tau030000um_M0600_2017.root
    mfv_neu_tau030000um_M0800_2017.root
    mfv_neu_tau030000um_M1200_2017.root
    mfv_neu_tau030000um_M1600_2017.root
    mfv_neu_tau030000um_M3000_2017.root
    mfv_stopdbardbar_tau000100um_M0400_2017.root
    mfv_stopdbardbar_tau000100um_M0600_2017.root
    mfv_stopdbardbar_tau000100um_M0800_2017.root
    mfv_stopdbardbar_tau000100um_M1200_2017.root
    mfv_stopdbardbar_tau000100um_M1600_2017.root
    mfv_stopdbardbar_tau000100um_M3000_2017.root
    mfv_stopdbardbar_tau000300um_M0400_2017.root
    mfv_stopdbardbar_tau000300um_M0600_2017.root
    mfv_stopdbardbar_tau000300um_M0800_2017.root
    mfv_stopdbardbar_tau000300um_M1200_2017.root
    mfv_stopdbardbar_tau000300um_M1600_2017.root
    mfv_stopdbardbar_tau000300um_M3000_2017.root
    mfv_stopdbardbar_tau001000um_M0400_2017.root
    mfv_stopdbardbar_tau001000um_M0600_2017.root
    mfv_stopdbardbar_tau001000um_M0800_2017.root
    mfv_stopdbardbar_tau001000um_M1200_2017.root
    mfv_stopdbardbar_tau001000um_M1600_2017.root
    mfv_stopdbardbar_tau001000um_M3000_2017.root
    mfv_stopdbardbar_tau010000um_M0400_2017.root
    mfv_stopdbardbar_tau010000um_M0600_2017.root
    mfv_stopdbardbar_tau010000um_M0800_2017.root
    mfv_stopdbardbar_tau010000um_M1200_2017.root
    mfv_stopdbardbar_tau010000um_M1600_2017.root
    mfv_stopdbardbar_tau010000um_M3000_2017.root
    mfv_stopdbardbar_tau030000um_M0400_2017.root
    mfv_stopdbardbar_tau030000um_M0600_2017.root
    mfv_stopdbardbar_tau030000um_M0800_2017.root
    mfv_stopdbardbar_tau030000um_M1200_2017.root
    mfv_stopdbardbar_tau030000um_M1600_2017.root
    mfv_stopdbardbar_tau030000um_M3000_2017.root
)

files2018=(
)

for ntk in 3 4 5
do
  for year in 2017
  do
    outdir=MET_study/output_studyNewTriggers_ntk${ntk}_${year}

    if [[ $year -eq 2017 ]]; then
      echo "Year is: $year"
      #files=("${files2017[@]}")
      files=("${splitSUSY2017[@]}")
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
        
        if [[ $x == *"mfv"* ]]; then
          if [[ $ntk != 5 ]]; then
            echo "Skipping $x"
            continue
          fi
        fi

        fin=$indir/$x
        fout=$outdir/$x
        if [[ ! -e $fin ]]; then
            echo $fin missing
            exit 1
        fi

        echo $x
        ./studyNewTriggers.exe $fin $fout $ntk
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

#!/bin/bash

clobber=clobber

if false; then
    wd=$(pwd)
    y=zzz_bkgsub
    mkdir -p $y
    for ex in nstlaystereomin{1..7}; do   # npxlay2 eta0 eta2 eta4 # default nsigdxy3 nsigdxy5 npxlaymin3 nstlay6 nstlay8 nstlay10 nstlaymin8 nstlaymin10 nstlaystereo{0..7} nstlaystereomin{1..7}; do   # npxlay2 eta0 eta2 eta4
        z=$y/$ex
        echo $z
        if [[ $clobber != "clobber" && -d $z ]]; then
            echo refusing to clobber $z
            continue
        fi
        mkdir $z ; cd $z
        for x in $crd/V0EfficiencyV1_v15/*.root; do
            echo $x
            python $wd/bkgsub.py $x $ex $clobber >$(basename $x .root).log 2>&1
        done
        cd -
    done
fi

if true; then
    for ex in nstlaystereomin{1..7}; do # nsigdxy3 nsigdxy5 npxlaymin3 nstlay6 nstlay8 nstlay10 nstlaymin8 nstlaymin10 nstlaystereo{0..7} nstlaystereomin{1..7}; do
        thedir=zzz_bkgsub/$ex
        for y in h_vtx_rho h_track_dxybs h_track_sigmadxy; do # h_track_pt h_track_eta h_track_phi h_track_npxlayers h_track_nstlayers h_track_dxybs h_track_dzbs h_track_sigmadxy; do
            for x in BCD EF BCDEF H ''; do #B3 C D E F H BCD BCDEF EF ''; do
                python cmp.py $ex $y $thedir/JetHT2016${x}.root $thedir/JetHT2016G.root
                python cmp.py $ex $y $thedir/ZeroBias2016${x}.root $thedir/ZeroBias2016G.root
            done
            #python cmp.py $ex $y $thedir/qcdht1000and1500_hip1p0_mit.root $thedir/qcdht1000and1500.root
        done
    done
fi

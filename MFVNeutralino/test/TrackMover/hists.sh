#!/bin/bash

fns="\
 JetHT2015.root \
 JetHT2015C.root \
 JetHT2015D.root \
 JetHT2016.root \
 JetHT2016B3.root \
 JetHT2016BCD.root \
 JetHT2016BthruG.root \
 JetHT2016C.root \
 JetHT2016D.root \
 JetHT2016E.root \
 JetHT2016EF.root \
 JetHT2016F.root \
 JetHT2016G.root \
 JetHT2016H.root \
 JetHT2016H2.root \
 JetHT2016H3.root \
 qcdht0500sum.root \
 qcdht0500sum_2015.root \
 qcdht0700sum.root \
 qcdht0700sum_2015.root \
 qcdht1000sum.root \
 qcdht1000sum_2015.root \
 qcdht1500sum.root \
 qcdht1500sum_2015.root \
 qcdht2000sum.root \
 qcdht2000sum_2015.root \
 ttbar.root \
 ttbar_2015.root"

echo $fns

for nl in 2 3; do
    for nb in 0 1 2; do
        echo $nl $nb
        z=${nl}${nb}
        mkdir $z
        for x in $fns; do
            ./hists.exe root://cmseos.fnal.gov//store/user/tucker/TrackMoverV1/$z/$x $z/$x $nl $nb
        done
        echo
    done
done
-
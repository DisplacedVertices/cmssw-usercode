
bkgnames=(
  zjetstonunuht
  qcd
)
for ntk in 3 4 5
do
  for b in $bkgnames
  do
    hadd MET_study/output_studyNewTriggers_ntk${ntk}_2017/${b}_sum_2017.root `ls MET_study/output_studyNewTriggers_ntk${ntk}_2017/${b}* | grep -v unscaled`
  done
done
#hadd qcd_sum_2017.root qcdht0700_2017.root qcdht1000_2017.root qcdht1500_2017.root qcdht2000_2017.root
#hadd ttbar_sum_2017.root ttbarht0600_2017.root ttbarht0800_2017.root ttbarht1200_2017.root ttbarht2500_2017.root

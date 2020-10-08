for ntk in 3 4 7 5
do
  for year in 2017 2018
  do
    ln -s 2v_from_jets_${year}_${ntk}track_btags_V27p1Bm.root 2v_from_jets_${year}_${ntk}track_btag_corrected_nom_V27p1Bm.root
  done
done

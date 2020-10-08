#comparehists.py output_btags_vs_bquarks_MiniTreeV27p1Bm_ntk3_2017/background.root "" /publicweb/j/joeyr/plots/btags_vs_bquarks_MiniTreeV7p1Bm_ntk3_2017 --draw-command '"colz text0" if "flavor_code" in name else ""' --nice "MCbackground_2017"
#comparehists.py output_btags_vs_bquarks_MiniTreeV27p1Bm_ntk4_2017/background.root "" /publicweb/j/joeyr/plots/btags_vs_bquarks_MiniTreeV7p1Bm_ntk4_2017 --draw-command '"colz text0" if "flavor_code" in name else ""' --nice "MCbackground_2017"
#comparehists.py output_btags_vs_bquarks_MiniTreeV27p1Bm_ntk5_2017/background.root "" /publicweb/j/joeyr/plots/btags_vs_bquarks_MiniTreeV7p1Bm_ntk5_2017 --draw-command '"colz text0" if "flavor_code" in name else ""' --nice "MCbackground_2017"
#comparehists.py output_btags_vs_bquarks_MiniTreeV27p1Bm_ntk7_2017/background.root "" /publicweb/j/joeyr/plots/btags_vs_bquarks_MiniTreeV7p1Bm_ntk7_2017 --draw-command '"colz text0" if "flavor_code" in name else ""' --nice "MCbackground_2017"

python compare_btags_vs_bquarks.py 2017 3
python compare_btags_vs_bquarks.py 2017 4
python compare_btags_vs_bquarks.py 2017 5
python compare_btags_vs_bquarks.py 2017 7
#python presel_btags_vs_bquarks.py

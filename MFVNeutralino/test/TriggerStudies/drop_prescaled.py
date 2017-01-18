import gzip
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.general import intlumi_from_brilcalc_csv as parse

# 2420  brilcalc lumi -i 2015.json -o 2015.byls.csv --byls --normtag=normtag_2015.json
# 2424  brilcalc lumi -i 2016.json -o 2016.byls.csv --byls --normtag=normtag_2016.json
# 2421  brilcalc lumi -i 2015.json -o 2015.byls.HLT_PFHT800.csv --byls --normtag=normtag_2015.json --hltpath=HLT_PFHT800_v\*
# 2422  brilcalc lumi -i 2016.json -o 2016.byls.HLT_PFHT900.csv --byls --normtag=normtag_2016.json --hltpath=HLT_PFHT900_v\*

ils = [
    (2015, (parse('2015.byls.csv.gz',            False),
            parse('2015.byls.HLT_PFHT800.csv.gz', True))),
    (2016, (parse('2016.byls.csv.gz',            False),
            parse('2016.byls.HLT_PFHT900.csv.gz', True))),
    ]

for year, ((wohlt, wohlt_sum), (whlt, whlt_sum)) in ils:
    print year, wohlt_sum/1e9, whlt_sum/1e9
    good_run_lses = []
    run_lses = sorted(set(wohlt.keys()) & set(whlt.keys()))
    for run_ls in run_lses:
        wohlt_l = wohlt[run_ls]
        whlt_l  = whlt [run_ls]
        if wohlt_l != whlt_l:
            print run_ls, wohlt_l, whlt_l
        else:
            good_run_lses.append(run_ls)
    LumiList(lumis=good_run_lses).writeJSON('ana_%i.json' % year)

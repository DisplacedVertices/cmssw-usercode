import random, sys, gzip
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.general import intlumi_from_brilcalc_csv

def doit(*x):
    print x
    ll_fn, lumi_fn, check_intlumi_sum, goal, out_fn = x

    random.seed(8675309)
    
    goal *= check_intlumi_sum

    in_ll = LumiList(ll_fn).getLumis()
    
    intlumis, intlumi_sum = intlumi_from_brilcalc_csv(lumi_fn, False)
    assert abs(intlumi_sum - check_intlumi_sum) < 1e6
       
    tot = 0.
    out_ll = []
    
    while tot < goal:
        i = random.randrange(len(in_ll))
        rl = in_ll.pop(i)
        #if not intlumis.has_key(rl):
        #    continue
        tot += intlumis[rl]
        out_ll.append(rl)
    
    print 'tot = %f, picked %i lumis' % (tot, len(out_ll))
    LumiList(lumis=out_ll).writeJSON(out_fn)

doit('jsons/ana_2015.json', 'TriggerStudies/2015.byls.csv.gz',  2.691e9, 0.1,  'jsons/ana_2015_10pc.json')  # 1e9 because csv in /ub
doit('jsons/ana_2015.json', 'TriggerStudies/2015.byls.csv.gz',  2.691e9, 0.01, 'jsons/ana_2015_1pc.json')
doit('jsons/ana_2016.json', 'TriggerStudies/2016.byls.csv.gz', 36.814e9, 0.1,  'jsons/ana_2016_10pc.json')
doit('jsons/ana_2016.json', 'TriggerStudies/2016.byls.csv.gz', 36.814e9, 0.01, 'jsons/ana_2016_1pc.json')

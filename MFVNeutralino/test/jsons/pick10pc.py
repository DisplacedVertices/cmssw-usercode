import random, sys, gzip
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.general import intlumi_from_brilcalc_csv

def doit(*x):
    print x
    ll_fn, lumi_fn, check_intlumi_sum, goal, out_fn = x
    check_intlumi_sum *= 1e9 # csv in /ub

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

for year, intlumi in (2017, 41.529), (2018, 50.983):
    for pc in 10, 1:
        doit('ana_%s.json' % year, '/uscms/home/tucker/public/mfv/lumi/%s.byls.csv.gz' % year, intlumi, pc/100., 'ana_%s_%spc.json' % (year, pc))

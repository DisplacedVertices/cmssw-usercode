import random, sys
from FWCore.PythonUtilities.LumiList import LumiList

random.seed(8675309)

in_ll = LumiList('TriggerStudies/jsons/L1_HTT175--ls where bit mask == 0, tot. presc. == 1.json').getLumis()

intlumis = [x.strip().split() for x in open('TriggerStudies/prescales_intlumi.txt') if x.strip()]
intlumis = dict(((int(r),int(l)), float(i)) for r,l,i in intlumis)

tot = 0.
goal = 0.1 * 2.6 * 1e9 # 1e9 bc input file has it in /ub
out_ll = []

while tot < goal:
    i = random.randrange(len(in_ll))
    rl = in_ll.pop(i)
    #if not intlumis.has_key(rl):
    #    continue
    tot += intlumis[rl]
    out_ll.append(rl)

print 'tot = %f, picked %i lumis' % (tot, len(out_ll))
LumiList(lumis=out_ll).writeJSON('ana_10pc.json')

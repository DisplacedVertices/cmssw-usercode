import random, sys, gzip
from FWCore.PythonUtilities.LumiList import LumiList

random.seed(8675309)

ll_fn = 'ana_2016.json'
lumi_fn = '2016.byls.csv.gz'
check_intlumi_sum = 36.814e9 # byls file expected to be in /ub # brilcalc lumi --normtag=normtag_2016.json -i 2016.json --byls -o 2016.byls.csv
goal = 0.01 * check_intlumi_sum
out_fn = 'ana_2016_1pc.json'

in_ll = LumiList(ll_fn).getLumis()

intlumis = {}
intlumi_sum = 0.
with gzip.open(lumi_fn) as lumi_f:
    first = True
    for line in lumi_f:
        line = line.strip()
        if first:
            assert line == '#run:fill,ls,time,beamstatus,E(GeV),delivered(/ub),recorded(/ub),avgpu,source'
            first = False
        else:
            line = line.split(',')
            run = int(line[0].split(':')[0])
            ls0,ls1 = line[1].split(':')
            assert ls0 == ls1 or (ls0 != '0' and ls1 == '0')
            ls = int(ls0)
            intlumi = float(line[-3])
            intlumis[(run, ls)] = intlumi
            intlumi_sum += intlumi

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


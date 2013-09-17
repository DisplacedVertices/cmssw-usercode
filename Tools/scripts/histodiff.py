#!/usr/bin/env python

import sys
from pprint import pprint
from JMTucker.Tools.ROOTTools import ROOT, flatten_directory, check_consistency

fn1, fn2 = fns = [x for x in sys.argv[1:] if '.root' in x]
f1, f2 = fs = [ROOT.TFile(fn) for fn in fns]

d1 = set(flatten_directory(f1))
d2 = set(flatten_directory(f2))

# could remap
#assert sorted(d1) == sorted(d2)

d = sorted(d1 & d2)
in1not2 = sorted(d1 - d2)
in2not1 = sorted(d2 - d1)
print 'warning: not comparing these:'
print 'in f1 not f2:'
pprint(in1not2)
print 'in f2 not f1:'
pprint(in2not1)
print

for n in d:
    #print n
    h1 = f1.Get(n)
    h2 = f2.Get(n)
    if not issubclass(type(h1), ROOT.TH1) or not check_consistency(h1, h2, log='problem with %s:' % n):
        continue
    h = h1.Clone(n + '_subtract')
    h.Add(h2, -1)
    if h.GetEntries() != 0:
        print 'problem with %s: entries differ' % n

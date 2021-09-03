#!/usr/bin/env python

import sys
from pprint import pprint
from DVCode.Tools.ROOTTools import ROOT, flatten_directory, check_consistency

ROOT.TH1.AddDirectory(0)

fn1, fn2 = fns = [x for x in sys.argv[1:] if '.root' in x]
print 'comparing', fn1, fn2
f1, f2 = fs = [ROOT.TFile(fn) for fn in fns]

d1 = set(flatten_directory(f1))
d2 = set(flatten_directory(f2))

# could remap
#assert sorted(d1) == sorted(d2)

d = sorted(d1 & d2)
in1not2 = sorted(d1 - d2)
in2not1 = sorted(d2 - d1)
if 'small' in sys.argv:
    print 'comparing %i hists (and not %i+%i of them)' % (len(d), len(in1not2), len(in2not1))
elif in1not2 or in2not1:
    print 'warning: not comparing these:'
    print 'in f1 not f2:'
    pprint(in1not2)
    print 'in f2 not f1:'
    pprint(in2not1)
    print

problem_seen = False
verbose = 'verbose' in sys.argv
done = {}

for n in d:
    b = n.split('/')[0]
    if verbose:
        print 'comparing', n
    elif not done.has_key(b):
        print 'comparing dir', b
    done[b] = 1

    h1 = f1.Get(n)
    h2 = f2.Get(n)
    if not issubclass(type(h1), ROOT.TH1):
        continue
    if not check_consistency(h1, h2, log='problem with %s:' % n):
        problem_seen = True
        continue
    h = h1.Clone(n + '_subtract')
    h.Add(h2, -1)
    if h.GetEntries() != 0:
        print 'problem with %s: entries differ' % n
        problem_seen = True

sys.exit(1 if problem_seen else 0)

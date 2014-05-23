#!/usr/bin/env python

import sys, os
from JMTucker.Tools.ROOTTools import *
from JMTucker.Tools.Samples import *

p1,p2 = sys.argv[1:3]

for sample in qcd_samples + ttbar_samples:
    fn1 = os.path.join(p1, sample.name + '.root')
    fn2 = os.path.join(p2, sample.name + '.root')
    if not os.path.isfile(fn1) or not os.path.isfile(fn2):
        print 'no', fn1, fn2
        continue
    f1 = ROOT.TFile(fn1)
    f2 = ROOT.TFile(fn2)
    t1 = f1.Get('evids/event_ids')
    t2 = f2.Get('evids/event_ids')
    d1 = detree(t1)
    d2 = detree(t2)
    l1 = list(d1)
    l2 = list(d2)
    s1 = set(l1)
    s2 = set(l2)
    assert sorted(s1) == sorted(l1)
    assert sorted(s2) == sorted(l2)

    print 's1-s2'
    print s1-s2
    print 's2-s1'
    print s2-s1

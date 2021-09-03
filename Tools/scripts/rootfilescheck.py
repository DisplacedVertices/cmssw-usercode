#!/usr/bin/env python

import sys, os
from DVCode.Tools.ROOTTools import ROOT

fns = [x for x in sys.argv if x.endswith('.root')]
nofile = []
probs = []
for fn in fns:
    if not os.path.isfile(fn):
        nofile.append(fn)
    else:
        try:
            f = ROOT.TFile(fn)
            z = []
            for x in f.GetListOfKeys():
                z.append(x.GetName())
        except:
            probs.append(fn)

if probs:
    print 'probs'
    for p in probs:
        print p
if nofile:
    print 'nofile'
    for p in nofile:
        print p
if probs or nofile:
    sys.exit(1)
else:
    print 'all OK'


#!/usr/bin/env python

import sys
from JMTucker.Tools.ROOTTools import ROOT

fn = sys.argv[1]
try:
    path = sys.argv[2]
except IndexError:
    path = None
    print 'just print file'
ls = 'ls' in sys.argv

f = ROOT.TFile(fn)
if path is None:
    f.ls()
else:
    x = f.Get(path)
    if ls:
        x.ls()
    else:
        x.Print()
        nbins = x.GetNbinsX()
        print 'nbins:', nbins
        for i in xrange(0, nbins+2):
            print '%7i %10.1f %10.1f %10.1f' % (i, x.GetBinLowEdge(i), x.GetBinContent(i), x.GetBinError(i))

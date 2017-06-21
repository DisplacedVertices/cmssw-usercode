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
        print '%10s %10s %10s %10s' % ('ibin', 'low edge', 'content', 'error')
        for i in xrange(0, nbins+2):
            if i == 0:
                bin = 'underflow'
            elif i == nbins+1:
                bin = 'overflow'
            else:
                bin = str(i)
            print '%10s %10.2f %10.2f %10.2f' % (bin, x.GetBinLowEdge(i), x.GetBinContent(i), x.GetBinError(i))

#!/usr/bin/env python

import os, sys, time
from math import log, ceil, floor

os.environ['JMT_ROOTTOOLS_NOBATCHMODE'] = '1'
from JMTucker.Tools.ROOTTools import *
set_style()

binning = []
title = []
for arg in sys.argv:
    try:
        binning.append(float(arg))
    except ValueError:
        title.append(arg)

if 0 < len(binning) < 3:
    print 'binning from argv not understood, will figure it out myself'
    binning = []

vals = []

for line in sys.stdin:
    line = line.strip()
    if line:
        try:
            vals.append(float(line))
        except ValueError:
            pass

if vals:
    n = len(vals)
    print 'histogramming %i vals' % n
    if not binning:
        min_ = int(floor(min(vals) * 0.9))-1
        max_ = int(ceil(max(vals) * 1.1))+1
        nbins = max_ - min_
        if n > 50:
            nbins = 1 + log(n, 2)
        nbins = int(ceil(nbins))
        binning = [nbins, min_, max_]
    binning = [int(binning[0]), float(binning[1]), float(binning[2])]
    h = ROOT.TH1D(title[0], ' '.join(title[1:]), *binning)
    print vals
    for v in vals:
        h.Fill(v)
else:
    raise ValueError('no floatable input found')

h.Draw()

ROOT.c1.SaveAs('pipe2hist.root')

while ROOT.c1:
    ROOT.gSystem.ProcessEvents()
    time.sleep(0.01)

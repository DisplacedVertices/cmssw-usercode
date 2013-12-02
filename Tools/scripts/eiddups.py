#!/usr/bin/env python

import sys
from JMTucker.Tools.ROOTTools import *

for arg in sys.argv[1:]:
    if arg.endswith('.root'):
        f = ROOT.TFile(arg)
        x = list(detree(f.Get('eid/event_ids')))
        sx = set(x)
        print arg, len(x), len(sx)


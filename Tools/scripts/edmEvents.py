#!/usr/bin/env python

import sys
from DVCode.Tools.ROOTTools import *
cmssw_setup()

fn = sys.argv[1]
f = ROOT.TFile(fn)
t = f.Get('Events')

for rle in sorted(detree(t, 'EventAuxiliary.id().run():EventAuxiliary.luminosityBlock():EventAuxiliary.id().event()', xform=int)):
    print '(%i,%i,%i),' % rle

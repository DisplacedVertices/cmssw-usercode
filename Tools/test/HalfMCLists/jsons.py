#!/usr/bin/env python
raise NotImplementedError('run2 sample arch')
import sys, os
from FWCore.PythonUtilities.LumiList import LumiList
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples

for fn in sys.argv[1:]:
    if os.path.isfile(fn):
        print fn
        name = os.path.basename(fn).replace('.root', '')
        sample = getattr(Samples, name)
        f = ROOT.TFile(fn)
        t = f.Get('evids/event_ids')
        n = t.GetEntries()
        n2 = int(sample.nevents_orig/2 * sample.ana_filter_eff)
        print '%30s: %s %s %s' % (name, n, n2, '\033[36;7m not equal \033[m' if n != n2 else '')
        rles = list(detree(t))
        assert len(rles) == n

        ll = LumiList(lumis=[(r,l) for r,l,e in rles])
        ll.writeJSON('%s.json' % name)

        

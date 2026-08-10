import sys, os
from collections import defaultdict
from JMTucker.Tools.ROOTTools import *

for fn in sys.argv[1:]:
    f = ROOT.TFile(fn)
    t = f.Get('EventIdRecorder/t')
    dd = defaultdict(int)
    for r,l,e in detree(t):
        assert r == 1
        dd[l] += 1
    z = dd.values()
    print os.path.basename(fn), len(dd), min(z), max(z), sum(z)/len(z)

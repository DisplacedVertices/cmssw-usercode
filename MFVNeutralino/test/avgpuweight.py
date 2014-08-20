import sys, os
from JMTucker.Tools.ROOTTools import *
import JMTucker.Tools.Samples as Samples
set_style()

path = 'pFullSel'

res = []
for fn in sys.argv[1:]:
    if os.path.isfile(fn) and fn.endswith('.root'):
        name = os.path.basename(fn).replace('.root','')
        f = ROOT.TFile(fn)
        t = f.Get('SimpleTriggerResults/t')
        z = list(detree(t, 'weight', path, lambda x: float(x[0])))
        a = '%10.6f' % (sum(z)/len(z)) if z else ''
        res.append((name, len(z), a))

print
for r in res:
    print '%40s %7i %6s' % r


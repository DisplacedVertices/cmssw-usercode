#!/usr/bin/env python

from JMTucker.Tools.ROOTTools import *

f = ROOT.TFile('trees/qcdht1500.root')
t = f.Get('mfvMiniTree/t')
t.SetAlias('dbv0', '(x0*x0 + y0*y0)**0.5')

z = list(detree(t, 'dbv0', 'nvtx==1 && dbv0 > 0.02', xform=float))

f = open('hogg_data.h','wt')
f.write('const int Ndd = %i;\nconst double ddd[Ndd] = {\n' % len(z))
for x in z:
    f.write('%.6e,\n' % x)
f.write('};\n')
f.close()

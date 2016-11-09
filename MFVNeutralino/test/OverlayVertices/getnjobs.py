import sys
from JMTucker.Tools.ROOTTools import *
for x in sys.argv[1:]:
    f = ROOT.TFile(x)
    t = f.Get('mfvMiniTree/t')
    for ntk in [3,4,5]:
        n = t.Draw('1', 'nvtx == 1 && ntk0 == %i' % ntk)
        if n:
            print x, ntk, n

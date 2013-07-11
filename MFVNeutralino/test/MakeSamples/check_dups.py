import sys
from JMTucker.Tools.ROOTTools import *

def check(fn):
    f = ROOT.TFile(fn)
    t = f.Get('MFVGenNtupleDumper/t')

    flt = lambda x: tuple(float(y) for y in x)
    a = list(detree(t, 'lsp_pt:lsp_eta:lsp_phi', '', flt))
    b = list(detree(t, 'lsp_pt:lsp_eta:lsp_mass', '', flt))
    c = list(detree(t, 'lsp_pt:lsp_decay_vx:lsp_decay_vy:lsp_decay_vz', '', flt))

    n = t.GetEntriesFast()
    print n, '->', n*2
    for l in (a,b,c):
        ll = len(l)
        ls = len(set(l))
        print ll, ls
        assert len(l) == len(set(l))

for fn in sys.argv[1:]:
    if fn.endswith('.root'):
        print fn
        check(fn)
        print

import sys, os
from JMTucker.Tools.ROOTTools import *

fns = [fn for fn in sys.argv[1:] if os.path.isfile(fn) and fn.endswith('.root')]
width = max(len(fn) for fn in fns) + 2

cutsets = ['nocuts', 'ntracks', 'all']
print 'fn'.ljust(width), ' '.join('%19s' % x for x in cutsets)

z = []
for fn in fns:
    f = ROOT.TFile(fn)
    print fn.ljust(width),
    zz = []
    for cutset in cutsets:
        num = get_integral(f.Get('%s_npv_num' % cutset))[0]
        den = get_integral(f.Get('%s_npv_den' % cutset))[0]
        r,l,h = wilson_score(num, den)
        e = (h-l)/2
        print '   %6.4f +- %6.4f' % (r, e),
        zz.append((r,e))
    z.append(zz)
    print

if len(z) == 2:
    print 'difference'.ljust(width),
    a,b = z
    for (aa,ea),(bb,eb) in zip(a,b):
        print '   %6.4f +- %6.4f' % (bb-aa, (ea**2 + eb**2)**0.5),

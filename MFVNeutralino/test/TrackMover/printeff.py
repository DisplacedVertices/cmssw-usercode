# for x in $crd/TrackMoverHistsV21mV2/nsig4p0/tau010000um/* ; py printeff.py $x/{JetHT,background_}2017.root

from JMTucker.Tools.ROOTTools import *

fns = root_fns_from_argv()
width = max(len(fn) for fn in fns) + 2

cutsets = ['all', 'nocuts', 'ntracks']
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
        print '   %7.4f +- %7.4f' % (r, e),
        zz.append((r,e))
    z.append(zz)
    print

if len(z) == 2:
    print 'difference'.ljust(width),
    a,b = z
    for (aa,ea),(bb,eb) in zip(a,b):
        print '   %7.4f +- %7.4f' % (bb-aa, (ea**2 + eb**2)**0.5),

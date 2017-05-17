import sys, os
from JMTucker.Tools.ROOTTools import *

fns = [fn for fn in sys.argv[1:] if os.path.isfile(fn) and fn.endswith('.root')]
ml = max(len(fn) for fn in fns)

for fn in sys.argv[1:]:
    if os.path.isfile(fn) and fn.endswith('.root'):
        f = ROOT.TFile(fn)
        print fn.ljust(ml+2),
        for x in 'nocuts', 'ntracks', 'all':
            num = get_integral(f.Get('%s_npv_num'%x))[0]
            den = get_integral(f.Get('%s_npv_den'%x))[0]
            r,l,h = wilson_score(num, den)
            print '   %6.4f +- %6.4f' % (r, (h-l)/2),
        print

               

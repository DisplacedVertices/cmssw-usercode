import os
from JMTucker.Tools.ROOTTools import *

ps = [
    '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_8/',
    '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_7/',
    '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_5/',
]

samples = ['ttbar']

for sample in samples:
    l = []
    for p in ps:
        f = ROOT.TFile(os.path.join(p, '%s.root' % sample))
        t = f.Get('mfvMiniTree/t')
        for x in detree(t, 'lumi:event'):
            l.append(x)
        print sample, len(l)
    l = sorted(set(l))
    print 'after set', sample, len(l)
    fn = 'vetolist.%s' % sample
    f = open(fn, 'wt')
    for x in l:
        f.write('(%i,%i),' % x)
    f.close()
    os.system('gzip %s' % fn)

import os
from JMTucker.Tools.ROOTTools import *

def getlist(root_fn):
    l = []
    f = ROOT.TFile(root_fn)
    t = f.Get('mfvMiniTree/t')
    for x in detree(t, 'lumi:event'):
        l.append(x)
    return sorted(set(l))
    
def writelist(l, out_fn, gzip):
    f = open(out_fn, 'wt')
    for x in l:
        f.write('(%i,%i),\n' % x)
    f.close()
    if gzip:
        os.system('gzip %s' % out_fn)

def makelist(root_fn, out_fn, gzip):
    writelist(getlist(root_fn), out_fn, gzip)

def dosamples():
    ps = [
        '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_8/',
        '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_7/',
        '/uscms_data/d3/jchu/crab_dirs/mfv_763p2/MinitreeV6p1_76x_nstlays3_5/',
    ]

    samples = ['qcdht1000', 'qcdht1500', 'qcdht2000', 'ttbar']

    for sample in samples:
        writelist(sum([getlist(os.path.join(p, '%s.root' % sample)) for p in ps], []), 'vetolist.%s' % sample, True)

#makelist('/uscms_data/d2/tucker/crab_dirs/MinitreeV9_temp/ttbar.root', 'veto_ttbar_temp', False)
dosamples()

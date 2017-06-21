import os, sys, glob
from JMTucker.Tools.ROOTTools import *

def stats(fn_or_f, obs, obs_nosyst, l, header='sigma_sig_limit'):
    if type(fn_or_f) == file:
        f = fn_or_f
    else:
        f = open(fn_or_f, 'wt')
    l.sort()
    n = len(l)
    if n % 2 == 0:
        median = (l[n/2] + l[n/2-1])/2.
    else:
        median = l[n/2]
    lo68 = l[int(n/2 - 0.34*n)]
    hi68 = l[int(n/2 + 0.34*n)]
    lo95 = l[int(n/2 - 0.475*n)]
    hi95 = l[int(n/2 + 0.475*n)]
    f.write(header + ':Expected  2.5%: r < ' + '%f\n' % lo95)
    f.write(header + ':Expected 16.0%: r < ' + '%f\n' % lo68)
    f.write(header + ':Expected 50.0%: r < ' + '%f\n' % median)
    f.write(header + ':Expected 84.0%: r < ' + '%f\n' % hi68)
    f.write(header + ':Expected 97.5%: r < ' + '%f\n' % hi95)
    f.write(header + ':Observed Limit: r < ' + '%f\n' % obs)
    f.write(header + ':NoSystObserved Limit: r < ' + '%f\n' % obs_nosyst)
    f.close()
    return median, lo68, hi68, lo95, hi95

def fromtree(fn):
    f = ROOT.TFile(fn)
    t = f.Get('limit')
    return [x[0] for x in detree(t, 'limit', '', float)]

def doit(path, out_fn):
    x = fromtree(os.path.join(path, 'observed.root'))
    assert len(x) == 1
    obs = x[0]

    x = fromtree(os.path.join(path, 'observed_nosyst.root'))
    assert len(x) == 1
    obs_nosyst = x[0]

    x = fromtree(os.path.join(path, 'expected.root'))
    assert len(x) == 100
    expected = x

    stats(out_fn, obs, obs_nosyst, expected)

if __name__ == '__main__':
    import sys
    doit(sys.argv[1], sys.stdout)

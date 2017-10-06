import os, sys, glob, ROOT
ROOT.gROOT.SetBatch()

def stats(fn_or_f, obs, l, header='sigma_sig_limit'):
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
    f.close()
    return median, lo68, hi68, lo95, hi95

def fromtree(fn):
    l = []
    f = ROOT.TFile(fn)
    t = f.Get('limit')
    for jentry in xrange(t.GetEntriesFast()):
        if t.LoadTree(jentry) < 0: break
        if t.GetEntry(jentry) <= 0: continue
        l.append(t.limit)
    return l

def doit(path, out_fn):
    x = fromtree(os.path.join(path, 'observed.root'))
    assert len(x) <= 1
    if len(x) != 1:
        print 'using observed_byhand for this!'
        x = fromtree(os.path.join(path, 'observed_byhand.root'))
    obs = x[0]

    x = fromtree(os.path.join(path, 'expected.root'))
    assert len(x) >= 99 # maybe one toy crashes, who is zoidberg to judge
    exp = x

    stats(out_fn, obs, exp)

def rrange(path):
    l = fromtree(os.path.join(path, 'expected.root'))
    minl, maxl = min(l), max(l)
    print 'rm *.root %(path)s/observed_byhand.root ; combine -M BayesianToyMC %(path)s/datacard.txt --rMin %(minl)f --rMax %(maxl)f | tee %(path)s/byhand ; mv higgsCombineTest.BayesianToyMC.mH120.root %(path)s/observed_byhand.root' % locals()


if __name__ == '__main__':
    import sys
    path = os.path.abspath(sys.argv[1])

    cmd = '' if len(sys.argv) < 3 else sys.argv[2]
    if cmd == 'rrange':
        rrange(path)
    else:
        doit(path, sys.stdout)

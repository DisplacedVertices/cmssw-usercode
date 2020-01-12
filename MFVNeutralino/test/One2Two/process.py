import os, sys
from glob import glob
from JMTucker.Tools import colors
from JMTucker.Tools.ROOTTools import ROOT, detree
from JMTucker.Tools.hadd import hadd

def stats(fn_or_f, obs, l, header='sigma_sig_limit'):
    if type(fn_or_f) == file:
        f = fn_or_f
    else:
        f = file(fn_or_f, 'wt')
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
    bn = os.path.basename(fn)
    f = ROOT.TFile(fn)
    ll = [x for x in detree(f.Get('limit'), 'limit:iToy', xform=(float,int))]
    if bn.startswith('expected'):
        if len(ll) == 10000: # for some reason, there are two entries for every iToy when --saveToys used
            ll2 = []
            for mi,(l,i) in enumerate(ll):
                assert (mi/2 % 100)+1 == i
                if mi % 2 == 1:
                    ll2.append(l)
                elif mi % 200 == 0: # and the limit value saved in the first entry for the first toy in each batch is ~1e-300!
                    assert l < 1e-300
                elif mi > 0:
                    assert l == ll2[-1]
            assert len(ll2) == 5000
            return ll2
        else:
            assert len(ll) == 5000 and [b for _,b in ll] == range(1,101)*50
            return [a for a,_ in ll]
    else:
        assert bn == 'observed.root' and len(ll) == 1 and ll[0][1] == 0
        return [ll[0][0]]

def doit(path, out_fn):
    x = fromtree(os.path.join(path, 'observed.root'))
    assert len(x) <= 1
    #if len(x) != 1:
    #    print 'using observed_byhand for this!'
    #    x = fromtree(os.path.join(path, 'observed_byhand.root'))
    obs = x[0]

    exp_fn = os.path.join(path, 'expected.root')
    if not os.path.isfile(exp_fn):
        exp_fns = glob(exp_fn.replace('.root','_*.root'))
        if len(exp_fns) != 50 or not hadd(exp_fn, exp_fns):
            raise ValueError('problem hadding %f from %i files' % len(exp_fns))

    exp = fromtree(exp_fn)
    if len(exp) != 5000:
        raise ValueError('unexpected number of points in %s' % exp_fn)

    stats(out_fn, obs, exp)

def rrange(path):
    l = fromtree(os.path.join(path, 'expected.root'))
    minl, maxl = min(l), max(l)
    print 'rm *.root %(path)s/observed_byhand.root ; combine -M BayesianToyMC %(path)s/datacard.txt --rMin %(minl)f --rMax %(maxl)f | tee %(path)s/byhand ; mv higgsCombineTest.BayesianToyMC.mH120.root %(path)s/observed_byhand.root' % locals()


if __name__ == '__main__':
    for path in sys.argv[1:]:
        print path
        doit(path, os.path.join(path, 'results'))

import os, sys, re
from glob import glob
from DVCode.Tools import colors
from DVCode.Tools.ROOTTools import ROOT, detree
from DVCode.Tools.general import bool_from_argv
from DVCode.Tools.hadd import hadd

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

njobs, ntoysperjob = 50, 100
#njobs, ntoysperjob = 5, 20

def fromtree(fn, _jobre=re.compile(r'_(\d+)\.root$')):
    bn = os.path.basename(fn)
    f = ROOT.TFile(fn)
    ll = [x for x in detree(f.Get('limit'), 'limit:iToy', xform=(float,int))]
    if bn.startswith('expected'):
        mo = _jobre.search(bn)
        if mo:
            njobsexp = 1
            ntoysexp = ntoysperjob
        else:
            njobsexp = njobs
            ntoysexp = njobs * ntoysperjob

        if len(ll) == 2*ntoysexp: # for some reason, there are two entries for every iToy when --saveToys used
            ll2 = []
            for mi,(l,i) in enumerate(ll):
                assert (mi/2 % ntoysperjob)+1 == i
                if mi % 2 == 1:
                    ll2.append(l)
                elif mi % 2*ntoysperjob == 0: # and the limit value saved in the first entry for the first toy in each batch is ~1e-300!
                    assert l < 1e-300
                elif mi > 0:
                    assert l == ll2[-1]
            assert len(ll2) == ntoysexp
            return ll2
        else:
            if len(ll) != ntoysexp:
                raise ValueError('fromtree %s failed: len(ll) = %i != %i' % (fn, len(ll), ntoysexp))
            jobordercheck = [b for _,b in ll]
            jobordershouldbe = range(1,ntoysperjob+1)*njobsexp
            if jobordercheck != jobordershouldbe:
                raise ValueError('fromtree %s failed: jobordercheck %r != $r' % (fn, jobordercheck, jobordershouldbe))
            return [a for a,_ in ll]
    else:
        assert bn == 'observed.root' and len(ll) == 1 and ll[0][1] == 0
        return [ll[0][0]]

def doit(path, out_fn):
    x = fromtree(os.path.join(path, 'observed.root'))
    if len(x) != 1:
        print 'using observed_byhand for this!'
        x = fromtree(os.path.join(path, 'observed_byhand.root'))
    obs = x[0]

    exp_fn = os.path.join(path, 'expected.root')
    if not os.path.isfile(exp_fn):
        exp_fns = glob(exp_fn.replace('.root','_*.root'))
        if len(exp_fns) != njobs:
            raise ValueError('only found %i files, expected %i' % (len(exp_fns), njobs))
        if not hadd(exp_fn, exp_fns):
            raise ValueError('problem hadding %s from %s files' % (exp_fn, len(exp_fns)))

    exp = fromtree(exp_fn)
    if len(exp) != njobs*ntoysperjob:
        raise ValueError('unexpected number of points in %s' % exp_fn) # this can't be given the asserts in fromtree right now

    stats(out_fn, obs, exp)

def rrange(path):
    l = fromtree(os.path.join(path, 'expected.root'))
    minl, maxl = min(l), max(l)
    print 'rm *.root %(path)s/observed_byhand.root ; combine -M BayesianToyMC %(path)s/datacard.txt --rMin %(minl)f --rMax %(maxl)f | tee %(path)s/byhand ; mv higgsCombineTest.BayesianToyMC.mH120.root %(path)s/observed_byhand.root' % locals()


if __name__ == '__main__':
    remake = bool_from_argv('remake')
    for path in sys.argv[1:]:
        out_fn = os.path.join(path, 'results')
        if not remake and os.path.isfile(out_fn):
            continue
        print path
        doit(path, out_fn)

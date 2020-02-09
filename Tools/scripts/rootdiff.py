#!/usr/bin/env python

import sys, os
from pprint import pprint
sys.argv.append('-b')
import ROOT

verbose = False
print_only = True
use_pdb = False
relative_diff_allowed = 1e-9
max_rel_diff_seen = 0.

files = [x for x in sys.argv if '.root' in x and os.path.isfile(x)]
if len(files) != 2:
    raise RuntimeError('need two files in sys.argv')

fn0, fn1 = files
f0, f1 = ROOT.TFile(fn0), ROOT.TFile(fn1)
dirs0 = sorted([x.GetName() for x in f0.GetListOfKeys()])
dirs1 = sorted([x.GetName() for x in f1.GetListOfKeys()])
sd0 = set(dirs0)
sd1 = set(dirs1)

if sd0 != sd1:
    print 'list of dirs different!'
    print 'in %s but not in %s:' % (fn0, fn1)
    pprint(sorted(sd0 - sd1))
    print 'in %s but not in %s:' % (fn1, fn0)
    pprint(sorted(sd1 - sd0))
    print 'common:'
    pprint(sorted(sd0 & sd1))

dirs = sorted(sd0 & sd1)

def handle_problem(msg):
    msg = 'PROBLEM ' + msg
    if print_only:
        print msg
    elif use_pdb:
        print msg
        import pdb
        pdb.set_trace()
    else:
        raise RuntimeError(msg)
    
for d in dirs:
    if verbose: print d
    d0, d1 = f0.Get(d), f1.Get(d)
    hs0 = sorted([x.GetName() for x in d0.GetListOfKeys()])
    hs1 = sorted([x.GetName() for x in d1.GetListOfKeys()])
    if hs0 != hs1:
        handle_problem('list of hists different in %s' % d)

    for h in hs0:
        if verbose: print '\t',h
        h0, h1 = d0.Get(h), d1.Get(h)
        if type(h0) != type(h1):
            handle_problem('hist types diff for %s' % h)
            continue

        if 'TH1' not in h0.Class().GetName() or 'TH1' not in h1.Class().GetName():
            handle_problem('skipping %s that is not a TH1...' % h)
            continue

        if h0.GetNbinsX() != h1.GetNbinsX():
            handle_problem('d: %s h: %s nbins diff' % (d, h))
            continue

        for i in xrange(0, h0.GetNbinsX()+1):
            bc0 = h0.GetBinContent(i)
            bc1 = h1.GetBinContent(i)
            if bc0 != bc1:
                rel_diff = abs(bc0 - bc1)/(bc0 + bc1)*2
                max_rel_diff_seen = max(rel_diff, max_rel_diff_seen)
                if rel_diff > relative_diff_allowed:
                    handle_problem('d %s h %s bin %i diff (%f, %f)' % (d,h,i, bc0, bc1))
            bce0 = h0.GetBinError(i)
            bce1 = h1.GetBinError(i)
            if bce0 != bce1:
                rel_diff = abs(bce0 - bce1)/(bce0 + bce1)*2
                max_rel_diff_seen = max(rel_diff, max_rel_diff_seen)
                if rel_diff > relative_diff_allowed:
                    handle_problem('d %s h %s bin error %i diff (%f, %f)' % (d,h,i,bce0,bce1))

print 'max_rel_diff_seen =', max_rel_diff_seen

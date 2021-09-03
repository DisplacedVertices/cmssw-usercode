#!/usr/bin/env python

import os, sys, shutil, re
from fnmatch import fnmatch
from pprint import pprint
from collections import defaultdict
from DVCode.Tools.ROOTTools import *
from DVCode.Tools.general import bool_from_argv

if len(sys.argv) < 5:
    print 'usage: mergeByRunTH1.py in_fn out_fn min_run max_run [glob_pattern_1 ...]'
    sys.exit(1)

yes = bool_from_argv('yes')
in_fn = sys.argv[1]
out_fn = sys.argv[2]
min_run = int(sys.argv[3])
max_run = int(sys.argv[4])
patterns = sys.argv[5:]
def use(path):
    return not patterns or any(fnmatch(path, pattern) for pattern in patterns)

if not os.path.isfile(in_fn):
    print 'no file', in_fn
    sys.exit(1)

if os.path.isfile(out_fn):
    print 'refusing to clobber', out_fn
    sys.exit(1)

shutil.copy2(in_fn, out_fn)

f = ROOT.TFile(out_fn, 'update')
run_re = re.compile(r'(.*)_run(\d+)$')
title_re = re.compile(r'(.*) \(run \d+\)$')
groups = defaultdict(list)

for path in flatten_directory(f):
    if use(path):
        mo = run_re.search(path)
        if mo:
            path_norun, run = mo.groups()
            groups[path_norun].append(path)
            o = f.Get(path)
            if not issubclass(type(o), ROOT.TH1):
                raise ValueError("object %r isn't a TH1" % o)

groups = dict(groups)

print 'will add these groups:'
pprint(groups)
if not yes:
    raw_input('<hit enter if ok>')

for path in sorted(groups.keys()):
    l = groups[path]
    dn, bn = os.path.split(path)
    d = f.Get(dn)
    new_o = f.Get(l[0]).Clone(bn)
    new_o.SetDirectory(d)
    mo = title_re.search(new_o.GetTitle())
    assert mo is not None
    new_o.SetTitle(mo.group(1))
    for o in l[1:]:
        new_o.Add(f.Get(o))
    d.cd()
    new_o.Write()

f.Close()

#!/usr/bin/env python

# this script compares a series hlt menus dumped from the hltGetConfiguration tool
# in order to understand the evolution of a trigger over different versions
# (there are usually just small tweaks, but good to look at this to confirm)

import imp, tempfile, gzip, os, sys
from JMTucker.Tools import colors

wanted_path = None

def module_names(path):
    s = str(path)
    assert '*' not in s
    return s.split('+')

def isint(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parse(fn):
    bn = os.path.basename(fn).replace('.gz','')
    assert isint(bn) and len(bn) == 6

    if sys.modules.has_key(bn):
        x = sys.modules[bn]
    else:
        tmpfn = tempfile.mktemp()
        open(tmpfn, 'wt').write(gzip.open(fn).read())
        x = imp.load_source('p' + bn, tmpfn)
        os.remove(tmpfn)

    ret = None
    for path in x.process.paths.keys():
        if path.startswith(wanted_path):
            if ret:
                raise ValueError('%s found twice in %s' % (wanted_path, fn))
            pobj = x.process.paths[path]
            ver = int(path.replace(wanted_path, ''))
            #ret = x.process, pobj, module_names(pobj), ver
            ret = x.process, module_names(pobj), ver

    if ret is None:
        assert [path.startswith('HLT_') for path in x.process.paths.keys()]
        raise ValueError('%s not found in %s' % (wanted_path, fn))
    return ret

def compare(fn1, fn2):
    pair_name = '%s->%s' % (fn1.replace('.gz',''), fn2.replace('.gz',''))
    process1, names1, ver1 = parse(fn1)
    process2, names2, ver2 = parse(fn2)

    if ver1 != ver2:
        print colors.yellow('%s changed versions %s to %s' % (pair_name, ver1, ver2))

    commn = [n for n in names1 if n in names2]
    commn_diff = []

    for x in commn:
        o1, o2 = [getattr(p, x).dumpPython() for p in process1, process2]
        if o1 != o2:
            if not commn_diff:
                print colors.yellow(pair_name + ' changed these:\n')
            print colors.yellow(x)
            print 'process1.%s =' % x, o1
            print 'process2.%s =' % x, o2
            commn_diff.append(x)

    added = [n for n in names2 if n not in names1]
    deled = [n for n in names1 if n not in names2]
  
    if added:
        print colors.yellow('%s added these: %s\n' % (pair_name, ' '.join(added)))
        for x in added:
            print 'process2.%s =' % x, getattr(process2, x).dumpPython()
    if deled:
        print colors.yellow('%s deled these: %s\n' % (pair_name, ' '.join(deled)))
        for x in deled:
            print 'process1.%s =' % x, getattr(process1, x).dumpPython()

    return commn_diff or added or deled

if __name__ == '__main__':
    wanted_path = sys.argv[1]
    fns = sys.argv[2:]
    del sys.argv[1:] # ?
    for fn1, fn2 in zip(fns, fns[1:]):
        if compare(fn1, fn2):
            print colors.bold('------------------------------------------------------------------\n')

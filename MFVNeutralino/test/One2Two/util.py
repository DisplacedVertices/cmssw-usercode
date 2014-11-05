#!/usr/bin/env python

import os, sys
from pprint import pprint
from JMTucker.Tools.CRABTools import *

if 'lists' in sys.argv:
    clobber = bool_from_argv('clobber')

    to_do = []
    bad = []
    for d in crab_dirs_from_argv():
        lst_fn = os.path.basename(d).replace('crab_', '') + '.lst'
        if os.path.isfile(lst_fn):
            bad.append(lst_fn)
        cmd = 'crtools -outputFromFJR %s noraise | grep root > %s' % (d, lst_fn)
        to_do.append((lst_fn, cmd))

    if bad and not clobber:
        print 'these already exist:'
        pprint(bad)
        raise RuntimeError('refusing to clobber')

    for lst_fn, cmd in to_do:
        print lst_fn
        os.system(cmd)

elif 'draws' in sys.argv:
    for arg in sys.argv:
        if arg.endswith('.lst') and os.path.isfile(arg):
            lst_fn = arg
            out_fn = lst_fn.replace('.lst', '.out')
            print lst_fn
            os.system('python draw_fit.py %s >& %s' % (lst_fn, out_fn))

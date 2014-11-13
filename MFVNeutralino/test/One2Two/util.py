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

elif 'swapplots' in sys.argv:
    try:
        plots_crab = os.readlink('plots_crab')
        plots_asdf = os.readlink('plots_asdf')
        plots = os.readlink('plots')
    except OSError:
        raise RuntimeError('one of plots_crab, plots_asdf, plots missing')
    if plots != plots_crab and plots != plots_asdf:
        raise RuntimeError('bad setup: plots_crab: %s plots_asdf: %s plots: %s' % (plots_crab, plots_asdf, plots))

    os.unlink('plots')
    if plots == plots_crab:
        os.symlink(plots_asdf, 'plots')
    elif plots == plots_asdf:
        os.symlink(plots_crab, 'plots')

elif 'tarball' in sys.argv:
    if not os.path.isdir('plots/'):
        raise RuntimeError('no plots dir')
    os.system('tar czf /tmp/a.tgz plots/')
    print 'pscp -load cmslpc42 tucker@cmslpc42.fnal.gov:/tmp/a.tgz .'

elif 'recrabtar' in sys.argv:
    for d in crab_dirs_from_argv():
        path = os.path.join(d, 'share')
        cmd = 'tar -zxf %(path)s/default.tgz -C %(path)s/ runme.csh mfvo2t.exe' % locals()
        print cmd

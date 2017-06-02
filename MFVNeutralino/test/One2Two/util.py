#!/usr/bin/env python

import os, sys, fnmatch, glob
from pprint import pprint
try:
    from JMTucker.Tools.CRAB3Tools import *
except ImportError:
    print 'no crab'

if 'lists' in sys.argv:
    clobber = bool_from_argv('clobber')

    to_do = []
    bad = []
    for d in crab_dirs_from_argv():
        lst_fn = os.path.basename(d).replace('crab_', '') + '.lst'
        if os.path.isfile(lst_fn):
            bad.append(lst_fn)
        to_do.append((d, lst_fn))

    if bad and not clobber:
        print 'these already exist:'
        pprint(bad)
        raise RuntimeError('refusing to clobber')

    empty = []

    for d, lst_fn in to_do:
        print d, '->', lst_fn
        files = []
        try_count = 0
        while not files:
            if try_count > 0:
                print 'retry %i' % try_count
            files = crab_output_files(d)
            try_count += 1
            if try_count == 4:
                break
        files = ['/store' + x.split('/store')[1] for x in files]
        if len(files) == 0:
            empty.append(d)
        open(lst_fn, 'wt').write('\n'.join(files) + '\n')

    print 'these were empty'
    pprint(empty)

elif 'manuallist' in sys.argv:
    try:
        path = sys.argv[sys.argv.index('manuallist') + 1]
    except IndexError:
        raise RuntimeError('syntax: manuallist path/to/files crab_jobs_list')
    if not os.path.isdir(path):
        raise RuntimeError('path %s does not exist' % path)

    jobs = crab_jobs_from_argv()
    if not jobs:
        raise RuntimeError('no jobs in argv?')

    roots = []
    while not roots:
        paths = glob(os.path.join(path, '*'))
        if all(x.endswith('.root') for x in paths):
            roots = paths
        else:
            assert len(paths) == 1
            path = paths[0]

    for job in jobs:
        root = fnmatch.filter(roots, '*/mfvo2t_%s_?_???.root' % job)
        if len(root) != 1:
            print "don't know what to do with job", job
            pprint(root)
            raise RuntimeError('fix it')
        root = root[0].replace('/eos/uscms/store', '/store')
        print root

elif 'draws' in sys.argv:
    for arg in sys.argv:
        if arg.endswith('.lst') and os.path.isfile(arg):
            lst_fn = arg
            out_fn = lst_fn.replace('.lst', '.draw_fit.out')
            print lst_fn
            os.system('python draw_fit.py %s >& %s' % (lst_fn, out_fn))

elif 'limits' in sys.argv:
    for arg in sys.argv:
        if arg.endswith('.lst') and os.path.isfile(arg):
            lst_fn = arg
            plot_dir = os.path.basename(lst_fn).replace('.lst', '')
            out_fn = lst_fn.replace('.lst', '.limits.out')
            print lst_fn
            os.system('python limits.py %s >& %s' % (lst_fn, out_fn))
            os.system('mv plots/xxxlimits plots/%s' % plot_dir)

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

elif 'exercisefiles' in sys.argv:
    lsts = []
    for x in sys.argv:
        if x.endswith('.lst'):
            lsts.append(x)
            
    for d in crab_dirs_from_argv():
        print d
        d_mangled = d.replace('/', '_')
        lst_fn = '/tmp/tucker/o2ttmp_%s.lst' % d_mangled
        lsts.append(lst_fn)
        os.system('rm -f %s' % lst_fn)
        os.system('crtools -outputFromFJR %s noraise | grep root > %s' % (d, lst_fn))

    for lst in lsts:
        print lst
        from JMTucker.Tools.ROOTTools import ROOT
        for line in open(lst):
            line = line.strip()
            if line:
                line = line.replace('/store', 'root://cmsxrootd.fnal.gov//store')
                print line
                f = ROOT.TFile(line)
                t = f.Get('Fitter/t_fit_info')
                t.Scan('seed')
                f.Close()

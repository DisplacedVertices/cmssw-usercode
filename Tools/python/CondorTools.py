#!/usr/bin/env python

import sys, os, re, fnmatch
from datetime import datetime
from glob import glob
from JMTucker.Tools.general import sub_popen
from JMTucker.Tools.hadd import hadd

class CSHelpersException(Exception):
    pass

def is_cs_dir(d):
    return os.path.isdir(d) and os.path.isfile(os.path.join(d, 'cs_dir'))

def cs_dirs_from_argv():
    return [arg for arg in sys.argv if is_cs_dir(arg)]

def cs_njobs(d):
    return int(open(os.path.join(d, 'njobs')).read())

def cs_cluster(d):
    return int(open(os.path.join(d, 'cluster')).read())

def cs_logs(d):
    return glob(os.path.join(d, 'log.*'))

def cs_job_from_log(fn):
    return int(os.path.basename(fn).replace('log.', ''))

def cs_jobs_running(d):
    jobs = []
    cluster = str(cs_cluster(d))
    for line in sub_popen('condor_q -wide %s' % cluster).stdout:
        if line.startswith(cluster):
            jobs.append(int(line.split()[0].split('.')[1]))
    return jobs

def cs_rets(d, _re=re.compile(r'return value (\d+)')):
    njobs = cs_njobs(d)
    rets = [-1]*njobs

    for log_fn in cs_logs(d):
        job = cs_job_from_log(log_fn)
        for line in open(log_fn):
            mo = _re.search(line)
            if mo:
                ret = int(mo.group(1))
                rets[job] = ret

    return rets

def cs_timestamp():
    return datetime.now().strftime('%y%m%d_%H%M%S')

def cs_hadd(working_dir, new_name=None, new_dir=None, raise_on_empty=False, chunk_size=900, pattern=None):
    if working_dir.endswith('/'):
        working_dir = working_dir[:-1]
    if new_name is None:
        new_name = '_'.join(os.path.basename(working_dir).split('_')[1:])
    if not new_name.endswith('.root'):
        new_name += '.root'
    if new_dir is not None:
        new_name = os.path.join(new_dir, new_name)

    expected = cs_njobs(working_dir)
    print '%s: expecting %i files if all jobs succeeded' % (working_dir, expected)

    files = glob(os.path.join(working_dir, '*.root'))

    if pattern:
        if '/' not in pattern:
            pattern = '*/' + pattern
        files = fnmatch.filter(files, pattern)

    jobs = [int(f.split('_')[-1].split('.root')[0]) for f in files]
    jobs.sort()
    expected = range(expected)

    if jobs != expected:
        print '\033[36;7m %i files found %s not what expected \033[m' % (len(jobs), jobs)
        missing = sorted(set(expected) - set(jobs))
        print '\033[36;7m    %i missing: %r \033[m' % (len(missing), ' '.join(str(j) for j in missing))

    l = len(files)
    if l == 0:
        msg = 'cs_hadd: no files found in %s' % working_dir
        if raise_on_empty:
            raise CSHelpersException(msg)
        else:
            print '\033[36;7m', msg, '\033[m'
    elif l == 1:
        print working_dir, ': just one file found, copying'
        cmd = 'cp %s %s' % (files[0], new_name)
        os.system(cmd)
        os.chmod(new_name, 0644)
    else:
        hadd(new_name, files, chunk_size)

    return new_name

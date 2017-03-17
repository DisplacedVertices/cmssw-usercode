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
    dirs = []
    for arg in sys.argv:
        if is_cs_dir(arg):
            dirs.append(arg)
        elif os.path.isdir(arg):
            for sub in glob(os.path.join(arg, '*')):
                if is_cs_dir(sub):
                    dirs.append(sub)
    return dirs

def cs_njobs(d):
    return int(open(os.path.join(d, 'njobs')).read())

def cs_resubs(d):
    return glob(os.path.join(d, 'resub*'))

def cs_clusters(d):
    return [int(open(os.path.join(p, 'cluster')).read()) for p in [d] + cs_resubs(d)]
    
def cs_kill(d):
    for c in cs_clusters(d):
        os.system('condor_rm %s' % c)

def cs_logs(d):
    return glob(os.path.join(d, 'log.*'))

def cs_job_from_log(fn):
    return int(os.path.basename(fn).replace('log.', ''))

def cs_jobs_running(d):
    jobs = []
    for cluster in cs_clusters(d):
        cluster = str(cluster)
        for line in sub_popen('condor_q -wide %s' % cluster).stdout:
            if line.startswith(cluster):
                jobs.append(int(line.split()[0].split('.')[1]))
    return jobs

def cs_published(d):
    return [line.strip() for fn in glob(os.path.join(d, 'publish_*.txt')) if os.path.isfile(fn) for line in open(fn) if line.strip()]

def cs_analyze(d, 
            _re=re.compile(r'return value (\d+)'),
            _cmsRun_re=re.compile(r"cmsRun exited with code (\d+)"),
            _exception_re=re.compile(r"An exception of category '(.*)' occurred while")):
    class cs_analyze_result:
        def _list(self, ret):
            if type(ret) == int:
                ret = lambda r: ret
            return [i for i,r in enumerate(self.returns) if ret(r)]
        def idle(self):
            return self._list(-1)
        def running(self):
            return self._list(-2)
        def killed(self):
            return self._list(lambda r: r == -3 or r == -4)
        def probs(self):
            return self._list(lambda r: r > 0)
        def done(self):
            return self._list(0)
    result = cs_analyze_result()
    result.working_dir = d
    result.njobs = cs_njobs(d)
    result.returns = [-1] * result.njobs # -1 means idle, -2 means still running
    result.cmsRun_returns = {}
    result.exceptions = {}

    ns = [0]*5

    for log_fn in cs_logs(d):
        job = cs_job_from_log(log_fn)

        ret = -1
        for line in open(log_fn):
            if 'Image size of job updated' in line:
                ret = -2
            elif 'Job was evicted' in line:
                ret = -3
            elif 'Job was aborted by the user' in line:
                ret = -4
            else:
                mo = _re.search(line)
                if mo:
                    ret = int(mo.group(1))

        if ret == 0:
            ns[0] += 1
        elif ret == -1:
            ns[1] += 1
        elif ret == -2:
            ns[2] += 1
        elif ret == -3 or ret == -4:
            ns[3] += 1
        else:
            ns[4] += 1

        result.returns[job] = ret

        if ret > 0:
            stdout_fn = os.path.join(d, 'stdout.%i' % job)
            for line in open(stdout_fn):
                mo = _cmsRun_re.search(line)
                if mo:
                    result.cmsRun_returns[job] = int(mo.group(1))
                mo = _exception_re.search(line)
                if mo:
                    result.exceptions[job] = mo.group(1)

    result.ndone, result.nidle, result.nrun, result.nkilled, result.nprobs = ns
    result.ns = [result.njobs] + ns

    return result

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

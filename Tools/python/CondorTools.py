#!/usr/bin/env python

import sys, os, re, fnmatch, imp
from collections import defaultdict
from datetime import datetime
from glob import glob
from itertools import combinations
import xml.etree.ElementTree as ET
from JMTucker.Tools.LumiJSONTools import fjr2ll
from JMTucker.Tools.general import sub_popen, touch
from JMTucker.Tools.hadd import HaddBatchResult, hadd
from JMTucker.Tools import colors

class CSHelpersException(Exception):
    pass

def is_cs_dir(d):
    return os.path.isdir(d) and os.path.isfile(os.path.join(d, 'cs_dir'))

def cs_dirs(trydirs):
    dirs = []
    for arg in trydirs:
        if is_cs_dir(arg):
            dirs.append(arg)
        elif os.path.isdir(arg):
            for sub in glob(os.path.join(arg, '*')):
                if is_cs_dir(sub):
                    dirs.append(sub)
    r = []
    for d in dirs:
        if d not in r and d is not None:
            r.append(d)
    return r

def cs_dirs_from_argv():
    return cs_dirs(sys.argv)

def cs_done_fn(wd):
    return os.path.join(wd, 'mmon_done')

def is_cs_done(wd):
    return os.path.isfile(cs_done_fn(wd))

def set_cs_done(wd):
    return touch(cs_done_fn(wd))

def cs_fjrs(d):
    return glob(os.path.join(d, 'fjr_*.xml'))

def cs_eventsread(d):
    n = 0
    for fjr_fn in cs_fjrs(d):
        fjr = ET.parse(fjr_fn)
        for f in fjr.findall('InputFile'):
            n += int(f.find('EventsRead').text)
    return n

def cs_eventswritten(d):
    n = 0
    for fjr_fn in cs_fjrs(d):
        fjr = ET.parse(fjr_fn)
        for f in fjr.findall('File'):
            n += int(f.find('TotalEvents').text)
    return n

def cs_njobs(d):
    return int(open(os.path.join(d, 'njobs')).read())

def cs_jobmap(d):
    # takes fake job # (the jobnum in the cluster) to the original real job number
    # same for original submission, for resubdirs can be different
    return dict(enumerate(open(os.path.join(d, 'cs_jobmap')).read().split()))

def cs_realjob(d, job):
    return cs_jobmap(d)[job]

def cs_resubs(d):
    return glob(os.path.join(d, 'resub*'))

def cs_clusters(d):
    return [(p, tuple(open(os.path.join(p, 'cluster')).read().strip().split())) for p in [d] + cs_resubs(d)]

def _cluster2cmd(c, n=False):
    if len(c) == 2:
        if n:
            return '%s -n %s' % c
        else:
            return '%s -name %s' % c
    else:
        assert len(c) == 1
        return c[0]
    
def cs_kill(d):
    for _, c in cs_clusters(d):
        os.system('condor_rm %s' % _cluster2cmd(c))

def cs_output_fn(d, job, kind='stdout'):
    return os.path.join(d, '%s.%s' % (kind, job))

def cs_logs(d):
    return [os.path.join(d, 'log.%i' % i) for i in xrange(cs_njobs(d))]

def cs_job_from_log(fn):
    return int(os.path.basename(fn).replace('log.', ''))

def cs_jobs_running(d):
    jobs = []
    for subdir, cluster in cs_clusters(d):
        for line in sub_popen('condor_q -wide %s' % _cluster2cmd(cluster)).stdout:
            if line.startswith(str(cluster[0])+'.'):
                j = int(line.split()[0].split('.')[1])
                j = cs_realjob(subdir, j)
                jobs.append(int(j))
    return jobs

def cs_primaryds(d):
    return open(os.path.join(d, 'cs_primaryds')).read()

def cs_published(d):
    return [line.strip() for fn in glob(os.path.join(d, 'publish_*.txt')) if os.path.isfile(fn) for line in open(fn) if line.strip()]

def _cs_bn_jobify(d, bn, i):
    a,b = os.path.splitext(bn)
    return os.path.join(d, '%s_%i%s' % (a,i,b))

def cs_outputfiles(d, jobs=None):
    ffn = os.path.join(d, 'cs_outputfiles')
    if not os.path.isfile(ffn):
        return []
    else:
        njobs = cs_njobs(d)
        bns = open(ffn).read().split()
        if jobs is None:
            jobs = list(range(njobs))
        elif type(jobs) == int:
            jobs = [jobs]
        return [_cs_bn_jobify(d, bn, i) for bn in bns for i in jobs]

def cs_rootfiles(d):
    return [fn for fn in glob(os.path.join(d, '*.root')) if os.path.isfile(fn)]

def cs_analyze(d, 
               outputfile_callback=None,
               _re=re.compile(r'return value (\d+)'),
               _ab_re=re.compile(r'Abnormal termination \(signal (\d+)\)'),
               _cmsRun_re=re.compile(r"(?:cmsRun|meat) exited with code (\d+)"),
               _exception_re=re.compile(r"An exception of category '(.*)' occurred while")
               ):

    as_killed = lambda r: r in (-3,-4,-5,-6,-7)

    class cs_analyze_result:
        def _list(self, ret):
            return [i for i,r in enumerate(self.returns) if ret(r)]
        def idle(self):
            return self._list(lambda r: r == -1)
        def running(self):
            return self._list(lambda r: r == -2)
        def killed(self):
            return self._list(lambda r: as_killed(r))
        def probs(self):
            return self._list(lambda r: r > 0)
        def done(self):
            return self._list(lambda r: r == 0)
        def __repr__(self):
            return '<cs_analyze_result idle=%r running=%r killed=%r probs=%r done=%r>' % (self.idle(), self.running(), self.killed(), self.probs(), self.done())

    result = cs_analyze_result()
    result.working_dir = d
    result.njobs = cs_njobs(d)
    result.returns = [-1] * result.njobs # -1 means idle, -2 means still running, -3,-4,-5 mean killed of some sort
    result.cmsRun_returns = {}
    result.exceptions = {}

    ns = [0]*5

    for log_fn in cs_logs(d):
        job = cs_job_from_log(log_fn)
        ret = -1
        if os.path.isfile(log_fn):
            for line in open(log_fn):
                # later lines can override earlier lines, e.g. held = killed, then released -> idle
                if 'Image size of job updated' in line:
                    ret = -2
                elif 'Job was evicted' in line:
                    ret = -3
                elif 'Job executing on host' in line and as_killed(ret):
                    ret = -2
                elif 'Job was released' in line and as_killed(ret):
                    ret = -1
                elif 'Job was aborted by the user' in line:
                    ret = -4
                elif 'Job was held' in line:
                    ret = -5
                else:
                    mo = _ab_re.search(line)
                    if not mo:
                        mo = _re.search(line)
                    if mo:
                        ret = int(mo.group(1))
        else:
            print log_fn, 'is missing'
            ret = -6 # missing log file, either never started or got lost--count as killed

        if ret == 0:
            job_is_resub = os.path.islink(log_fn)
            if job_is_resub:
                resub = os.path.basename(os.path.dirname(os.readlink(log_fn)))
                assert resub.startswith('resub')
            else:
                resub = None

            for out_fn in cs_outputfiles(d, job):
                if not os.path.isfile(out_fn):
                    print out_fn, 'is missing'
                    if job_is_resub: # maybe the symlink was not made/broken
                        out_bn = os.path.basename(out_fn)
                        resub_pfn = os.path.join(resub, out_bn)
                        try_out_fn = os.path.join(d, resub_pfn)
                        if os.path.isfile(try_out_fn):
                            print '... looks like the symlink was broken, %s exists, fixing/making worse mess' % try_out_fn
                            os.symlink(resub_pfn, out_fn)
                        else:
                            ret = -7 # missing output file, ditto comment above
                    else:
                        ret = -7

                if outputfile_callback and os.path.isfile(out_fn) and not outputfile_callback(out_fn, job):
                    print out_fn, 'failed callback'
                    ret = -7

        if ret == 0:
            ns[0] += 1
        elif ret == -1:
            ns[1] += 1
        elif ret == -2:
            ns[2] += 1
        elif as_killed(ret):
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

    result.by_exit = defaultdict(list)
    for i, r in enumerate(result.returns):
        if r > 0:
            #if (result.cmsRun_returns.has_key(i) and result.cmsRun_returns[i] != (0 if r in (147,19) else r) or # xrdcp exit code (?), xrdcp signal socket error
            #    len(result.cmsRun_returns) != 0):
            #        raise ValueError('bad cmsRun return %r for job %i in %s' % (result.cmsRun_returns.get(i), i, d))
            result.by_exit[r].append(i)

    result.by_exception = defaultdict(list)
    for i, e in result.exceptions.iteritems():
        result.by_exception[e].append(i)

    return result

def cs_analyze_mmon(wds):
    results = {}
    for wd in wds:
        ana = cs_analyze(wd)
        results[wd] = {}
        s = results[wd]['jobListByStatus'] = {}
        s2 = results[wd]['jobsPerStatus'] = {}
        s3 = results[wd]['jobsPerStatusEx'] = {}
        for x in 'idle', 'running', 'killed', 'probs', ('done', 'finished'):
            if type(x) != tuple:
                y = x
            else:
                x,y = x
            l = getattr(ana, x)()
            if l:
                s[y] = l
                s2[y] = s3[y] = len(l)
    return results

def cs_timestamp():
    return datetime.now().strftime('%y%m%d_%H%M%S')

def cs_hadd_args(working_dir, new_name=None, new_dir=None):
    if working_dir.endswith('/'):
        working_dir = working_dir[:-1]
    if new_name is None:
        new_name = '_'.join(os.path.basename(working_dir).split('_')[1:])
    if not new_name.endswith('.root'):
        new_name += '.root'
    if new_dir is not None:
        new_name = os.path.join(new_dir, new_name)
    return working_dir, new_name, new_dir

def cs_hadd_files(working_dir, **kwargs):
    expected = cs_njobs(working_dir)
    files = cs_published(working_dir)
    if not files:
        files = cs_rootfiles(working_dir)
    rf = kwargs.get('range_filter')
    if rf:
        a,b,c = rf
        files = files[a:b:c]
    return expected, files

def cs_hadd(working_dir, new_name=None, new_dir=None, raise_on_empty=False, chunk_size=900, pattern=None, range_filter=None):
    working_dir, new_name, new_dir = cs_hadd_args(working_dir, new_name, new_dir)
    expected, files = cs_hadd_files(working_dir, range_filter=range_filter)
    result = HaddBatchResult('condor', working_dir, new_name, new_dir, expected, files)
    print '%s: expecting %i files if all jobs succeeded' % (working_dir, expected)

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
        result.success = False
        msg = 'cs_hadd: no files found in %s' % working_dir
        if raise_on_empty:
            raise CSHelpersException(msg)
        else:
            print '\033[36;7m', msg, '\033[m'
    elif l == 1:
        print working_dir, ': just one file found, copying'
        if files[0].startswith('root://'):
            cmd = 'xrdcp -s %s %s' % (files[0], new_name)
        else:
            cmd = 'cp %s %s' % (files[0], new_name)
        result.success = os.system(cmd) == 0
        if result.success and not new_name.startswith('root://'):
            os.chmod(new_name, 0644)
    else:
        result.success = hadd(new_name, files)

    return result

def cs_report(wd, partial=False):
    njobs = cs_njobs(wd)
    lls = []

    for i in xrange(njobs):
        fjr_fn = os.path.join(wd, 'fjr_%i.xml' % i)
        if os.path.isfile(fjr_fn):
            lls.append((i, fjr2ll(fjr_fn)))
        elif partial:
            print colors.yellow('missing fjr %s but partial allowed' % fjr_fn)
        else:
            raise IOError('missing fjr %s' % fjr_fn)

    for (ia,lla),(ib,llb) in combinations(lls,2):
        if lla & llb:
            problem = 'problem with fjrs for %s: overlap found in pair %i + %i\n' % (wd,ia,ib)
            problem += repr((ia, lla)) + '\n'
            problem += repr((ib, llb)) + '\n'
            problem += 'and ' + repr(lla & llb) + '\n'
            raise ValueError(problem)

    ll_all = lls.pop()[1]
    for _,ll in lls:
        ll_all |= ll
    ll_all.writeJSON(os.path.join(wd, 'processedLumis.json'))
    return ll_all

def cs_last_input_file(wd, job):
    _r = re.compile(r'(/store.*\.root)')
    for line in reversed(file(cs_output_fn(wd, job)).readlines()):
        mo = _r.search(line)
        if mo:
            return mo.group(1)

def cs_prio(wd, prio):
    for _, c in cs_clusters(wd):
        os.system('condor_prio %s %s' % (prio, _cluster2cmd(c, n=True)))

def cs_filelist(wd):
    fn = os.path.join(wd, 'cs_filelist.py')
    if not os.path.isfile(fn):
        raise IOError('no %s' % fn)
    m = imp.load_source('dummy', fn)
    return m._l

__all__ = [
    'is_cs_dir',
    'cs_dirs',
    'cs_dirs_from_argv',
    'cs_done_fn',
    'is_cs_done',
    'set_cs_done',
    'cs_fjrs',
    'cs_eventsread',
    'cs_eventswritten',
    'cs_njobs',
    'cs_jobmap',
    'cs_realjob',
    'cs_resubs',
    'cs_clusters',
    'cs_kill',
    'cs_output_fn',
    'cs_logs',
    'cs_job_from_log',
    'cs_jobs_running',
    'cs_primaryds',
    'cs_published',
    'cs_outputfiles',
    'cs_rootfiles',
    'cs_analyze',
    'cs_analyze_mmon',
    'cs_timestamp',
    'cs_hadd_args',
    'cs_hadd',
    'cs_report',
    'cs_last_input_file',
    'cs_prio',
    'cs_filelist',
    ]

if __name__ == '__main__':
    pass

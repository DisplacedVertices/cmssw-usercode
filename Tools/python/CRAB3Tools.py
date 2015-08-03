#!/usr/bin/env python

# author: J. Tucker

import cPickle
import getpass
import glob
import httplib
import multiprocessing
import json
import os
import pycurl
import sys
import time
import zlib
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from collections import defaultdict
from cStringIO import StringIO
from pprint import pprint
from JMTucker.Tools.general import bool_from_argv, typed_from_argv, popen
from JMTucker.Tools.hadd import hadd
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config as Config
from CRABClient.UserUtilities import getUsernameFromSiteDB

class CRABToolsException(Exception):
    pass

class CRABToolsGlobalOptions:
    def __init__(self, cfg_path=os.path.expanduser('~/.jmtct')):
        self.cfg_path = cfg_path

        if os.path.isfile(self.cfg_path):
            self.cfg = ConfigParser()
            self.cfg.read(self.cfg_path)

            def get_default(section, name, default):
                try:
                    return self.cfg.get(section, name)
                except (NoSectionError, NoOptionError):
                    return default

            self.allow_insecure_stupidity = get_default('Global', 'allow_insecure_stupidity', False) == 'True'
            self.crab_dirs_root = get_default('Global', 'crab_dirs_root', '/dev/null')
        else:
            raise IOError('no such file %s' % cfg_path)

crab_global_options = CRABToolsGlobalOptions()

def crab_dirs_root(ex=''):
    if not os.path.isdir(crab_global_options.crab_dirs_root):
        os.makedirs(crab_global_options.crab_dirs_root)
    if ex:
        return os.path.join(crab_global_options.crab_dirs_root, ex) # caller expected to mkdir ex as crab does for config.General.workArea
    else:
        return crab_global_options.crab_dirs_root

def crabify_list(l, simple=False):
    if simple:
        return ','.join(str(x) for x in sorted(l))

    a = b = None
    s = []
    def sforab(a,b):
        if a == b:
            return str(a)
        else:
            return '%i-%i' % (a,b)
    for x in sorted(l):
        if a is None:
            a = x
            b = x
        elif x == b+1:
            b = x
        else:
            s.append(sforab(a,b))
            a = b = x
        #print a, b, s
    s.append(sforab(a,b))
    return ','.join(s)

def decrabify_list(s):
    if s.lower() == 'all':
        raise CrabError('warning: decrabify_list does not support "all"')
    s = s.split(',')
    l = []
    for x in s:
        if '-' in x:
            y,z = x.split('-')
            l += range(int(y), int(z)+1)
        else:
            l.append(int(x))
    return l

def crab_jobs_from_list(from_list):
    jobs = []
    for x in from_list:
        was_list = False
        try:
            l = decrabify_list(x)
            if l:
                jobs += l
                was_list = True
        except ValueError:
            pass
        if not was_list:
            try:
                j = int(x)
                jobs.append(j)
            except ValueError:
                pass
    jobs.sort()
    return jobs

def crab_jobs_from_argv():
    return crab_jobs_from_list(sys.argv)

def is_crab_working_dir(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, '.requestcache'))

def crab_working_dirs(path=''):
    return [d for d in glob.glob(os.path.join(path, 'crab_*')) if is_crab_working_dir(d)]
    
def last_crab_working_dir(path=''):
    dirs = [(d, os.stat(d).st_mtime) for d in crab_working_dirs(path)]
    if dirs:
        dirs.sort(key=lambda x: x[1])
        return dirs[-1][0]

def crab_dirs_from_argv():
    dirs = []

    if 'all' in sys.argv:
        dirs = crab_working_dirs()
    elif 'except' in sys.argv:
        dirs = [d for d in crab_working_dirs() if d not in sys.argv]
    elif len(sys.argv) > 1:
        for d in sys.argv[1:]:
            if is_crab_working_dir(d):
                dirs.append(d)
            elif os.path.isdir(d):
                # if we have a dir of crab dirs, take all of them
                for dd in glob.glob(os.path.join(d, '*')):
                    if is_crab_working_dir(dd):
                        dirs.append(dd)

    if not dirs:
        dirs = [last_crab_working_dir()]

    # make sure each entry is in only once, but don't use
    # list(set(dirs)) because we want to keep the sorted order
    r = []
    for d in dirs:
        if d not in r and d is not None:
            r.append(d)

    return r

def crab_dir_from_argv():
    d = crab_dirs_from_argv()
    if len(d) != 1:
        raise CRABToolsException('exactly one directory in argv expected')
    return d[0]

def crab_cleanup(extra=[]):
    to_remove = [] #['crab.history', 'SiteDBusername.conf', 'server_legnaro.conf'] + extra #+['glite_wms_CERN.conf', 'glite.conf.CMS_CERN']
    for f in to_remove:
        if os.path.isfile(f):
            os.remove(f)

def crab_get_and_save_grid_passphrase(path=None):
    if not crab_global_options.allow_insecure_stupidity:
        raise ValueError('allow_insecure_stupidity is not set')

    if path is None:
        path = os.path.expanduser('~/.jmtctgpp')

    print '''
*******************************************************************************
WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING

DO NOT, under any circumstances, enter your GRID passphrase at the prompts.
It will not be treated securely, and may end up in the hands of anyone.

WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING WARNING
*******************************************************************************
'''

    while 1:
        pp = getpass.getpass('GRID passphrase:')
        pp2 = getpass.getpass('again:')
        if pp != pp2 or len(pp) < 4:
            print 'did not match'
        else:
            break

    open(path, 'wt').write(zlib.compress(pp))
    os.chmod(path, 0400)
    return pp

def crab_load_grid_passphrase(path=None):
    if not crab_global_options.allow_insecure_stupidity:
        raise ValueError('allow_insecure_stupidity is not set')

    if path is None:
        path = os.path.expanduser('~/.jmtctgpp')
    if os.path.isfile(path):
        return zlib.decompress(open(path).read())
    else:
        return crab_get_and_save_grid_passphrase(path)

def crab_need_renew_proxy(min_hours=144):
    # JMTBAD should use the CRAB function if exists in v3
    if os.system('voms-proxy-info -exists -valid %i:0' % min_hours) != 0:
        return True
    out = popen('myproxy-info -d -s myproxy.cern.ch')
    for line in out.split('\n'):
        if 'timeleft' in line:
            return int(line.split(':')[1]) < min_hours
    print '\033[36;7m warning: \033[m crab_need_renew_proxy could not parse output of myproxy-info'
    return True

def crab_renew_proxy_if_needed(min_hours=144):
    if crab_need_renew_proxy(min_hours):
        if crab_global_options.allow_insecure_stupidity:
            try:
                import pexpect
            except ImportError:
                raise ImportError('need pexpect module to do this insecure stupidity')
            pp = crab_load_grid_passphrase()
            p = pexpect.spawn('voms-proxy-init -voms cms -valid 192:00')
            p.expect('.*GRID.*:')
            p.sendline(pp)
            p.interact()
            p = pexpect.spawn('myproxy-init -d -n -s myproxy.cern.ch')
            p.expect('.*GRID.*:')
            p.sendline(pp)
            p.interact()
        else:
            os.system('voms-proxy-init -voms cms -valid 192:00')
            os.system('myproxy-init -d -n -s myproxy.cern.ch')

def crab_job_lists_by_status(result):
    d = defaultdict(list)
    for status, job in result['jobList']:
        d[status].append(job)
    return dict(d)

def crab_command(*args, **kwargs):
    # Only call this once per process -- if you want to do tasks in
    # parallel, use multiprocessing, not threads. See
    # crab_multiprocess below.

    def from_kwargs(key, default):
        if kwargs.has_key(key):
            val = kwargs[key]
            del kwargs[key]
            return val
        else:
            return default

    cache_file = from_kwargs('cache_file', '/tmp/crab3.%i.%s' % (os.getpid(), str(int(time.time()*1e6))))
    old_cache_file = os.environ.get('CRAB3_CACHE_FILE', '')
    open(cache_file, 'wt').write('{"crab_project_directory": ""}')
    os.environ['CRAB3_CACHE_FILE'] = cache_file

    suppress_stdout = from_kwargs('suppress_stdout', True)
    if suppress_stdout:
        old_stdout = sys.stdout
        sys.stdout = buf = StringIO()

    try:
        result = crabCommand(*args, **kwargs)
    except httplib.HTTPException, e:
        result = {}
        result['jobList'] = []
        result['HTTPException'] = e
        result['status'] = 'HTTPException'

    if suppress_stdout:
        result['stdout'] = buf.getvalue()
        sys.stdout = old_stdout

    os.remove(cache_file)
    os.environ['CRAB3_CACHE_FILE'] = old_cache_file

    return result

def crab_multiprocess(fcn, dirs, max_processes):
    # fcn must return 2-tuple (dir, result), and can't be a class instance method
    if max_processes == 1:
        results = [fcn(d) for d in dirs]
    else:
        pool = multiprocessing.Pool(max_processes)
        results = pool.map(fcn, dirs)
        pool.close()
        pool.join()
    return results

def crab_status(working_dir, verbose=True):
    if verbose:
        print 'checking', working_dir

    #if options.run_in_debugger:
    #    print 'running process for %s in debugger' % working_dir
    #    pdb.set_trace()

    # options.debug_output
    # options.resub_any
    # options.resub_done_stuck
    # options.resub_none
    # options.resub_site_control
    # options.status_until_none_done
    # options.resub_created
    # options.resub_white_codes
    # options.resub_black_codes

    result = crab_command('status', '--long', dir=working_dir)

    jl = crab_job_lists_by_status(result)
    if not jl:
        jl = {'crmonerror': xrange(9999)}
        result['jobsPerStatus'] = {'crmonerror': 9999}
    result['jobListByStatus'] = jl

    result['jobsPerStatusEx'] = d = dict(result['jobsPerStatus'])
    if d.has_key('failed'):
        del d['failed']
        for job_num, job_info in result['jobs'].iteritems():
            if job_info['State'] == 'failed':
                state_ex = 'failed_%i' % job_info['Error'][0]
                if d.has_key(state_ex):
                    d[state_ex] += 1
                else:
                    d[state_ex] = 1

    #if post_process_fcn is not None:
    #    post_process_fcn(working_dir, result)

    #if not options.keep_exe_code:
    #    result_final = {}
    #    for k,v in result.iteritems():
    #        if k.startswith('Retrieved') and k.count('_') == 2:
    #            k = k.split('_')
    #            k = k[0] + '_' + k[-1]
    #        if result_final.has_key(k):
    #            res_final[k].extend(v)
    #        else:
    #            res_final[k] = v
    #    result = res_final

    return working_dir, result

def crab_process_statuses(working_dirs, max_processes, verbose=True):
    if verbose:
        print 'launching processes...'
    results = crab_multiprocess(crab_status, working_dirs, max_processes)
    if verbose:
        print 'done waiting for processes!'
    return results

def crab_process_statuses_with_redo(working_dirs, max_processes, verbose=True):
    results = dict(crab_process_statuses(working_dirs, max_processes, verbose))

    def redoable(res):
        return res.has_key('HTTPException') or \
               'Timeout when waiting for remote host' in res.get('taskFailureMsg', '')

    to_redo = [d for d, res in results.iteritems() if redoable(res)]

    if to_redo:
        if verbose:
            print 'redo these that had possibly transient problems:'
            pprint(to_redo)
        results.update(dict(crab_process_statuses(to_redo, max_processes, verbose)))

    if verbose:
        for d,res in results.iteritems():
            if res['jobsPerStatus'].keys() == ['crmonerror'] and not redoable(res):
                print "for %s, no job list but not redoable either, here's the entire res" % d
                print repr(res)

    return results

def crab_output_files(working_dir, jobs=None):
    if jobs is not None:
        d = crab_command('getoutput', '--xrootd', '--jobids=%s' % crabify_list(jobs, simple=True), dir=working_dir)
    else:
        d = crab_command('getoutput', '--xrootd', dir=working_dir)
    return d.get('xrootd', [])

'''
def crab_hadd(working_dir, new_name=None, new_dir=None, raise_on_empty=False, chunk_size=900):
    if working_dir.endswith('/'):
        working_dir = working_dir[:-1]
    if new_name is None:
        new_name = os.path.basename(working_dir).replace('crab_','')
    if not new_name.endswith('.root'):
        new_name += '.root'
    if new_dir is not None:
        new_name = os.path.join(new_dir, new_name)

    expected = crab_get_njobs(working_dir)
    print '%s: expecting %i files if all jobs succeeded' % (working_dir, expected)

    on_store = False
    cfg = crab_cfg_parser(working_dir)
    try:
        storage_element = cfg.get('USER', 'storage_element')
        on_store = storage_element == 'T3_US_FNALLPC'
    except NoOptionError:
        pass

    files = []
    
    if on_store:
        pfns = []
        for path in glob.glob(os.path.join(working_dir, 'res/crab_fjr*xml')):
            if crab_get_exit_codes(path) == (0,0):
                pfns.append(crab_analysis_file_pfn(path))
        files = ['root://cmsxrootd.fnal.gov//store' + pfn.split('/store')[1] for pfn in pfns] # JMTBAD
    else:    
        files = glob.glob(os.path.join(working_dir, 'res/*root'))

    job_nums = defaultdict(lambda: defaultdict(list))
    for f in files:
        f_ = f.split('_')
        job, num = int(f_[-3]), int(f_[-2])
        job_nums[job][num].append(f)

    sexpected = set(xrange(1,expected+1))
    sjobs = set(job_nums)
    if sjobs != sexpected:
        print '\033[36;7m %i files found %s not what expected \033[m' % (len(sjobs), crabify_list(sorted(sjobs)))

        missing = sorted(sexpected - sjobs)
        print '\033[36;7m    %i missing: %r \033[m' % (len(missing), crabify_list(missing))

        to_drop = []
        for job, nums_and_fs in job_nums.iteritems():
            for num, fs in nums_and_fs.iteritems():
                if len(fs) > 1:
                    print '\033[36;7m     for job %i, more than one file with resub num %i *** will keep latest by mtime *** \033[m' % (job, num)
                    fs.sort(key=lambda f: os.stat(f).st_mtime)
                    good_f = fs[-1]
                    while len(fs) > 1:
                        bad_f = fs.pop(0)
                        to_drop.append((bad_f, good_f))
            if len(nums_and_fs) > 1:
                good_num = max(nums_and_fs)
                assert len(nums_and_fs[good_num]) == 1
                good_f = nums_and_fs[good_num][0]
                for num, fs in nums_and_fs.iteritems():
                    if num != good_num:
                        assert len(fs) == 1
                        to_drop.append((fs[0], good_f))

        for f, good_f in to_drop:
            print '\033[36;7m     dropping %s in favor of %s \033[m' % (f, good_f)
            files.remove(f)

    
    l = len(files)
    if l == 0:
        msg = 'crab_hadd: no files found in %s' % working_dir
        if raise_on_empty:
            raise CrabError(msg)
        else:
            print '\033[36;7m', msg, '\033[m'
    elif l == 1:
        print working_dir, ': just one file found, copying'
        cmd = '%scp %s %s' % ('dc' if 'dcap' in files[0] else '', files[0], new_name)
        os.system(cmd)
        os.chmod(new_name, 0644)
    else:
        hadd(new_name, files, chunk_size)

    return new_name
'''

def crab_requestcache(working_dir):
    return cPickle.load(open(os.path.join(working_dir, '.requestcache'), 'rb'))

def crab_results_by_task_status(results):
    d = defaultdict(dict)
    for working_dir, res in results.iteritems():
        d[res['status']][working_dir] = dict(res)
    return d

class UserCacheHelper:
   def __init__(self, proxy=None, user=None):
      if proxy is None:
         proxy = os.getenv('X509_USER_PROXY')
         if not proxy or not os.path.isfile(proxy):
            raise CRABToolsException('X509_USER_PROXY is %r, get grid proxy first' % proxy)
      self.proxy = proxy

      if user is None:
         user = getUsernameFromSiteDB()
         if not user:
            raise CRABToolsException('could not get username from sitedb, returned %r' % user)
      self.user = user

   def _curl(self, url, debug=False, raw=False):
      buf = StringIO()
      c = pycurl.Curl()
      c.setopt(pycurl.URL, str(url))
      c.setopt(pycurl.WRITEFUNCTION, buf.write)
      c.setopt(pycurl.SSL_VERIFYPEER, False)
#      c.setopt(pycurl.SSL_VERIFYHOST, False)
      c.setopt(pycurl.SSLKEY, self.proxy)
      c.setopt(pycurl.SSLCERT, self.proxy)
      if debug:
          def debug_callback(debug_type, msg):
              print 'curl debug(%s): %s' % (debug_type, msg)
          c.setopt(pycurl.VERBOSE, 1)
          c.setopt(pycurl.DEBUGFUNCTION, debug_callback)
      c.perform()
      c.close()

      if raw:
          return buf.getvalue()

      j = buf.getvalue().replace('\n','')
      try:
         j = json.loads(j)
      except ValueError:
         raise CRABToolsException('json decoding problem: %r' % j)
      
      k = sorted(j.keys())
      if k == ['result']:
         return j['result']
      elif k == ['desc', 'result'] and j['desc'].keys() == ['columns']:
         return dict(zip(j['desc']['columns'], j['result']))
      else:
         return j

   def _only(self, l):
      if len(l) != 1:
         raise CRABToolsException('return value was supposed to have one element, but: %r' % l)
      return l[0]

   def listusers(self):
      return self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=listusers')

   def userinfo(self):
      return self._only(self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=userinfo&username=' + self.user))

   def quota(self):
      return self._only(self.userinfo()['used_space'])

   def filelist(self):
      return self.userinfo()['file_list']

   def fileinfo(self, hashkey):
      return self._only(self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=fileinfo&hashkey=' + hashkey))

   def fileinfos(self):
      return [self.fileinfo(x) for x in self.filelist() if '.log' not in x] # why doesn't it work for e.g. '150630_200330:tucker_crab_repubmerge_tau0300um_M0400_TaskWorker.log' (even after quoting the :)?

   def fileremove(self, hashkey):
      x = self._only(self._curl('https://cmsweb.cern.ch/crabcache/info?subresource=fileremove&hashkey=' + hashkey))
      if x:
         raise CRABToolsException('fileremove failed: %r' % x)

if __name__ == '__main__':
   dirs = crab_dirs_from_argv()
   max_processes = typed_from_argv(int, 5, name='max_processes')

   if 'rq' in sys.argv:
       rq = dict((d, crab_requestcache(d)) for d in dirs)

   elif 'resub' in sys.argv:
      def fcn(d):
         print d
         return d, crab_command('resubmit', dir=d)
      results = crab_multiprocess(fcn, dirs, max_processes)
      failed = [(d, res) for d, res in results if res.get('status', '') != 'SUCCESS']
      if failed:
         print 'these failed to resubmit (may HTTPException if task in state FAILED, i.e. there were no jobs to resubmit):'
         for d, res in failed:
            print d
            pprint(res)

   elif 'user_cache_quota' in sys.argv:
       h = UserCacheHelper()
       print h.quota()

   elif 'clean_user_cache' in sys.argv:
      skip = [x.split('=')[1] for x in sys.argv if x.startswith('skip=')]
      h = UserCacheHelper()
      for x in h.filelist():
         if '.log' not in x and x not in skip:
            print 'remove', x
            h.fileremove(x)

   elif 'list_schedds' in sys.argv:
      for d in dirs:
         rq = crab_requestcache(d)
         name = rq['RequestName']
         wf = h._curl('https://cmsweb.cern.ch/crabserver/prod/task?subresource=search&workflow=' + name)
         print d.ljust(60), name.rjust(75), wf['tm_schedd'].rjust(30)

   elif 'datasets' in sys.argv:
       results = crab_process_statuses_with_redo(dirs, max_processes)
       results = crab_results_by_task_status(results)
       for status, res in results.iteritems():
           print status
           for d, r in res.iteritems():
               l = r['outdatasets']
               if len(l) == 1:
                   print l[0]
               else:
                   print l

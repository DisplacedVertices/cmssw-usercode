#!/usr/bin/env python

# author: J. Tucker

import httplib
import multiprocessing
import json
import pycurl
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import config as Config
from CRABClient.UserUtilities import getUsernameFromSiteDB
from JMTucker.Tools.CRAB3ToolsBase import *

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

    ok = True

    try:
        result = crabCommand(*args, **kwargs)

        # what the hell happened in the last crab version?
        if type(result) == tuple:
            d = {}
            for r in result:
                if type(r) == dict:
                    for k,v in r.iteritems():
                        if d.has_key(k):
                            if d[k] != v:
                                ok = False
                        else:
                            d[k] = v
                elif r is not None:
                    ok = False
            result = d

    except httplib.HTTPException, e:
        result = {}
        result['jobList'] = []
        result['HTTPException'] = e
        result['status'] = 'HTTPException'
    except pycurl.error, e:
        result = {}
        result['jobList'] = []
        result['pycurlError'] = e
        result['status'] = 'pycurlError'

    for k,v in result.get('shortResult', {}).iteritems():
        if not result.has_key(k):
            result[k] = v

    if not result.has_key('jobList'):
        result['jobList'] = []
        result['unhandledProblem'] = True

    #pprint(result)

    if suppress_stdout:
        result['stdout'] = buf.getvalue()
        sys.stdout = old_stdout

    if not ok or type(result) != dict:
        print 'problem with crabCommand return value'
        print type(result)
        pprint(result)
        raise CRABToolsException('problem')

    os.remove(cache_file)
    os.environ['CRAB3_CACHE_FILE'] = old_cache_file

    return result

def crab_multiprocess(fcn, dirs, max_processes):
    # fcn must return 2-tuple (dir, result), and has to be a module-level method (?)
    if max_processes == 1:
        results = [fcn(d) for d in dirs]
    else:
        pool = multiprocessing.Pool(max_processes)
        results = pool.map(fcn, dirs)
        pool.close()
        pool.join()
    return results

# This is used with crab_process_simple_cmd to have a function that
# multiprocess can access.
crab_multiprocess_simple_fcn_cmd = None
def crab_multiprocess_simple_fcn(d):
    if crab_multiprocess_simple_fcn_cmd is None:
        raise ValueError('must set crab_multiprocess_simple_fcn_cmd before calling')
    print d
    return d, crab_command(crab_multiprocess_simple_fcn_cmd, dir=d)

def crab_process_simple_cmd(cmd, dirs, max_processes):
    global crab_multiprocess_simple_fcn_cmd
    crab_multiprocess_simple_fcn_cmd = cmd
    results = crab_multiprocess(crab_multiprocess_simple_fcn, dirs, max_processes)
    failed = [(d, res) for d, res in results if res.get('status', '') != 'SUCCESS']
    if failed:
        print 'these failed to resubmit (may HTTPException if task in state FAILED, i.e. there were no jobs to %s):' % cmd
        for d, res in failed:
            print d
            pprint(res)
    return results

def crab_status(working_dir, verbose=False):
    if verbose:
        print 'checking', working_dir

    result = crab_command('status', dir=working_dir)

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
                err = job_info.get('Error', ['Unk'])[0]
                state_ex = 'failed_%s' % err
                if d.has_key(state_ex):
                    d[state_ex] += 1
                else:
                    d[state_ex] = 1

    return working_dir, result

def crab_process_statuses(working_dirs, max_processes, verbose=False):
    if verbose:
        print 'launching processes...'
    #results = {working_dirs[0]: crab_status(working_dirs[0])}
    results = crab_multiprocess(crab_status, working_dirs, max_processes)
    if verbose:
        print 'done waiting for processes!'
    return results

def crab_process_statuses_with_redo(working_dirs, max_processes, verbose=False):
    results = dict(crab_process_statuses(working_dirs, max_processes, verbose))

    def redoable(res):
        return \
            res.has_key('HTTPException') or \
            res.has_key('pycurlError') or \
            (res.get('taskFailureMsg', '') != None and 'Timeout when waiting for remote host' in res.get('taskFailureMsg', ''))

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

def crab_output_files(working_dir, jobs=None, logs=False):
    cmd = 'getlog' if logs else 'getoutput'
    if jobs is not None:
        d = crab_command(cmd, '--xrootd', '--jobids=%s' % crabify_list(jobs, simple=True), dir=working_dir)
    else:
        d = crab_command(cmd, '--xrootd', dir=working_dir)
    return d.get('xrootd', [])

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
       crab_process_simple_cmd('resub', dirs, max_processes)

   elif 'kill' in sys.argv:
       crab_process_simple_cmd('kill', dirs, max_processes)

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
       h = UserCacheHelper()
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
           ds = []
           for d, r in res.iteritems():
               l = r['outdatasets']
               if len(l) == 1:
                   ds.append(l[0])
               else:
                   ds.append(l)
           ds.sort()
           for d in ds:
               print d

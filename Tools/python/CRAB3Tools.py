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
from JMTucker.Tools.general import bool_from_argv, popen
from JMTucker.Tools.hadd import hadd
from CRABAPI.RawCommand import crabCommand
from CRABClient.UserUtilities import getUsernameFromSiteDB

username = getpass.getuser()
mycrab_tmp_dir = '/tmp/%s/mycrab' % username
if not os.path.isdir(mycrab_tmp_dir):
    os.mkdir(mycrab_tmp_dir)

# JMTBAD improve global options
allow_insecure_stupidity = False
global_options_path = os.path.expanduser('~/.jmtct')
if os.path.isfile(global_options_path):
    global_options_cfg = ConfigParser()
    global_options_cfg.read(global_options_path)
    try:
        allow_insecure_stupidity = global_options_cfg.get('Global', 'allow_insecure_stupidity')
    except (NoSectionError, NoOptionError):
        pass

class CRABToolsException(Exception):
    pass

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
    if not allow_insecure_stupidity:
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
    if not allow_insecure_stupidity:
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
        if allow_insecure_stupidity:
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

    def from_kwargs(key, default_):
        if kwargs.has_key(key):
            val = kwargs[key]
            del kwargs[key]
            return val
        else:
            return default_

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
    if max_processes == 1:
        results = [fcn(d) for d in dirs]
    else:
        pool = multiprocessing.Pool(max_processes)
        results = pool.map(fcn, dirs)
        pool.close()
        pool.join()
    return results

def crab_output_files(working_dir, jobs=None):
    if jobs is not None:
        d = crab_command('getoutput', '--xrootd', '--jobids=%s' % crabify_list(jobs, simple=True), dir=working_dir)
    else:
        d = crab_command('getoutput', '--xrootd', dir=working_dir)
    return d.get('xrootd', [])

def crab_requestcache(working_dir):
   return cPickle.load(open(os.path.join(working_dir, '.requestcache'), 'rb'))

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
   h = UserCacheHelper()
   if False:
      for x in h.filelist():
         if '.log' in x: # or x == '18420b98cfaa556dc2c94fe2acb83b451806144b5d284763eae5f0a354b3f34b':
            continue
         print 'remove', x
         h.fileremove(x)
   elif False:
      dirs = crab_dirs_from_argv()
      for d in dirs:
         rq = crab_requestcache(d)
         name = rq['RequestName']
         wf = h._curl('https://cmsweb.cern.ch/crabserver/prod/task?subresource=search&workflow=' + name)
         print d.ljust(60), name.rjust(75), wf['tm_schedd'].rjust(30)

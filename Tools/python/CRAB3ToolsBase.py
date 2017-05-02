#!/usr/bin/env python

# author: J. Tucker

import cPickle
import fnmatch
import getpass
import glob
import os
import json
import sys
import time
import zlib
from ConfigParser import ConfigParser, NoSectionError, NoOptionError
from collections import defaultdict
from cStringIO import StringIO
from pprint import pprint
from JMTucker.Tools.general import bool_from_argv, typed_from_argv, popen

class CRABToolsException(Exception):
    pass

class CRABToolsGlobalOptions:
    def __init__(self, cfg_path=os.path.expanduser('~/.jmtct')):
        self.cfg_path = cfg_path
        self.allow_insecure_stupidity = False
        self.crab_dirs_root = '/dev/null'

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

def crab_requestcache(working_dir):
    return cPickle.load(open(os.path.join(working_dir, '.requestcache'), 'rb'))

def is_crab_working_dir(path):
    return os.path.isdir(path) and os.path.isfile(os.path.join(path, '.requestcache'))

def crab_dirs_from_argv():
    dirs = []

    for d in sys.argv[1:]:
        if is_crab_working_dir(d):
            dirs.append(d)
        elif os.path.isdir(d):
            # if we have a dir of crab dirs, take all of them
            for dd in glob.glob(os.path.join(d, '*')):
                if is_crab_working_dir(dd):
                    dirs.append(dd)

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

def crab_results_by_task_status(results):
    d = defaultdict(dict)
    for working_dir, res in results.iteritems():
        d[res['status']][working_dir] = dict(res)
    return d

def crab_get_output_dir(working_dir):
    rq = crab_requestcache(working_dir)
    rq_name = rq['RequestName'].split(':')
    timestamp = rq_name[0]
    username = rq_name[1].split('_')[0]
    try:
        primary_dataset = rq['OriginalConfig'].Data.inputDataset.split('/')[1]
    except AttributeError:
        primary_dataset = 'CRAB_PrivateMC'
    try:
        publish_name = rq['OriginalConfig'].Data.outputDatasetTag
    except AttributeError:
        publish_name = None
    if not publish_name:
        assert not rq['OriginalConfig'].Data.publication
        publish_name = rq['RequestName'].split(username + '_')[1]
    return '/store/user/%s/%s/%s/%s' % (username, primary_dataset, publish_name, timestamp)

if __name__ == '__main__':
    rq = crab_requestcache(sys.argv[1])

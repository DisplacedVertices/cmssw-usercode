#!/usr/bin/env python

# author: J. Tucker

from JMTucker.Tools.CRAB3ToolsBase import *

def crab_command(*args, **kwargs):
    if kwargs and kwargs.keys() != ['dir']:
        raise ValueError('crab_command popen version: kwargs not used other than dir')
    cmd = '/cvmfs/cms.cern.ch/crab3/crab-env-bootstrap.sh ' + ' '.join(args)
    cmd += ' -d ' + kwargs['dir']
    return popen(cmd)
    
def crab_status(working_dir, verbose=False):
    if verbose:
        print 'checking', working_dir
    output = crab_command('status', '--json', dir=working_dir)
    if verbose:
        print output
    result = None
    for line in output.split('\n'):
        if line.startswith('{') and line.endswith('}'):
            result = json.loads(line)
    if result is None:
        raise CRABToolsException('could not get json object from status output')
    return result

def crab_get_njobs(working_dir):
    return len(crab_status(working_dir))

def crab_hadd(working_dir, new_name=None, new_dir=None, raise_on_empty=False, chunk_size=900, pattern=None):
    if working_dir.endswith('/'):
        working_dir = working_dir[:-1]
    if new_name is None:
        new_name = '_'.join(os.path.basename(working_dir).split('_')[2:])
    if not new_name.endswith('.root'):
        new_name += '.root'
    if new_dir is not None:
        new_name = os.path.join(new_dir, new_name)

    expected = crab_get_njobs(working_dir)
    print '%s: expecting %i files if all jobs succeeded' % (working_dir, expected)

    files = [x.strip() for x in crab_command('out', '--xrootd', dir=working_dir).split('\n') if x.strip()]
    if pattern:
        if '/' not in pattern:
            pattern = '*/' + pattern
        files = fnmatch.filter(files, pattern)

    jobs = [int(f.split('_')[-1].split('.root')[0]) for f in files]
    jobs.sort()
    expected = range(1, expected+1)

    if jobs != expected:
        print '\033[36;7m %i files found %s not what expected \033[m' % (len(jobs), crabify_list(jobs))
        missing = sorted(set(expected) - set(jobs))
        print '\033[36;7m    %i missing: %r \033[m' % (len(missing), ' '.join(missing))

    l = len(files)
    if l == 0:
        msg = 'crab_hadd: no files found in %s' % working_dir
        if raise_on_empty:
            raise CRABToolsException(msg)
        else:
            print '\033[36;7m', msg, '\033[m'
    elif l == 1:
        print working_dir, ': just one file found, copying'
        cmd = 'xrdcp -s %s %s' % (files[0], new_name)
        os.system(cmd)
        os.chmod(new_name, 0644)
    else:
        hadd(new_name, files, chunk_size)

    return new_name

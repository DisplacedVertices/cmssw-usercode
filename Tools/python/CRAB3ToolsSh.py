#!/usr/bin/env python

# author: J. Tucker

import re
from JMTucker.Tools.CRAB3ToolsBase import *
from JMTucker.Tools.hadd import hadd

def crab_command(*args, **kwargs):
    if kwargs and kwargs.keys() != ['dir']:
        raise ValueError('crab_command popen version: kwargs not used other than dir')
    cmd = 'crab ' + ' '.join(args)
    cmd += ' -d ' + kwargs['dir']
    return popen(cmd)
    
def crab_status(working_dir, verbose=False):
    if verbose:
        print 'checking', working_dir
    output = crab_command('status', '--json', dir=working_dir)
    if verbose:
        print output
    result = None
    stdout = []
    for line in output.split('\n'):
        if line.startswith('{') and line.endswith('}'):
            result = json.loads(line)
        else:
            stdout.append(line.strip())
    if result is None:
        print output
        raise CRABToolsException('could not get json object from status output')
    result = {'jobs': result, 'stdout': stdout}
    return result

def crab_get_njobs(working_dir):
    return len(crab_status(working_dir)['jobs'])

def crab_get_njobs_from_log(working_dir, jobs_re=re.compile(r'\([\d ]+/([\d ]+)\)')):
    # find njobs using a line printed as result of crab status that looks like ( 76/788)
    # check that it's a constant, too
    njobs = set()
    for line in open(os.path.join(working_dir, 'crab.log')):
        mo = jobs_re.search(line)
        if mo:
            njobs.add(mo.groups())
    if len(njobs) != 1:
        raise ValueError('problem parsing wd=%s for njobs %r' % (working_dir, njobs))
    return int(njobs.pop()[0])

def crab_get_output_dataset_from_log(working_dir):
    datasets = set()
    for line in open(os.path.join(working_dir, 'crab.log')):
        line = line.strip()
        if line.startswith('Output dataset:'):
            dataset = line.split()[-1]
            assert dataset.endswith('/USER')
            datasets.add(dataset)
    assert len(datasets) <= 1
    return datasets.pop() if datasets else None

def crab_hadd(working_dir, new_name=None, new_dir=None, raise_on_empty=False, chunk_size=900, pattern=None, lpc_shortcut=False):
    if working_dir.endswith('/'):
        working_dir = working_dir[:-1]
    if new_name is None:
        new_name = '_'.join(os.path.basename(working_dir).split('_')[2:])
    if not new_name.endswith('.root'):
        new_name += '.root'
    if new_dir is not None:
        new_name = os.path.join(new_dir, new_name)

    if lpc_shortcut:
        username = os.environ['USER']
        expected = crab_get_njobs_from_log(working_dir)
        rq = crab_requestcache(working_dir)
        timestamp = rq['RequestName'].split(':')[0]
        primary_dataset = rq['OriginalConfig'].Data.inputDataset.split('/')[1]
        publish_name = rq['OriginalConfig'].Data.outputDatasetTag
        if not publish_name:
            assert not rq['OriginalConfig'].Data.publication
            publish_name = rq['RequestName'].split(username + '_')[1]
        path = '/eos/uscms/store/user/%(username)s/%(primary_dataset)s/%(publish_name)s/%(timestamp)s' % locals()
        zero_dirs = [x.strip() for x in popen('eos root://cmseos.fnal.gov ls %s' % path).split('\n') if x.strip()]
        files = []
        dbase = path.replace('/eos/uscms', 'root://cmseos.fnal.gov/') + '/'
        for zd in zero_dirs:
            d = dbase + zd + '/'
            files += [d + x.strip() for x in popen('eos root://cmseos.fnal.gov ls %s/%s' % (path, zd)).split() if x.strip().endswith('.root')]
    else:
        expected = crab_get_njobs(working_dir)
        res = crab_command('out', '--xrootd', dir=working_dir)
        if 'No files to retrieve.' in res:
            files = []
        else:
            files = [x.strip() for x in res.split('\n') if x.strip() and '.root' in x]

    print '%s: expecting %i files if all jobs succeeded' % (working_dir, expected)

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
        print '\033[36;7m    %i missing: %r \033[m' % (len(missing), ' '.join(str(j) for j in missing))

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

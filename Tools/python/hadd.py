#!/usr/bin/env python

import os, subprocess, tempfile, re
import ROOT 
from datetime import datetime
from JMTucker.Tools import colors, eos

class HaddBatchResult(object):
    def __init__(self, kind, working_dir, new_name, new_dir, expected, files, submit):
        self.success = True
        self.kind = kind
        self.working_dir = working_dir
        self.new_name = new_name
        self.new_dir = new_dir
        self.expected = expected
        self.files = files
        self.submit = submit

class HaddlogParser(object):
    target_re = re.compile(r'hadd Target file: (.*)')
    source_re = re.compile(r'hadd Source file (\d+): (.*)')
    def __init__(self, fn):
        self.target = None
        self.sources = {}
        for line in open(fn):
            line = line.strip()
            if self.target is None:
                tmo = self.target_re.search(line)
                if tmo:
                    self.target = t = tmo.group(1)
                    assert t.endswith('.root')
                    continue

            smo = self.source_re.search(line)
            if smo:
                num = int(smo.group(1))
                fn = smo.group(2)
                assert fn.endswith('.root')
                self.sources[num] = fn
        self.num_sources = len(self.sources)
        self.files = self.sources.values()

def haddcondor(dir_hadd_target, flist):
    """If submit == True, hadd jobs are sent to condor. A condor 
    submission file is created for a given input dataset. These 
    are then submitted to condor, where haddOnWorker.py is called 
    in order to do the hadding. There is the option to hadd fewer 
    files together. Edit the path to the executable to work on 
    personal space.
    """
    #splitting up the arguments into the hadd directory and input dataset
    dir_hadd, target = dir_hadd_target.rsplit("/", 1)

    target = target.replace('.root','')
    nTotal = len(flist)
    nLoops = 0

    while len(flist) > 0 :
        strNLoops = str(nLoops)

        #nItemsToPop = 10
        nItemsToPop = 200

        inputFiles = ''

        for i in xrange(nItemsToPop) :
            if len(flist) > 0 :
                fstr = flist.pop()
                inputFiles = inputFiles + ' ' + fstr

        #prefixStr = dir_hadd+'/'+target+'-'+strNLoops
        prefixStr = dir_hadd+'/'+target

        #condorFile = open(dir_hadd+'/submit_'+strNLoops, 'w')
        condorFile = open(dir_hadd+'/submit_'+target, 'w')
        condorFile.write('executable       = /afs/hep.wisc.edu/home/acwarden/work/llp/mfv_1068p1/src/JMTucker/Tools/python/haddOnWorker.py\n')

        condorFile.write('universe         = vanilla\n')
        condorFile.write('log              = '+prefixStr+'.log\n')
        condorFile.write('output           = '+prefixStr+'.out\n')
        condorFile.write('error            = '+prefixStr+'.err\n')
        condorFile.write('arguments        = '+prefixStr+'.root ' + inputFiles + '\n')
        condorFile.write('getenv           = True\n')


        condorFile.write('queue\n')
        condorFile.close()

        #args = ['condor_submit '+dir_hadd+'/submit_'+target+'-'+strNLoops]
        args = ['condor_submit '+dir_hadd+'/submit_'+target]
        p = subprocess.Popen(args =args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        
    return p

def hadd(output_fn, input_fns, submit):
    """This is a simple wrapper around hadd that suppresses the stdout
    from hadd, only reporting a summary line of how many files were
    merged. Output to eos is supported, including for the log file for
    stdout. Checks that the number of files reported merged by hadd is
    the same as the number in the input list, or if there were any
    other problems reported by hadd. If so, prints an error to
    stdout. Returns true if success.
    """
    
    l = len(input_fns)
    start = datetime.now()
    print 'hadding %i files to %s at %s' % (l, output_fn, start)
    
    if submit : 
        p = haddcondor(output_fn, input_fns)

    else : 
        args = ['hadd', output_fn] + input_fns
        p = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stdout, stderr = p.communicate()
    assert stderr is None

    ## output files for the non-submit case
    if not submit : 
        log_fn = output_fn + '.haddlog'
        is_eos = '/store/' in output_fn # ugh
        while eos.exists(log_fn) if is_eos else os.path.exists(log_fn):
            log_fn += '.2'
            
        if is_eos:
            fd, tmp_fn = tempfile.mkstemp()
            os.fdopen(fd, 'wt').write(stdout)
            eos.cp(tmp_fn, log_fn) # if the haddlog already exists the new one will silently go into the ether...
            os.remove(tmp_fn)
        else:
            open(log_fn, 'wt').write(stdout)

    if p.returncode != 0:
        print colors.error('PROBLEM hadding %s' % output_fn)
        #print p.stdout.read()
        return False

    #more output for non-submit case
    if not submit : 
        max_file_num = max(int(line.split(':')[0].split(' ')[-1]) for line in stdout.split('\n') if 'Source file' in line)
        print '-> %i files merged in %s' % (max_file_num, datetime.now() - start)
        if max_file_num != l:
            print colors.error('PROBLEM hadding %s' % output_fn)
            return False

    return True

__all__ = [
    'HaddBatchResult',
    'HaddlogParser',
    'hadd',
    ]

if __name__ == '__main__':
    #x = HaddlogParser('/uscms_data/d2/tucker/crab_dirs/NtupleV20m_EventHistosOnly/qcdht2000_2017.root.haddlog')
    import sys
    hadd(sys.argv[1], sys.argv[2:])

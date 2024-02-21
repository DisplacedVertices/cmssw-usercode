#!/usr/bin/env python

import os, subprocess, tempfile, re
from datetime import datetime
from JMTucker.Tools import colors, eos

class HaddBatchResult(object):
    def __init__(self, kind, working_dir, new_name, new_dir, expected, files):
        self.success = True
        self.kind = kind
        self.working_dir = working_dir
        self.new_name = new_name
        self.new_dir = new_dir
        self.expected = expected
        self.files = files

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

def hadd(output_fn, input_fns):
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
    args = ['hadd', output_fn] + input_fns

    p = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    assert stderr is None
    
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

    max_file_num = max(int(line.split(':')[0].split(' ')[-1]) for line in stdout.split('\n') if 'Source file' in line)
    print '-> %i files merged in %s' % (max_file_num, datetime.now() - start)
    if max_file_num != l:
        print colors.error('PROBLEM hadding %s' % output_fn)
        return False


__all__ = [
    'HaddBatchResult',
    'HaddlogParser',
    'hadd',
    ]

if __name__ == '__main__':
    #x = HaddlogParser('/uscms_data/d2/tucker/crab_dirs/NtupleV20m_EventHistosOnly/qcdht2000_2017.root.haddlog')
    import sys
    hadd(sys.argv[1], sys.argv[2:])

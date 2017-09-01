#!/usr/bin/env python

import os, subprocess, tempfile
from datetime import datetime
from JMTucker.Tools import colors, eos

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
    print 'hadding %i files to %s at %s' % (l, output_fn, datetime.now())
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

    if p.returncode != 0:
        print colors.boldred('PROBLEM hadding %s' % output_fn)
        #print p.stdout.read()
        return False

    max_file_num = max(int(line.split(':')[0].split(' ')[-1]) for line in stdout.split('\n') if 'Source file' in line)
    print '-> %i files merged' % max_file_num
    if max_file_num != l:
        print colors.boldred('PROBLEM hadding %s' % output_fn)
        return False

    return True

__all__ = [
    'hadd',
    ]

if __name__ == '__main__':
    import sys
    hadd(sys.argv[1], sys.argv[2:])

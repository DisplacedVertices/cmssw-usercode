#!/usr/bin/env python

import os, subprocess, tempfile
from JMTucker.Tools import colors, eos

def hadd(new_name, files):
    """Use ROOT's hadd tool to merge files into a new file with path
    new_name. This is a simple wrapper that suppresses the stdout from
    hadd, only reporting a summary line of how many files were
    merged. We check that the number of files reported merged by hadd
    is the same as the number in the input list, or if there were any
    other problems reported by hadd. If so, we print an error to
    stdout (with reverse video to make it stand out) and return
    False. On success, return True.
    """
    
    l = len(files)
    print 'hadding %i files to %s' % (l, new_name)
    args = ['hadd', new_name] + files

    p = subprocess.Popen(args=args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    stdout, stderr = p.communicate()
    assert stderr is None

    log_fn = new_name + '.haddlog'
    is_eos = '/store/' in new_name # ugh
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
        print colors.boldred('PROBLEM hadding %s' % new_name)
        #print p.stdout.read()
        return False

    max_file_num = max(int(line.split(':')[0].split(' ')[-1]) for line in stdout.split('\n') if 'Source file' in line)
    print '-> %i files merged' % max_file_num
    if max_file_num != l:
        print colors.boldred('PROBLEM hadding %s' % new_name)
        return False

    return True

__all__ = [
    'hadd',
    ]

if __name__ == '__main__':
    import sys
    hadd(sys.argv[1], sys.argv[2:])

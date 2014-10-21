#!/usr/bin/env python

import os, sys, gzip, cPickle, subprocess, glob, time

def big_warn(s):
    x = '#' * 80
    print x
    print s
    print x

def bool_from_argv(s, remove=True, return_pos=False):
    val = s in sys.argv
    ret = val
    if val and return_pos:
        ret = val, sys.argv.index(s) 
    if val and remove:
        sys.argv.remove(s)
    return ret

def from_pickle(fn, comp=False):
    if comp or '.gzpickle' in fn:
        f = gzip.GzipFile(fn, 'rb')
    else:
        f = open(fn, 'rb')
    return cPickle.load(f)

def to_pickle(obj, fn, proto=-1, comp=False):
    if comp or '.gzpickle' in fn:
        f = gzip.GzipFile(fn, 'wb')
    else:
        f = open(fn, 'wb')
    cPickle.dump(obj, f, proto)

def typed_from_argv(type_, default_value=None, raise_on_multiple=False):
    found = []
    for x in sys.argv:
        try:
            z = type_(x)
            found.append(z)
        except ValueError:
            pass
    if raise_on_multiple and len(found) > 1:
        raise ValueError('multiple values found in argv')
    if found:
        return found[0]
    else:
        return default_value

def popen(cmd, return_exit_code=False, print_output=False):
    child = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    output = []
    for line in child.stdout:
        if print_output:
            print line,
        output.append(line)
    output = ''.join(output)
    if return_exit_code:
        return output, child.returncode
    else:
        return output

def save_git_status(path):
    existed = os.path.isdir(path)
    if existed:
        files = glob.glob(os.path.join(path, '*'))
        if files:
            replaced_path = os.path.join(path, str(int(time.time())))
            os.mkdir(replaced_path)
            for f in files:
                os.rename(f, os.path.join(replaced_path, os.path.basename(f)))
    else:
        os.system('mkdir -p %s' % path)
    os.system("git log --pretty=format:'%%H' -n 1 > %s" % os.path.join(path, 'hash'))
    os.system("git status --untracked-files=all --ignored | grep -v pyc > %s" % os.path.join(path, 'status'))
    git_untracked_tmp_fn = '/tmp/%s/untracked.tgz' % os.environ['USER']
    git_untracked_file_list_cmd = "git status --porcelain | grep '^??' | sed 's/??//'"
    git_untracked_file_list = popen(git_untracked_file_list_cmd)
    if git_untracked_file_list:
        git_tar_ret = os.system("tar czf %s -C `git rev-parse --show-toplevel` `%s`" % (git_untracked_tmp_fn, git_untracked_file_list_cmd))
        if git_tar_ret != 0:
            print '\033[36;7m warning: \033[m git-untracked tar returned non-zero exit code'
        elif os.stat(git_untracked_tmp_fn).st_size > 100*1024**2:
            print '\033[36;7m warning: \033[m git-untracked tarball is bigger than 100M, leaving in %s' % git_untracked_tmp_fn
        else:
            os.system('mv %s %s' % (git_untracked_tmp_fn, path))
    os.system('git diff > %s' % os.path.join(path, 'diff'))

__all__ = [
    'bool_from_argv',
    'big_warn',
    'from_pickle',
    'to_pickle',
    'typed_from_argv',
    'popen',
    'save_git_status',
    ]

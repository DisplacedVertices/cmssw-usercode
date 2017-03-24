#!/usr/bin/env python

import os, sys, gzip, cPickle, subprocess, glob, time
from itertools import chain
from pprint import pprint

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

def coderep_compactify_list(l):
    a = b = None
    xranges = []
    singles = []
    def sforab(a,b):
        if a == b:
            singles.append(a)
        elif a == 0:
            xranges.append('xrange(%i)' % (b+1))
        else:
            xranges.append('xrange(%i,%i)' % (a, b+1))
    for x in sorted(l):
        if a is None:
            a = x
            b = x
        elif x == b+1:
            b = x
        else:
            sforab(a,b)
            a = b = x
    sforab(a,b)
    singles.sort()
    if xranges:
        if singles:
            return 'chain(%s, %r)' % (', '.join(xranges), singles)
        else:
            if len(xranges) == 1:
                return xranges[0]
            return 'chain(%s)' % ', '.join(xranges)
    else:
        return repr(singles)

def coderep_files(files):
    if len(files) == 1:
        return repr(files)
    bn = os.path.basename(files[0]).split('_')[0]
    bases = set(fn.rsplit('/', 2)[0] for fn in files)
    codes = []
    check = []
    if len(bases) == 1:
        nums = [int(fn.rsplit('_',1)[1].split('.root')[0]) for fn in files]
        cnums = coderep_compactify_list(nums)
        if cnums.count('xrange') == 1:
            assert cnums.startswith('xrange(')
            base = bases.pop()
            from1 = cnums.startswith('xrange(1,')
            s = '_fromnum%i("%s", %i)' % (1 if from1 else 0, base, len(files))
            if bn != 'ntuple':
                s = s.replace(')', ', fnbase="%s")' % bn)
            return s
    for base in bases:
        nums = [int(fn.rsplit('_',1)[1].split('.root')[0]) for fn in files if fn.startswith(base)]
        if len(nums) == 1:
            code = "['%s/%04i/%s_%i.root']" % (base, nums[0]/1000, bn, nums[0])
        else:
            cnums = coderep_compactify_list(nums)
            mn,mx = min(nums), max(nums)
            if mn/1000 != mx/1000:
                code = "[%r + '/%%04i/%s_%%i.root' %% (i/1000,i) for i in %s]" % (base, bn, cnums)
            else:
                code = "['%s/%04i/%s_%%i.root' %% i for i in %s]" % (base, mn/1000, bn, cnums)
        codes.append(code)
        check += eval(code)
    #pprint(codes)
    check.sort()
    if sorted(set(check)) != check:
        raise ValueError('I made the same file twice somehow')
    if set(check) != set(files):
        x = set(l); y = set(files); print 'x-y'; pprint(x-y); print 'y-x'; pprint(y-x)
        raise ValueError('I am dumb')
    code = ' + '.join(codes)
    return code

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

def typed_from_argv(type_, default_value=None, raise_on_multiple=False, name=None, return_multiple=False):
    found = []
    if name and not name.endswith('='):
        name += '='
    for x in sys.argv:
        if name:
            if not x.startswith(name):
                continue
            x = x.replace(name, '')
        try:
            z = type_(x)
            found.append(z)
        except ValueError:
            pass
    if raise_on_multiple and len(found) > 1:
        raise ValueError('multiple values found in argv')
    if found:
        if return_multiple:
            return found
        else:
            return found[0]
    else:
        return default_value

def from_argv(*args, **kwargs):
    return typed_from_argv(str, *args, **kwargs)

def int_ceil(x,y):
    return (x+y-1)/y

def mkdirp(path):
    if not os.path.exists(path):
        os.mkdir(path)

def mail(to, subject, body):
    process = subprocess.Popen(['mail', '-s', subject, to], stdin=subprocess.PIPE)
    process.communicate(body)

def mkdirs_if_needed(path):
    dn = os.path.dirname(path)
    if dn:
        os.system('mkdir -p %s' % dn)

def sub_popen(cmd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)

def popen(cmd, return_exit_code=False, print_output=False):
    child = sub_popen(cmd)
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
    os.system('mkdir -p /tmp/%s' % os.environ['USER'])
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

def reverse_readline(filename, buf_size=8192):
    """a generator that returns the lines of a file in reverse order

    Ripped off from
    http://stackoverflow.com/questions/2301789/read-a-file-in-reverse-order-using-python
    """

    with open(filename) as fh:
        segment = None
        offset = 0
        fh.seek(0, os.SEEK_END)
        total_size = remaining_size = fh.tell()
        while remaining_size > 0:
            offset = min(total_size, offset + buf_size)
            fh.seek(-offset, os.SEEK_END)
            buffer = fh.read(min(remaining_size, buf_size))
            remaining_size -= buf_size
            lines = buffer.split('\n')
            # the first line of the buffer is probably not a complete line so
            # we'll save it and append it to the last line of the next buffer
            # we read
            if segment is not None:
                # if the previous chunk starts right from the beginning of line
                # do not concact the segment to the last line of new chunk
                # instead, yield the segment first
                if buffer[-1] is not '\n':
                    lines[-1] += segment
                else:
                    yield segment
            segment = lines[0]
            for index in range(len(lines) - 1, 0, -1):
                yield lines[index]
        yield segment

def touch(path):
    with open(path, 'a'):
        os.utime(path, None)

def intlumi_from_brilcalc_csv(fn, has_hlt):
    intlumis = {}
    intlumi_sum = 0.
    with gzip.open(fn) as lumi_f:
        intlumi_column = None
        for line in lumi_f:
            line = line.strip()
            if line.startswith('#'):
                if intlumi_column is None and line.startswith('#run:fill'):
                    if has_hlt:
                        assert line == '#run:fill,ls,time,hltpath,delivered(/ub),recorded(/ub),source'
                        intlumi_column = -2
                    else:
                        assert line == '#run:fill,ls,time,beamstatus,E(GeV),delivered(/ub),recorded(/ub),avgpu,source'
                        intlumi_column = -3
            else:
                line = line.split(',')
                run = int(line[0].split(':')[0])
                ls0,ls1 = line[1].split(':')
                assert ls0 == ls1 or (ls0 != '0' and ls1 == '0')
                ls = int(ls0)
                intlumi = float(line[intlumi_column])
                intlumis[(run, ls)] = intlumi
                intlumi_sum += intlumi
    return intlumis, intlumi_sum

__all__ = [
    'bool_from_argv',
    'big_warn',
    'intlumi_from_brilcalc_csv',
    'from_pickle',
    'to_pickle',
    'typed_from_argv',
    'from_argv',
    'int_ceil',
    'mkdirp',
    'mkdirs_if_needed',
    'sub_popen',
    'popen',
    'reverse_readline',
    'save_git_status',
    'touch',
    ]

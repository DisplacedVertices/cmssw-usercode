import sys, subprocess, os, fnmatch

url = 'root://cmseos.fnal.gov/'
global_url = 'root://cms-xrd-global.cern.ch/'
user = os.environ['USER']

def _popen(cmd, shell=False):
    if type(cmd) == str:
        cmd = cmd.split()
    return subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell)

def _system(cmd):
    if type(cmd) == str:
        cmd = cmd.split()
    return subprocess.call(cmd, stdout=open(os.devnull, 'w'), stderr=subprocess.STDOUT) == 0
    
def quota():
    x = _popen('eos root://cmseos.fnal.gov quota').communicate()[0].split('\n')
    for i, line in enumerate(x):
        if user in line:
            return x[i-1] + '\n' + line
    return "eos quota command didn't work or didn't find user %s" % user

def exists(fn):
    return _system('eos %s ls %s' % (url, fn))

def mkdir(fn):
    dn = os.path.dirname(fn)
    if exists(dn):
        return True
    return _system('eos %s mkdir -p %s' % (url, dn))

def ls(path):
    #print 'ls', path
    cmd = str('eos %s ls %s' % (url, path))
    #print repr(cmd)
    fns = _popen(cmd).communicate()[0].strip().split()
    return [os.path.join(path, fn) for fn in fns]

def glob(path, pattern):
    fns = ls(path)
    return [fn for fn in fns if fnmatch.fnmatch(os.path.basename(fn), pattern)]

def cp(src, dst):
    return _system('xrdcp -s %s%s %s%s' % (url, src, url, dst))

def rm(fn):
    return _system('eos %s rm %s' % (url, fn))

def md5sum(fn):
    cmd = 'xrdcp -s %s%s -' % (url, fn)
    p  = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p2 = subprocess.Popen(('md5sum',), stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    return p2.communicate()[0].split()[0]


if __name__ == '__main__':
    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == 'md5sum':
            for x in sys.argv[2:]:
                if x.startswith('/store'):
                    print '%s  %s' % (md5sum(x), x)

        elif cmd == 'cp' or cmd == 'mv':
            import general

            dest = sys.argv[-1]
            if not dest.startswith('/store'):
                raise ValueError('dest must start with /store')
            if not exists(dest):
                raise IOError("dest %s doesn't exist" % dest)
            if not dest.endswith('/'):
                dest += '/'
            fns = sys.argv[2:-1]
            if not fns:
                raise ValueError('usage: eos.py mv fn1 [fn2...] /store/.../dest')
            for fn in fns:
                print fn
                if not os.path.isfile(fn):
                    raise ValueError("files only, can't recurse")
                if not cp(fn, dest):
                    raise IOError("problem copying?")
                dest_fn = os.path.join(dest, os.path.basename(fn))
                raw_input('ok?')
                md5src = general.md5sum(fn)
                md5dst = md5sum(dest_fn)
                print fn, md5src, md5dst, dest_fn
                if md5src != md5dst:
                    raise ValueError("problem with md5sums: src %s dst %s" % (md5src, md5dst))
                raw_input('ok?')
                if cmd == 'mv':
                    raw_input('going to rm, ok?')
                    os.remove(fn)

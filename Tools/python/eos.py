import subprocess, os

url = 'root://cmseos.fnal.gov/'
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
    x = popen('eos root://cmseos.fnal.gov quota').communicate()[0].split('\n')
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

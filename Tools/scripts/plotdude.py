#!/usr/bin/env python

################################################################################

# Set up.

import getpass, os, subprocess, sys, tarfile, time

def bool_from_argv(s):
    val = s in sys.argv
    if val:
        sys.argv.remove(s)
    return val

testing = bool_from_argv('--testing')
rm_dir = bool_from_argv('--rm')

def cmd(c):
    print c
    if not testing:
        return os.system(c)
    else:
        return 0

def die(msg='', usage=False):
    if msg:
        sys.stderr.write(msg + '\n')
    if usage:
        sys.stderr.write('usage: plotdude.py path/to/abide\n')
    sys.exit(1)

def usage(msg=''):
    die(msg)

try:
    to_tar = sys.argv[1]
except IndexError:
    usage()

if not os.path.isdir(to_tar):
    usage('arg %s is not a directory' % to_tar)

to_tar_basename = os.path.basename(to_tar)
if not to_tar_basename: # avoid '/'
    usage('refusing to use /\n')

user = getpass.getuser()
timestamp = time.strftime('%Y%m%d-%H%M%S')
arc_name = '%(user)s/%(timestamp)s_%(to_tar_basename)s' % locals()
temp_fn = timestamp + '.plotdude.tar.bz2'
local_temp_fn = '/tmp/%s/' % user + temp_fn
host_name = 'plotdude'
host_temp_dir = '/home/plotdude/temp/'
host_temp_fn = host_temp_dir + temp_fn
host_dest_dir = '/home/plotdude/public_html'

# Check that the doubletunnel is set up.
if not os.path.isfile(os.path.expanduser('~/.ssh/id_plotdude')) or os.system('grep "Host %s" ~/.ssh/config > /dev/null' % host_name) != 0:
    die('must have plotdude keyfile and doubletunnel set up in ~/.ssh')

for x in 'testing rm_dir to_tar to_tar_basename user timestamp arc_name temp_fn local_temp_fn host_name host_temp_dir host_temp_fn host_dest_dir'.split():
    print x.ljust(30), ':', eval(x)

################################################################################

# Check that we have enough free space before doing anything. (And
# don't let plotdude eat up the last 10G on the disk, either.)

print 'calculating tree size'
size_needed = 0
for root, dirs, files in os.walk(to_tar):
    for f in files:
        size_needed += os.stat(os.path.join(root, f)).st_size
size_needed /= 1024.

print 'checking remote disk space'
df = subprocess.Popen(['ssh', host_name, 'df .'], stdout=subprocess.PIPE)
df_output = df.communicate()[0]
assert '1K-blocks' in df_output
free_space = int(df_output.split('\n')[1].split()[-3])
if free_space < 10*1024**2 + size_needed:
    die("plotdude wouldn't have enough free space on %s" % host_name)
    
# Make the tarball, renaming the top level directory inside it using
# arcname so that it goes in the "right" place with a username and
# timestamp.
print 'tarring'
tar = tarfile.open(local_temp_fn, 'w:bz2')
tar.add(to_tar, arcname=arc_name)
tar.close()

print 'scping'
cmd('scp %s %s:%s' % (local_temp_fn, host_name, host_temp_fn))

print 'remotely untarring'
cmd("ssh %s 'tar -C %s -jxf %s'" % (host_name, host_dest_dir, host_temp_fn))

print 'deleting temp files'
cmd('rm %s' % local_temp_fn)
cmd("ssh %s 'rm %s'" % (host_name, host_temp_fn))

if rm_dir:
    print 'deleting directory'
    cmd('rm -r %s' % to_tar)

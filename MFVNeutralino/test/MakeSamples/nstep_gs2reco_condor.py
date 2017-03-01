#!/usr/bin/env python

which = 'qcdht2000_76_16PU'
output_dir = which
inputfns_fn = 'inputfns.txt'
todos = [
    'fns,%s,$(Process)' % inputfns_fn,
    'pu16',
    ]
njobs = None

####

if len(todos) > 2:
    print 'fyi: rawhlt will get todos'
    print todos
    print 'while reco will get'
    print todos[2:]

import os, sys, shutil

if not os.path.isfile(inputfns_fn):
    sys.exit('no file %s' % inputfns_fn)

ninputfns = len([x for x in open(inputfns_fn).read().split('\n') if x.strip().endswith('.root')])
if ninputfns == 0:
    sys.exit("no input fns in %s?", inputfns_fn)

if len(todos) > 7:
    sys.exit("I'm lazy, max 7 todos supported")

full_output_dir = '/eos/uscms/store/user/tucker/%s' % output_dir
if os.path.exists(full_output_dir):
    sys.exit('%s already exists' % full_output_dir)

####

from JMTucker.Tools.CRAB3ToolsBase import crab_dirs_root
from JMTucker.Tools.general import save_git_status
from JMTucker.Tools import colors

testing = 'testing' in sys.argv
work_area = crab_dirs_root('nstep_gs2reco_condor_%s' % which)
if os.path.isdir(work_area):
    sys.exit('work_area %s exists' % work_area)
os.makedirs(work_area)
save_git_status(os.path.join(work_area, 'gitstatus'))

inputs_dir = os.path.join(work_area, 'inputs')
os.mkdir(inputs_dir)

sh_fn = 'nstep_gs2reco_condor.sh'
input_files = 'todoify.sh rawhlt.py reco.py modify.py inputfns.txt minbias.py minbias_files.py minbias_files.pkl'.split()
for fn in [sh_fn] + input_files:
    shutil.copy2(fn, inputs_dir)

sh_fn = os.path.join(inputs_dir, sh_fn)
input_files = ','.join([os.path.join(inputs_dir, x) for x in input_files])

todos = ' '.join('todo=' + x for x in todos)

if njobs is None:
    njobs = str(ninputfns)

jdl_template = '''universe = vanilla
Executable = %(sh_fn)s
arguments = $(Process) %(output_dir)s %(todos)s
Output = stdout.$(Process)
Error = stderr.$(Process)
Log = log.$(Process)
stream_output = false
stream_error = false
notification = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = %(input_files)s
x509userproxy = $ENV(X509_USER_PROXY)
Queue %(njobs)s
'''

jdl_fn = os.path.join(work_area, 'jdl')
open(jdl_fn, 'wt').write(jdl_template % locals())

cwd = os.getcwd()
os.chdir(work_area)
os.system('condor_submit %s' % jdl_fn)
os.chdir(cwd)

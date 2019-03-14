#!/usr/bin/env python

import os, sys, shutil

inputfns_fn = sys.argv[1]
which = sys.argv[2]
output_dir = which
todos = [
    'fns,inputfns.txt,$(Process)' % inputfns_fn,
    ]
njobs = None

####

if len(todos) > 1:
    print 'fyi: rawhlt will get todos'
    print todos
    print 'while reco, miniaod will get'
    print todos[1:]

if not os.path.isfile(inputfns_fn):
    sys.exit('no file %s' % inputfns_fn)

inputfns = [x for x in open(inputfns_fn).read().split('\n') if x.strip().endswith('.root')]
if not inputfns:
    sys.exit("no input fns in %s?", inputfns_fn)
open('inputfns.txt','wt').write('\n'.join(inputfns) + '\n')

if len(todos) > 7:
    sys.exit("I'm lazy, max 7 todos supported")

full_output_dir = '/eos/uscms/store/user/tucker/%s' % output_dir
if os.path.exists(full_output_dir):
    sys.exit('%s already exists' % full_output_dir)

####

from JMTucker.Tools.CRAB3ToolsBase import crab_dirs_root
from JMTucker.Tools.Year import year; assert year == 2017
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

open('year.txt', 'wt').write(str(year))

sh_fn = 'nstep_gs2reco_condor.sh'
input_files = 'todoify.sh rawhlt.py reco.py miniaod.py dynamicconf.py year.txt modify.py inputfns.txt minbias.py minbias_premix.txt.gz'.split()
for fn in [sh_fn] + input_files:
    shutil.copy2(fn, inputs_dir)

sh_fn = os.path.join(inputs_dir, sh_fn)
input_files = ','.join([os.path.join(inputs_dir, x) for x in input_files])

todos = ' '.join('todo=' + x for x in todos)

if njobs is None:
    njobs = len(inputfns)

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
request_memory = 3000
Queue %(njobs)i
'''

jdl_fn = os.path.join(work_area, 'jdl')
open(jdl_fn, 'wt').write(jdl_template % locals())

cwd = os.getcwd()
os.chdir(work_area)
os.system('condor_submit %s' % jdl_fn)
os.chdir(cwd)

for x in 'year.txt', 'inputfns.txt':
    os.remove(x)

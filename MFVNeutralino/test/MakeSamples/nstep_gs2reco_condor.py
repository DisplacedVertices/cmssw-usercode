#!/usr/bin/env python

which = 'qcdht2000_76'
output_dir = which
inputfns_fn = 'inputfns.txt'
todos = [
    'fns,%s,$(Process)' % inputfns_fn,
    ]
njobs = None

####

import os, sys

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
work_area = crab_dirs_root('mfv_run2_nstep_gs2reco_condor_%s' % which)
if os.path.isdir(work_area):
    sys.exit('work_area %s exists' % work_area)
os.makedirs(work_area)
save_git_status(os.path.join(work_area, 'gitstatus'))

sh_fn = os.path.abspath('nstep_gs2reco_condor.sh')
todos = ' '.join('todo=' + x for x in todos)
input_files = ','.join([os.path.abspath(x) for x in 'todoify.sh rawhlt.py reco.py modify.py inputfns.txt minbias.py minbias_files.py minbias_files.pkl'.split()])
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

#!/usr/bin/env python

# this script must be run from One2Two/

from submitcommon import *
import shutil
from JMTucker.Tools.CondorSubmitter import CondorSubmitter

steering_sh = '''
ISAMPLE=%(isample)s
XRDCPCOMBINETARBALL=1
DATACARDARGS="%(datacard_args)s"
SAVETOYS=
'''

jdl_template = '''universe = vanilla
Executable = submit.sh
arguments = $(Process)
Output = stdout.$(Process)
Error = stderr.$(Process)
Log = log.$(Process)
stream_output = true
stream_error  = false
notification  = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = %(input_files)s,cs_jobmap
+REQUIRED_OS = "rhel7"
+DesiredOS = REQUIRED_OS
Queue %(njobs)s
'''

batch_root = crab_dirs_root('combine_output_%i' % time())
if os.path.isdir(batch_root):
    raise IOError('%s exists' % batch_root)
print batch_root
os.mkdir(batch_root)
os.mkdir(os.path.join(batch_root, 'inputs'))

save_git_status(os.path.join(batch_root, 'gitstatus'))

input_files = []
for x in ['signal_efficiency.py', 'datacard.py', 'limitsinput.root', 'submit.sh']:
    nx = os.path.abspath(os.path.join(batch_root, 'inputs', os.path.basename(x)))
    shutil.copy2(x, nx)
    input_files.append(nx)
input_files = ','.join(input_files)

def callback(config, sample):
    print sample.isample, sample.name,
    isample = sample.isample # for locals use below

    batch_dir = os.path.join(batch_root, submit_config.batch_dir(sample))
    os.mkdir(batch_dir)
    open(os.path.join(batch_dir, 'nice_name'), 'wt').write(sample.name)

    run_fn = os.path.join(batch_dir, 'run.sh')
    open(run_fn, 'wt').write(script_template % locals())

    open(os.path.join(batch_dir, 'cs_dir'), 'wt')
    open(os.path.join(batch_dir, 'cs_jobmap'), 'wt').write('\n'.join(str(i) for i in xrange(njobs)) + '\n')
    open(os.path.join(batch_dir, 'cs_submit.jdl'), 'wt').write(jdl_template % locals())
    open(os.path.join(batch_dir, 'cs_njobs'), 'wt').write(str(njobs))
    open(os.path.join(batch_dir, 'cs_outputfiles'), 'wt').write('observed.root expected.root combine_output.txtgz')

    CondorSubmitter._submit(batch_dir, submit_config.njobs)

submit(callback)

# zcat signal_*/combine_output* | sort | uniq | egrep -v '^median expected limit|^mean   expected limit|^Observed|^Limit: r|^Generate toy|^Done in|random number generator seed is|^   ..% expected band|^DATACARD:' | tee /tmp/duh

# JMTBAD need to figure out general version of CondorSubmitter not tied into CMSSW jobs

import os, sys, shutil
from glob import glob
from JMTucker.Tools.general import chdir

if len(sys.argv) < 2:
    sys.exit('usage: submit.py output_dir')

txts = glob('/uscms_data/d2/tucker/crab_dirs/AAdone/TrackingTreerV2/*txt')
if not txts:
    raise ValueError('no txts?')

jdl = '''universe = vanilla
Executable = submit.sh
arguments = %(batch)s $(Process) %(eos_output_dir)s
transfer_input_files = hists.exe,%(txt)s
Output = %(batch)s_$(Process).stdout
Error = %(batch)s_$(Process).stderr
Log = %(batch)s_$(Process).log
stream_output = false
stream_error  = false
notification  = never
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
Queue %(njobs)i
'''

user = os.environ['USER']
prevwd = os.getcwd()
batch_dir = sys.argv[1]
eos_output_dir = '/store/user/%s/%s' % (user, batch_dir)

if os.path.exists(batch_dir) or \
        os.system('mkdir %s' % batch_dir) != 0 or \
        os.system('eos root://cmseos.fnal.gov ls %s 2>/dev/null >/dev/null' % eos_output_dir) == 0 or \
        os.system('eos root://cmseos.fnal.gov mkdir %s' % eos_output_dir) != 0:
    raise IOError('working or eos output directory already exists?')

for x in ['hists.exe', 'submit.sh'] + txts:
    shutil.copy2(x, batch_dir)

with chdir(batch_dir) as _, open('checkem.sh', 'wt') as checkem, open('haddem.sh', 'wt') as haddem, open('cleanup.sh', 'wt') as cleanup:
    for txt in txts:
        txt = os.path.basename(txt)
        batch = os.path.splitext(txt)[0]
        njobs = len(open(txt).readlines())
        open('%s.jdl' % batch, 'wt').write(jdl % locals())
        if os.system('condor_submit %s.jdl' % batch) != 0:
            raise ValueError('problem submitting')

        log_files = ' '.join(os.path.join(os.getcwd(), '%s_%i.log' % (batch, i)) for i in xrange(njobs))
        checkem.write('if [[ $(grep "Normal termination (return value 0)" %(log_files)s | wc -l) != "%(njobs)s" ]]; then echo %(batch)s not done or bad; fi\n' % locals())

        out_fn = 'root://cmseos.fnal.gov/%s/%s.root' % (eos_output_dir, batch)
        out_files_base = ['%s/%s_%i.root' % (eos_output_dir, batch, i) for i in xrange(njobs)]
        out_files = ' '.join('root://cmseos.fnal.gov/' + x for x in out_files_base)
        haddem.write('hadd.py %s %s\n' % (out_fn, out_files))
        for x in out_files_base:
            cleanup.write('eos root://cmseos.fnal.gov/ rm %s\n' % x)

for sh in 'checkem.sh', 'haddem.sh', 'cleanup.sh':
    os.chmod(os.path.join(batch_dir, sh), 0755)

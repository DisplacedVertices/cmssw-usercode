import os, sys

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
output_dir = raw_input('output dir? ')
assert '/' not in output_dir
eos_output_dir = '/store/user/%s/%s' % (user, output_dir)
if os.system('mkdir %s' % output_dir) != 0 or os.system('eos root://cmseos.fnal.gov mkdir %s' % eos_output_dir) != 0:
    raise IOError('directory already existed')

txts = []
for x in sys.argv[1:]:
    if x.endswith('.txt') and os.path.isfile(x):
        txts.append(x)

if not txts:
    raise ValueError('no txts')

checkem = open('checkem.sh', 'wt')
haddem = open('haddem.sh', 'wt')

for txt in txts:
    batch = os.path.splitext(os.path.basename(txt))[0]
    njobs = len(open(txt).readlines())
    open('temp.jdl', 'wt').write(jdl % locals())
    if os.system("condor_submit temp.jdl") != 0:
        raise ValueError('problem submitting')

    log_files = ['%(batch)s_%(i)i.log' % locals() for i in xrange(njobs)]
    log_files = ' '.join(log_files)
    checkem.write('''
if [[ $(grep "Normal termination (return value 0)" %(log_files)s  | wc -l) == "%(njobs)s" ]]; then
  echo %(batch)s OK
else
  echo %(batch)s BAD
fi
''' % locals())

    out_files = ['root://cmseos.fnal.gov/%(eos_output_dir)s/%(batch)s_%(i)i.root' % locals() for i in xrange(njobs)]
    out_files = ' '.join(out_files)
    out_fn = '/uscmst1b_scratch/lpc1/3DayLifetime/%s/%s.root' % (user, batch)
    haddem.write('hadd.py %(out_fn)s %(out_files)s\n' % locals())
    haddem.write('xrdcp %(out_fn)s root://cmseos.fnal.gov/%(eos_output_dir)s\n\n' % locals())

checkem.close()
haddem.close()

os.chmod('checkem.sh', 0766)
os.chmod('haddem.sh', 0766)


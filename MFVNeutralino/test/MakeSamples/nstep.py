import sys, os, shutil

jdl = '''universe = vanilla
Executable = %(executable)s
arguments = $(Process) %(events_per)s %(todo)s %(outdir)s
transfer_input_files = %(tar_fn_base)s
x509userproxy = $ENV(X509_USER_PROXY)
Output = stdout_$(Process).txt
Log = condor_$(Process).log
stream_output = false
stream_error  = false
notification  = never
should_transfer_files   = YES
when_to_transfer_output = ON_EXIT
+LENGTH="SHORT"
Queue %(njobs)s
'''

if os.system('voms-proxy-info -exists -valid 100:0') != 0:
    if os.system('voms-proxy-init -rfc -voms cms -valid 192:00') != 0:
        sys.exit(1)

executable = 'nstep.sh'
input_files = 'gensim.py modify.py rawhlt.py minbias.py minbias_files.py minbias_files.pkl reco.py'
tar_fn_base = 'input.tgz'

for fn in input_files.split() + [executable]:
    if not os.path.isfile(fn):
        raise IOError('missing %s' % fn)

user = os.environ['USER']

events_per = 30
njobs = 333

if 1:
    taus = [100, 300, 1000, 10000]
    masses = [300, 400, 800, 1200, 1600]

    taus = [1000]
    masses = [800]

    for tau in taus:
        for mass in masses:
            todo = 'mfv_neutralino,%.1f,%i' % (tau/1000., mass)
            nice = 'mfv_neutralino_tau%05ium_M%04i' % (tau, mass)
            outdirb = '/store/user/%s/nstep/%s' % (user, nice)
            loutdir = '/eos/uscms' + outdirb
            outdir = 'root://cmseos.fnal.gov/' + outdirb
            workdir = 'workdirs/' + nice
            if os.path.isdir(loutdir) or os.path.isdir(workdir):
                raise IOError('%s or %s already exists' % (loutdir, workdir))

            os.system('mkdir -p ' + loutdir)
            os.system('mkdir -p ' + workdir)

            tar_fn = os.path.join(workdir, tar_fn_base)
            os.system('tar czf %s %s' % (tar_fn, input_files))
            
            shutil.copy2(executable, os.path.join(workdir, executable))

            open(os.path.join(workdir, 'jdl'), 'wt').write(jdl % locals())

            pubinfo = open(os.path.join(workdir, 'pubinfo'), 'wt')
            pubinfo.write(nice + '\n')
            pubinfo.write('\n'.join(os.path.join(outdir, 'reco_%i.root' % i) for i in xrange(njobs)))

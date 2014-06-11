#!/usr/bin/env python

import os, sys

script_template = '''#!/bin/tcsh
echo script starting on `date`
echo script args: $argv
echo wd: `pwd`

setenv JMT_WD `pwd`
setenv JOB_NUM $argv[1]

setenv SCRAM_ARCH slc5_amd64_gcc462
setenv JMT_CMSSW_VERSION CMSSW_5_3_13

source /uscmst1/prod/sw/cms/cshrc prod

echo trying to setup CMSSW $JMT_CMSSW_VERSION
scram project CMSSW $JMT_CMSSW_VERSION
cd $JMT_CMSSW_VERSION/src
cmsenv
echo ROOTSYS: $ROOTSYS
echo root-config: `root-config --libdir --version`
echo

echo set up libs
cd $CMSSW_BASE/lib/$SCRAM_ARCH
tar zxf $JMT_WD/lib.tgz
echo pwd `pwd`
echo ls -la
ls -la
echo

echo set up py
cd $CMSSW_BASE/src
tar zxvf $JMT_WD/py.tgz
mkdir $CMSSW_BASE/python/JMTucker
touch $CMSSW_BASE/python/JMTucker/__init__.py
cd $CMSSW_BASE/python/JMTucker
ln -s $CMSSW_BASE/src/JMTucker/Tools/python Tools
touch $CMSSW_BASE/python/JMTucker/Tools/__init__.py
echo PYTHONPATH $PYTHONPATH
echo pwd `pwd`
echo ls -laR
ls -laR
echo

echo untar trees
cd $JMT_WD
tar zxvf all_trees.tgz
echo

echo run one2two.py
cd $JMT_WD

setenv mfvo2t_job_num $JOB_NUM
setenv mfvo2t_seed $JOB_NUM
%(env)s

cmsRun one2two.py env >& out.$JOB_NUM
'''

jdl_template = '''universe = vanilla
Executable = runme.csh
arguments = $(Process)
Output = stdout.$(Cluster)_$(Process)
Error = stderr.$(Cluster)_$(Process)
Log = condor_log.$(Cluster)_$(Process)
stream_output = false
stream_error  = false
notification  = never
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files = one2two.py, /uscms_data/d2/tucker/crab_dirs/mfv_535/MiniTreeV18/all_trees.tgz, lib.tgz, py.tgz
x509userproxy = $ENV(X509_USER_PROXY)
Queue %(njobs)s
'''

tars_made = False
output_root = '/uscms/home/tucker/nobackup/One2Two'
def make_tars():
    global tars_made
    if not tars_made:
        print 'making tars'
        os.system('mkdir -p ' + output_root)
        os.system('cp one2two.py ' + output_root)
        os.system('cd $CMSSW_BASE/lib/* ; tar czf %s/lib.tgz * .edmplugincache ; cd - > /dev/null' % output_root)
        os.system('cd $CMSSW_BASE/src/ ; tar czf %s/py.tgz JMTucker/Tools/python/Samples.py JMTucker/Tools/python/ROOTTools.py JMTucker/Tools/python/general.py JMTucker/Tools/python/DBS.py ; cd - > /dev/null' % output_root)
        tars_made = True

def submit(njobs, min_ntracks, svdist_cut, sampling_type, how_events, phi_exp, signal_contamination, n1v_scale, samples):
    make_tars()
    batch_name = 'Ntk%i_Svd%s_Styp%i_HE%s_Phi%s_SC%s_Nsc%i_S%s' % (min_ntracks,
                                                                   ('%.3f' % svdist_cut).replace('.','p'),
                                                                   sampling_type,
                                                                   how_events,
                                                                   'fit' if phi_exp is None else ('%.2f' % phi_exp).replace('.','p'),
                                                                   'no' if signal_contamination is None else 'n%ix%i' % signal_contamination,
                                                                   n1v_scale,
                                                                   samples)

    batch_wd = os.path.join(output_root, batch_name)
    os.system('mkdir -p ' + batch_wd)
    old_wd = os.getcwd()
    os.chdir(batch_wd)

    os.system('cp %s/one2two.py .' % output_root)
    os.system('cp %s/lib.tgz .' % output_root)
    os.system('cp %s/py.tgz .' % output_root)

    env = [
        'min_ntracks %i' % min_ntracks,
        'svdist2d_cut %f' % svdist_cut,
        'sampling_type %s' % sampling_type,
        'n1v_scale %i' % n1v_scale,
        ]

    if signal_contamination is not None:
        sig_samp, sig_scale = signal_contamination
        env.append('signal_contamination %i' % sig_samp)
        env.append('signal_scale %f' % sig_scale)

    if phi_exp is not None:
        env.append('phi_exp %f' % phi_exp)

    if 'full' in how_events:
        pass
    elif 'toy' in how_events:
        env.append('toy_mode 1')
        if 'pois' in how_events:
            env.append('poisson_n1vs 1')

    if 'all' in samples:
        env.append('sample all')
        if '500' in samples:
            env.append('use_qcd500 1')
    else:
        env.append('sample %s' % samples)

    env = '\n'.join('setenv mfvo2t_' + e for e in env)
    open('runme.csh', 'wt').write(script_template % {'env': env})
    open('runme.jdl', 'wt').write(jdl_template % {'njobs': njobs})

    if 'doit' in sys.argv:
        os.system('condor_submit runme.jdl')

    os.chdir(old_wd)

# For ntracks in 5-8:
#     For svdist_cut in 0.02-0.05 in steps of 10 micron:
#         With and without replacement:
#             For phi_exp in (fit for), 1-5 in steps of 0.5:
#                 For signal contamination in None + (1x, 10x, 50x, 100x) * (100um, 300um, 1000um, 9900um)
#                     For seed in 0-1000:
#                         if signal_contam is None
#                             Test all the samples individually, with full statistics available.
#                             Test all the samples individually, sampling N_20ifb events in each pseudoexp.
#                             Test all the samples individually, sampling Pois(N_20ifb events) in each pseudoexp.
#                         With and without qcd500:
#                             Test all samples, sampling N_20ifb events in each pseudoexp.
#                             Test all samples, sampling Pois(N_20ifb events) in each pseudoexp.

sampling_type = 0
phi_exp = None
signal_contam = None
batches = []
how_events = 'toypois'
for min_ntracks, n1v_scale in ((5,50),(6,50),(7,38),(8,20)):
    for svdist_cut in [0.036 + 0.002*i for i in xrange(7)]:
        for sample in 'all all500'.split():
            if 'all' in sample and 'full' in how_events:
                continue
            batches.append((min_ntracks, svdist_cut, sampling_type, how_events, phi_exp, signal_contam, int(n1v_scale/5.) if '500' in sample else n1v_scale, sample))

raw_input('%i batches = %i jobs?' % (len(batches), len(batches)*200))
for batch in batches:
    submit(200, *batch)

'''
qcdht0500 qcdht1000 ttbarhadronic ttbarsemilep ttbardilep
        for how_events in 'full toy toypois'.split():
            for sample in 'qcdht0500 qcdht1000 ttbarhadronic ttbarsemilep ttbardilep all all500'.split():
                if 'all' in sample and 'full' in how_events:
                    continue
                batches.append((min_ntracks, svdist_cut, sampling_type, how_events, phi_exp, signal_contam, sample))
'''

'''
grep -L 'Normal termination (return value 0)' condor_log*
tar --remove-files -czf condor_logs.tgz condor_log.*


find . -name stderr\* -size 0
rm stderr*


less stdout.*_0

foreach x (stdout*)
  sed --in-place -e 's@condor/execute/dir_[0-9]*@@g' $x
end

touch diffstdouts
foreach x (stdout*)
  foreach y (stdout*)
    if ($x != $y) then
      diff $x $y >> diffstdouts
    endif
  end
end
sort -o diffstdouts diffstdouts

tar --remove-files -czf stdouts.tgz stdout.*


mkdir outs
mv out.* outs/

mkdir roots
mv *.root roots/


py ~/test/One2Two draw.py roots/one2two_0.root
...
mv plots/one2two plots/one2two_`basename $PWD`
'''

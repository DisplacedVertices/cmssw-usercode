#!/usr/bin/env python

import os, sys, time
from JMTucker.Tools.general import save_git_status

sample_number_to_name = {}
i = -1
for t in [100, 300, 1000, 9900]:
    for m in [200, 300, 400, 600, 800, 1000]:
        sample_number_to_name[i] = 'mfv_neutralino_tau%04ium_M%04i' % (t, m)
        i -= 1
#for i in xrange(-1, -25, -1):
#    print i, sample_number_to_name[i]


script_template = '''#!/bin/sh
echo mfvo2t script starting on `date`
echo mfvo2t script args: $argv
echo wd: `pwd`

export JOB_NUM=$1

%(unzip_files)s

echo ROOTSYS: $ROOTSYS
echo root-config: `root-config --libdir --version`

echo pwd `pwd`
echo ls -la
ls -la
echo

export mfvo2t_tree_path=.
export mfvo2t_no_progressbar=1
export mfvo2t_seed=$JOB_NUM
export mfvo2t_ntoys=1
export mfvo2t_toythrower_allow_cap=1
%(env)s

%(extra_setup)s

echo run mfvo2t.exe
set -o pipefail
./mfvo2t.exe | python filtertee.py
ECODE=$?
if [ "$ECODE" -ne "0" ]; then
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  echo @@@@ mfvo2t.exe exited with error code $ECODE
  echo @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
  exit $ECODE
fi
echo mfvo2t.exe done
echo

cat > $RUNTIME_AREA/crab_fjr_${JOB_NUM}.xml << EOF
<FrameworkJobReport>
<PerformanceReport>
  <PerformanceSummary Metric="StorageStatistics">
    <Metric Name="Parameter-untracked-bool-enabled" Value="true"/>
    <Metric Name="Parameter-untracked-bool-stats" Value="true"/>
    <Metric Name="Parameter-untracked-string-cacheHint" Value="application-only"/>
    <Metric Name="Parameter-untracked-string-readHint" Value="auto-detect"/>
    <Metric Name="ROOT-tfile-read-totalMegabytes" Value="0"/>
    <Metric Name="ROOT-tfile-write-totalMegabytes" Value="0"/>
  </PerformanceSummary>
</PerformanceReport>

<GeneratorInfo>
</GeneratorInfo>
</FrameworkJobReport>
EOF
'''

dummy_pset = '''
import FWCore.ParameterSet.Config as cms
process = cms.Process('One2Two')
process.source = cms.Source('EmptySource')
'''

crab_cfg = '''
[CMSSW]
events_per_job=1
number_of_jobs=%(njobs)s
pset=%(dummy_pset_fn)s
datasetpath=None
output_file=mfvo2t.root

[USER]
script_exe=runme.csh
ui_working_dir=%(batch_root)s/crab_%(batch_name)s
ssh_control_persist=no
additional_input_files=mfvo2t.exe,filtertee.py,%(files_needed)s
copy_data=1
publish_data_name=mfvo2t_%(batch_name)s
publish_data=1
dbs_url_for_publication=phys03
storage_element=%(storage_element)s
jmt_skip_input_files=lib/*,src/*

[CRAB]
jobtype=cmssw
scheduler=%(scheduler)s

[GRID]
#se_black_list=T2_US_Purdue,T2_CH_CERN,T3_UK_SGrid_Oxford,T3_RU_FIAN,T2_RU_JINR
'''

maked = 'nomake' in sys.argv
setuped = False

def submit(njobs, template_type, min_ntracks, signal_sample, template_signal, samples):
    global maked
    global setuped

    if not maked:
        if os.system('make clean; make -j 16') != 0:
            raise 'no make'
        raw_input('did the make go OK?')
        maked = True

    cornell = 'cornell' in sys.argv
    grid = 'condor' not in sys.argv
    scheduler = 'condor' if not grid else 'remoteGlidein'
    storage_element = 'T3_US_FNALLPC' if not cornell else 'T3_US_Cornell'

    extra_name = ''
    batch_root = 'crab/One2Two'
    for x in sys.argv:
        if x.startswith(batch_root):
            extra_name = x.replace(batch_root + '_', '') + '_'
            batch_root = x
            break

    dummy_pset_fn = os.path.join(batch_root, 'dummy_pset.py')

    files_needed = set()

    if not setuped:
        os.system('mkdir -p %s' % batch_root)
        save_git_status(os.path.join(batch_root, 'gitstatus'))
        open(dummy_pset_fn, 'wt').write(dummy_pset)
        setuped = True

    batch_name = '%sTmp%s_Ntk%i_SigTmp%s_SigSam%s_Sam%s' % (extra_name,
                                                            template_type,
                                                            min_ntracks,
                                                            template_signal,
                                                            'no' if signal_sample is None else 'n%ix%i' % signal_sample,
                                                            samples)

    files_needed.add('backgrounds.tgz')
    files_needed.add('MultiJetPk2012.root.gz')
    files_needed.add(sample_number_to_name[template_signal] + '.root.gz')

    extra_setup = ''

    env = [
        'toythrower_min_ntracks=%i' % min_ntracks,
        'toythrower_template_signal=%i' % template_signal,
        ]

    if template_signal >= -12:
        env.append('fitter_sig_limit_step=1')

    if template_type == 'PS':
        env.append('templates_kind=phishift')
        env.append('fitter_start_nuis0=2')
        env.append('fitter_start_nuis1=0.003')
    elif template_type == 'SC':
        env.append('templates_kind=simpleclear')
        env.append('fitter_fix_nuis1=1')
        env.append('fitter_start_nuis0=10')
        env.append('fitter_start_nuis1=0')

    if signal_sample is not None:
        sig_samp, sig_scale = signal_sample
        assert sig_samp < 0
        files_needed.add(sample_number_to_name[sig_samp] + '.root.gz')

        if sig_scale < 0:
            env.append('ntoys=0')
            env.append('process_data=1')
            env.append('fitter_run_minos=0')
            if sig_scale == -2:
                env.append('seed=1')
                env.append('fitter_i_limit_job=$JOB_NUM')
                env.append('fitter_do_signif=0')
            else:
                assert njobs <= 20
        else:
            env.append('fitter_do_limit=0')
            env.append('toythrower_injected_signal=%i' % sig_samp)
            env.append('toythrower_injected_signal_scale=%f' % sig_scale)
    else:
        env.append('fitter_do_limit=0')

    if type(samples) == int:
        env.append('toythrower_sample_only=%i' % samples)
    elif type(samples) == str and '500' in samples:
        env.append('toythrower_use_qcd500=1')
    elif 'ttbarsyst' in samples:
        which_syst = samples.replace('ttbarsyst', '')
        files_needed.add('myttbar%s.root.gz' % which_syst)
        extra_setup += '''
cd trees
ln -s myttbar%s.root bkgsyst.root
cd -
''' % which_syst
        env.append('toythrower_sample_only=99')

    ###

    env = '\n'.join('export mfvo2t_' + e for e in env)

    unzip_files = []
    for fn in files_needed:
        if fn.endswith('.tgz'):
            unzip_files.append('tar zxf %s' % fn)
        else:
            unzip_files.append('gunzip %s' % fn)
    unzip_files = '\n'.join(unzip_files)
    tree_path = '/uscms_data/d2/tucker/mfvo2t_trees/mfvo2t_all_trees_444de711cdc630ddfe7cb6cd8f64ec8b46d09990_plussomettbarsyst'
    files_needed = ','.join(os.path.join(tree_path, f) for f in files_needed)

    open('runme.csh', 'wt').write(script_template % locals())
    open('crab.cfg', 'wt').write(crab_cfg % locals())
    os.system('crab -create -submit all')
    os.system('rm -f runme.csh crab.cfg')

###

if 1:
    template_type = 'CJ'
    min_ntracks = 5

    sig_first = [-15, -21, -9, -6]
    signals = sig_first + sorted(set(range(-24, 0)) - set(sig_first))

    strengths = (-2, -1, None, 1, 5)

    batches = []
    for signal in signals:
        for strength in strengths:
            sg = (signal, strength) if strength is not None else None
            njobs = 20 if strength == -1 else 500
            batches.append((njobs, template_type, min_ntracks, sg, signal, ''))

    for batch in batches:
        submit(*batch)

if 0:
    for syst in 'default bowing curl elliptical radial sagitta skew'.split():
        for signal in [-9, -15]:
            for strength in (None, 1):
                sg = (signal, strength) if strength is not None else None
                submit(10, 'CJ', 5, sg, signal, syst)

'''
for line in open('screen-exchange'):
    if line.startswith('crab_'):
        sam = int(line.split('SigTmp-')[1].split('_')[0])
        if sam <= 6:
            print line,

'''

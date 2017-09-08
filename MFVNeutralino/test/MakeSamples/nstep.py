#!/usr/bin/env python

nevents = 10000
events_per = 100
from_lhe = False
output_level = 'reco'
output_dataset_tag = 'RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6'
fixed_salt = ''
use_this_cmssw = False
premix = True
trig_filter = False
hip_simulation = False
hip_mitigation = False
ex = ''
already = []

if 0:
    meta, taus, masses = 'neu', [100, 300, 1000, 10000, 30000], [300, 400, 600, 800, 1200, 1600]
elif 0:
    meta, taus, masses = 'lq2', [100, 300, 1000, 10000], [300, 400, 600, 800, 1200, 1600]
elif 0:
    meta, taus, masses = 'glu', [100, 300, 1000, 10000], [300, 400, 600, 800, 1200, 1600]
elif 0:
    meta, taus, masses = 'ddbar', [100, 300, 1000, 10000, 30000], [300, 400, 500, 600, 800, 1200, 1600]
elif 0:
    meta = 'ttbar'
    nevents, events_per
    output_level = 'minitree'
elif 1:
    meta = 'minbias'
    nevents, events_per = 999000, 3000
    output_level = 'gensim'
    output_dataset_tag = 'RunIISummer15GS-MCRUN2_71_V1'
elif 0:
    meta = 'qcdht2000_gensim_ext1'
    nevents, events_per = 396000, 1500
    from_lhe = True
    output_level = 'gensim'
    output_dataset_tag = 'RunIISummer15GS-MCRUN2_71_V1'
elif 0:
    meta = 'qcdht2000_80'
    nevents, events_per = 396000, 1500
    from_lhe = True
    output_level = 'gensim'
    output_dataset_tag = 'RunIISummer15GS-MCRUN2_71_V1'
elif 0:
    meta = 'qcdht1500'
    fixed_salt = 'fixedsalt'
    nevents, events_per = 200000, 1000 # 0.06 eff at gen matching with lhe events for 1000, more like 0.025 for 700
    if meta.endswith('0700'):
        nevents *= 14
    from_lhe = True
    trig_filter = True
    hip_simulation = 1.0
    hip_mitigation = True
    ex = ''
elif 0:
    meta, taus, masses = 'neu', [100, 300, 1000, 10000, 30000], [300, 400, 600, 800, 1200, 1600]
    already = [] # [(t,m) for t in [300, 1000, 10000] for m in [400, 800]]
    hip_simulation = 1.0
    hip_mitigation = True
    ex = ''

if hip_simulation:
    use_this_cmssw = True
    premix = False
    exx = '%.1f' % hip_simulation
    ex += '_hip' + exx.replace('.','p')
    if hip_mitigation:
        ex += '_mit'

if not premix:
    output_dataset_tag = output_dataset_tag.replace('Premix', '')

#ex = '_test'
#nevents, events_per = 10,10
#meta, taus, masses = 'neu', [1000, 10000], [800]

################################################################################

if output_level not in ('reco', 'ntuple', 'minitree', 'gensim'):
    raise ValueError('output_level %s not supported' % output_level)

import sys, os
from math import ceil
from pprint import pprint
from time import time
from JMTucker.Tools.CRAB3Tools import Config, crab_dirs_root, crab_command
from JMTucker.Tools.general import index_startswith, save_git_status
import JMTucker.Tools.colors as colors

testing = 'testing' in sys.argv
work_area = crab_dirs_root('nstep_%s%s' % (meta, ex))
if os.path.isdir(work_area):
    sys.exit('work_area %s exists' % work_area)
os.makedirs(work_area)
save_git_status(os.path.join(work_area, 'gitstatus'))

config = Config()

to_rm = []

if output_level in ('minitree', 'ntuple'):
    for x in ['ntuple.py', 'minitree.py']:
        to_rm.append(x)
        os.system('cmsDumpPython.py ../%s > %s' % (x,x))

config.General.transferLogs = True
config.General.transferOutputs = True
config.General.workArea = work_area
config.General.requestName = 'SETME'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummy.py'
config.JobType.scriptExe = 'nstep.sh'
config.JobType.sendPythonFolder = True

steering_fn = 'steering.sh'

config.JobType.inputFiles = ['todoify.sh', steering_fn, 'lhe.py', 'gensim.py', 'dynamicconf.py', 'modify.py', 'rawhlt.py', 'minbias.py', 'minbias.txt.gz', 'minbias_premix.txt.gz', 'reco.py', 'fixfjr.py']
if output_level in ('minitree', 'ntuple'):
    config.JobType.inputFiles += ['ntuple.py', 'minitree.py']

if output_level == 'reco':
    config.JobType.outputFiles = ['reco.root']
elif output_level == 'gensim':
    config.JobType.outputFiles = ['gensim.root']
elif output_level == 'ntuple':
    config.JobType.outputFiles = ['ntuple.root', 'vertex_histos.root']
elif output_level == 'minitree':
    config.JobType.outputFiles = ['minitree.root', 'vertex_histos.root']

config.JobType.scriptArgs = [] # steering file will take care of what we did before

config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = events_per
config.Data.totalUnits = nevents
config.Data.publication = output_level not in ('minitree', 'ntuple')
config.Data.outputPrimaryDataset = 'SETME'
config.Data.outputDatasetTag = output_dataset_tag

config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.whitelist = ['T1_US_FNAL', 'T2_CH_CERN', 'T2_DE_DESY', 'T2_DE_RWTH', 'T2_FR_CCIN2P3', 'T2_US_Caltech', 'T2_US_Florida', 'T2_US_MIT', 'T2_US_Nebraska', 'T2_US_Purdue', 'T2_US_UCSD', 'T2_US_Vanderbilt', 'T2_US_Wisconsin']
if output_level == 'gensim':
    config.Site.whitelist += ['T3_US_*']

outputs = {}

def submit(config, name, todo, todo_rawhlt=[], todo_reco=[], todo_ntuple=[]):
    config.General.requestName = name
    config.Data.outputPrimaryDataset = name

    dummy_for_hash = int(time()*1e6)
    steering = [
        'MAXEVENTS=%i' % events_per,
        'EXPECTEDEVENTS=%i' % (ceil(events_per*0.06) if from_lhe else events_per),
        'USETHISCMSSW=%i' % use_this_cmssw,
        'FROMLHE=%i' % from_lhe,
        'TRIGFILTER=%i' % trig_filter,
        'PREMIX=%i' % premix,
        'export DUMMYFORHASH=%i' % dummy_for_hash,  # exported so the python script executed in cmsRun can just get it from os.environ instead of parsing argv like we do the rest
        'OUTPUTLEVEL=%s' % output_level,
        'TODO=todo=' + todo,
        ]

    salt = fixed_salt
    if not fixed_salt:
        salt = '%s %s' % (name, todo)

    if hip_simulation:
        assert type(hip_simulation) in (float,int)
        todo_rawhlt.append('hip_simulation,%f' % float(hip_simulation))

    if hip_mitigation:
        assert hip_simulation
        todo_reco  .append('hip_mitigation')
        todo_ntuple.append('hip_mitigation')

    todo2s = ('RAWHLT', todo_rawhlt), ('RECO', todo_reco), ('NTUPLE', todo_ntuple)
    for todo2_name, todo2 in todo2s:
        if todo2:
            todo2 = ' '.join('todo=%s' % x for x in todo2)
            steering.append('TODO%s="%s"' % (todo2_name, todo2))

            if not fixed_salt:
                salt += ' ' + todo2

    salt = salt.replace(' ', '_').replace('=','EQ')
    steering.append('SALT="%s"' % salt)

    open(steering_fn, 'wt').write('\n'.join(steering) + '\n')
    
    if not testing:
        output = crab_command('submit', config=config)
        print colors.boldwhite(name)
        pprint(output)
        print
    else:
        print 'crab config:'
        print config
        print 'steering.sh:'
        os.system('cat ' + steering_fn)
    os.remove(steering_fn)


def taus_masses():
    for tau in taus:
        for mass in masses:
            tm = tau, mass
            if tm in already:
                continue
            yield tm

if meta == 'neu':
    for tau, mass in taus_masses():
        name = 'mfv_neu_tau%05ium_M%04i' % (tau, mass)
        todo = 'mfv_neutralino,%.1f,%i' % (tau/1000., mass)
        submit(config, name, todo)

elif meta == 'glu':
    for tau, mass in taus_masses():
        name = 'mfv_glu_tau%05ium_M%04i' % (tau, mass)
        todo = 'mfv_gluino,%.1f,%i' % (tau/1000., mass)
        submit(config, name, todo)

elif meta == 'ddbar':
    for tau, mass in taus_masses():
        name = 'mfv_ddbar_tau%05ium_M%04i' % (tau, mass)
        todo = 'gluino_ddbar,%.1f,%i' % (tau/1000., mass)
        submit(config, name, todo)

elif meta == 'lq2':
    for tau, mass in taus_masses():
        name = 'mfv_lq2_tau%05ium_M%04i' % (tau, mass)
        todo = 'leptoquark,%.1f,%i,2' % (tau/1000., mass)
        submit(config, name, todo)

elif meta == 'ttbar':
    from modify import DummyBeamSpots
    todo2s = ['nominal'] + [x for x in dir(DummyBeamSpots) if not x.startswith('_')]
    for todo2 in todo2s:
        name = 'ttbar_%s' % todo2
        todo = 'ttbar'
        if todo2 != 'nominal':
            todo2 = 'weakmode,' + todo2
        else:
            todo2 = None
        submit(config, name, todo,
               todo_rawhlt=(todo2,),
               todo_reco  =(todo2,),
               todo_ntuple=(todo2,))

elif meta == 'minbias':
    name = meta
    todo = 'minbias'
    submit(config, name, todo)

elif meta.startswith('qcdht2000_gensim'):
    name = meta
    todo = 'qcdht2000'
    submit(config, name, todo)

elif meta.startswith('qcdht'):
    name = meta
    todo = meta.replace('qcdht', 'qcdht,')
    submit(config, name, todo)


if not testing:
    for x in to_rm:
        os.remove(x)

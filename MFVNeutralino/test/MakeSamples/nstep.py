#!/usr/bin/env python

nevents = 10000
events_per = 200
from_lhe = False
output_level = 'reco'
output_dataset_tag = 'RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12'

if 0:
    meta, taus, masses = 'neu', [100, 300, 1000, 10000], [300, 400, 800, 1200, 1600]
elif 0:
    meta, taus, masses = 'lq2', [100, 300, 1000, 10000], [300, 400, 800, 1200, 1600]
elif 0:
    meta, taus, masses = 'glu', [100, 300, 1000, 10000], [300, 400, 800, 1200, 1600]
elif 0:
    meta, taus, masses = 'gluddbar', [100, 300, 1000, 10000], [300, 400, 800, 1200, 1600]
elif 0:
    meta = 'ttbar'
    nevents, events_per
    output_level = 'minitree'
elif 1:
    meta = 'qcdht2000_gensim'
    nevents, events_per = 99000, 1500
    from_lhe = True
    output_level = 'gensim'
    output_dataset_tag = 'RunIISummer15GS-MCRUN2_71_V1'

ex = ''

################################################################################

if output_level not in ('reco', 'minitree', 'gensim'):
    raise ValueError('output_level %s not supported' % output_level)

import sys, os
from pprint import pprint
from time import time
from JMTucker.Tools.CRAB3Tools import Config, crab_dirs_root, crab_command
from JMTucker.Tools.general import save_git_status
import JMTucker.Tools.colors as colors

testing = 'testing' in sys.argv
work_area = crab_dirs_root('mfv_run2_nstep_%s%s' % (meta, ex))
if os.path.isdir(work_area):
    sys.exit('work_area %s exists' % work_area)
os.makedirs(work_area)
save_git_status(os.path.join(work_area, 'gitstatus'))

dummy_for_hash = int(time()*1e6)

config = Config()

to_rm = []

if output_level == 'minitree':
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

config.JobType.inputFiles = ['todoify.sh', 'lhe.py', 'gensim.py', 'modify.py', 'rawhlt.py', 'minbias.py', 'minbias_files.py', 'minbias_files.pkl', 'reco.py', 'fixfjr.py']
if output_level == 'minitree':
    config.JobType.inputFiles += ['ntuple.py', 'minitree.py']

config.JobType.outputFiles = ['RandomEngineState_GENSIM.xml.gz']
if from_lhe:
    config.JobType.outputFiles += ['RandomEngineState_LHE.xml.gz']

if output_level == 'reco':
    config.JobType.outputFiles += ['RandomEngineState_RAWHLT.xml.gz', 'reco.root']
elif output_level == 'gensim':
    config.JobType.outputFiles += ['gensim.root']
elif output_level == 'minitree':
    config.JobType.outputFiles += ['RandomEngineState_RAWHLT.xml.gz', 'minitree.root', 'vertex_histos.root']


config.JobType.scriptArgs = [
    'maxevents=%i' % events_per,
    'fromlhe=%i' % from_lhe,
    'dummyforhash=%i' % dummy_for_hash,  # stupid crab requires a =
    'outputlevel=%s' % output_level,
    'todo=SETME',
    'todo2=placeholder', # yes this gets replaced with todo= below
    ]

config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = events_per
config.Data.totalUnits = nevents
config.Data.publication = output_level != 'minitree'
config.Data.outputPrimaryDataset = 'SETME'
config.Data.outputDatasetTag = output_dataset_tag

config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.whitelist = '''T1_US_FNAL
T2_AT_Vienna
T2_BE_IIHE
T2_BE_UCL
T2_BR_SPRACE
T2_CH_CERN
T2_CH_CSCS
T2_CN_Beijing
T2_DE_DESY
T2_DE_RWTH
T2_EE_Estonia
T2_ES_CIEMAT
T2_ES_IFCA
T2_FI_HIP
T2_FR_CCIN2P3
T2_FR_GRIF_IRFU
T2_FR_GRIF_LLR
T2_FR_IPHC
T2_GR_Ioannina
T2_HU_Budapest
T2_IT_Bari
T2_IT_Legnaro
T2_IT_Pisa
T2_IT_Rome
T2_KR_KNU
T2_PK_NCP
T2_PL_Swierk
T2_PT_NCG_Lisbon
T2_RU_INR
T2_RU_JINR
T2_TH_CUNSTDA
T2_UA_KIPT
T2_UK_London_Brunel
T2_UK_London_IC
T2_UK_SGrid_RALPP
T2_US_Caltech
T2_US_Florida
T2_US_MIT
T2_US_Nebraska
T2_US_Purdue
T2_US_UCSD
T2_US_Vanderbilt
T2_US_Wisconsin'''.split('\n')

outputs = {}

def submit(config, name, todo, todo2=None):
    config.General.requestName = name
    config.Data.outputPrimaryDataset = name
    config.JobType.scriptArgs[4] = todo
    if todo2 is not None:
        config.JobType.scriptArgs[5] = todo2

    if not testing:
        output = crab_command('submit', config=config)
        print colors.boldwhite(name)
        pprint(output)
        print
    else:
        print config

if meta == 'neu':
    for tau in taus:
        for mass in masses:
            name = 'mfv_neu_tau%05ium_M%04i' % (tau, mass)
            todo = 'todo=mfv_neutralino,%.1f,%i' % (tau/1000., mass)
            submit(config, name, todo)

elif meta == 'glu':
    for tau in taus:
        for mass in masses:
            name = 'mfv_glu_tau%05ium_M%04i' % (tau, mass)
            todo = 'todo=mfv_gluino,%.1f,%i' % (tau/1000., mass)
            submit(config, name, todo)

elif meta == 'gluddbar':
    for tau in taus:
        for mass in masses:
            name = 'mfv_gluddbar_tau%05ium_M%04i' % (tau, mass)
            todo = 'todo=gluino_ddbar,%.1f,%i' % (tau/1000., mass)
            submit(config, name, todo)

elif meta == 'lq2':
    for tau in taus:
        for mass in masses:
            name = 'mfv_lq2_tau%05ium_M%04i' % (tau, mass)
            todo = 'todo=leptoquark,%.1f,%i,2' % (tau/1000., mass)
            submit(config, name, todo)

elif meta == 'ttbar':
    from modify import DummyBeamSpots
    todo2s = ['nominal'] + [x for x in dir(DummyBeamSpots) if not x.startswith('_')]
    for todo2 in todo2s:
        name = 'ttbar_%s' % todo2
        todo = 'todo=ttbar'
        if todo2 != 'nominal':
            todo2 = 'todo=weakmode,' + todo2
        else:
            todo2 = None
        submit(config, name, todo, todo2)

elif meta == 'qcdht2000_gensim':
    name = meta
    todo = 'todo=qcdht2000'
    submit(config, name, todo)

if not testing:
    for x in to_rm:
        os.remove(x)

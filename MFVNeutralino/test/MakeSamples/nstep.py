#!/usr/bin/env python

nevents = 2
events_per = 1

meta, taus, masses = 'neu', [100, 300, 1000, 10000], [300, 400, 800, 1200, 1600]
meta, taus, masses = 'neu', [1000], [800]

ex = ''

################################################################################

import sys, os
from datetime import datetime
from JMTucker.Tools.CRAB3Tools import Config, crab_dirs_root, crab_command
from JMTucker.Tools.general import save_git_status

testing = 'testing' in sys.argv
work_area = crab_dirs_root('mfv_run2_nstep_%s%s' % (meta, ex))
if os.path.isdir(work_area):
    sys.exit('work_area %s exists' % work_area)
os.makedirs(work_area)
save_git_status(os.path.join(work_area, 'gitstatus'))

dummy_for_hash = str(datetime.now())

config = Config()

config.General.transferLogs = True
config.General.transferOutputs = True
config.General.workArea = work_area
config.General.requestName = 'SETME'

config.JobType.pluginName = 'PrivateMC'
config.JobType.psetName = 'dummy.py'
config.JobType.inputFiles = ['gensim.py', 'modify.py', 'rawhlt.py', 'minbias.py', 'minbias_files.py', 'minbias_files.pkl', 'reco.py']
config.JobType.scriptExe = 'nstep.sh'
config.JobType.scriptArgs = ['maxevents=%i' % events_per, dummy_for_hash, 'todo=mfv_neutralino,1,800']
config.JobType.outputFiles = ['RandomEngineState_GENSIM.xml.gz', 'RandomEngineState_RAWHLT.xml.gz', 'reco.root']

config.Data.splitting = 'EventBased'
config.Data.unitsPerJob = events_per
config.Data.totalUnits = nevents
config.Data.publication = True
config.Data.outputPrimaryDataset = 'SETME'
config.Data.outputDatasetTag = 'nstep' # 'RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12'

config.Site.storageSite = 'T3_US_FNALLPC'
config.Site.whitelist = '''T1_US_FNAL
T2_BE_IIHE
T2_CH_CERN
T2_DE_DESY
T2_DE_RWTH
T2_EE_Estonia
T2_ES_CIEMAT
T2_FR_CCIN2P3
T2_IT_Bari
T2_IT_Legnaro
T2_IT_Pisa
T2_IT_Rome
T2_PL_Swierk
T2_UK_London_IC
T2_UK_SGrid_RALPP
T2_US_Caltech
T2_US_Florida
T2_US_MIT
T2_US_Nebraska
T2_US_UCSD
T2_US_Vanderbilt
T2_US_Wisconsin
T2_UK_London_Brunel'''.split('\n')

outputs = {}

if meta == 'neu':
    for tau in taus:
        for mass in masses:
            todo = 'mfv_neutralino,%.1f,%i' % (tau/1000., mass)
            name = 'mfv_neu_tau%05ium_M%04i' % (tau, mass)

            config.JobType.scriptArgs[-1] = todo

            config.General.requestName = name
            config.Data.outputPrimaryDataset = name

            if not testing:
                outputs[name] = crab_command('submit', config=config)

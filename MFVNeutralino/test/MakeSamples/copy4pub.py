import sys, os
from pprint import pprint

pubinfo = open(sys.argv[1]).read().split('\n')
primary_dataset = pubinfo[0]
input_files = pubinfo[1:]

n_input_files = len(input_files)
files_per_job = 5

tag = 'RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12'

################################################################################

py_fn = 'copy4pub_tmp.py'

open(py_fn, 'wt').write('''
from JMTucker.Tools.Merge_cfg import process

del process.source.inputCommands
del process.out.outputCommands
del process.out.dropMetaData
''')

crab_fn = 'copy4pub_crab.py'

open(crab_fn, 'wt').write('''
from CRABClient.UserUtilities import config as Config
config = Config()

config.General.transferLogs = False
config.General.transferOutputs = True
config.General.workArea = 'crab_copy4pub'
config.General.requestName = %(primary_dataset)s

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = %(py_fn)s

config.Data.userInputFiles = %(input_files)r
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = %(files_per_job)s
config.Data.totalUnits = %(n_input_files)s
config.Data.publication = True
config.Data.outputPrimaryDataset = %(primary_dataset)s
config.Data.outputDatasetTag = %(tag)s

config.Site.whitelist = ['T1_US_FNAL', 'T3_US_FNALLPC', 'T2_US_Nebraska']
config.Site.storageSite = 'T3_US_FNALLPC'
''' % locals())

if os.system('/cvmfs/cms.cern.ch/crab3/crab-env-bootstrap.sh submit -c %s' % crab_fn) == 0:
    pass
    #os.remove(py_fn


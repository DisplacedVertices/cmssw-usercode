#!/usr/bin/env python

# this script must be run from One2Two/

import sys
ex = sys.argv[1]
del sys.argv[1:2]

################################################################################

from CRABClient.ClientExceptions import ConfigException as CRABConfigException
from JMTucker.Tools.CRAB3Tools import Config, crab_command
from submitcommon import *

if not ex:
    raise ValueError('must set ex')
if not ex.startswith('_'):
    ex = '_' + ex
batch_name = 'combine_output%s' % ex
work_area = crab_dirs_root(batch_name)
if not os.path.isdir(work_area):
    os.makedirs(work_area)
gitstatus_dir = 'gitstatus_%s' % int(time()*1e6)
save_git_status(os.path.join(work_area, gitstatus_dir))

dummy_pset_fn = 'dummy.py'
fjr_fn = 'FrameworkJobReport.xml'
combine_tarball_fn = 'root://cmseos.fnal.gov//store/user/tucker/combine.tgz'
combine_tarball_bn = os.path.basename(combine_tarball_fn)
steering_fn = 'steering.sh'

to_rm = [dummy_pset_fn, fjr_fn, combine_tarball_bn, steering_fn]

open(dummy_pset_fn, 'wt').write('''import FWCore.ParameterSet.Config as cms
process = cms.Process('dummy')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('EmptySource')
''')

open(fjr_fn,'wt').write('''<FrameworkJobReport>
<ReadBranches>
</ReadBranches>
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
''')

os.system('xrdcp -sf %s .' % combine_tarball_fn)

crab_config = Config()

crab_config.General.transferLogs = False
crab_config.General.transferOutputs = True
crab_config.General.workArea = work_area
crab_config.General.requestName = 'SETME'

crab_config.JobType.pluginName = 'PrivateMC'
crab_config.JobType.psetName = 'dummy.py'
crab_config.JobType.scriptExe = 'submit.sh'
crab_config.JobType.scriptArgs = []
crab_config.JobType.sendPythonFolder = True
#crab_config.JobType.maxMemoryMB = 3000
crab_config.JobType.inputFiles = ['limitsinput.root', 'signal_efficiency.py', 'datacard.py', fjr_fn, combine_tarball_bn, steering_fn]
crab_config.JobType.outputFiles = ['expected.root', 'observed.root', 'combine_output.txtgz']
if submit_config.no_systematics:
    crab_config.JobType.outputFiles += ['expectedS0.root', 'observedS0.root']

crab_config.Data.splitting = 'EventBased'
crab_config.Data.unitsPerJob = 1
crab_config.Data.totalUnits = submit_config.njobs
crab_config.Data.publication = False
crab_config.Data.outputPrimaryDataset = batch_name
crab_config.Data.outputDatasetTag = 'SETME'

crab_config.Site.storageSite = 'T3_US_FNALLPC'
crab_config.Site.whitelist = ['T2_*', 'T3_*']

def callback(sample):
    crab_config.General.requestName = crab_config.Data.outputDatasetTag = submit_config.batch_dir(sample)
    steering = submit_config.steering_sh(sample, xrdcp_combine_tarball=False)
    open(steering_fn, 'wt').write(steering)

    if not submit_config.testing:
        try:
            output = crab_command('submit', config=crab_config)
        except CRABConfigException:
            output = 'problem'
        open(os.path.join(crab_config.General.workArea, 'crab_%s' % crab_config.General.requestName, 'cs_ex'), 'wt').write(gitstatus_dir)
        print colors.boldwhite(sample.name)
        pprint(output)
        print
    else:
        print 'crab config:'
        print crab_config
        print 'steering.sh:'
        os.system('cat ' + steering_fn)

submit(callback)

if not submit_config.testing:
    for x in to_rm:
        os.remove(x)

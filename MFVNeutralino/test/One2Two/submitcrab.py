#!/usr/bin/env python

from JMTucker.Tools.CRAB3Tools import Config, crab_command
from submitcommon import *

submitter = Submitter()

dummy_pset_fn = 'dummy.py'
fjr_fn = 'FrameworkJobReport.xml'
combine_tarball_fn = 'root://cmseos.fnal.gov//store/user/tucker/combine.tgz'
combine_tarball_bn = os.path.basename(combine_tarball_fn)

submitter.tmp_fns += [dummy_pset_fn, fjr_fn, combine_tarball_bn]

open(dummy_pset_fn, 'wt').write('''
import FWCore.ParameterSet.Config as cms
process = cms.Process('dummy')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.maxLuminosityBlocks = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('EmptySource')
''')

open(fjr_fn,'wt').write('''
<FrameworkJobReport>
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
crab_config.General.workArea = submitter.work_area
crab_config.General.requestName = 'SETME'

crab_config.JobType.allowUndistributedCMSSW = True
crab_config.JobType.pluginName = 'PrivateMC'
crab_config.JobType.psetName = 'dummy.py'
crab_config.JobType.scriptExe = 'submit.sh'
crab_config.JobType.scriptArgs = []
#crab_config.JobType.sendPythonFolder = True
#crab_config.JobType.maxMemoryMB = 3000
crab_config.JobType.inputFiles = submitter.input_files +  [fjr_fn, combine_tarball_bn]
crab_config.JobType.outputFiles = submitter.output_files

crab_config.Data.splitting = 'EventBased'
crab_config.Data.unitsPerJob = 1
crab_config.Data.publication = False
crab_config.Data.outputPrimaryDataset = submitter.batch_name
crab_config.Data.outputDatasetTag = 'SETME'

crab_config.Site.storageSite = 'T3_US_FNALLPC'
crab_config.Site.whitelist = ['T2_*', 'T3_*']

def callback(njobs, samples):
    batch_dir = crab_config.General.requestName = crab_config.Data.outputDatasetTag = submitter.batch_dir(samples)
    crab_config.Data.totalUnits = njobs

    if not submitter.testing:
        output = crab_command('submit', config=crab_config)
        open(os.path.join(crab_config.General.workArea, 'crab_%s' % crab_config.General.requestName, 'cs_ex'), 'wt').write(submitter.gitstatus_dir)
        print colors.boldwhite(batch_dir)
        pprint(output)
        print
    else:
        print 'crab config:'
        print crab_config
        print submitter.steering_fn + ':'
        os.system('cat ' + submitter.steering_fn)
        print

submitter.submit('crab', callback)

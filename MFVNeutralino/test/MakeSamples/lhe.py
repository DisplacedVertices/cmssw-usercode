raise NotImplementedError('LHE step not updated for 2017 yet')

import sys, FWCore.ParameterSet.Config as cms

debug = 'debug' in sys.argv
randomize = 'norandomize' not in sys.argv
salt = ''
maxevents = 1
jobnum = 1

for arg in sys.argv:
    if arg.startswith('salt='):
        salt = arg.replace('salt=','')
    elif arg.startswith('maxevents='):
        maxevents = int(arg.replace('maxevents=',''))
    elif arg.startswith('jobnum='):
        jobnum = int(arg.replace('jobnum=',''))

################################################################################

process = cms.Process('LHE')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxevents))
process.source = cms.Source('EmptySource', firstLuminosityBlock = cms.untracked.uint32(jobnum))

process.LHEoutput = cms.OutputModule('PoolOutputModule',
    splitLevel = cms.untracked.int32(0),
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    outputCommands = process.LHEEventContent.outputCommands,
    fileName = cms.untracked.string('lhe.root'),
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All', '')

process.externalLHEProducer = cms.EDProducer('ExternalLHEProducer',
    nEvents = cms.untracked.uint32(maxevents),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    numberOfParameters = cms.uint32(1),
    args = cms.vstring('/cvmfs/cms.cern.ch/phys_generator/gridpacks/slc6_amd64_gcc481/13TeV/madgraph/V5_2.2.2/QCD_HT_LO_MLM/QCD_HT2000toInf/v1/QCD_HT2000toInf_tarball.tar.xz')
)

process.lhe_step = cms.Path(process.externalLHEProducer)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.LHEoutput_step = cms.EndPath(process.LHEoutput)
process.schedule = cms.Schedule(process.lhe_step,process.endjob_step,process.LHEoutput_step)

if debug:
    process.options.wantSummary = True
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.a = cms.EDAnalyzer('DummyLHEAnalyzer', src = cms.InputTag('externalLHEProducer'))
    process.pa = cms.Path(process.a)
    process.schedule.insert(-1, process.pa)

if randomize:
    from modify import deterministic_seeds
    deterministic_seeds(process, 1701, salt, jobnum)

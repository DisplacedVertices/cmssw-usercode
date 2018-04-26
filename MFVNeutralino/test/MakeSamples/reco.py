# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17DRPremix
# 9_4_0_patch1 cmsDriver.py step2 --mc --eventcontent AODSIM runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v10 --step RAW2DIGI,RECO,EI --nThreads 8 --era Run2_2017  --fileout file:step1.root --no_exec

import os, sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
import dynamicconf

premix = True

for arg in sys.argv:
    if arg.startswith('premix='):
        premix = arg.replace('premix=','') == '1'

process = cms.Process('RECO', eras.Run2_2017)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
if premix:
    pass
else:
    raise NotImplementedError('need to set up non-premix')
    process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:rawhlt.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
                                        compressionAlgorithm = cms.untracked.string('LZMA'),
                                        compressionLevel = cms.untracked.int32(4),
                                        eventAutoFlushCompressedSize = cms.untracked.int32(31457280),
                                        fileName = cms.untracked.string('reco.root'),
                                        outputCommands = process.AODSIMEventContent.outputCommands,
                                        )

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, dynamicconf.globaltag, '')

process.raw2digi_step = cms.Path(process.RawToDigi)
if not premix:
    raise NotImplementedError('need to set up non-premix')
    process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.raw2digi_step)
if not premix:
    raise NotImplementedError('need to set up non-premix')
    process.schedule.append(process.L1Reco_step)
process.schedule.extend([process.reconstruction_step,process.eventinterpretaion_step,process.AODSIMoutput_step])
# task?

from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)

process.dummyForPsetHash = cms.PSet(dummy = cms.string(os.environ.get('DUMMYFORHASH', '')))

# from configs in dbs for /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM
# and /QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM
# and https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMCcampaignRunIISummer16DR80Premix

import os, sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

premix = True

for arg in sys.argv:
    if arg.startswith('premix='):
        premix = arg.replace('premix=','') != '0'

process = cms.Process('RECO', eras.Run2_2016)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
if not premix:
    process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:hlt.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True),
    )

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
                                        compressionAlgorithm = cms.untracked.string('LZMA'),
                                        compressionLevel = cms.untracked.int32(4),
                                        eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                        fileName = cms.untracked.string('reco.root'),
                                        outputCommands = process.AODSIMEventContent.outputCommands,
                                        )

from Configuration.AlCa.GlobalTag import GlobalTag
from dynamicconf import globaltag
process.GlobalTag = GlobalTag(process.GlobalTag, globaltag, '')

process.raw2digi_step = cms.Path(process.RawToDigi)
if not premix:
    process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.raw2digi_step)
if not premix:
    process.schedule.append(process.L1Reco_step)
process.schedule.extend([process.reconstruction_step,process.eventinterpretaion_step,process.AODSIMoutput_step])

from FWCore.ParameterSet.Utilities import convertToUnscheduled, cleanUnscheduled
process = cleanUnscheduled(convertToUnscheduled(process))

process.dummyForPsetHash = cms.PSet(dummy = cms.string(os.environ.get('DUMMYFORHASH', '')))

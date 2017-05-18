# from configs in dbs for /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM
# and /QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISummer16DR80Premix-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/AODSIM
# and https://twiki.cern.ch/twiki/bin/viewauth/CMS/PdmVMCcampaignRunIISummer16DR80Premix

import sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

randomize = 'norandomize' not in sys.argv
salt = ''
premix = True
trigfilter = False
trigfilterpath = 'HLT_PFHT800_v7'
jobnum = 1

for arg in sys.argv:
    if arg.startswith('salt='):
        salt = arg.replace('salt=','')
    elif arg.startswith('jobnum='):
        jobnum = int(arg.replace('jobnum=',''))
    elif arg.startswith('premix='):
        premix = arg.replace('premix=','') == '1'
    elif arg.startswith('trigfilter='):
        trigfilter = arg.replace('trigfilter=','') == '1'

process = cms.Process('HLT', eras.Run2_2016)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
if premix:
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    process.load('Configuration.StandardSequences.DigiDMPreMix_cff')
    process.load('SimGeneral.MixingModule.digi_MixPreMix_cfi')
    process.load('Configuration.StandardSequences.DataMixerPreMix_cff')
    process.load('Configuration.StandardSequences.SimL1EmulatorDM_cff')
    process.load('Configuration.StandardSequences.DigiToRawDM_cff')
else:
    process.load('SimGeneral.MixingModule.mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi')
    process.load('Configuration.StandardSequences.Digi_cff')
    process.load('Configuration.StandardSequences.SimL1Emulator_cff')
    process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_25ns15e33_v4_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:gensim.root'))

if 'debug' in sys.argv:
    process.options.wantSummary = True
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.maxEvents.input = 50

process.output = cms.OutputModule('PoolOutputModule',
                                  fileName = cms.untracked.string('rawhlt.root'),
                                  outputCommands = process.PREMIXRAWEventContent.outputCommands if premix else process.RAWSIMEventContent.outputCommands,
                                  eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
                                  splitLevel = cms.untracked.int32(0),
                                  )
if trigfilter:
    process.output.SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring(trigfilterpath))

import minbias
if premix:
    process.mixData.input.fileNames = minbias.premix_files()
    process.mix.digitizers = cms.PSet(process.theDigitizersMixPreMix)
else:
    process.mix.input.fileNames = minbias.files()

from Configuration.AlCa.GlobalTag import GlobalTag
from dynamicconf import globaltag
process.GlobalTag = GlobalTag(process.GlobalTag, globaltag, '')

process.digitisation_step = cms.Path(process.pdigi)
if premix:
    process.datamixing_step = cms.Path(process.pdatamix)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.output_step = cms.EndPath(process.output)

process.schedule = cms.Schedule(process.digitisation_step)
if premix:
    process.schedule.append(process.datamixing_step)
process.schedule.extend([process.L1simulation_step,process.digi2raw_step])

if trigfilter:
    process.HLTSchedule = cms.Schedule(process.HLTriggerFirstPath, getattr(process, trigfilterpath), process.HLTriggerFinalPath, process.HLTAnalyzerEndpath)
process.schedule.extend(process.HLTSchedule)

process.schedule.append(process.output_step)

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforFullSim 
process = customizeHLTforFullSim(process)

if randomize: # for minbias
    from modify import deterministic_seeds
    deterministic_seeds(process, 74205, salt, jobnum)

categories = ['L1TGlobal']
print 'silencing MessageLogger about these categories:', categories
for category in categories:
    process.MessageLogger.categories.append(category)
    setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

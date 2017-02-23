# from configs in dbs for /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM

import sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

randomize = 'norandomize' not in sys.argv

process = cms.Process('HLT', eras.Run2_2016)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('SimGeneral.MixingModule.mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi')
process.load('HLTrigger.Configuration.HLT_25ns15e33_v4_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:gensim.root'))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
                                        fileName = cms.untracked.string('hlt.root'),
                                        outputCommands = process.RAWSIMEventContent.outputCommands,
                                        eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
                                        splitLevel = cms.untracked.int32(0),
                                        )

import minbias
process.mix.input.fileNames = minbias.files

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '80X_mcRun2_asymptotic_2016_TrancheIV_v6', '')

process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.RAWSIMoutput_step])

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforFullSim 
process = customizeHLTforFullSim(process)

if randomize: # for minbias
    from modify import randomize_seeds
    randomize_seeds(process)

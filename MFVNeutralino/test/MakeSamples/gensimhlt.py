import sys, os, FWCore.ParameterSet.Config as cms
from modify import *

process = cms.Process('HLT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_2012_Summer_50ns_PoissonOOTPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('HLTrigger.Configuration.HLT_7E33v2_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

import minbias
process.mix.input.fileNames = minbias.files

process.source = cms.Source('EmptySource')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.output = cms.OutputModule('PoolOutputModule',
				  splitLevel = cms.untracked.int32(0),
				  eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
				  outputCommands = process.RAWSIMEventContent.outputCommands,
				  fileName = cms.untracked.string('gensimhlt.root'),
				  dataset = cms.untracked.PSet(filterName = cms.untracked.string(''), dataTier = cms.untracked.string('GEN-SIM-RAW')),
				  SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('generation_step')),
				  )

process.genstepfilter.triggerConditions = cms.vstring('generation_step')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V7C::All', '')

process.generator = cms.EDFilter('Pythia8175GeneratorFilter',
				 crossSection = cms.untracked.double(1),
				 maxEventsToPrint = cms.untracked.int32(0),
				 pythiaPylistVerbosity = cms.untracked.int32(0),
				 filterEfficiency = cms.untracked.double(1.0),
				 pythiaHepMCVerbosity = cms.untracked.bool(False),
				 comEnergy = cms.double(8000.0),
				 PythiaParameters = cms.PSet(
                                     parameterSets = cms.vstring('processParameters'),
                                     processParameters = cms.vstring(
                                         'Main:timesAllowErrors = 10000',
                                         'SLHA:file = minSLHA.spc',
                                         'SUSY:gg2gluinogluino = on',
                                         'SUSY:qqbar2gluinogluino = on',
                                         'SUSY:idA = 1000021',
                                         'SUSY:idB = 1000021',
                                         'Tune:pp 5',
					 )
                                     ),
				 )

process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.output)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.simulation_step,process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.endjob_step,process.output_step])

for path in process.paths:
    getattr(process,path)._seq = process.generator * getattr(process,path)._seq 

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 
process = customizeHLTforMC(process)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
for category in ['TwoTrackMinimumDistance']:
    process.MessageLogger.categories.append(category)
    setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

if 'modify' in sys.argv:
    set_neutralino_tau0(process, 1)
    set_masses(405, 400)

#process.maxEvents.input = 1 ; open('pset.py','wt').write(process.dumpPython())

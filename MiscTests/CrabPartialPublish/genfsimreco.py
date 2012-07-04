import FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('FastSimulation.Configuration.EventContent_cff')
process.load('FastSimulation.PileUpProducer.PileUpSimulator_2012_Startup_inTimeOnly_cff')
process.load('FastSimulation.Configuration.Geometries_START_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('FastSimulation.Configuration.FamosSequences_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedParameters_cfi')
process.load('HLTrigger.Configuration.HLT_GRun_Famos_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.source = cms.Source("EmptySource")
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
                                        outputCommands = process.AODSIMEventContent.outputCommands,
                                        fileName = cms.untracked.string('fastsim.root'),
                                        SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('generation_step'))
                                        )

process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic8TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.GlobalTag.globaltag = 'START52_V10::All'

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
				 crossSection = cms.untracked.double(1),
				 maxEventsToPrint = cms.untracked.int32(1),
				 pythiaPylistVerbosity = cms.untracked.int32(1),
				 filterEfficiency = cms.untracked.double(1.0),
				 pythiaHepMCVerbosity = cms.untracked.bool(False),
				 comEnergy = cms.double(8000.0),
				 offsetNeutralinoDecayProducts = cms.untracked.bool(True),
				 PythiaParameters = cms.PSet(
					 processParameters = cms.vstring(
						 'Main:timesAllowErrors    = 10000',
						 'SLHA:file = minSLHA.spc',
						 'SUSY:gg2gluinogluino  = on',
						 'SUSY:qqbar2gluinogluino  = on',
						 'SUSY:idA        = 1000021 ',
						 'SUSY:idB        = 1000021 ',
                                                 '1000022:tau0 = 1.0' #mm
						 'Tune:pp 2',                      
						 'Tune:ee 3'),
					 parameterSets = cms.vstring('processParameters')
					 )
				 )

process.ProductionFilterSequence = cms.Sequence(process.generator)
process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])
for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

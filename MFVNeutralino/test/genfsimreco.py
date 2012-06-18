import os, sys, FWCore.ParameterSet.Config as cms

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
process.options = cms.untracked.PSet()

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.AODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('fastsim.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RECO')
    ),
    SelectEvents = cms.untracked.PSet(
        SelectEvents = cms.vstring('generation_step')
    )
)

process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic8TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.GlobalTag.globaltag = 'START52_V9::All'

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
				 crossSection = cms.untracked.double(1),
				 maxEventsToPrint = cms.untracked.int32(1),
				 pythiaPylistVerbosity = cms.untracked.int32(1),
				 filterEfficiency = cms.untracked.double(1.0),
				 pythiaHepMCVerbosity = cms.untracked.bool(False),
				 comEnergy = cms.double(8000.0),
				 PythiaParameters = cms.PSet(
					 processParameters = cms.vstring(
						 'Main:timesAllowErrors    = 10000',
						 'SLHA:file = minSLHA.spc',
						 'SUSY:gg2gluinogluino  = on',
						 'SUSY:qqbar2gluinogluino  = on',
						 'SUSY:idA        = 1000021 ',
						 'SUSY:idB        = 1000021 ',
						 '1000022:tau0 = 0.1 ',  # c*tau = 1/10 mm
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

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = glite

[CMSSW]
datasetpath = None
pset = nino3jet.py
get_edm_output = 1
number_of_jobs = 100
events_per_job = 1000
first_lumi = 1

[USER]
ui_working_dir = crab/crab_nino3jet_genfsimreco_test
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = nino3jet_genfsimreco_test
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''
    
    open('crab.cfg','wt').write(crab_cfg)
    os.system('crab -create -submit')
    os.system('rm -f crab.cfg')

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
				 offsetNeutralinoDecayProducts = cms.untracked.bool(True),
				 PythiaParameters = cms.PSet(
					 processParameters = cms.vstring(
						 'Main:timesAllowErrors    = 10000',
						 'SLHA:file = minSLHA.spc',
						 'SUSY:gg2gluinogluino  = on',
						 'SUSY:qqbar2gluinogluino  = on',
						 'SUSY:idA        = 1000021 ',
						 'SUSY:idB        = 1000021 ',
						 'Tune:pp 2',                      
						 'Tune:ee 3'),
					 parameterSets = cms.vstring('processParameters')
					 )
				 )

def set_neutralino_tau0(tau0):
    process.generator.PythiaParameters.processParameters.append('1000022:tau0 = %f' % tau0) # tau0 is in mm by pythia convention

set_neutralino_tau0(1) # if this gets called again later (e.g. in the batch scripts) it's fine -- the last instance will be used by pythia

process.ProductionFilterSequence = cms.Sequence(process.generator)

process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])

if 0:
	process.printList = cms.EDAnalyzer('ParticleListDrawer',
					   maxEventsToPrint = cms.untracked.int32(100),
					   src = cms.InputTag('genParticles'),
					   printOnlyHardInteraction = cms.untracked.bool(False),
					   useMessageLogger = cms.untracked.bool(False),
					   printVertex = cms.untracked.bool(True),
					   )
	
	process.ppp = cms.Path(process.printList)
	process.schedule.extend([process.ppp])

for path in process.paths:
	getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = glite

[CMSSW]
datasetpath = None
pset = genfsimreco_crab.py
get_edm_output = 1
number_of_jobs = 50
events_per_job = 500
first_lumi = 1

[USER]
additional_input_files = minSLHA.spc
ui_working_dir = crab/crab_mfvneutralino_genfsimreco_%(name)s
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = mfvneutralino_genfsimreco_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''

    testing = 'testing' in sys.argv

    jobs = [
        ('tau1mm', 1.0),
        ('tau9p9mm', 9.9),
        ('tau100um', 0.1),
        ('tau10um', 0.01),
        ]

    for name, tau0 in jobs:
        new_py = open('genfsimreco.py').read()
        new_py += '\nset_neutralino_tau0(%e)\n' % tau0
        open('genfsimreco_crab.py', 'wt').write(new_py)
        open('crab.cfg','wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg genfsimreco_crab.py')

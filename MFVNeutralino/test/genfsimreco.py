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

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.source = cms.Source("EmptySource")

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

process.genstepfilter.triggerConditions = cms.vstring("generation_step")
process.famosSimHits.SimulateCalorimetry = True
process.famosSimHits.SimulateTracking = True
process.simulation = cms.Sequence(process.simulationWithFamos)
process.HLTEndSequence = cms.Sequence(process.reconstructionWithFamos)
process.Realistic8TeVCollisionVtxSmearingParameters.type = cms.string("BetaFunc")
process.famosSimHits.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
process.famosPileUp.VertexGenerator = process.Realistic8TeVCollisionVtxSmearingParameters
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:startup_GRun', '')

process.generator = cms.EDFilter("Pythia8GeneratorFilter",
				 crossSection = cms.untracked.double(1),
				 maxEventsToPrint = cms.untracked.int32(0),
				 pythiaPylistVerbosity = cms.untracked.int32(0),
				 filterEfficiency = cms.untracked.double(1.0),
				 pythiaHepMCVerbosity = cms.untracked.bool(False),
				 comEnergy = cms.double(8000.0),
				 offsetDecayParent = cms.int32(1000021),
				 offsetDecayProducts = cms.vint32(3,5,6),
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

process.ProductionFilterSequence = cms.Sequence(process.generator)

process.generation_step = cms.Path(process.pgen_genonly)
process.reconstruction = cms.Path(process.reconstructionWithFamos)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.reconstruction,process.AODSIMoutput_step])

if 'debug' in sys.argv:
    process.generator.maxEventsToPrint = 5
    process.generator.pythiaPylistVerbosity = 1
    process.generator.pythiaHepMCVerbosity = True
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

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 
customizeHLTforMC(process)


def set_particle_tau0(id, tau0):
    line = '%i:tau0' % id
    params = [x for x in process.generator.PythiaParameters.processParameters.value() if line not in x]
    process.generator.PythiaParameters.processParameters = params
    process.generator.PythiaParameters.processParameters.append('%s = %f' % (line, tau0)) # tau0 is in mm by pythia convention

def set_gluino_tau0(tau0):
    set_particle_tau0(1000021, tau0)

def set_mass(m_gluino, fn='minSLHA.spc'):
    slha = '''
BLOCK SPINFO  # Spectrum calculator information
     1   Minimal    # spectrum calculator
     2   1.0.0         # version number
#
BLOCK MODSEL  # Model selection
     1     1   #
#

BLOCK MASS  # Mass Spectrum
# PDG code           mass       particle
  1000021     %(m_gluino)E       # ~g

DECAY   1000021     0.01E+00   # gluino decays
#           BR         NDA      ID1       ID2       ID3
     0.5E+00          3            3          5           6   # BR(~g -> s b t)
     0.5E+00          3           -3         -5          -6   # BR(~g -> sbar bbar tbar)
'''
    open(fn, 'wt').write(slha % locals())

set_gluino_tau0(1)
set_mass(300)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = glite

[CMSSW]
datasetpath = None
pset = genfsimreco_crab.py
get_edm_output = 1
number_of_jobs = 1000
events_per_job = 200
first_lumi = 1

[USER]
additional_input_files = minSLHA.spc
ui_working_dir = crab/genfsimreco/crab_mfv_genfsimreco_%(name)s
copy_data = 1
storage_element = T3_US_Cornell
publish_data = 1
publish_data_name = mfv_genfsimreco_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''

    os.system('mkdir -p crab/genfsimreco')
    testing = 'testing' in sys.argv

    def submit(name, tau0, mass):
        new_py = open('genfsimreco.py').read()
        new_py += '\nset_gluino_tau0(%e)\n' % tau0
        new_py += '\nset_mass(%i)\n' % mass
        open('genfsimreco_crab.py', 'wt').write(new_py)
        open('crab.cfg','wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create')
            os.system('rm -f crab.cfg genfsimreco_crab.py genfsimreco_crab.pyc')

    tau0s = [0., 0.01, 0.1, 1.0, 4.0, 9.9]
    masses = [200, 400, 600, 800, 1000]

    tau0s = [0.01]
    masses = [400]
    
    for tau0 in tau0s:
        for mass in masses:
            name = 'gluino_tau%04ium_M%i' % (int(tau0*1000), mass)
            submit(name, tau0, mass)

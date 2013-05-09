import sys, os, FWCore.ParameterSet.Config as cms

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

process.source = cms.Source('EmptySource')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

process.output = cms.OutputModule('PoolOutputModule',
				  splitLevel = cms.untracked.int32(0),
				  eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
				  outputCommands = process.RAWDEBUGEventContent.outputCommands,
				  fileName = cms.untracked.string('gensimhlt.root'),
				  dataset = cms.untracked.PSet(filterName = cms.untracked.string(''), dataTier = cms.untracked.string('GEN-SIM-RAW')),
				  SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('generation_step')),
				  )

process.genstepfilter.triggerConditions = cms.vstring('generation_step')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V7C::All', '')

process.generator = cms.EDFilter('Pythia8GeneratorFilter',
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

if 'genonly' in sys.argv:
    process.schedule = cms.Schedule(process.generation_step,process.genfiltersummary_step,process.output_step)
    process.maxEvents.input = 1000

if 'debug' in sys.argv:
    process.options.wantSummary = True
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.generator.maxEventsToPrint = 2
    process.generator.pythiaPylistVerbosity = 13
    process.generator.pythiaHepMCVerbosity = True
    process.printList = cms.EDAnalyzer('ParticleListDrawer',
                                       maxEventsToPrint = cms.untracked.int32(100),
                                       src = cms.InputTag('genParticles'),
                                       printOnlyHardInteraction = cms.untracked.bool(False),
                                       useMessageLogger = cms.untracked.bool(False),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.dumpGraph = cms.EDAnalyzer('GenParticlesGraphDumper',
                                       src = cms.InputTag('genParticles'),
                                       use_mothers = cms.bool(True),
                                       use_daughters = cms.bool(False),
                                       include_id_and_stat = cms.bool(True),
                                       )
    process.pprint = cms.Path(process.printList * process.dumpGraph)
    process.schedule.extend([process.pprint])
else:
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
    for category in ['TwoTrackMinimumDistance']:
        process.MessageLogger.categories.append(category)
        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

def set_particle_tau0(id, tau0):
    params = [x for x in process.generator.PythiaParameters.processParameters.value() if ':tau0' not in x]
    process.generator.PythiaParameters.processParameters = params
    process.generator.PythiaParameters.processParameters.append('%i:tau0 = %f' % (id, tau0)) # tau0 is in mm by pythia convention

def set_gluino_tau0(tau0):
    set_particle_tau0(1000021, tau0)

def set_neutralino_tau0(tau0):
    set_particle_tau0(1000022, tau0)

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

def set_masses(m_gluino, m_neutralino, fn='minSLHA.spc'):
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
  1000022     %(m_neutralino)E   # ~chi_10

DECAY   1000021     0.01E+00   # gluino decays
#          BR         NDA      ID1       ID2
    1.0E00            2      1000022    21   # BR(~g -> ~chi_10  g)

DECAY   1000022     0.01E+00   # neutralino decays
#           BR         NDA      ID1       ID2       ID3
     0.5E+00          3            3          5           6   # BR(~chi_10 -> s b t)
     0.5E+00          3           -3         -5          -6   # BR(~chi_10 -> sbar bbar tbar)
'''
    open(fn, 'wt').write(slha % locals())

#set_gluino_tau0(1)
#set_mass(400)

set_neutralino_tau0(1)
set_masses(405, 400)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = glite

[CMSSW]
datasetpath = None
pset = gensimhlt_crab.py
get_edm_output = 1
events_per_job = 40
total_number_of_events = 10000
first_lumi = 1

[USER]
additional_input_files = minSLHA.spc
ui_working_dir = crab/gensimhlt/crab_mfv_gensimhlt_%(name)s
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = mfv_gensimhlt_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
jmt_externals_hack = pythia8_hack
jmt_externals_hack_dirs = GeneratorInterface/Pythia8Interface

[GRID]
ce_black_list = metu.edu.tr,uoi.gr,troitsk.ru,brunel.ac.uk,bris.ac.uk,kfki.hu,pi.infn.it,ihep.su,ciemat.es,jinr-t1.ru,nectec.or.th,ts.infn.it,hep.by
'''

    pythia8_hack = '''config/toolbox/${SCRAM_ARCH}/tools/selected/pythia8.xml
pythia8
165-cms
<tool name="pythia8" version="165-cms">
  <lib name="pythia8"/>
  <lib name="hepmcinterface"/>
  <client>
    <environment name="PYTHIA8_BASE" default="${CMSSW_RELEASE_BASE}/../../../external/pythia8/165-cms"/>
    <environment name="LIBDIR" default="${CMSSW_RELEASE_BASE}/../../../external/pythia8/165-cms/lib"/>
    <environment name="INCLUDE" default="${CMSSW_RELEASE_BASE}/../../../external/pythia8/165-cms/include"/>
  </client>
  <runtime name="PYTHIA8DATA" value="${CMSSW_RELEASE_BASE}/../../../external/pythia8/165-cms/xmldoc"/>
  <use name="cxxcompiler"/>
  <use name="hepmc"/>
  <use name="pythia6"/>
  <use name="clhep"/>
  <use name="lhapdf"/>
</tool>
'''

    if os.environ['USER'] != 'tucker':
        raw_input('do you have the jmt_externals_hack for crab? if not, ^C now.')

    os.system('mkdir -p crab/gensimhlt')
    testing = 'testing' in sys.argv

    def submit(name, tau0, mass):
        new_py = open('gensimhlt.py').read()
        if 'gluino' in name:
            new_py += '\nset_gluino_tau0(%e)\n' % tau0
            new_py += '\nset_mass(%i)\n' % mass
        elif 'neutralino' in name:
            new_py += '\nset_neutralino_tau0(%e)\n' % tau0
            new_py += '\nset_masses(%i,%i)\n' % (mass+5, mass)
        else:
            raise 'buh?'
        open('gensimhlt_crab.py', 'wt').write(new_py)
        open('pythia8_hack', 'wt').write(pythia8_hack)
        open('crab.cfg','wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg gensimhlt_crab.py gensimhlt_crab.pyc pythia8_hack')

    submit('neutralino_tau1000um_M0400', 1.0, 400)
    sys.exit(0)

    tau0s = [0., 0.01, 0.1, 1.0, 4.0, 9.9]
    masses = [200, 400, 600, 800, 1000]

    for tau0 in tau0s:
        for mass in masses:
            name = 'gluino_tau%04ium_M%04i' % (int(tau0*1000), mass)
            submit(name, tau0, mass)

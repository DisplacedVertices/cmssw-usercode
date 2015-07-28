# 740pre6: cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi --no_exec -n 10 --conditions MCRUN2_74_V7 --eventcontent RAWSIM -s GEN --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1

debug = False

import sys, os, FWCore.ParameterSet.Config as cms

process = cms.Process('GEN')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.source = cms.Source('EmptySource')

process.genstepfilter.triggerConditions = cms.vstring('generation_step')

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

process.generator = cms.EDFilter('Pythia8GeneratorFilter',
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        parameterSets = cms.vstring(
            'pythia8CommonSettings', 
            'tuneSettings', 
            'processParameters'
            ),
        processParameters = cms.vstring(
            'SLHA:file = my.slha',
            'SUSY:gg2gluinogluino = on',
            'SUSY:qqbar2gluinogluino = on',
            'SUSY:idA = 1000021',
            'SUSY:idB = 1000021',
            ),
        tuneSettings = cms.vstring(
            # CUEP8M1
            'Tune:pp 14', 
            'Tune:ee 7', 
            'MultipartonInteractions:pT0Ref=2.4024', 
            'MultipartonInteractions:ecmPow=0.25208', 
            'MultipartonInteractions:expPow=1.6'
            ),
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2', 
            'Main:timesAllowErrors = 10000', 
            'Check:epTolErr = 0.01', 
            'Beams:setProductionScalesFromLHEF = off', 
            'SLHA:keepSM = on', 
            'SLHA:minMassSM = 1000.', 
            'ParticleDecays:limitTau0 = on', 
            'ParticleDecays:tau0Max = 20', 
            'ParticleDecays:allowPhotonRadiation = on'
            ),
        ),
    )

process.generation_step = cms.Path(process.pgen)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('generation_step')),
    fileName = cms.untracked.string('gen.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    splitLevel = cms.untracked.int32(0),
)

process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

sched = [process.generation_step, process.genfiltersummary_step, process.RAWSIMoutput_step]

if debug:
    process.options.wantSummary = True
    process.MessageLogger.cerr.FwkReport.reportEvery = 1
    process.generator.maxEventsToPrint = 2
    process.generator.pythiaPylistVerbosity = 13
    process.generator.pythiaHepMCVerbosity = True
    process.p = cms.EDAnalyzer('JMTParticleListDrawer',
                               src = cms.InputTag('genParticles'),
                               printVertex = cms.untracked.bool(True),
                               )
    process.pp = cms.Path(process.p)
    sched.insert(-1, process.pp)

process.schedule = cms.Schedule(*sched)

process.ProductionFilterSequence = cms.Sequence(process.generator)
for path in process.paths:
    getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein

[CMSSW]
datasetpath = None
pset = gen.py
get_edm_output = 1
events_per_job = 4000
total_number_of_events = 100000
first_lumi = 1
use_dbs3 = 1

[USER]
ssh_control_persist = no
additional_input_files = minSLHA.spc
ui_working_dir = %(ui_working_dir)s
copy_data = 1
storage_element = T3_US_Cornell
publish_data = 1
publish_data_name = mfv_hltrun2_%(name)s
dbs_url_for_publication = phys03

[GRID]
#se_black_list =
'''

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

    testing = 'testing' in sys.argv
    dir_root = 'crab/HLTRun2/Gen'
    os.system('mkdir -p %s' % dir_root)

    masses = range(200, 1001, 100)

    for m_neutralino in masses:
        m_gluino = m_neutralino + 5
        name = 'M%04i' % m_neutralino

        ui_working_dir = os.path.join(dir_root, 'crab_' + name)

        open('minSLHA.spc', 'wt').write(slha % locals())
        open('crab.cfg', 'wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit all')
            os.system('rm minSLHA.spc crab.cfg')

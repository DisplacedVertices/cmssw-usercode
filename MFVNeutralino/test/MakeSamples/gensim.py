# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17GS
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/EXO-RunIIFall17GS-02252
# 9_3_13 cmsDriver.py Configuration/GenProduction/python/s17.py --fileout file:EXO-RunIIFall17GS-02252.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2017 --python_filename EXO-RunIIFall17GS-02252_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 380
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVCampaignRunIIFall18GS
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/EXO-RunIIFall18GS-00073
# 10_2_6 cmsDriver.py Configuration/GenProduction/python/s18.py --fileout file:EXO-RunIIFall18GS-00073.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2018 --python_filename EXO-RunIIFall18GS-00073_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring --customise_commands process.source.numberEventsInLuminosityBlock="cms.untracked.uint32(1000)" -n 892

import sys, FWCore.ParameterSet.Config as cms, dynamicconf

genonly = 'genonly' in sys.argv
debug = 'debug' in sys.argv
randomize = 'norandomize' not in sys.argv
salt = ''
maxevents = 1
jobnum = 1
scanpack = None

for arg in sys.argv:
    if arg.startswith('scanpack='):
        print 'scanpack: wiping out todos'
        todos = []
        scanpack = arg.replace('scanpack=','').split(',')
    elif arg.startswith('salt='):
        salt = arg.replace('salt=','')
    elif arg.startswith('maxevents='):
        maxevents = int(arg.replace('maxevents=',''))
    elif arg.startswith('jobnum='):
        jobnum = int(arg.replace('jobnum=',''))

################################################################################

process = dynamicconf.process()

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly%sCollision_cfi' % dynamicconf.year)
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxevents))
process.source = cms.Source('EmptySource', firstLuminosityBlock = cms.untracked.uint32(jobnum))

process.XMLFromDBSource.label = cms.string("Extended")
process.genstepfilter.triggerConditions = cms.vstring('generation_step')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, dynamicconf.globaltag(), '')

from Configuration.Generator.Pythia8CommonSettings_cfi import pythia8CommonSettingsBlock
from Configuration.Generator.MCTunes2017.PythiaCP2Settings_cfi import pythia8CP2SettingsBlock

# from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import pythia8PSweightsSettingsBlock
# ^ doesn't exist in 2017 CMSSW but the commands work in 2017 CMSSW's pythia 8230
pythia8PSweightsSettingsBlock = cms.PSet(
    pythia8PSweightsSettings = cms.vstring(
        'UncertaintyBands:doVariations = on',
# 3 sets of variations for ISR&FSR up/down
# Reduced sqrt(2)/(1/sqrt(2)), Default 2/0.5 and Conservative 4/0.25 variations
# 32 decorrelated variations of muR and non-singular terms (cNS) for each branching type
        'UncertaintyBands:List = {\
isrRedHi isr:muRfac=0.707,fsrRedHi fsr:muRfac=0.707,isrRedLo isr:muRfac=1.414,fsrRedLo fsr:muRfac=1.414,\
isrDefHi isr:muRfac=0.5,fsrDefHi fsr:muRfac=0.5,isrDefLo isr:muRfac=2.0,fsrDefLo fsr:muRfac=2.0,\
isrConHi isr:muRfac=0.25,fsrConHi fsr:muRfac=0.25,isrConLo isr:muRfac=4.0,fsrConLo fsr:muRfac=4.0,\
fsr_G2GG_muR_dn fsr:G2GG:muRfac=0.5,\
fsr_G2GG_muR_up fsr:G2GG:muRfac=2.0,\
fsr_G2QQ_muR_dn fsr:G2QQ:muRfac=0.5,\
fsr_G2QQ_muR_up fsr:G2QQ:muRfac=2.0,\
fsr_Q2QG_muR_dn fsr:Q2QG:muRfac=0.5,\
fsr_Q2QG_muR_up fsr:Q2QG:muRfac=2.0,\
fsr_X2XG_muR_dn fsr:X2XG:muRfac=0.5,\
fsr_X2XG_muR_up fsr:X2XG:muRfac=2.0,\
fsr_G2GG_cNS_dn fsr:G2GG:cNS=-2.0,\
fsr_G2GG_cNS_up fsr:G2GG:cNS=2.0,\
fsr_G2QQ_cNS_dn fsr:G2QQ:cNS=-2.0,\
fsr_G2QQ_cNS_up fsr:G2QQ:cNS=2.0,\
fsr_Q2QG_cNS_dn fsr:Q2QG:cNS=-2.0,\
fsr_Q2QG_cNS_up fsr:Q2QG:cNS=2.0,\
fsr_X2XG_cNS_dn fsr:X2XG:cNS=-2.0,\
fsr_X2XG_cNS_up fsr:X2XG:cNS=2.0,\
isr_G2GG_muR_dn isr:G2GG:muRfac=0.5,\
isr_G2GG_muR_up isr:G2GG:muRfac=2.0,\
isr_G2QQ_muR_dn isr:G2QQ:muRfac=0.5,\
isr_G2QQ_muR_up isr:G2QQ:muRfac=2.0,\
isr_Q2QG_muR_dn isr:Q2QG:muRfac=0.5,\
isr_Q2QG_muR_up isr:Q2QG:muRfac=2.0,\
isr_X2XG_muR_dn isr:X2XG:muRfac=0.5,\
isr_X2XG_muR_up isr:X2XG:muRfac=2.0,\
isr_G2GG_cNS_dn isr:G2GG:cNS=-2.0,\
isr_G2GG_cNS_up isr:G2GG:cNS=2.0,\
isr_G2QQ_cNS_dn isr:G2QQ:cNS=-2.0,\
isr_G2QQ_cNS_up isr:G2QQ:cNS=2.0,\
isr_Q2QG_cNS_dn isr:Q2QG:cNS=-2.0,\
isr_Q2QG_cNS_up isr:Q2QG:cNS=2.0,\
isr_X2XG_cNS_dn isr:X2XG:cNS=-2.0,\
isr_X2XG_cNS_up isr:X2XG:cNS=2.0}',
        
        'UncertaintyBands:nFlavQ = 4', # define X=bottom/top in X2XG variations
        'UncertaintyBands:MPIshowers = on',
        'UncertaintyBands:overSampleFSR = 10.0',
        'UncertaintyBands:overSampleISR = 10.0',
        'UncertaintyBands:FSRpTmin2Fac = 20',
        'UncertaintyBands:ISRpTmin2Fac = 1'
        )
)

isrfsr = pythia8PSweightsSettingsBlock.pythia8PSweightsSettings[1] # 2-45
pdf = [
    'pdfplus isr:PDF:plus=1', # 46
    'pdfminus isr:PDF:minus=1', # 47
    'pdffamily isr:PDF:family=1', # 48-147  # needs pythia >= 8240
    ]
pythia8PSweightsSettingsBlock.pythia8PSweightsSettings[1] = isrfsr.replace('}', ',' + ','.join(pdf) + '}')

process.generator = cms.EDFilter('Pythia8GeneratorFilter',
    comEnergy = cms.double(13000.0),
    filterEfficiency = cms.untracked.double(1.0),
    maxEventsToPrint = cms.untracked.int32(0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    pythiaPylistVerbosity = cms.untracked.int32(0),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP2SettingsBlock,
        pythia8PSweightsSettingsBlock,
        pdfSettings = cms.vstring(
            'PDF:pSet = LHAPDF6:NNPDF31_lo_as_0130',
            ),
        parameterSets = cms.vstring(
            'pythia8CommonSettings',
            'pythia8CP2Settings',
            'pdfSettings',
            'pythia8PSweightsSettings',
            'processParameters'
            ),
        processParameters = cms.vstring(),
        ),
    )

process.generation_step = cms.Path(process.pgen)
process.simulation_step = cms.Path(process.psim)
process.genfiltersummary_step = cms.EndPath(process.genFilterSummary)

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
    SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('generation_step')),
    fileName = cms.untracked.string('gensim.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    eventAutoFlushCompressedSize = cms.untracked.int32(20971520),
    splitLevel = cms.untracked.int32(0),
)

process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

if genonly:
    sched = [process.generation_step, process.genfiltersummary_step,                          process.RAWSIMoutput_step]
else:
    sched = [process.generation_step, process.genfiltersummary_step, process.simulation_step, process.RAWSIMoutput_step]

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
#from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
#associatePatAlgosToolsTask(process)

process.ProductionFilterSequence = cms.Sequence(process.generator)
for path in process.paths:
    getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq

if randomize:
    from modify import deterministic_seeds
    deterministic_seeds(process, 8675309, salt, jobnum)

if scanpack:
    from scanpack import do_scanpack
    scanpack_x, scanpack_batch = scanpack
    do_scanpack(process, scanpack_x, int(scanpack_batch), jobnum-1)

from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)

#import modify; modify.set_stop_dbardbar(process, 1., 800); open('gensim_test.py','wt').write(process.dumpPython())

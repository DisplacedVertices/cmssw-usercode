# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17GS and a later request in McM
# 9_3_6_patch2 cmsDriver.py Configuration/GenProduction/python/ThirteenTeV/MC17_DYTo2Mu_M800to1300_CP5_Pythia8_v1.py --fileout file:EXO-RunIIFall17GS-00423.root --mc --eventcontent RAWSIM --datatier GEN-SIM --conditions 93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --step GEN,SIM --nThreads 8 --geometry DB:Extended --era Run2_2017 --python_filename EXO-RunIIFall17GS-00423_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1300 --no_exec

import sys, FWCore.ParameterSet.Config as cms, dynamicconf
from Configuration.StandardSequences.Eras import eras

genonly = 'genonly' in sys.argv
debug = 'debug' in sys.argv
randomize = 'norandomize' not in sys.argv
salt = ''
fromlhe = False
maxevents = 1
jobnum = 1
scanpack = None

for arg in sys.argv:
    if arg == 'fromlhe=1':
        print 'fromlhe: wiping out todos'
        todos = []
        fromlhe = True
    elif arg.startswith('scanpack='):
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

process = cms.Process('SIM', eras.Run2_2017)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic25ns13TeVEarly2017Collision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.cerr.FwkReport.reportEvery = 10000
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))

if fromlhe:
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
    process.source = cms.Source('PoolSource',
                                fileNames = cms.untracked.vstring('file:lhe.root'),
                                inputCommands = cms.untracked.vstring('keep *', 'drop LHEXMLStringProduct_*_*_*'),
                                dropDescendantsOfDroppedBranches = cms.untracked.bool(False),
                                )
else:
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxevents))
    process.source = cms.Source('EmptySource', firstLuminosityBlock = cms.untracked.uint32(jobnum))

process.XMLFromDBSource.label = cms.string("Extended")
process.genstepfilter.triggerConditions = cms.vstring('generation_step')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, dynamicconf.globaltag, '')

process.generator = cms.EDFilter('Pythia8HadronizerFilter' if fromlhe else 'Pythia8GeneratorFilter',
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
        processParameters = cms.vstring(),
        tuneSettings = cms.vstring(
            # CP5
            'Tune:pp 14',
            'Tune:ee 7',
            'MultipartonInteractions:ecmPow=0.03344',
            'PDF:pSet=20',
            'MultipartonInteractions:bProfile=2',
            'MultipartonInteractions:pT0Ref=1.41',
            'MultipartonInteractions:coreRadius=0.7634',
            'MultipartonInteractions:coreFraction=0.63',
            'ColourReconnection:range=5.176',
            'SigmaTotal:zeroAXB=off',
            'SpaceShower:alphaSorder=2',
            'SpaceShower:alphaSvalue=0.118',
            'SigmaProcess:alphaSvalue=0.118',
            'SigmaProcess:alphaSorder=2',
            'MultipartonInteractions:alphaSvalue=0.118',
            'MultipartonInteractions:alphaSorder=2',
            'TimeShower:alphaSorder=2',
            'TimeShower:alphaSvalue=0.118',
            ),
        pythia8CommonSettings = cms.vstring(
            'Tune:preferLHAPDF = 2',
            'Main:timesAllowErrors = 10000',
            'Check:epTolErr = 0.01',
            'Beams:setProductionScalesFromLHEF = off',
            'SLHA:keepSM = on',
            'SLHA:minMassSM = 1000.',
            'ParticleDecays:limitTau0 = on',
            'ParticleDecays:tau0Max = 10',
            'ParticleDecays:allowPhotonRadiation = on'
            ),
        ),
    )

if fromlhe:
    process.generator.PythiaParameters.processParameters = [
        'JetMatching:setMad = off',
        'JetMatching:scheme = 1',
        'JetMatching:merge = on',
        'JetMatching:jetAlgorithm = 2',
        'JetMatching:etaJetMax = 5.',
        'JetMatching:coneRadius = 1.',
        'JetMatching:slowJetPower = 1',
        'JetMatching:qCut = 14.',
        'JetMatching:nQmatch = 5',
        'JetMatching:nJetMax = 4',
        'JetMatching:doShowerKt = off',
        ]

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
    sched = [process.generation_step, process.genfiltersummary_step, process.RAWSIMoutput_step]
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
#task?

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

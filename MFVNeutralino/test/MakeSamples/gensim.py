import sys, FWCore.ParameterSet.Config as cms

fromlhe = 'fromlhe' in sys.argv
genonly = 'genonly' in sys.argv
debug = 'debug' in sys.argv
randomize = 'norandomize' not in sys.argv
maxevents = 1
jobnum = 1

if fromlhe:
    print 'fromlhe: wiping out todo, todo_args, maxevents, jobnum'
    todo, todo_args = None, []
else:
    for arg in sys.argv:
        if arg.startswith('maxevents='):
            maxevents = int(arg.replace('maxevents=',''))
        elif arg.startswith('jobnum='):
            jobnum = int(arg.replace('jobnum=',''))

################################################################################

process = cms.Process('GENSIM')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedNominalCollision2015_cfi')
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

process.genstepfilter.triggerConditions = cms.vstring('generation_step')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_71_V1::All', '')

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
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
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

process.ProductionFilterSequence = cms.Sequence(process.generator)
for path in process.paths:
    getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1
process = customisePostLS1(process)

if randomize:
    from modify import randomize_seeds
    randomize_seeds(process)

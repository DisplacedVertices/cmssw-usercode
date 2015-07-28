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
    from JMTucker.Tools.CRAB3Tools import Config, crab_dirs_root, crab_command
    from JMTucker.Tools.general import save_git_status

    testing = 'testing' in sys.argv
    work_area = crab_dirs_root('mfv_run2_gen')
    if os.path.isdir(work_area):
        sys.exit('work_area %s exists' % work_area)
    os.makedirs(work_area)
    save_git_status(os.path.join(work_area, 'gitstatus'))

    config = Config()

    config.General.transferLogs = True
    config.General.transferOutputs = True
    config.General.workArea = work_area
    config.General.requestName = 'SETME'

    config.JobType.pluginName = 'PrivateMC'
    config.JobType.psetName = 'forsubmit_gen.py'
    config.JobType.inputFiles = ['my.slha']

    config.Data.primaryDataset = 'SETME'
    config.Data.splitting = 'EventBased'
    config.Data.unitsPerJob = 2000
    config.Data.totalUnits = 100000
    config.Data.publication = True
    config.Data.publishDataName = 'gen'

    config.Site.storageSite = 'T3_US_Cornell'

    masses = range(400, 1601, 400)
    tau0s = [100, 300, 1000, 10000] 

    masses = [1000]
    tau0s = [1000]

    outputs = {}

    for tau0 in tau0s:
        for mass in masses:
            name = 'tau%04ium_M%04i' % (tau0, mass)
            print name

            tau0_in_mm = tau0 / 1000.
            write_slha_mfv_neutralino(tau0_in_mm, mass)

            new_py = open('gen.py').read()
            new_py += dedent('''
                             from modify import set_neutralino_tau0
                             set_neutralino_tau0(process, %(tau0_in_mm)f)
                             ''' % locals())

            new_py_fn = config.JobType.psetName
            open(new_py_fn, 'wt').write(new_py)

            config.General.requestName = name
            config.Data.primaryDataset = name

            if not testing:
                outputs[name] = crab_command('submit', config=config)
                os.system('rm my.slha ' + config.JobType.psetName)
                print

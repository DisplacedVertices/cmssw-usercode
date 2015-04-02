# 740pre6: cmsDriver.py TTbar_13TeV_TuneCUETP8M1_cfi --no_exec -n 10 --conditions MCRUN2_74_V7 --eventcontent RAWSIM -s GEN --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1

import FWCore.ParameterSet.Config as cms

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
            'pythia8CUEP8M1Settings', 
            'processParameters'
            ),
        processParameters = cms.vstring(
            'SLHA:file = minSLHA.spc',
            'SUSY:gg2gluinogluino = on',
            'SUSY:qqbar2gluinogluino = on',
            'SUSY:idA = 1000021',
            'SUSY:idB = 1000021',
            '1000022:tau0 = 1.',
            ),
        pythia8CUEP8M1Settings = cms.vstring(
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

process.schedule = cms.Schedule(process.generation_step, process.genfiltersummary_step, process.RAWSIMoutput_step)

process.ProductionFilterSequence = cms.Sequence(process.generator)
for path in process.paths:
    getattr(process,path)._seq = process.ProductionFilterSequence * getattr(process,path)._seq 

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)

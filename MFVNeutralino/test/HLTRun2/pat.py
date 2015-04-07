# 740: cmsDriver.py step5 --no_exec --mc --conditions MCRUN2_74_V7 -n 5 --eventcontent MINIAODSIM --runUnscheduled -s PAT --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1

import FWCore.ParameterSet.Config as cms

process = cms.Process('PAT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:reco.root'))

process.MINIAODSIMoutput = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('pat.root'),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
    dropMetaData = cms.untracked.string('ALL'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.mfvEvent.skip_event_filter = ''
process.mfvEvent.trigger_results_src = ''
process.mfvEvent.cleaning_results_src = ''
process.MINIAODSIMoutput.outputCommands += [
    'keep MFVVertexAuxs_mfvVerticesAux_*_*',
    'keep MFVEvent_mfvEvent__*',
    'keep edmTriggerResults_TriggerResults__HLT',
    'keep edmTriggerResults_TriggerResults__HLT2',
    ]
        
process.pmfv = cms.Path(process.mfvVertexSequence * process.mfvEvent)

from FWCore.ParameterSet.Utilities import convertToUnscheduled
process = convertToUnscheduled(process)

process.load('Configuration.StandardSequences.PATMC_cff')

from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 
process = miniAOD_customizeAllMC(process)

process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False
process.patTrigger.processName = 'HLT2'

process.MessageLogger.categories.extend(["GetManyWithoutRegistration","GetByLabelWithoutRegistration"])
process.MessageLogger.cerr.GetManyWithoutRegistration = process.MessageLogger.cerr.GetByLabelWithoutRegistration = cms.untracked.PSet(reportEvery = cms.untracked.int32(1), optionalPSet = cms.untracked.bool(True), limit = cms.untracked.int32(10000000))

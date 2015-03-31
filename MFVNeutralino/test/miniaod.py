import FWCore.ParameterSet.Config as cms

process = cms.Process('PAT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(

#400 
'/store/user/mzientek/Neutralino_M400_13TeV_DisplaceVtx_GENSIM_721/Neutralino_731_m400_RECO/d44c2d8538052a1dfd80836022488188/step3_731_m400_10_1_KSd.root',

))

process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True))

process.MINIAODSIMoutput = cms.OutputModule('PoolOutputModule',
    compressionLevel = cms.untracked.int32(4),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    outputCommands = process.MINIAODSIMEventContent.outputCommands,
    fileName = cms.untracked.string('file:out.root'),
    dataset = cms.untracked.PSet(
        filterName = cms.untracked.string(''),
        dataTier = cms.untracked.string('MINIAODSIM')
    ),
    dropMetaData = cms.untracked.string('ALL'),
    fastCloning = cms.untracked.bool(False),
    overrideInputFileSplitLevels = cms.untracked.bool(True)
)

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'PHYS14_25_V1', '')

process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

process.load('JMTucker.MFVNeutralino.Vertexer_cff')
process.load('JMTucker.MFVNeutralino.EventProducer_cfi')
process.mfvEvent.skip_event_filter = ''
#process.mfvEvent.trigger_results_src = ''
process.mfvEvent.cleaning_results_src = ''
process.MINIAODSIMoutput.outputCommands += ['keep MFVVertexAuxs_mfvVerticesAux_*_*', 'keep MFVEvent_mfvEvent__*', 'keep edmTriggerResults_TriggerResults__HLT']
        
process.pmfv = cms.Path(process.mfvVertexSequence * process.mfvEvent)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
from FWCore.ParameterSet.Utilities import convertToUnscheduled
process=convertToUnscheduled(process)
process.load('Configuration.StandardSequences.PATMC_cff')

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.PatAlgos.slimming.miniAOD_tools
from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 

#call to customisation function miniAOD_customizeAllMC imported from PhysicsTools.PatAlgos.slimming.miniAOD_tools
process = miniAOD_customizeAllMC(process)

# End of customisation functions



process.MessageLogger.categories.extend(["GetManyWithoutRegistration","GetByLabelWithoutRegistration"])
_messageSettings = cms.untracked.PSet(
                reportEvery = cms.untracked.int32(1),
                            optionalPSet = cms.untracked.bool(True),
                            limit = cms.untracked.int32(10000000)
                        )

process.MessageLogger.cerr.GetManyWithoutRegistration = _messageSettings
process.MessageLogger.cerr.GetByLabelWithoutRegistration = _messageSettings

process.patMuons.embedTrack = False
process.patElectrons.embedTrack = False

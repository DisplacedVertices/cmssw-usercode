import FWCore.ParameterSet.Config as cms

def pat_tuple_process(customize_before_unscheduled, is_mc):
    process = cms.Process('PAT')

    process.load('FWCore.MessageService.MessageLogger_cfi')
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
    for x in ['GetManyWithoutRegistration', 'GetByLabelWithoutRegistration']:
        process.MessageLogger.categories.append(x)
        setattr(process.MessageLogger.cerr, x, cms.untracked.PSet(reportEvery = cms.untracked.int32(1),
                                                                  optionalPSet = cms.untracked.bool(True),
                                                                  limit = cms.untracked.int32(10000000)
                                                                  ))

    process.load('Configuration.StandardSequences.Services_cff')
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.load('Configuration.EventContent.EventContent_cff')
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_38T_cff')
    #process.load('Configuration.StandardSequences.EndOfProcess_cff')

    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V9', '')

    process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True))
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:/uscms_data/d2/tucker/F47E7F59-8A29-E511-8667-002590A52B4A.root'))

    process.out = cms.OutputModule('PoolOutputModule',
                                   fileName = cms.untracked.string('file:pat.root'),
                                   compressionLevel = cms.untracked.int32(4),
                                   compressionAlgorithm = cms.untracked.string('LZMA'),
                                   eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                   outputCommands = process.MINIAODSIMEventContent.outputCommands,
                                   dropMetaData = cms.untracked.string('ALL'),
                                   fastCloning = cms.untracked.bool(False),
                                   overrideInputFileSplitLevels = cms.untracked.bool(True)
                                   )

    process.outp = cms.EndPath(process.out)

    if customize_before_unscheduled is not None:
        customize_before_unscheduled(process)

    from FWCore.ParameterSet.Utilities import convertToUnscheduled
    process = convertToUnscheduled(process)

    from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData, miniAOD_customizeAllMC
    if is_mc:
        process.load('Configuration.StandardSequences.PATMC_cff') # right now, same as PAT_cff
        process = miniAOD_customizeAllMC(process)
    else:
        process.load('Configuration.StandardSequences.PAT_cff')
        process = miniAOD_customizeAllData(process)

    process.load('JMTucker.Tools.PATTupleSelection_cfi')
    process.selectedPatJets.cut = process.jtupleParams.jetCut
    process.selectedPatMuons.cut = process.jtupleParams.muonCut
    process.selectedPatElectrons.cut = process.jtupleParams.electronCut

    return process

def keep_random_state(process):
    process.out.outputCommands.append('keep *_randomEngineStateProducer_*_*')

def keep_mixing_info(process):
    process.out.outputCommands.append('keep CrossingFramePlaybackInfoExtended_*_*_*')

if __name__ == '__main__':
    process = pat_tuple_process(None, True)

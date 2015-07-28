import FWCore.ParameterSet.Config as cms

def pat_tuple_process(customize_before_unscheduled, is_mc):
    process = cms.Process('PAT')

    process.load('FWCore.MessageService.MessageLogger_cfi')
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
    process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V9A', '')

    process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True))
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/mc/RunIISpring15DR74/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/Asympt50ns_MCRUN2_74_V9A-v2/80000/F47E7F59-8A29-E511-8667-002590A52B4A.root'))

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

    # We're not saving the PAT branches, but if the embedding is on then
    # we can't match leptons by track to vertices.
    process.patMuons.embedTrack = False
    process.patElectrons.embedTrack = False

    print '''

JMTBAD still missing:
- jet/muon/electron id
- PV rejiggering
- particular trigger bits
- event cleaning filters (these are done somewhere in the pat now, yes?)
- extra IVF producers
- stdout suppressor
- final event content slimming
- fast sim handling
- pileup removal studies

'''
    return process

def keep_random_state(process):
    process.out.outputCommands.append('keep *_randomEngineStateProducer_*_*')

def keep_mixing_info(process):
    process.out.outputCommands.append('keep CrossingFramePlaybackInfoExtended_*_*_*')

if __name__ == '__main__':
    process = pat_tuple_process(None, True)

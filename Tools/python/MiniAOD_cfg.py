import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import output_file, registration_warnings, report_every, silence_messages

def which_global_tag(is_mc):
    return '74X_mcRun2_asymptotic_v4' if is_mc else '74X_dataRun2_v5'

def pat_tuple_process(customize_before_unscheduled, is_mc):
    process = cms.Process('PAT')

    report_every(process, 1000000)
    registration_warnings(process)
    print 'suppressing MatchedJetsFarApart, HLTConfigData, NoModule warnings'
    silence_messages(process, ['MatchedJetsFarApart', 'HLTConfigData', 'NoModule'])

    process.load('Configuration.StandardSequences.Services_cff')
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.load('Configuration.EventContent.EventContent_cff')
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')

    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, which_global_tag(is_mc), '')

    process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True),
                                         wantSummary = cms.untracked.bool(False),
                                         )
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/F47E7F59-8A29-E511-8667-002590A52B4A.root'))

    output_file(process, 'pat.root', process.MINIAODSIMEventContent.outputCommands)

    if is_mc:
        from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
        process = customisePostLS1(process)
    else:
        from Configuration.DataProcessing.RecoTLR import customiseDataRun2Common_25ns
        process = customiseDataRun2Common_25ns(process)

    if customize_before_unscheduled is not None:
        customize_before_unscheduled(process)

    from FWCore.ParameterSet.Utilities import convertToUnscheduled, cleanUnscheduled
    process = convertToUnscheduled(process)
    
    from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData, miniAOD_customizeAllMC
    if is_mc:
        process.load('Configuration.StandardSequences.PATMC_cff') # right now, same as PAT_cff
        customize = miniAOD_customizeAllMC
    else:
        process.load('Configuration.StandardSequences.PAT_cff')
        customize = miniAOD_customizeAllData

    process = cleanUnscheduled(process)
    process = customize(process)

    if is_mc:
        process.load('JMTucker.Tools.MCStatProducer_cff')

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

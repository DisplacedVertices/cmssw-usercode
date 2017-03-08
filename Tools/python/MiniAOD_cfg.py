import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import output_file, registration_warnings, report_every, silence_messages

def which_global_tag(is_mc):
    return '80X_mcRun2_asymptotic_2016_miniAODv2_v1' if is_mc else '80X_dataRun2_2016SeptRepro_v4'

def pat_tuple_process(customize_before_unscheduled, is_mc):
    from Configuration.StandardSequences.Eras import eras
    process = cms.Process('PAT', eras.Run2_25ns if is_mc else eras.Run2_2016)

    report_every(process, 1000000)
    registration_warnings(process)
    #silence_messages(process, ['MatchedJetsFarApart', 'HLTConfigData', 'NoModule'])
    print 'suppressing EcalLaserCorrFilter warnings'
    silence_messages(process, ['EcalLaserDbService'])

    process.load('Configuration.StandardSequences.Services_cff')
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.load('Configuration.EventContent.EventContent_cff')
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')

    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, which_global_tag(is_mc), '')

    process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True),
                                         wantSummary = cms.untracked.bool(False),
                                         )
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/mc/RunIISpring16DR80/QCD_HT2000toInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUSpring16_80X_mcRun2_asymptotic_2016_v3-v1/30000/00E624D5-F6FA-E511-B7EF-0CC47A4C8E56.root'))
    if not is_mc:
        process.source.fileNames = ['/store/data/Run2016G/JetHT/AOD/23Sep2016-v1/100000/0006CE1E-9986-E611-8DFB-6C3BE5B5C0B0.root']

    output_file(process, 'pat.root', process.MINIAODSIMEventContent.outputCommands)

    # the only customization in the 23sept rereco for runs B-F (not G
    # or H) was the customizeMinPtForHitRecoveryInGluedDet, but this
    # doesn't affect re-miniaoding

    #if not is_mc: # is_mc taken care of by Eras in cms.Process definition?

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

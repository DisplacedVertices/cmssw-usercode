import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import CMSSWSettings, output_file, registration_warnings, report_every, silence_messages, which_global_tag

def pat_tuple_process(settings, customize_before_unscheduled=None): #, paths=[]):
    '''Need to call associate_paths_to_task after defining the paths.'''

    if settings.year not in (2017,):
        raise ValueError('what year is it')

    from Configuration.StandardSequences.Eras import eras
    if settings.year == 2017:
        process = cms.Process('PAT', eras.Run2_2017, eras.run2_miniAOD_94XFall17)

    report_every(process, 1000000)
    registration_warnings(process)
    #silence_messages(process, ['EcalLaserDbService'])

    process.load('Configuration.StandardSequences.Services_cff')
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.load('Configuration.EventContent.EventContent_cff')
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    #process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')

    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, which_global_tag(settings), '')

    process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring())
    process.source.fileNames = [{
        (2017, False): 'file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/3CF97E8C-41DF-E711-9D55-008CFA56D6F4.root',
        (2017, True):  'file:/uscmst1b_scratch/lpc1/3DayLifetime/tucker/itch/B60ECF80-38F1-E711-BE32-02163E01A564.root',
        }[(settings.year, settings.is_mc)]]

    output_file(process, 'pat.root', process.MINIAODSIMEventContent.outputCommands)
    from PhysicsTools.PatAlgos.slimming.MicroEventContent_cff import MiniAODOverrideBranchesSplitLevel
    process.out.overrideBranchesSplitLevel = MiniAODOverrideBranchesSplitLevel

    if customize_before_unscheduled is not None:
        customize_before_unscheduled(process)

    from FWCore.ParameterSet.Utilities import convertToUnscheduled, cleanUnscheduled
    process = convertToUnscheduled(process)
    
    from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllData, miniAOD_customizeAllMC
    if settings.is_mc:
        process.load('Configuration.StandardSequences.PATMC_cff') # right now, same as PAT_cff
        customize = miniAOD_customizeAllMC
    else:
        process.load('Configuration.StandardSequences.PAT_cff')
        customize = miniAOD_customizeAllData

    process = cleanUnscheduled(process)
    process = customize(process)

    from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
    process = customiseEarlyDelete(process)

    process.load('JMTucker.Tools.MCStatProducer_cff')

    process.load('JMTucker.Tools.PATTupleSelection_cfi')
    process.selectedPatJets.cut = process.jtupleParams.jetCut
    process.selectedPatMuons.cut = '' #process.jtupleParams.muonCut
    process.selectedPatElectrons.cut = '' #process.jtupleParams.electronCut

    if hasattr(process, 'ptau'):
        del process.ptau

    if settings.year == 2017:
        # what the hell?
        #process.patTask.add(*process.producers_().values())
        #print 'before hamfisting:\n', process.patTask.moduleNames(), '\n'
        for x in 'CHSCands NjettinessAK8 NjettinessAK8Puppi NjettinessAK8Subjets QGTagger TrkCands ak4PFCHSL1FastL2L3CorrectorNoHF ak4PFCHSL1FastL2L3ResidualCorrectorNoHF ak4PFCHSL1FastjetCorrectorNoHF ak4PFCHSL2RelativeCorrectorNoHF ak4PFCHSL3AbsoluteCorrectorNoHF ak4PFCHSResidualCorrectorNoHF ak4PFJetTracksAssociatorAtVertex ak4PFJetsCHSNoHF ak4PFJetsLegacyHPSPiZeros ak4PFJetsRecoTauChargedHadrons ak8GenJetsNoNuConstituents ak8GenJetsNoNuSoftDrop ak8PFJetsCHSConstituents ak8PFJetsCHSPruned ak8PFJetsCHSPrunedMass ak8PFJetsCHSSoftDrop ak8PFJetsCHSSoftDropMass ak8PFJetsCHSValueMap ak8PFJetsPuppi ak8PFJetsPuppiConstituents ak8PFJetsPuppiSoftDrop ak8PFJetsPuppiSoftDropMass ak8PFJetsPuppiSoftDropValueMap basicJetsForMet caloJetMap cleanedPatJets combinatoricRecoTaus corrPfMetType1NoHF egmElectronPUPPIIsolation egmElectronPUPPINoLeptonsIsolation egmGsfElectronIDs egmPhotonIDs egmPhotonIsolation egmPhotonPUPPIIsolation electronMVAValueMapProducer goodOfflinePrimaryVerticesNoHF heepIDVarValueMaps hpsPFTauChargedIsoPtSum hpsPFTauChargedIsoPtSumdR03 hpsPFTauDiscriminationByDecayModeFinding hpsPFTauDiscriminationByDecayModeFindingNewDMs hpsPFTauDiscriminationByIsolationMVArun2v1DBdR03oldDMwLTraw hpsPFTauDiscriminationByIsolationMVArun2v1DBnewDMwLTraw hpsPFTauDiscriminationByIsolationMVArun2v1PWdR03oldDMwLTraw hpsPFTauDiscriminationByIsolationMVArun2v1PWnewDMwLTraw hpsPFTauDiscriminationByIsolationMVArun2v1PWoldDMwLTraw hpsPFTauDiscriminationByLooseCombinedIsolationDBSumPtCorr3Hits hpsPFTauDiscriminationByLooseIsolationMVArun2v1DBdR03oldDMwLT hpsPFTauDiscriminationByLooseIsolationMVArun2v1DBnewDMwLT hpsPFTauDiscriminationByLooseIsolationMVArun2v1PWdR03oldDMwLT hpsPFTauDiscriminationByLooseIsolationMVArun2v1PWnewDMwLT hpsPFTauDiscriminationByLooseIsolationMVArun2v1PWoldDMwLT hpsPFTauDiscriminationByLooseMuonRejection3 hpsPFTauDiscriminationByMVA6LooseElectronRejection hpsPFTauDiscriminationByMVA6MediumElectronRejection hpsPFTauDiscriminationByMVA6TightElectronRejection hpsPFTauDiscriminationByMVA6VLooseElectronRejection hpsPFTauDiscriminationByMVA6VTightElectronRejection hpsPFTauDiscriminationByMVA6rawElectronRejection hpsPFTauDiscriminationByMediumCombinedIsolationDBSumPtCorr3Hits hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBdR03oldDMwLT hpsPFTauDiscriminationByMediumIsolationMVArun2v1DBnewDMwLT hpsPFTauDiscriminationByMediumIsolationMVArun2v1PWdR03oldDMwLT hpsPFTauDiscriminationByMediumIsolationMVArun2v1PWnewDMwLT hpsPFTauDiscriminationByMediumIsolationMVArun2v1PWoldDMwLT hpsPFTauDiscriminationByPhotonPtSumOutsideSignalCone hpsPFTauDiscriminationByRawCombinedIsolationDBSumPtCorr3Hits hpsPFTauDiscriminationByTightCombinedIsolationDBSumPtCorr3Hits hpsPFTauDiscriminationByTightIsolationMVArun2v1DBdR03oldDMwLT hpsPFTauDiscriminationByTightIsolationMVArun2v1DBnewDMwLT hpsPFTauDiscriminationByTightIsolationMVArun2v1PWdR03oldDMwLT hpsPFTauDiscriminationByTightIsolationMVArun2v1PWnewDMwLT hpsPFTauDiscriminationByTightIsolationMVArun2v1PWoldDMwLT hpsPFTauDiscriminationByTightMuonRejection3 hpsPFTauDiscriminationByVLooseIsolationMVArun2v1DBdR03oldDMwLT hpsPFTauDiscriminationByVLooseIsolationMVArun2v1DBnewDMwLT hpsPFTauDiscriminationByVLooseIsolationMVArun2v1PWdR03oldDMwLT hpsPFTauDiscriminationByVLooseIsolationMVArun2v1PWnewDMwLT hpsPFTauDiscriminationByVLooseIsolationMVArun2v1PWoldDMwLT hpsPFTauDiscriminationByVTightIsolationMVArun2v1DBdR03oldDMwLT hpsPFTauDiscriminationByVTightIsolationMVArun2v1DBnewDMwLT hpsPFTauDiscriminationByVTightIsolationMVArun2v1PWdR03oldDMwLT hpsPFTauDiscriminationByVTightIsolationMVArun2v1PWnewDMwLT hpsPFTauDiscriminationByVTightIsolationMVArun2v1PWoldDMwLT hpsPFTauDiscriminationByVVTightIsolationMVArun2v1DBdR03oldDMwLT hpsPFTauDiscriminationByVVTightIsolationMVArun2v1DBnewDMwLT hpsPFTauDiscriminationByVVTightIsolationMVArun2v1PWdR03oldDMwLT hpsPFTauDiscriminationByVVTightIsolationMVArun2v1PWnewDMwLT hpsPFTauDiscriminationByVVTightIsolationMVArun2v1PWoldDMwLT hpsPFTauFootprintCorrection hpsPFTauFootprintCorrectiondR03 hpsPFTauNeutralIsoPtSum hpsPFTauNeutralIsoPtSumWeight hpsPFTauNeutralIsoPtSumWeightdR03 hpsPFTauNeutralIsoPtSumdR03 hpsPFTauPUcorrPtSum hpsPFTauPUcorrPtSumdR03 hpsPFTauPhotonPtSumOutsideSignalCone hpsPFTauPhotonPtSumOutsideSignalConedR03 hpsPFTauPrimaryVertexProducer hpsPFTauProducer hpsPFTauProducerSansRefs hpsPFTauSecondaryVertexProducer hpsPFTauTransverseImpactParameters hpsSelectionDiscriminator jetSelectorForMet lostTracksForTkIso muonPUPPIIsolation muonPUPPINoLeptonsIsolation nb1AK8PuppiSoftDrop nb1AK8PuppiSoftDropSubjets nb2AK8PuppiSoftDrop nb2AK8PuppiSoftDropSubjets noHFCands packedCandsForTkIso packedPatJetsAK8 particleFlowClusterOOTECAL particleFlowClusterOOTECALUncorrected particleFlowClusterPS particleFlowDisplacedVertex particleFlowRecHitOOTECAL patCHSMet patCaloMet patJetCorrFactorsAK8 patJetCorrFactorsAK8PFPuppiSoftDrop patJetCorrFactorsAK8PFPuppiSoftDropSubjets patJetCorrFactorsAK8Puppi patJetFlavourAssociationAK8 patJetFlavourAssociationAK8PFPuppiSoftDropSubjets patJetFlavourAssociationAK8Puppi patJetFlavourAssociationLegacyAK8 patJetFlavourAssociationLegacyAK8PFPuppiSoftDropSubjets patJetFlavourAssociationLegacyAK8Puppi patJetGenJetMatchAK8 patJetGenJetMatchAK8PFPuppiSoftDrop patJetGenJetMatchAK8PFPuppiSoftDropSubjets patJetGenJetMatchAK8Puppi patJetPartonAssociationLegacyAK8 patJetPartonAssociationLegacyAK8PFPuppiSoftDropSubjets patJetPartonAssociationLegacyAK8Puppi patJetPartonMatchAK8 patJetPartonMatchAK8PFPuppiSoftDrop patJetPartonMatchAK8PFPuppiSoftDropSubjets patJetPartonMatchAK8Puppi patJetsAK8 patJetsAK8PFPuppiSoftDrop patJetsAK8PFPuppiSoftDropSubjets patJetsAK8Puppi patMETsNoHF patPFMet patPFMetT0Corr patPFMetT0pcT1 patPFMetT0pcT1SmearTxy patPFMetT0pcT1Txy patPFMetT1SmearTxy patPFMetT1T2Corr patPFMetT1T2SmearCorr patPFMetT1Txy patPFMetTxy patPFMetTxyCorr patSmearedJets patTrigger patTrkMet pfBoostedDoubleSVAK8TagInfosAK8Puppi pfBoostedDoubleSecondaryVertexAK8BJetTagsAK8Puppi pfCandidateToVertexAssociation pfCombinedInclusiveSecondaryVertexV2BJetTagsAK8PFPuppiSoftDropSubjets pfCombinedInclusiveSecondaryVertexV2BJetTagsAK8Puppi pfCombinedMVAV2BJetTagsAK8PFPuppiSoftDropSubjets pfCombinedMVAV2BJetTagsAK8Puppi pfCombinedSecondaryVertexV2BJetTagsAK8Puppi pfDeepCSVDiscriminatorsJetTags pfDeepCSVJetTags pfDeepCSVJetTagsAK8PFPuppiSoftDropSubjets pfDeepCSVJetTagsAK8Puppi pfDeepCSVTagInfos pfDeepCSVTagInfosAK8PFPuppiSoftDropSubjets pfDeepCSVTagInfosAK8Puppi pfImpactParameterAK8TagInfosAK8Puppi pfImpactParameterTagInfos pfImpactParameterTagInfosAK8PFPuppiSoftDropSubjets pfImpactParameterTagInfosAK8Puppi pfInclusiveSecondaryVertexFinderAK8TagInfosAK8Puppi pfInclusiveSecondaryVertexFinderTagInfos pfInclusiveSecondaryVertexFinderTagInfosAK8PFPuppiSoftDropSubjets pfInclusiveSecondaryVertexFinderTagInfosAK8Puppi pfMetCHS pfMetNoHF pfMetT1NoHF pfMetTrk pfNoLepPUPPI pfNoPileUpCandidates pfNoPileUpIso pfNoPileUpJMENoHF pfPileUpIso pfPileUpJMENoHF pfRecoTauTagInfoProducer pfSecondaryVertexTagInfosAK8PFPuppiSoftDropSubjets pfSecondaryVertexTagInfosAK8Puppi photonIDValueMapProducer photonMVAValueMapProducer pileupJetId puppi puppiNoLep recoTauAK4PFJets08Region selectedPatJetsAK8PFPuppiSoftDrop selectedPatJetsAK8PFPuppiSoftDropSubjets selectedPatJetsAK8Puppi selectedPatJetsForMetT1T2SmearCorr selectedPrimaryVertexHighestPtTrackSumForPFMEtCorrType0 selectedVerticesForPFMEtCorrType0 slimmedGenJetsAK8SoftDropSubJets slimmedJetsAK8PFPuppiSoftDropPacked slimmedJetsAK8PFPuppiSoftDropSubjets softPFElectronsTagInfosAK8PFPuppiSoftDropSubjets softPFElectronsTagInfosAK8Puppi softPFMuonsTagInfosAK8PFPuppiSoftDropSubjets softPFMuonsTagInfosAK8Puppi tmpPFCandCollPtrNoHF'.split():
            process.patTask.add(getattr(process,x))

    return process

def keep_random_state(process):
    process.out.outputCommands.append('keep *_randomEngineStateProducer_*_*')

def keep_mixing_info(process):
    process.out.outputCommands.append('keep CrossingFramePlaybackInfoExtended_*_*_*')

def remove_met_filters(process):
    for k in process.paths.keys():
        if k.startswith('Flag_'):
            delattr(process, k)

def remove_output_module(process):
    del process.out
    del process.outp

def streamline_jets(process, drop_tags=True, drop_puid=True):
    process.patJets.addGenJetMatch    = False
    process.patJets.addGenPartonMatch = False
    process.patJets.addJetFlavourInfo = False
    process.patJets.embedGenJetMatch  = False
    process.patJets.getJetMCFlavour   = False
    if drop_tags:
        process.patJets.addTagInfos = False
        process.patJets.addBTagInfo = False
        process.patJets.addDiscriminators = False
        process.patJets.userData.userFunctionLabels = []
        process.patJets.userData.userFunctions = []
    if drop_puid:
        process.patJets.userData.userFloats.src = [cms.InputTag("caloJetMap","pt"), cms.InputTag("caloJetMap","emEnergyFraction")]
        process.patJets.userData.userInts.src = []

def jets_only(process):
    remove_met_filters(process)
    remove_output_module(process)
    streamline_jets(process)

def associate_paths_to_task(process, *paths):
    if not paths:
        paths = process.paths_().itervalues()
    for p in paths:
        p.associate(process.patTask)

if __name__ == '__main__':
    process = pat_tuple_process(CMSSWSettings())

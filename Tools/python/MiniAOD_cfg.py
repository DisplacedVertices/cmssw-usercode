import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.CMSSWTools import output_file, registration_warnings, report_every, silence_messages

def which_global_tag(is_mc, year, H):
    if H:
        assert not is_mc and year != 2015
    if year == 2015:
        return '76X_mcRun2_asymptotic_v12' if is_mc else '76X_dataRun2_v15'
    elif year == 2016:
        if is_mc:
            return '80X_mcRun2_asymptotic_2016_TrancheIV_v8'
        else:
            return '80X_dataRun2_Prompt_v16' if H else '80X_dataRun2_2016SeptRepro_v7'
    else:
        raise ValueError('what year is it')

def pat_tuple_process(customize_before_unscheduled, is_mc, year, H):
    if year not in (2015,2016):
        raise ValueError('what year is it')

    from Configuration.StandardSequences.Eras import eras
    if year == 2015:
        if is_mc:
            from Configuration.StandardSequences.Eras import eras
            process = cms.Process('PAT', eras.Run2_25ns)
        else:
            process = cms.Process('PAT')
    elif year == 2016:
        process = cms.Process('PAT', eras.Run2_25ns if is_mc else eras.Run2_2016)

    report_every(process, 1000000)
    registration_warnings(process)
    if year == 2015:
        silence_messages(process, ['HLTConfigData'])
    elif year == 2016:
        silence_messages(process, ['EcalLaserDbService'])

    process.load('Configuration.StandardSequences.Services_cff')
    process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
    process.load('Configuration.EventContent.EventContent_cff')
    process.load('SimGeneral.MixingModule.mixNoPU_cfi')
    process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
    process.load('Configuration.StandardSequences.MagneticField_cff')
    #process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')

    process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
    from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
    process.GlobalTag = GlobalTag(process.GlobalTag, which_global_tag(is_mc, year, H), '')

    process.options = cms.untracked.PSet(allowUnscheduled = cms.untracked.bool(True),
                                         wantSummary = cms.untracked.bool(False),
                                         )
    process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(100))
    process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring())
    process.source.fileNames = [{
        (2015, True):  '/store/mc/RunIIFall15DR76/TTJets_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/AODSIM/PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/00000/0039E642-58BD-E511-B773-002590DE7230.root',
        (2015, False): '/store/data/Run2015D/JetHT/AOD/16Dec2015-v1/00000/0A2C6696-AEAF-E511-8551-0026189438EB.root',
        (2016, True):  '/store/mc/RunIISummer16DR80Premix/QCD_HT1500to2000_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/AODSIM/PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/70000/1E575201-1EB8-E611-A523-549F3525C4EC.root',
        (2016, False): '/store/data/Run2016G/JetHT/AOD/23Sep2016-v1/100000/0006CE1E-9986-E611-8DFB-6C3BE5B5C0B0.root',
        }[(year, is_mc)]]

    output_file(process, 'pat.root', process.MINIAODSIMEventContent.outputCommands)

    if year == 2015:
        if not is_mc: # is_mc taken care of by Eras in cms.Process definition?
            # I think these next two are already set but just in
            # case. This replaces the use of
            # Configuration.DataProcessing.RecoTLR.customiseDataRun2Common_25ns,
            # which seems to be only needed if running raw2digi, L1reco,
            # reco, or dqm.
            process.CSCGeometryESModule.useGangedStripsInME1a = False
            process.idealForDigiCSCGeometry.useGangedStripsInME1a = False
    #elif year == 2016:
        # the only customization in the 23sept rereco for runs B-F (not G
        # or H) was the customizeMinPtForHitRecoveryInGluedDet, but this
        # doesn't affect re-miniaoding
        #pass

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

    if year == 2015:
        # Don't use the CombinedMVAV2 jet tags, they crash on the data from memory leak (can remove after next (?) patch of 763)
        process.patJets.discriminatorSources = cms.VInputTag(cms.InputTag("pfJetBProbabilityBJetTags"),
                                                             cms.InputTag("pfJetProbabilityBJetTags"),
                                                             cms.InputTag("pfTrackCountingHighPurBJetTags"),
                                                             cms.InputTag("pfTrackCountingHighEffBJetTags"),
                                                             cms.InputTag("pfSimpleSecondaryVertexHighEffBJetTags"),
                                                             cms.InputTag("pfSimpleSecondaryVertexHighPurBJetTags"),
                                                             cms.InputTag("pfCombinedSecondaryVertexV2BJetTags"),
                                                             cms.InputTag("pfCombinedInclusiveSecondaryVertexV2BJetTags"))

    process = cleanUnscheduled(process)
    process = customize(process)

    process.load('JMTucker.Tools.MCStatProducer_cff')

    process.load('JMTucker.Tools.PATTupleSelection_cfi')
    process.selectedPatJets.cut = process.jtupleParams.jetCut
    process.selectedPatMuons.cut = process.jtupleParams.muonCut
    process.selectedPatElectrons.cut = process.jtupleParams.electronCut

    if hasattr(process, 'ptau'):
        del process.ptau
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

if __name__ == '__main__':
    process = pat_tuple_process(None, True, 2016)

# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17MiniAODv2
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/EXO-RunIIFall17MiniAODv2-00064
# CMSSW_9_4_6_patch1 cmsDriver.py step1 --mc --eventcontent MINIAODSIM --runUnscheduled --datatier MINIAODSIM --conditions 94X_mc2017_realistic_v14 --step PAT --nThreads 4 --scenario pp --era Run2_2017,run2_miniAOD_94XFall17 --python_filename BPH-RunIIFall17MiniAODv2-00046_1_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 4800 --no_exec

import sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
import dynamicconf

process = cms.Process('PAT',eras.Run2_2017,eras.run2_miniAOD_94XFall17)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.PatAlgos.slimming.metFilterPaths_cff')
process.load('Configuration.StandardSequences.PATMC_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:reco.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, dynamicconf.globaltag_miniaod, '')

process.MINIAODSIMoutput = cms.OutputModule('PoolOutputModule',
                                            fileName = cms.untracked.string('miniaod.root'),
                                            outputCommands = process.MINIAODSIMEventContent.outputCommands,
                                            compressionAlgorithm = cms.untracked.string('LZMA'),
                                            compressionLevel = cms.untracked.int32(4),
                                            dataset = cms.untracked.PSet(dataTier = cms.untracked.string('MINIAODSIM'), filterName = cms.untracked.string('')),
                                            dropMetaData = cms.untracked.string('ALL'),
                                            eventAutoFlushCompressedSize = cms.untracked.int32(-900),
                                            fastCloning = cms.untracked.bool(False),
                                            overrideInputFileSplitLevels = cms.untracked.bool(True),
                                            splitLevel = cms.untracked.int32(0),
                                            overrideBranchesSplitLevel = cms.untracked.VPSet(
                                                cms.untracked.PSet(branch = cms.untracked.string('patPackedCandidates_packedPFCandidates__*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('recoGenParticles_prunedGenParticles__*'), splitLevel = cms.untracked.int32(99) ), 
                                                cms.untracked.PSet(branch = cms.untracked.string('patTriggerObjectStandAlones_slimmedPatTrigger__*'), splitLevel = cms.untracked.int32(99) ), 
                                                cms.untracked.PSet(branch = cms.untracked.string('patPackedGenParticles_packedGenParticles__*'), splitLevel = cms.untracked.int32(99) ), 
                                                cms.untracked.PSet(branch = cms.untracked.string('patJets_slimmedJets__*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('recoVertexs_offlineSlimmedPrimaryVertices__*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('recoCaloClusters_reducedEgamma_reducedESClusters_*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEBRecHits_*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedEERecHits_*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('recoGenJets_slimmedGenJets__*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('patJets_slimmedJetsPuppi__*'), splitLevel = cms.untracked.int32(99)), 
                                                cms.untracked.PSet(branch = cms.untracked.string('EcalRecHitsSorted_reducedEgamma_reducedESRecHits_*'), splitLevel = cms.untracked.int32(99))
                                                ),
                                            )

process.Flag_trackingFailureFilter = cms.Path(process.goodVertices+process.trackingFailureFilter)
process.Flag_goodVertices = cms.Path(process.primaryVertexFilter)
process.Flag_CSCTightHaloFilter = cms.Path(process.CSCTightHaloFilter)
process.Flag_trkPOGFilters = cms.Path(process.trkPOGFilters)
process.Flag_HcalStripHaloFilter = cms.Path(process.HcalStripHaloFilter)
process.Flag_trkPOG_logErrorTooManyClusters = cms.Path(~process.logErrorTooManyClusters)
process.Flag_EcalDeadCellTriggerPrimitiveFilter = cms.Path(process.EcalDeadCellTriggerPrimitiveFilter)
process.Flag_ecalLaserCorrFilter = cms.Path(process.ecalLaserCorrFilter)
process.Flag_globalSuperTightHalo2016Filter = cms.Path(process.globalSuperTightHalo2016Filter)
process.Flag_eeBadScFilter = cms.Path(process.eeBadScFilter)
process.Flag_METFilters = cms.Path(process.metFilters)
process.Flag_chargedHadronTrackResolutionFilter = cms.Path(process.chargedHadronTrackResolutionFilter)
process.Flag_globalTightHalo2016Filter = cms.Path(process.globalTightHalo2016Filter)
process.Flag_CSCTightHaloTrkMuUnvetoFilter = cms.Path(process.CSCTightHaloTrkMuUnvetoFilter)
process.Flag_HBHENoiseIsoFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseIsoFilter)
process.Flag_BadChargedCandidateSummer16Filter = cms.Path(process.BadChargedCandidateSummer16Filter)
process.Flag_hcalLaserEventFilter = cms.Path(process.hcalLaserEventFilter)
process.Flag_BadPFMuonFilter = cms.Path(process.BadPFMuonFilter)
process.Flag_ecalBadCalibFilter = cms.Path(process.ecalBadCalibFilter)
process.Flag_HBHENoiseFilter = cms.Path(process.HBHENoiseFilterResultProducer+process.HBHENoiseFilter)
process.Flag_trkPOG_toomanystripclus53X = cms.Path(~process.toomanystripclus53X)
process.Flag_EcalDeadCellBoundaryEnergyFilter = cms.Path(process.EcalDeadCellBoundaryEnergyFilter)
process.Flag_BadChargedCandidateFilter = cms.Path(process.BadChargedCandidateFilter)
process.Flag_trkPOG_manystripclus53X = cms.Path(~process.manystripclus53X)
process.Flag_BadPFMuonSummer16Filter = cms.Path(process.BadPFMuonSummer16Filter)
process.Flag_muonBadTrackFilter = cms.Path(process.muonBadTrackFilter)
process.Flag_CSCTightHalo2015Filter = cms.Path(process.CSCTightHalo2015Filter)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.MINIAODSIMoutput_step = cms.EndPath(process.MINIAODSIMoutput)

process.schedule = cms.Schedule(process.Flag_HBHENoiseFilter, process.Flag_HBHENoiseIsoFilter, process.Flag_CSCTightHaloFilter, process.Flag_CSCTightHaloTrkMuUnvetoFilter, process.Flag_CSCTightHalo2015Filter, process.Flag_globalTightHalo2016Filter, process.Flag_globalSuperTightHalo2016Filter, process.Flag_HcalStripHaloFilter, process.Flag_hcalLaserEventFilter, process.Flag_EcalDeadCellTriggerPrimitiveFilter, process.Flag_EcalDeadCellBoundaryEnergyFilter, process.Flag_ecalBadCalibFilter, process.Flag_goodVertices, process.Flag_eeBadScFilter, process.Flag_ecalLaserCorrFilter, process.Flag_trkPOGFilters, process.Flag_chargedHadronTrackResolutionFilter, process.Flag_muonBadTrackFilter, process.Flag_BadChargedCandidateFilter, process.Flag_BadPFMuonFilter, process.Flag_BadChargedCandidateSummer16Filter, process.Flag_BadPFMuonSummer16Filter, process.Flag_trkPOG_manystripclus53X, process.Flag_trkPOG_toomanystripclus53X, process.Flag_trkPOG_logErrorTooManyClusters, process.Flag_METFilters, process.endjob_step, process.MINIAODSIMoutput_step)
process.schedule.associate(process.patTask)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

from Configuration.DataProcessing.Utils import addMonitoring 
process = addMonitoring(process)

from FWCore.ParameterSet.Utilities import convertToUnscheduled
process = convertToUnscheduled(process)

from PhysicsTools.PatAlgos.slimming.miniAOD_tools import miniAOD_customizeAllMC 
process = miniAOD_customizeAllMC(process)

from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    import JMTucker.Tools.Samples as Samples

    samples = Samples.all_signal_samples_2017
    for s in samples:
        s.split_by = 'events'
        s.events_per = 2000

    ms = MetaSubmitter('SignalMiniAOD')
    ms.common.publish_name = 'RunIIFall17MiniAODv2-94X_mc2017_realistic_v14'
    ms.condor.stageout_files = 'all'
    ms.condor.jdl_extras = 'request_memory = 3000'
    ms.submit(samples)

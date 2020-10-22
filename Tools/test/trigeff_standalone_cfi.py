import FWCore.ParameterSet.Config as cms

process = cms.Process("TEST")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
                                fileNames = cms.untracked.vstring(
                                  'root://cmsxrootd.fnal.gov//store/mc/RunIIFall17MiniAODv2/gluinoGMSB_M800_ctau1p0_TuneCP2_13TeV_pythia8/MINIAODSIM/PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/270000/B832D304-82CF-E911-BBD0-0025901D08B2.root'
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_99.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_199.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_299.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_399.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_499.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_599.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_699.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_799.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_899.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_999.root',
                                  #'root://cmsxrootd.fnal.gov//store/group/dpg_bril/comm_bril/lumi/test/MC_test/SplitSUSY2017_AODSIM/gluinoGMSB_2017/SplitSUSY_M1600_1mm_CP2_AODSIM/190814_164254/0000/XXTo4J_AODSIM_1099.root',

                                  
                                )
                           )

process.trigeff_standalong = cms.EDAnalyzer('TriggerEffStudy_StandAlone',
                                            triggerTag = cms.untracked.InputTag("TriggerResults", "", "HLT"),
                                            processName = cms.untracked.string("HLT"),
                                            triggerPFHTTag = cms.untracked.string("HLT_PFHT1050_v14"),
                                            triggerMETTag = cms.untracked.string("HLT_PFMET120_PFMHT120_IDTight_v16"),
                                            triggerMETnoMuTag = cms.untracked.string("HLT_PFMETNoMu120_PFMHTNoMu120_IDTight_v16"),
                                            verbose = cms.untracked.bool(False),
)

process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
#process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = '94X_mc2017_realistic_v14'

process.TFileService = cms.Service("TFileService", fileName = cms.string("METtrigeff.root") )

process.runseq = cms.Sequence()
process.runseq += process.trigeff_standalong
process.path = cms.Path(process.runseq)
process.schedule = cms.Schedule(process.path)

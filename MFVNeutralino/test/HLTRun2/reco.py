# 740: cmsDriver.py step3 --conditions MCRUN2_74_V7 --no_exec -n 10 --eventcontent AODSIM -s RAW2DIGI,L1Reco,RECO,EI --datatier GEN-SIM-RECO --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1

import sys, FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
#process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
#process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('root://osg-se.cac.cornell.edu//xrootd/path/cms/store/user/tucker/mfv_hltrun2_M0400/hltpu40/17e0ae5ebda92df9604093b8c31d7d4c/hlt_64_1_AKX.root'))

process.AODSIMoutput = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('reco.root'),
    outputCommands = process.AODSIMEventContent.outputCommands,
    eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(4),
)

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.raw2digi_step, process.L1Reco_step, process.reconstruction_step, process.eventinterpretaion_step, process.AODSIMoutput_step)

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from samples import samples
    samples = [s for s in samples if s.hltpu40_done == True]
    for s in samples:
        s.dataset = s.hltpu40_dataset

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('HLTRun2_Recopu40',
                       events_per_job = 400,
                       total_number_of_events = -1,
                       get_edm_output = 1,
                       data_retrieval = 'cornell',
                       publish_data_name = 'recopu40',
                       aaa = True,
                       storage_catalog_override = 'cornell',
                       )
    cs.submit_all(samples)

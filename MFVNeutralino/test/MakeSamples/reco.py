# from configs in dbs for /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIISpring15DR74-Asympt25ns_MCRUN2_74_V9-v2/AODSIM

is_25ns = True # False for 50 ns

########################################################################

import sys, FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:hlt.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
#    for category in ['TwoTrackMinimumDistance']:
#        process.MessageLogger.categories.append(category)
#        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
                                        compressionAlgorithm = cms.untracked.string('LZMA'),
                                        compressionLevel = cms.untracked.int32(4),
                                        eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                        fileName = cms.untracked.string('reco.root'),
                                        outputCommands = process.AODSIMEventContent.outputCommands,
                                        )

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
tag = 'MCRUN2_74_V9'
if not is_25ns:
    tag += 'A'
process.GlobalTag = GlobalTag(process.GlobalTag, tag, '')

process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.eventinterpretaion_step,process.AODSIMoutput_step)

if is_25ns:
    from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
    process = customisePostLS1(process)
else:
    from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1_50ns
    process = customisePostLS1_50ns(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    pass

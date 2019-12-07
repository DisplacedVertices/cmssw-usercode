# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVMCcampaignRunIIFall17DRPremix
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/EXO-RunIIFall17DRPremix-02035
# 9_4_7 cmsDriver.py step2 --filein file:EXO-RunIIFall17DRPremix-02035_step1.root --fileout file:EXO-RunIIFall17DRPremix-02035.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 94X_mc2017_realistic_v11 --step RAW2DIGI,RECO,RECOSIM,EI --nThreads 8 --era Run2_2017 --python_filename EXO-RunIIFall17DRPremix-02035_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 1751
# https://twiki.cern.ch/twiki/bin/view/CMS/PdmVCampaignRunIIAutumn18DRPremix
# https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_test/EXO-RunIIAutumn18DRPremix-00193
# 10_2_6 cmsDriver.py step2 --filein file:EXO-RunIIAutumn18DRPremix-00193_step1.root --fileout file:EXO-RunIIAutumn18DRPremix-00193.root --mc --eventcontent AODSIM --runUnscheduled --datatier AODSIM --conditions 102X_upgrade2018_realistic_v15 --step RAW2DIGI,L1Reco,RECO,RECOSIM,EI --procModifiers premix_stage2 --nThreads 8 --era Run2_2018 --python_filename EXO-RunIIAutumn18DRPremix-00193_2_cfg.py --no_exec --customise Configuration/DataProcessing/Utils.addMonitoring -n 2626

import os, sys, FWCore.ParameterSet.Config as cms, dynamicconf

premix = True

for arg in sys.argv:
    if arg.startswith('premix='):
        premix = arg.replace('premix=','') == '1'

process = dynamicconf.process('RECO')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
if premix:
    pass
else:
    raise NotImplementedError('need to set up non-premix')
    if year == 2017:
        process.load('Configuration.StandardSequences.L1Reco_cff')
if year == 2018:
    process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.RecoSim_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:rawhlt.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

process.AODSIMoutput = cms.OutputModule("PoolOutputModule",
                                        compressionAlgorithm = cms.untracked.string('LZMA'),
                                        compressionLevel = cms.untracked.int32(4),
                                        eventAutoFlushCompressedSize = cms.untracked.int32(31457280),
                                        fileName = cms.untracked.string('reco.root'),
                                        outputCommands = process.AODSIMEventContent.outputCommands,
                                        )

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, dynamicconf.globaltag['reco'], '')

process.raw2digi_step = cms.Path(process.RawToDigi)
if not premix:
    raise NotImplementedError('need to set up non-premix')
    if year == 2017:
        process.L1Reco_step = cms.Path(process.L1Reco)
if year == 2018:
    process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.recosim_step = cms.Path(process.recosim)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.raw2digi_step)
if not premix:
    raise NotImplementedError('need to set up non-premix')
    if year == 2017:
        process.schedule.append(process.L1Reco_step)
if year == 2018:
    process.schedule.append(process.L1Reco_step)
process.schedule.extend([process.reconstruction_step,process.recosim_step,process.eventinterpretaion_step,process.AODSIMoutput_step])
# task?

from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)

process.dummyForPsetHash = cms.PSet(dummy = cms.string(os.environ.get('DUMMYFORHASH', '')))

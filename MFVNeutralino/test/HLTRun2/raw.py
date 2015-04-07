# in 740: cmsDriver.py raw2 --no_exec -n 10 --mc --conditions MCRUN2_74_V7 --eventcontent RAWSIM -s DIGI,L1,DIGI2RAW --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1 --pileup AVE_40_BX_25ns

import sys, FWCore.ParameterSet.Config as cms

process = cms.Process('DIGI2RAW')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_POISSON_average_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(5))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring('file:/uscms_data/d1/tucker/sim_100_1_qdc.root'),
    inputCommands = cms.untracked.vstring(
        'keep *', 
        'drop *_genParticles_*_*', 
        'drop *_genParticlesForJets_*_*', 
        'drop *_kt4GenJets_*_*', 
        'drop *_kt6GenJets_*_*', 
        'drop *_iterativeCone5GenJets_*_*', 
        'drop *_ak4GenJets_*_*', 
        'drop *_ak7GenJets_*_*', 
        'drop *_ak8GenJets_*_*', 
        'drop *_ak4GenJetsNoNu_*_*', 
        'drop *_ak8GenJetsNoNu_*_*', 
        'drop *_genCandidatesForMET_*_*', 
        'drop *_genParticlesForMETAllVisible_*_*', 
        'drop *_genMetCalo_*_*', 
        'drop *_genMetCaloAndNonPrompt_*_*', 
        'drop *_genMetTrue_*_*', 
        'drop *_genMetIC5GenJs_*_*'
        ),
    )

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('raw.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    splitLevel = cms.untracked.int32(0)
)

process.RAWSIMoutput.outputCommands += ['drop *_*_*_SIM']

process.mix.input.nbPileupEvents.averageNumber = cms.double(40)
process.mix.bunchspace = cms.int32(25)
process.mix.minBunch = cms.int32(-12)
process.mix.maxBunch = cms.int32(3)
from minbias import files
process.mix.input.fileNames = files

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.digitisation_step, process.L1simulation_step, process.digi2raw_step, process.RAWSIMoutput_step)

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from samples import samples
    samples = [s for s in samples if s.sim_done == True]
    for s in samples:
        s.dataset = s.sim_dataset

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('HLTRun2_Raw',
                       events_per_job = 400,
                       total_number_of_events = -1,
                       get_edm_output = 1,
                       data_retrieval = 'cornell',
                       publish_data_name = 'rawpu40',
                       aaa = True,
                       storage_catalog_override = 'cornell',
                       )
    cs.submit_all(samples)

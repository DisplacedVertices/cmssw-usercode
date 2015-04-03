# 740: cmsDriver.py step1 --no_exec -n 10 --conditions MCRUN2_74_V7 --eventcontent RAWSIM -s SIM --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1

import sys, FWCore.ParameterSet.Config as cms

process = cms.Process('SIM')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.Geometry.GeometrySimDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('root://osg-se.cac.cornell.edu//xrootd/path/cms/store/user/tucker/mfv_hltrun2_M0900/mfv_hltrun2_M0900/b0221db6bdc577a56c275739395c3940/gen_10_1_M2D.root'))

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('sim.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    splitLevel = cms.untracked.int32(0),
)

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'MCRUN2_74_V7', '')

process.simulation_step = cms.Path(process.psim)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.simulation_step, process.RAWSIMoutput_step)

from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
process = customisePostLS1(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from samples import samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('HLTRun2_Sim',
                       events_per_job = 200,
                       total_number_of_events = -1,
                       aaa = True,
                       storage_catalog_override = 'cornell',
                       )
    cs.submit_all(samples)

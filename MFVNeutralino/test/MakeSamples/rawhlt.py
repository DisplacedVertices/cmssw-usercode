# from configs in dbs for /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM

import sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process('HLT', eras.Run2_25ns)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('SimGeneral.MixingModule.mix_2015_25ns_FallMC_matchData_PoissonOOTPU_cfi')
process.load('HLTrigger.Configuration.HLT_25ns14e33_v4_cff')

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('root://cmseos.fnal.gov//store/user/tucker/mfv_neu_tau01000um_M0800/sim_10k/150729_201526/0000/sim_1.root'))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
                                        fileName = cms.untracked.string('hlt.root'),
                                        outputCommands = process.RAWSIMEventContent.outputCommands,
                                        eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
                                        splitLevel = cms.untracked.int32(0),
                                        )

import minbias
process.mix.input.fileNames = minbias.files

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_v12', '')

process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.RAWSIMoutput_step])

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforFullSim 
process = customizeHLTforFullSim(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples

    samples = mfv_signal_samples[-1:]

    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('mfv_run2_76x_rawhlt',
                       dataset = 'sim',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 1000,
                       total_units = -1,
                       aaa = True,
                       publish_name='76rawhlt_10k',
                       storage_site='T3_US_Cornell',
                       )
    cs.submit_all(samples)

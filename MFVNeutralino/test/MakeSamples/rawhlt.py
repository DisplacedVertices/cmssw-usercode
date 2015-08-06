# sim:
# 740: cmsDriver.py step1 --no_exec -n 10 --conditions MCRUN2_74_V7 --eventcontent RAWSIM -s SIM --beamspot NominalCollision2015 --customise SLHCUpgradeSimulations/Configuration/postLS1Customs.customisePostLS1 --magField 38T_PostLS1
# but looks same as that used in a QCD sample /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIWinter15GS-MCRUN2_71_V1-v2/GEN-SIM in 7_1_16_patch2
# raw and hlt from same qcd sample

is_25ns = True # False for 50 ns

########################################################################

import sys, FWCore.ParameterSet.Config as cms

process = cms.Process('HLT')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
if is_25ns:
    process.load('SimGeneral.MixingModule.mix_2015_25ns_Startup_PoissonOOTPU_cfi')
    process.load('HLTrigger.Configuration.HLT_25ns14e33_v1_cff')
else:
    process.load('SimGeneral.MixingModule.mix_2015_50ns_Startup_PoissonOOTPU_cfi')
    process.load('HLTrigger.Configuration.HLT_50ns_5e33_v1_cff')


process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('root://osg-se.cac.cornell.edu//xrootd/path/cms/store/user/tucker/mfv_neu_tau01000um_M0800/sim_10k/150729_201526/0000/sim_1.root'))

process.RAWSIMoutput = cms.OutputModule('PoolOutputModule',
    fileName = cms.untracked.string('hlt.root'),
    outputCommands = process.RAWSIMEventContent.outputCommands,
    eventAutoFlushCompressedSize = cms.untracked.int32(5242880),
    splitLevel = cms.untracked.int32(0),
)

import minbias
process.mix.input.fileNames = minbias.files

from Configuration.AlCa.GlobalTag_condDBv2 import GlobalTag
tag = 'MCRUN2_74_V9'
if not is_25ns:
    tag += 'A'
process.GlobalTag = GlobalTag(process.GlobalTag, tag, '')

process.digitisation_step = cms.Path(process.pdigi)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.digi2raw_step = cms.Path(process.DigiToRaw)
process.RAWSIMoutput_step = cms.EndPath(process.RAWSIMoutput)

process.schedule = cms.Schedule(process.digitisation_step,process.L1simulation_step,process.digi2raw_step)
process.schedule.extend(process.HLTSchedule)
process.schedule.extend([process.RAWSIMoutput_step])

if is_25ns:
    from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1 
    process = customisePostLS1(process)
else:
    from SLHCUpgradeSimulations.Configuration.postLS1Customs import customisePostLS1_50ns
    process = customisePostLS1_50ns(process)

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 
process = customizeHLTforMC(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Sample import anon_samples

    samples = anon_samples('''
/mfv_neu_tau00100um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00100um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00100um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00100um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00300um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00300um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00300um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau00300um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau01000um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau01000um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau01000um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau01000um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau10000um_M0400/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau10000um_M0800/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau10000um_M1200/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
/mfv_neu_tau10000um_M1600/tucker-sim_10k-c66f4a7649a68ea5b6afdf05975ce9cf/USER
''', dbs_inst='phys03')

    ex = '25ns' if is_25ns else '50ns'
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('mfv_run2_rawhlt%s' % ex,
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 1000,
                       total_units = -1,
                       aaa = True,
                       publish_name='rawhlt%s_10k' % ex,
                       )
    cs.submit_all(samples)

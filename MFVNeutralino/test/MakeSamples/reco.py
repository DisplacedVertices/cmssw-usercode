# from configs in dbs for /QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/RunIIFall15DR76-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1/AODSIM

import sys, FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process('RECO', eras.Run2_25ns)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('CommonTools.ParticleFlow.EITopPAG_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:hlt.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(10))
process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    allowUnscheduled = cms.untracked.bool(True),
    )

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

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '76X_mcRun2_asymptotic_v12', '')

process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.eventinterpretaion_step = cms.Path(process.EIsequence)
process.AODSIMoutput_step = cms.EndPath(process.AODSIMoutput)

process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.eventinterpretaion_step,process.AODSIMoutput_step)

from FWCore.ParameterSet.Utilities import convertToUnscheduled, cleanUnscheduled
process = cleanUnscheduled(convertToUnscheduled(process))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Sample import anon_samples

    samples = anon_samples('''
/mfv_neu_tau00100um_M0400/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau00100um_M0800/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
#/mfv_neu_tau00100um_M1200/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau00100um_M1600/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau00300um_M0400/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau00300um_M0800/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau00300um_M1200/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
#/mfv_neu_tau00300um_M1600/tucker-rawhlt25ns_10k-0c96c096b8e8cb8bdfef9c65972d8618/USER
/mfv_neu_tau01000um_M0400/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau01000um_M0800/tucker-rawhlt25ns_10k-0c96c096b8e8cb8bdfef9c65972d8618/USER
/mfv_neu_tau01000um_M1200/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau01000um_M1600/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau10000um_M0400/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau10000um_M0800/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau10000um_M1200/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
/mfv_neu_tau10000um_M1600/tucker-rawhlt25ns_10k-746f00b17b114c4573d3b7477a0ee83e/USER
''', dbs_inst='phys03')

    ex = '25ns' if is_25ns else '50ns'
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    cs = CRABSubmitter('mfv_run2_reco%s' % ex,
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 1000,
                       total_units = -1,
                       aaa = True,
                       publish_name='reco%s_10k' % ex,
                       )
    cs.submit_all(samples)

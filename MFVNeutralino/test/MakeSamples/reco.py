import sys, os, FWCore.ParameterSet.Config as cms

process = cms.Process('RECO')

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:gensimhlt.root'))
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))

if not 'debug' in sys.argv:
    process.options.wantSummary = False
    process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
    for category in ['TwoTrackMinimumDistance']:
        process.MessageLogger.categories.append(category)
        setattr(process.MessageLogger.cerr, category, cms.untracked.PSet(limit=cms.untracked.int32(0)))

process.output = cms.OutputModule('PoolOutputModule',
                                  fileName = cms.untracked.string('reco.root'),
                                  outputCommands = process.AODSIMEventContent.outputCommands,
                                  eventAutoFlushCompressedSize = cms.untracked.int32(15728640),
                                  dataset = cms.untracked.PSet(filterName = cms.untracked.string(''), dataTier = cms.untracked.string('AODSIM')),
                                  )

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V21::All', '')

process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.output)

process.load('SimTracker.TrackAssociation.TrackAssociatorByHits_cfi')
process.mfvTrackMatches = cms.EDProducer('MFVTrackMatcherLight',
                                         gen_particles_src = cms.InputTag('genParticles'),
                                         tracking_particles_src = cms.InputTag('mergedtruth','MergedTrackTruth'),
                                         tracks_src = cms.InputTag('generalTracks'),
                                         )
process.reconstruction_step *= process.mfvTrackMatches
process.output.outputCommands += ['keep *_mfvTrackMatches_*_*']

process.schedule = cms.Schedule(process.raw2digi_step,process.L1Reco_step,process.reconstruction_step,process.endjob_step,process.output_step)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.Samples import mfv_signal_samples as samples
    cs = CRABSubmitter('MFVReco',
                       use_parent_dataset = True,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       total_number_of_events = -1,
                       events_per_job = 200,
                       publish_data_name = 'reco',
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*',
                       )
    cs.submit_all(samples)

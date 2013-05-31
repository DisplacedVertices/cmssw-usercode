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
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = remoteGlidein

[CMSSW]
datasetpath = %(parent_dataset)s
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
pset = reco.py
get_edm_output = 1
events_per_job = 200
total_number_of_events = -1

[USER]
ui_working_dir = crab/reco/crab_reco_%(name)s
copy_data = 1
storage_element = T3_US_Cornell
publish_data = 1
publish_data_name = reco
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
'''

    os.system('mkdir -p crab/reco')
    testing = 'testing' in sys.argv

    datasets = [
        ('neutralino_tau1000um_M0400', '/mfv_neutralino_tau1000um_M0400/tucker-mfv_neutralino_tau1000um_M0400-c9c4c27381f6625ed3d8394ffaf0b9cd/USER'),
        ('neutralino_tau0000um_M0400', '/mfv_neutralino_tau0000um_M0400/tucker-mfv_neutralino_tau0000um_M0400-3e730b2f07d27fadb85eb50c5002cc81/USER'),
        ('neutralino_tau9900um_M0400', '/mfv_neutralino_tau9900um_M0400/tucker-mfv_neutralino_tau9900um_M0400-c91fb7b9ece3e3abc0445dc6699e16d6/USER'),
        ('neutralino_tau1000um_M1000', '/mfv_neutralino_tau1000um_M1000/tucker-mfv_neutralino_tau1000um_M1000-c9c4c27381f6625ed3d8394ffaf0b9cd/USER'),
        ]

    from JMTucker.Tools.Samples import mfv_signal_samples as samples
    for sample in samples:
        open('crab.cfg','wt').write(crab_cfg % sample)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg')

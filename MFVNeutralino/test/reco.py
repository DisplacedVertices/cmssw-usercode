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
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V7C::All', '')

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
scheduler = condor

[CMSSW]
datasetpath = %(dataset)s
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
pset = reco.py
get_edm_output = 1
events_per_job = 500
total_number_of_events = -1

[USER]
ui_working_dir = crab/reco/crab_mfv_reco_%(name)s
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = mfv_reco_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''

    os.system('mkdir -p crab/reco')
    testing = 'testing' in sys.argv

    datasets = [
        ('gluino_tau0000um_M1000', '/mfv_gensimhlt_gluino_tau0000um_M1000/tucker-mfv_gensimhlt_gluino_tau0000um_M1000-f418ab66d2aa2ce17edadebd0427e711/USER'),
        ('gluino_tau0000um_M200', '/mfv_gensimhlt_gluino_tau0000um_M200/tucker-mfv_gensimhlt_gluino_tau0000um_M200-f418ab66d2aa2ce17edadebd0427e711/USER'),
        ('gluino_tau0000um_M400', '/mfv_gensimhlt_gluino_tau0000um_M400/tucker-mfv_gensimhlt_gluino_tau0000um_M400-f418ab66d2aa2ce17edadebd0427e711/USER'),
        ('gluino_tau0000um_M600', '/mfv_gensimhlt_gluino_tau0000um_M600/tucker-mfv_gensimhlt_gluino_tau0000um_M600-f418ab66d2aa2ce17edadebd0427e711/USER'),
        ('gluino_tau0000um_M800', '/mfv_gensimhlt_gluino_tau0000um_M800/tucker-mfv_gensimhlt_gluino_tau0000um_M800-f418ab66d2aa2ce17edadebd0427e711/USER'),
        ('gluino_tau0010um_M1000', '/mfv_gensimhlt_gluino_tau0010um_M1000/tucker-mfv_gensimhlt_gluino_tau0010um_M1000-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0010um_M200', '/mfv_gensimhlt_gluino_tau0010um_M200/tucker-mfv_gensimhlt_gluino_tau0010um_M200-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0010um_M400', '/mfv_gensimhlt_gluino_tau0010um_M400/tucker-mfv_gensimhlt_gluino_tau0010um_M400-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0010um_M600', '/mfv_gensimhlt_gluino_tau0010um_M600/tucker-mfv_gensimhlt_gluino_tau0010um_M600-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0010um_M800', '/mfv_gensimhlt_gluino_tau0010um_M800/tucker-mfv_gensimhlt_gluino_tau0010um_M800-1a774d010111a1aed9668a1957d7b272/USER'),
        ('gluino_tau0100um_M1000', '/mfv_gensimhlt_gluino_tau0100um_M1000/tucker-mfv_gensimhlt_gluino_tau0100um_M1000-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau0100um_M200', '/mfv_gensimhlt_gluino_tau0100um_M200/tucker-mfv_gensimhlt_gluino_tau0100um_M200-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau0100um_M400', '/mfv_gensimhlt_gluino_tau0100um_M400/tucker-mfv_gensimhlt_gluino_tau0100um_M400-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau0100um_M600', '/mfv_gensimhlt_gluino_tau0100um_M600/tucker-mfv_gensimhlt_gluino_tau0100um_M600-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau0100um_M800', '/mfv_gensimhlt_gluino_tau0100um_M800/tucker-mfv_gensimhlt_gluino_tau0100um_M800-cd908390df85e15f67c1b503d4c4278e/USER'),
        ('gluino_tau1000um_M1000', '/mfv_gensimhlt_gluino_tau1000um_M1000/tucker-mfv_gensimhlt_gluino_tau1000um_M1000-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M200', '/mfv_gensimhlt_gluino_tau1000um_M200/tucker-mfv_gensimhlt_gluino_tau1000um_M200-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M400', '/mfv_gensimhlt_gluino_tau1000um_M400/tucker-mfv_gensimhlt_gluino_tau1000um_M400-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M600', '/mfv_gensimhlt_gluino_tau1000um_M600/tucker-mfv_gensimhlt_gluino_tau1000um_M600-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau1000um_M800', '/mfv_gensimhlt_gluino_tau1000um_M800/tucker-mfv_gensimhlt_gluino_tau1000um_M800-11e502b9027fe454bec38485095c4f53/USER'),
        ('gluino_tau4000um_M1000', '/mfv_gensimhlt_gluino_tau4000um_M1000/tucker-mfv_gensimhlt_gluino_tau4000um_M1000-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau4000um_M200', '/mfv_gensimhlt_gluino_tau4000um_M200/tucker-mfv_gensimhlt_gluino_tau4000um_M200-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau4000um_M400', '/mfv_gensimhlt_gluino_tau4000um_M400/tucker-mfv_gensimhlt_gluino_tau4000um_M400-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau4000um_M600', '/mfv_gensimhlt_gluino_tau4000um_M600/tucker-mfv_gensimhlt_gluino_tau4000um_M600-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau4000um_M800', '/mfv_gensimhlt_gluino_tau4000um_M800/tucker-mfv_gensimhlt_gluino_tau4000um_M800-9dcf202e97da119ad22d8e489ec7b88e/USER'),
        ('gluino_tau9900um_M1000', '/mfv_gensimhlt_gluino_tau9900um_M1000/tucker-mfv_gensimhlt_gluino_tau9900um_M1000-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ('gluino_tau9900um_M200', '/mfv_gensimhlt_gluino_tau9900um_M200/tucker-mfv_gensimhlt_gluino_tau9900um_M200-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ('gluino_tau9900um_M400', '/mfv_gensimhlt_gluino_tau9900um_M400/tucker-mfv_gensimhlt_gluino_tau9900um_M400-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ('gluino_tau9900um_M600', '/mfv_gensimhlt_gluino_tau9900um_M600/tucker-mfv_gensimhlt_gluino_tau9900um_M600-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ('gluino_tau9900um_M800', '/mfv_gensimhlt_gluino_tau9900um_M800/tucker-mfv_gensimhlt_gluino_tau9900um_M800-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ]

    datasets = [
        ('gluino_tau9900um_M400', '/mfv_gensimhlt_gluino_tau9900um_M400/tucker-mfv_gensimhlt_gluino_tau9900um_M400-dd93627319a5f24d5d7ad10ea45db562/USER'),
]
    for name, dataset in datasets:
        open('crab.cfg','wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg')

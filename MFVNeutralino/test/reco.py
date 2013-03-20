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

process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/mfv_gensimhlt_gluino_tau9900um_M400/mfv_gensimhlt_gluino_tau9900um_M400/dd93627319a5f24d5d7ad10ea45db562/gensimhlt_249_1_IN7.root'))
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

process.output.outputCommands += [
    'keep TrackingParticles_mergedtruth_MergedTrackTruth_*',
    'keep TrackingVertexs_mergedtruth_MergedTrackTruth_*',
    'keep edmHepMCProduct_*_*_*',
    'keep recoTrackExtras_generalTracks_*_*',
    'keep TrackingRecHitsOwned_generalTracks_*_*',
    'keep SimTracks_g4SimHits__*',
    'keep SimVertexs_g4SimHits__*',
    ]

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'START53_V7C::All', '')

process.raw2digi_step = cms.Path(process.RawToDigi)
process.L1Reco_step = cms.Path(process.L1Reco)
process.reconstruction_step = cms.Path(process.reconstruction)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.output_step = cms.EndPath(process.output)

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
events_per_job = 400
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
        ('gluino_tau9900um_M400', '/mfv_gensimhlt_gluino_tau9900um_M400/tucker-mfv_gensimhlt_gluino_tau9900um_M400-dd93627319a5f24d5d7ad10ea45db562/USER'),
        ]

    for name, dataset in datasets:
        open('crab.cfg','wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg gensimhlt_crab.py gensimhlt_crab.pyc pythia8_hack')

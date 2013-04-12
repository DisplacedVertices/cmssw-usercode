import sys, os, FWCore.ParameterSet.Config as cms

process = cms.Process('Skim')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('file:dummy.root'))

process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.skimFilter = cms.EDFilter('MFVBeamGasSkim',
                                  beamspot_src = cms.InputTag('offlineBeamSpot'),
                                  tracks_src = cms.InputTag('generalTracks'),
                                  min_pt = cms.double(8),
                                  min_dxy = cms.double(0.1),
                                  )
process.p = cms.Path(process.skimFilter)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('skim.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               )
                               
process.outp = cms.EndPath(process.out)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
datasetpath = %(dataset)s
pset = skim.py
get_edm_output = 1
total_number_of_lumis = -1
lumis_per_job = 200

[USER]
ui_working_dir = crab/crab_mfvbeamgasskim_%(name)s
copy_data = 1
storage_element = T3_US_FNALLPC
check_user_remote_dir = 0
publish_data = 1
publish_data_name = mfvbeamgasskim_%(name)s
dbs_url_for_publication = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
'''

    testing = 'testing' in sys.argv

    datasets = [
        ('name', 'dataset/path')
        ]

    for name, dataset in datasets:
        open('crab.cfg', 'wt').write(crab_cfg % locals())
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg skim.pyc')


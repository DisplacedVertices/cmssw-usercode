import FWCore.ParameterSet.Config as cms

process = cms.Process('EventIdRecorder')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(''))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(True))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 1000000
process.TFileService = cms.Service('TFileService', fileName = cms.string('eid.root'))

process.source.fileNames = [x.strip() for x in open('infiles.txt') if x.strip()]

process.eid = cms.EDAnalyzer('EventIdRecorder', check_gen_particles = cms.bool(True))
process.p = cms.Path(process.eid)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = condor

[CMSSW]
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
datasetpath = /QCD_Pt-15to30_TuneZ2star_8TeV_pythia6/tucker-sstoptuple_v1_qcd15-3312fbeda721580c3cdebaec6739016e/USER
pset = particle_list.py
total_number_of_events = -1
events_per_job = 500

[USER]
ui_working_dir = crab_buh
return_data = 1
'''
    
    just_testing = 'testing' in sys.argv
    open('crab.cfg', 'wt').write(crab_cfg)
    if not just_testing:
        os.system('crab -create -submit')
        os.system('rm crab.cfg')

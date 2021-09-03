import os, sys, FWCore.ParameterSet.Config as cms

process = cms.Process('PUInfo')
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(-1))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring('/store/user/tucker/sstop_genfsimreco_test/sstop_genfsimreco_test/15c4250952b10a469cc6da8beaecd65e/fastsim_1_1_y1u.root'))
process.options = cms.untracked.PSet(wantSummary = cms.untracked.bool(False))
process.TFileService = cms.Service('TFileService', fileName = cms.string('puinfo.root'))
process.load('FWCore.MessageLogger.MessageLogger_cfi')
process.MessageLogger.cerr.FwkReport.reportEvery = 100000

process.puinfo = cms.EDAnalyzer('SimPUInfo', sample_name = cms.string('interactive'))
    
process.p = cms.Path(process.puinfo)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = puinfo_crab.py
total_number_of_events = -1
events_per_job = 250000

[USER]
ui_working_dir = crab/puinfohack/crab_puinfo_%(name)s
return_data = 1
'''

    just_testing = 'testing' in sys.argv

    from DVCode.Tools.Samples import background_samples, stop_signal_samples
    for sample in background_samples + stop_signal_samples:
        if sample.name not in 'pythiastopm200':
            continue
        
        open('crab.cfg', 'wt').write(crab_cfg % sample)

        new_py = open('puinfo.py').read()
        new_py += '\nprocess.puinfo.sample_name = "%(name)s"\n' % sample 
        open('puinfo_crab.py', 'wt').write(new_py)
            
        if not just_testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg puinfo_crab.py puinfo_crab.pyc')

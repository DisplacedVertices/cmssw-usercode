import os, sys, glob
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

process.source.fileNames = ['file:gensimhlt.root']
process.TFileService.fileName = 'gen_histos.root'

#from JMTucker.MFVNeutralino.SimFiles import load
#load(process, 'tau1000um_M0400', [0,1])

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.load('JMTucker.MFVNeutralino.GenHistos_cff')
process.mfvGenHistos.check_all_gen_particles = True

process.p = cms.Path(process.mfvGenParticleFilter * process.mfvGenHistos)

if debug:
    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.mfvGenHistos.print_info = -1
    process.p.insert(0, process.printList)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if debug:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s

[CMSSW]
dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet
datasetpath = %(dataset)s
pset = gen_histos.py
total_number_of_events = -1
events_per_job = 50000

[USER]
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
ui_working_dir = crab/gen_histos/crab_%(name)s
return_data = 1
'''

    testing = 'testing' in sys.argv

    from JMTucker.Tools.Samples import mfv_signal_samples
    for sample in mfv_signal_samples:
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not testing:
            os.system('crab -create -submit')
            os.system('rm crab.cfg')

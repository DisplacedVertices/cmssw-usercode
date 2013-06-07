import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.TFileService.fileName = 'thrust.root'

#from JMTucker.MFVNeutralino.SimFiles import load
#load(process, 'tau1000um_M0400', file_range='all', sec_files=False)

process.source.fileNames = ['file:/uscms/home/jchaves/nobackup/pat_2_1_Nnk.root']

process.thrustNtuple = cms.EDAnalyzer('MFVThrustAnalysis',
                                      gen_particles_src = cms.InputTag('genParticles'),
                                      gen_jets_src = cms.InputTag('ak5GenJets'),
                                      gen_met_src = cms.InputTag('genMetTrue'),
                                      met_src = cms.InputTag('patMETsPF'),
                                      muon_src = cms.InputTag('semilepMuonsPF'),
                                      pt_cut = cms.double(30),
                                      eta_cut = cms.double(3),
                                      loose_pt_cut = cms.double(30), # 20
                                      loose_eta_cut = cms.double(3), # 3.5
                                      )

process.p = cms.Path(process.thrustNtuple)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    crab_cfg = '''
[CRAB]
jobtype = cmssw
scheduler = %(scheduler)s

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = ntuple.py
%(job_control)s

[USER]
ui_working_dir = crab/ThrustAnalysis/crab_ThAn_%(name)s
return_data = 1
additional_input_files = dict_C.so
jmt_skip_input_files = src/EGamma/EGammaAnalysisTools/data/*
'''

    os.system('mkdir -p crab/ThrustAnalysis')
    just_testing = 'testing' in sys.argv

    def submit(sample):
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not just_testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg mfvgen_analyzer_crab.py mfvgen_analyzer_crab.pyc')

    from JMTucker.Tools.Samples import mfv_gluino_tau1000um_M0400, ttbarnocut
    mfv_gluino_tau1000um_M0400_old = {'dbs_url':'dbs_url = https://cmsdbsprod.cern.ch:8443/cms_dbs_ph_analysis_02_writer/servlet/DBSServlet','scheduler':'glite','name':'old_mfv3j_gluino_tau1000um_M0400', 'dataset':'/mfv_genfsimreco_gluino_tau1000um_M400/tucker-mfv_genfsimreco_gluino_tau1000um_M400-e47fc4979466aacf88f2c30cc52afb0f/USER', 'job_control': 'total_number_of_events = 10000\nevents_per_job=1000\n'}
    for sample in (mfv_gluino_tau1000um_M0400, mfv_gluino_tau1000um_M0400_old, ttbarnocut):
        submit(sample)

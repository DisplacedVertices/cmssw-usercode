import sys, os
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.TFileService.fileName = 'thrust.root'

from JMTucker.MFVNeutralino.SimFiles import load
load(process, 'tau1000um_M0400', file_range='all', sec_files=False)

process.thrustNtuple = cms.EDAnalyzer('MFVThrustAnalysis',
                                      gen_particles_src = cms.InputTag('genParticles'),
                                      gen_jets_src = cms.InputTag('ak5GenJets'),
                                      gen_met_src = cms.InputTag('genMetTrue'),
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
scheduler = condor

[CMSSW]
%(dbs_url)s
datasetpath = %(dataset)s
pset = ntuple.py
%(job_control)s

[USER]
ui_working_dir = crab/ThrustAnalysis/crab_ThAn_%(name)s
return_data = 1
additional_input_files = dict_C.so
'''

    os.system('mkdir -p crab/ThrustAnalysis')
    just_testing = 'testing' in sys.argv

    def submit(sample):
        open('crab.cfg', 'wt').write(crab_cfg % sample)
        if not just_testing:
            os.system('crab -create -submit')
            os.system('rm -f crab.cfg mfvgen_analyzer_crab.py mfvgen_analyzer_crab.pyc')

    from JMTucker.Tools.Samples import mfv_signal_samples, ttbarnocut
    for sample in mfv_signal_samples + [ttbarnocut]:
        if 'mfv_' in sample.name and 'tau1000um_M0400' not in sample.name:
            continue
        submit(sample)

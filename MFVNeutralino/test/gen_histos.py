import os, sys, glob
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

process.source.fileNames = ['file:/uscms/home/tucker/nobackup/fromt3/mfv_neutralino_tau1000um_M0400_jtuple_v6_547d3313903142038335071634b26604_pat_1_1_Dpa.root']
process.TFileService.fileName = 'gen_histos.root'

#from JMTucker.MFVNeutralino.SimFiles import load
#load(process, 'tau1000um_M0400', [0,1])

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.load('JMTucker.MFVNeutralino.GenHistos_cff')
process.mfvGenHistos.check_all_gen_particles = False

process.p = cms.Path(process.mfvGenParticleFilter * process.mfvGenHistos)

if debug:
    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.p.insert(0, process.printList)
    file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    if debug:
        raise RuntimeError('refusing to submit jobs in debug (verbose print out) mode')

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('GenHistos',
                       total_number_of_events = -1,
                       events_per_job = 100000,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*'
                       )
    cs.submit_all(samples)

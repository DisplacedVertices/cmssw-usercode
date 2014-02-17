import os, sys, glob
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfv_neutralino_tau1000um_M0400/a6ab3419cb64660d6c68351b3cff9fb0/aodpat_1_1_X2h.root']
process.TFileService.fileName = 'gen_histos.root'

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.load('JMTucker.MFVNeutralino.GenHistos_cff')
process.mfvGenParticleFilter.cut_invalid = False
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

    import JMTucker.Tools.Samples as Samples
    #samples = [s for s in Samples.mfv_signal_samples + Samples.background_samples + Samples.auxiliary_background_samples if 'qcdmu' not in s.name]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('GenHistos',
                       total_number_of_events = -1,
                       events_per_job = 20000,
                       USER_jmt_skip_input_files = 'src/EGamma/EGammaAnalysisTools/data/*'
                       )
    samples = [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau1000um_M1000, Samples.mfv_neutralino_tau9900um_M0400, Samples.mfv_neutralino_tau9900um_M1000] + Samples.mfv_signal_samples
    cs.submit_all(samples)

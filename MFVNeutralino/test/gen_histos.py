import os, sys, glob
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

file_event_from_argv(process)
process.TFileService.fileName = 'gen_histos.root'

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.load('JMTucker.MFVNeutralino.GenHistos_cff')

process.p = cms.Path(process.mfvGenParticleFilter * process.mfvGenHistos)

if debug:
    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.p.insert(0, process.printList)
    file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = [
        TupleOnlyMCSample('mfv01000', '/mfv_neutralino_tau01000um_M0400/tucker-mfv_neutralino_tau01000um_M0400-554987f53c5d1493b23246ebbecfd44a/USER')
        ]
    for sample in samples:
        sample.dbs_url_num = 3
        sample.is_pythia8 = True

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('GenHistos',
                       total_number_of_events = -1,
                       events_per_job = 20000,
                       skip_common = True,
                       )
    cs.submit_all(samples)

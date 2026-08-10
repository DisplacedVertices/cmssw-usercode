import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev16'
sample_files(process, 'mfv_neu_tau01000um_M0800', dataset, -1)
process.TFileService.fileName = 'signalmatch.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.mfvAnalysisCuts.apply_vertex_cuts = False

process.m = cms.EDAnalyzer('MFVSignalMatch',
                           vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                           mevent_src = cms.InputTag('mfvEvent'),
                           max_dist = cms.double(0.0084),
                           )

process.m100 = process.m.clone(max_dist = 0.01)
process.m200 = process.m.clone(max_dist = 0.02)

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvAnalysisCuts * process.m * process.m100 * process.m200)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples

    for sample in samples:
        sample.datasets[dataset].files_per = 1000

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('SignalMatch', dataset = dataset)
    cs.submit_all(samples)

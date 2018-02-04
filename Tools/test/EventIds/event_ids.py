import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

file_event_from_argv(process)

process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.data_samples + Samples.qcd_samples + Samples.qcd_samples_ext + Samples.ttbar_samples + Samples.mfv_signal_samples

    samples = Samples.mfv_neuude_samples

    dataset = 'ntuplev16_wgenv2'
    samples = [s for s in samples if s.has_dataset(dataset)]

    for sample in samples:
        sample.datasets[dataset].split_by = 'files'
        sample.datasets[dataset].files_per = 1

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('EventIds', dataset=dataset)
    cs.submit_all(samples)

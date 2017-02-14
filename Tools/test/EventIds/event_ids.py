import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

file_event_from_argv(process)

process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.data_samples

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = 'ana_2015p6.json'

    cs = CondorSubmitter('EventIds_NtupleV10_15', dataset='ntuplev10')
    cs.submit_all(samples)

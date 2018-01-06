import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

file_event_from_argv(process)

process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.data_samples + Samples.qcd_samples + Samples.qcd_samples_ext + Samples.ttbar_samples

    for sample in samples:
        sample.files_per = 20
        #if not sample.is_mc:
        #    sample.json = 'jsons/ana_2015p6.json'

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('EventIds_NtupleV11_16', dataset='ntuplev11')
    cs.submit_all(samples)

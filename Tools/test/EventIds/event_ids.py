import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

file_event_from_argv(process)

process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv(Samples.ttbar_samples + Samples.qcd_samples + Samples.mfv_signal_samples)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('EventIdsV18',
                       total_number_of_events = -1,
                       events_per_job = 1000000,
                       use_ana_dataset = True,
                       )
    cs.submit_all(samples)

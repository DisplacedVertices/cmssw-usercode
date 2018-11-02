import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

file_event_from_argv(process)

process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.evids.prints = cms.untracked.bool('prints' in sys.argv)

process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    import JMTucker.Tools.Samples as Samples

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
    else:
        samples = Samples.data_samples_2018

    dataset = 'ntuplev21m'
    samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'default', default_files_per=50)

    batch_name = 'EventIds2017'
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    ms = MetaSubmitter(batch_name, dataset=dataset)
    ms.common.ex = year
    ms.common.publish_name = batch_name + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

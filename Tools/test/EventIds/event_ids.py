import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

tfileservice(process, 'evids.root')
file_event_from_argv(process)

add_analyzer(process, 'EventIdRecorder', prints = cms.untracked.bool('prints' in sys.argv))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
    else:
        samples = Samples.qcd_samples_2018 + Samples.data_samples_2018

    dataset = 'miniaod'
    samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'default', default_files_per=50)

    ms = MetaSubmitter('EventIds_MiniAOD', dataset=dataset)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

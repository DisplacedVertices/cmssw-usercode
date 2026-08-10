from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

dataset = 'miniaod'
sample_files(process, 'qcdht2000_2017', dataset, 1)
tfileservice(process, 'eventids.root')
cmssw_from_argv(process)

add_analyzer(process, 'EventIdRecorder', prints = cms.untracked.bool('prints' in sys.argv))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, data=False, all_signal=False)
    set_splitting(samples, dataset, 'default', default_files_per=50)

    ms = MetaSubmitter('EventIds', dataset=dataset)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

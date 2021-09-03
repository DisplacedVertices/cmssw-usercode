from DVCode.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev22m' # 'miniaod'
sample_files(process, 'qcdht0700_2017', dataset, 1)
remove_tfileservice(process)
file_event_from_argv(process)

add_analyzer(process, 'NoOP')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from DVCode.Tools.MetaSubmitter import *
    from DVCode.Tools.Year import year
    from DVCode.Tools import Samples

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
    else:
        samples = Samples.data_samples_2018

    samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'default', default_files_per=50)

    ms = MetaSubmitter('NoOPV22m', dataset=dataset)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

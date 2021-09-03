import sys
from DVCode.Tools.BasicAnalyzer_cfg import *
remove_tfileservice(process)
file_event_from_argv(process)
want_summary(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import DVCode.Tools.Samples as Samples
    samples = [Samples.JetHT2016B3, Samples.JetHT2016F]

    dataset = 'ntuplev15'
    for sample in samples:
        sample.set_curr_dataset(dataset)
        sample.split_by = 'files'
        sample.files_per = 1

    from DVCode.Tools.MetaSubmitter import *
    ms = MetaSubmitter('LumisInFiles', dataset = dataset)

    ms.submit(samples)

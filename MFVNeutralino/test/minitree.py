import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev19m'
sample_files(process, 'qcdht2000_2017', dataset, 1)
process.TFileService.fileName = 'minitree.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017
        #samples += Samples.leptonic_samples_2017

    #samples = [s for s in samples if s.has_dataset(dataset)]

    from JMTucker.Tools.MetaSubmitter import set_splitting, per_sample_pileup_weights_modifier
    set_splitting(samples, dataset, 'minitree', data_json='jsons/ana_2017.json')

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('MiniTreeV19m',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = per_sample_pileup_weights_modifier(),
                         )
    cs.submit_all(samples)

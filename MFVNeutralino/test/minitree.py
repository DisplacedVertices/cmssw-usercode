import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev27darksectorreviewm'
sample_files(process, 'mfv_HtoLLPto4j_tau0p1mm_M1000_100_2016', dataset, 1)
process.TFileService.fileName = 'minitree.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples
    if year == 2015:
        samples = Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            Samples.all_signal_samples_2015
    elif year == 2016:
        samples = Samples.mfv_HtoLLPto4j_samples_2016 + Samples.mfv_HtoLLPto4b_samples_2016 + Samples.mfv_ZprimetoLLPto4j_samples_2016 + Samples.mfv_ZprimetoLLPto4b_samples_2016
        #samples = Samples.data_samples + \
        #    Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + Samples.qcd_hip_samples + \
        #    Samples.all_signal_samples

    from JMTucker.Tools.MetaSubmitter import set_splitting
    set_splitting(samples, dataset, 'minitree', data_json='jsons/ana_2015p6.json')

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('MiniTreeV27darksectorreviewm',
                         ex = year,
                         dataset = dataset,
                         )
    cs.submit_all(samples)

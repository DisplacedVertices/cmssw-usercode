import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev15'
sample_files(process, 'qcdht2000', dataset, 1)
#process.source.fileNames = ['file:ntuple.root']
process.TFileService.fileName = 'minitree.root'

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples
    if year == 2015:
        samples = Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            Samples.mfv_signal_samples_2015
    elif year == 2016:
        samples = Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
            Samples.mfv_signal_samples + Samples.mfv_ddbar_samples + Samples.mfv_hip_samples

    from JMTucker.Tools.MetaSubmitter import set_splitting
    set_splitting(samples, dataset, 'minitree', data_json='ana_2015p6_10pc.json')

    def modify(sample):
        to_add, to_replace = [], []
        if not sample.is_mc:
            to_add.append('process.mfvAnalysisCutsGE1Vtx.max_nvertex = 1')
        return to_add, to_replace

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('MiniTreeV15',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = modify
                         )
    cs.submit_all(samples)

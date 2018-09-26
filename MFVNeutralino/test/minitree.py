import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'ntuplev20m'
sample_files(process, 'qcdht2000_2017', dataset, 1)
process.TFileService.fileName = 'minitree.root'
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
        #samples = Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017 + Samples.mfv_signal_samples_2017

    #samples = [s for s in samples if s.has_dataset(dataset)]

    set_splitting(samples, dataset, 'minitree', data_json='jsons/ana_2017_1pc.json')

    def modify(sample):
        to_add, to_replace = [], []
        if not sample.is_mc:
            to_add.append('''
# set all filters to only keep 1-vertex events and drop 3-or-4, 4, 5-track paths
for x in process.mfvAnalysisCutsGE1Vtx, process.mfvAnalysisCutsGE1VtxNtk3, process.mfvAnalysisCutsGE1VtxNtk4, process.mfvAnalysisCutsGE1VtxNtk3or4:
    x.max_nvertex = 1
del process.pMiniTreeNtk3or4
del process.pMiniTreeNtk4
del process.pMiniTree
''')
        return to_add, to_replace

    cs = CondorSubmitter('MiniTreeV20mp2',
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(half_mc_modifier(), per_sample_pileup_weights_modifier(), modify),
                         )
    cs.submit_all(samples)

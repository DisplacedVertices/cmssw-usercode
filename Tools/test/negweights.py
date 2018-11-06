import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

dataset = 'miniaod'
sample_files(process, 'ttbar_2017', dataset, 1)
tfileservice(process, 'negweights.root')
file_event_from_argv(process)

add_analyzer(process, 'JMTNegativeWeights', gen_info_src = cms.InputTag('generator'))


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.qcd_samples_2017 + Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017

    samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'default', default_files_per=50)

    ms = MetaSubmitter('NegWeightsV1', dataset=dataset)
    ms.submit(samples)

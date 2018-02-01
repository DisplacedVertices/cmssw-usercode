#!/usr/bin/env python

import sys
from JMTucker.Tools.Merge_cfg import cms, process

process.out.maxSize = cms.untracked.int32(2**21) # in kB, i.e. 2 GB

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    from JMTucker.Tools import Samples

    dataset = 'ntuplev17m'
    batch_name = 'NtupleV17m_merge'

    samples = [s for s in
               Samples.data_samples +
               Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext +
               Samples.mfv_signal_samples + Samples.mfv_ddbar_samples
               if s.has_dataset(dataset)]

    for sample in samples:
        sample.datasets[dataset].split_by = 'files'
        sample.datasets[dataset].files_per = -1

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter(batch_name,
                         ex = year,
                         dataset = dataset,
                         publish_name = batch_name + '_' + str(year),
                         skip_output_files = ['merge.root'], # don't autodetect it
                         stageout_files = ['merge*.root'], # let the wrapper script glob merge.root, merge001.root, ...
                         )
    cs.submit_all(samples)

# for now, can publish output with mpublish --partial --no-coderep

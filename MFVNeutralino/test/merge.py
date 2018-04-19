#!/usr/bin/env python

import sys
from JMTucker.Tools.Merge_cfg import cms, process

process.out.maxSize = cms.untracked.int32(2**21) # in kB, i.e. 2 GB

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    dataset = 'ntuplev16_noef'
    import re; mo = re.search(r'.*?(\d+).*?', dataset); assert mo
    if int(mo.group(1)) < 17:
        for i in xrange(20):
            print 'be sure all processing in chain was done by file'
    batch_name = 'NtupleV16_NoEF_merge'

    samples = [s for s in
               # not worth it to merge ttbar and qcd, haven't tried data
               #Samples.data_samples +
               #Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext +
               Samples.all_signal_samples
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

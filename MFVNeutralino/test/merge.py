#!/usr/bin/env python

import sys
from JMTucker.Tools.Merge_cfg import cms, process

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.SampleFiles import SampleFiles
    version = 'V15'
    cs = CRABSubmitter('MFVNtuple' + version + 'Merged',
                       total_number_of_events = -1,
                       events_per_job = 100000,
                       get_edm_output = True,
                       data_retrieval = 'fnal_eos',
                       max_threads = 3,
                       manual_datasets = SampleFiles['MFVNtuple' + version],
                       )

    samples = Samples.mfv_signal_samples

    for sample in samples:
        if sample.is_mc:
            sample.total_events = -1

    cs.submit_all(samples)

#!/usr/bin/env python

import sys
from JMTucker.Tools.Merge_cfg import cms, process

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv(Samples.mfv_signal_samples + [Samples.qcdht0100])

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('MergeNtupleV18_2',
                       use_ana_dataset = True,
                       total_number_of_events = -1,
                       events_per_job = 50000,
                       get_edm_output = True,
                       data_retrieval = 'fnal',
                       max_threads = 3,
                       publish_data_name = 'mfvmergentuple_v18',
                       )

    cs.submit_all(samples)

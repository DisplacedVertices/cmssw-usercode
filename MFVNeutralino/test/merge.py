#!/usr/bin/env python

import sys
from JMTucker.Tools.Merge_cfg import cms, process

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.registry.from_argv(
        Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        Samples.xx4j_samples
        )

    samples = [Samples.qcdht0500]

    cs = CRABSubmitter('MergeNtupleV5_smaller',
                       dataset = 'ntuplev5',
                       splitting = 'FileBased',
                       units_per_job = 50,
                       total_units = -1,
                       aaa = True,
                       publish_name = 'mergentuplev5',
                       )
    cs.submit_all(samples)

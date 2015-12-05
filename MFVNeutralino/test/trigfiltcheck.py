import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, file_event_from_argv

file_event_from_argv(process)
process.TFileService.fileName = 'trigeff.root'

from JMTucker.MFVNeutralino.TriggerFilter import setup_trigger_filter
setup_trigger_filter(process, 'pmfvfilt')

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    from JMTucker.Tools.Sample import anon_samples
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.xx4j_samples + Samples.mfv_signal_samples

    cs = CRABSubmitter('TriggerFilterCheck',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 20000,
                       total_units = 100000,
                       )
    cs.submit_all(samples)

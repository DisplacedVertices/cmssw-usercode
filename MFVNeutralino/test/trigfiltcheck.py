import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process, file_event_from_argv

file_event_from_argv(process)
process.TFileService.fileName = 'trigeff.root'

from JMTucker.MFVNeutralino.TriggerFilter import setup_trigger_filter
setup_trigger_filter(process, 'pmfvfilt')
setup_trigger_filter(process, 'ponlyhtpt', 'tfonlyhtpt')
setup_trigger_filter(process, 'ponlyht', 'tfonlyht')
setup_trigger_filter(process, 'ponlyht8', 'tfonlyht8')

process.tfonlyhtpt.HLTPaths = [
    'HLT_PFHT650_v*',
    'HLT_PFHT800_v*',
    'HLT_PFHT900_v*',
    'HLT_PFHT550_4Jet_v*',
    'HLT_PFHT450_SixJet40_v*',
    'HLT_PFHT400_SixJet30_v*',
    ]

process.tfonlyht.HLTPaths = [
    'HLT_PFHT650_v*',
    'HLT_PFHT800_v*',
    'HLT_PFHT900_v*',
    ]

process.tfonlyht8.HLTPaths = [
    'HLT_PFHT800_v*',
    'HLT_PFHT900_v*',
    ]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    from JMTucker.Tools.Sample import anon_samples
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.xx4j_samples + Samples.mfv_signal_samples

    cs = CRABSubmitter('TriggerFilterCheckv2',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 50000,
                       total_units = -1,
                       )
    cs.submit_all(samples)

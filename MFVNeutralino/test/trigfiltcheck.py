import sys
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True
H = False

process = pat_tuple_process(None, is_mc, year, H)
jets_only(process)

file_event_from_argv(process)
tfileservice(process, 'trigfiltcheck.root')

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
setup_event_filter(process, event_filter=True)

setup_event_filter(process, 'ponlytrig')

setup_event_filter(process, 'ponlyHT800', 'onlyHT800')
process.onlyHT800.HLTPaths = ["HLT_PFHT800_v*"]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)

if 'argv' in sys.argv:
    from JMTucker.Tools import Samples
    sample = [x for x in sys.argv if hasattr(Samples, x)][0]
    sample_files(process, sample, 'main', 100)
    tfileservice(process, 'trigfiltcheck_%s.root' % sample)
    process.maxEvents.input = 1000
    want_summary(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    from JMTucker.Tools.Sample import anon_samples
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.xx4j_samples + Samples.mfv_signal_samples

    samples = Samples.auxiliary_background_samples

    cs = CRABSubmitter('TrigFiltChkV3_76_ttaux_qcdpt',
                       splitting = 'EventAwareLumiBased',
                       units_per_job = 200000,
                       total_units = 1000000,
                       )
    cs.submit_all(samples)

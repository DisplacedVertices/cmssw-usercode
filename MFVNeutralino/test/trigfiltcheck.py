import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.Year import year

is_mc = True
H = False
repro = False
test_event_filter = False

if test_event_filter:
    process = pat_tuple_process(None, is_mc, year, H, repro)
    jets_only(process)

file_event_from_argv(process)
tfileservice(process, 'trigfiltcheck.root')

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter

if test_event_filter:
    setup_event_filter(process, event_filter=True)

setup_event_filter(process, 'ptrigger')

paths = process.triggerFilter.HLTPaths.value()

for x in paths:
    filt_name = x.split('_')[1]
    setup_event_filter(process, 'p%s' % filt_name, filt_name)
    getattr(process, filt_name).HLTPaths = [x]

setup_event_filter(process, 'pHcombination', 'Hcombination')
process.Hcombination.HLTPaths = paths[1:]

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
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples
    samples = Samples.mfv_signal_samples + Samples.mfv_ddbar_samples

    raise NotImplementedError('is_mc, H, repro modifiers?')
 
    for s in samples:
        s.split_by = 'files'
        s.files_per = 20

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('TrigFiltCheckV1')
    ms.common.ex = 2016
    ms.crab.job_control_from_sample = True
    ms.submit(samples)

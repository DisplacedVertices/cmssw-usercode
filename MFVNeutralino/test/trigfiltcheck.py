import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

sample_files(process, 'qcdht2000_2017', 'miniaod')
geometry_etc(process)
max_events(process, 10000)
file_event_from_argv(process)
tfileservice(process, 'trigfiltcheck.root')

from JMTucker.MFVNeutralino.EventFilter import setup_event_filter
sef = lambda *a,**kwa: setup_event_filter(process, *a, input_is_miniaod=True, **kwa)
sef('ptrigger')
sef('pevtsel',        event_filter = True)
sef('pevtselNoJESUp', event_filter = True, event_filter_jes_mult = 0, event_filter_name = 'mfvEventFilterNoJESUp')
sef('pevtselWoVtx',   event_filter = True, event_filter_require_vertex = False, event_filter_name = 'mfvEventFilterWoVtx')

for x in process.mfvTriggerFilter.HLTPaths.value():
    filt_name = ''.join(x.split('_')[1:-1])
    sef('p%s' % filt_name, filt_name)
    getattr(process, filt_name).HLTPaths = [x]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)

if 'argv' in sys.argv:
    from JMTucker.Tools import Samples
    sample_name = [x for x in sys.argv if hasattr(Samples, x)][0]
    sample_files(process, sample_name, 'miniaod')
    tfileservice(process, 'trigfiltcheck_%s.root' % sample_name)
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
    ms.submit(samples)

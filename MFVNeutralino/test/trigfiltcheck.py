import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, global_tag, process, file_event_from_argv
from JMTucker.Tools.MiniAOD_cfg import which_global_tag
from JMTucker.MFVNeutralino.Year import year

file_event_from_argv(process)
process.TFileService.fileName = 'trigeff.root'
global_tag(process, which_global_tag(True, year)) # needed for emulator that checks L1 bits

from JMTucker.MFVNeutralino.EventFilter import *
setup_event_filter_soup(process, 'pmfvfilt')
setup_event_filter_soup(process, 'ponlyhtpt', 'tfonlyhtpt')
setup_event_filter_soup(process, 'ponlyht', 'tfonlyht')
setup_event_filter_soup(process, 'ponlyht8', 'tfonlyht8')
setup_event_filter_soup(process, 'ponlyht9', 'tfonlyht9')
setup_event_filter(process, 'pemuht8',             need_pat=True)
setup_event_filter(process, 'pemuht9', 'emuht900', need_pat=True)

process.emuht900.return_actual = False
process.emuht900.return_ht900 = True

#process.options.wantSummary = True

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
    ]

process.tfonlyht9.HLTPaths = [
    'HLT_PFHT900_v*',
    ]

import JMTucker.Tools.SimpleTriggerEfficiency_cfi as SimpleTriggerEfficiency
SimpleTriggerEfficiency.setup_endpath(process)


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

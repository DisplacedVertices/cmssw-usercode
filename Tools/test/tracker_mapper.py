import sys
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.MFVNeutralino.Year import year

is_mc = True

process = pat_tuple_process(None, is_mc, year)
jets_only(process)

sample_files(process, 'qcdht2000ext', 'main', 5)
tfileservice(process, 'tracker_mapper.root')

if is_mc:
    process.load('JMTucker.Tools.MCStatProducer_cff')

import JMTucker.MFVNeutralino.TriggerFilter
JMTucker.MFVNeutralino.TriggerFilter.setup_trigger_filter(process)

process.load('JMTucker.MFVNeutralino.JetFilter_cfi')

process.load('JMTucker.Tools.TrackerMapper_cfi')
process.p = cms.Path(process.triggerFilter * process.mfvJetFilter * process.TrackerMapper)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext

    filter_eff = { 'qcdht0500': 2.9065e-03, 'qcdht0700': 3.2294e-01, 'ttbar': 3.6064e-02}
    for s in samples:
        s.files_per = 10
        if s.is_mc:
            for k,v in filter_eff.iteritems():
                if s.name.startswith(k):
                    s.events_per = min(int(25000/v), 400000)
        else:
            s.json = 'ana_2015p6_10pc.json'

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('TrackerMapperV0')
    ms.common.ex = year
    ms.common.pset_modifier = is_mc_modifier
    ms.crab.job_control_from_sample = True
    ms.submit(samples)

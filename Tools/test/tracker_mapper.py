import sys
from JMTucker.Tools.MiniAOD_cfg import *
from JMTucker.Tools.CMSSWTools import *
from JMTucker.Tools.Year import year

is_mc = True
H = False
repro = False

process = pat_tuple_process(None, is_mc, year, H, repro)
jets_only(process)

sample_files(process, 'qcdht2000ext', 'main', 5)
tfileservice(process, 'tracker_mapper.root')

process.load('JMTucker.Tools.MCStatProducer_cff')

import JMTucker.MFVNeutralino.EventFilter
JMTucker.MFVNeutralino.EventFilter.setup_event_filter(process)

process.load('JMTucker.Tools.JetFilter_cfi')

process.load('JMTucker.Tools.TrackerMapper_cfi')
process.TrackerMapperOldStCut = process.TrackerMapper.clone(old_stlayers_cut = True)
process.p = cms.Path(process.triggerFilter * process.jmtJetFilter * process.TrackerMapper * process.TrackerMapperOldStCut)

if False:
    from JMTucker.Tools.PileupWeights import pileup_weights
    for k,v in pileup_weights.iteritems():
        if type(k) == str and k.startswith('2016'):
            tm = process.TrackerMapper.clone(pileup_weights = v)
            setattr(process, 'tm%s' % k, tm)
            process.p *= tm

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    if year == 2015:
        samples = Samples.data_samples_2015 + Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015
    elif year == 2016:
        samples = Samples.data_samples + Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + Samples.mfv_signal_samples + Samples.mfv_ddbar_samples

    #samples = Samples.qcd_hip_samples + [Samples.qcdht0700ext, Samples.qcdht1000ext, Samples.qcdht1500ext] + Samples.data_samples

    filter_eff = { 'qcdht0500': 2.9065e-03, 'qcdht0700': 3.2294e-01, 'ttbar': 3.6064e-02}
    for s in samples:
        s.files_per = 10
        if s.is_mc:
            for k,v in filter_eff.iteritems():
                if s.name.startswith(k):
                    s.events_per = min(int(25000/v), 400000)
        else:
            s.json = 'jsons/ana_2015p6.json'

    from JMTucker.Tools.MetaSubmitter import *
    ms = MetaSubmitter('TrackerMapper_qcd_hip_v2')
    ms.common.ex = year
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, H_modifier, repro_modifier)
    ms.crab.job_control_from_sample = True
    ms.submit(samples)

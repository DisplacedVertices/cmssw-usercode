#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.event_filter = 'jets only'

process = ntuple_process(settings)
max_events(process, 10000)
report_every(process, 1000000)
#want_summary(process)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'qcdht2000_2017', dataset, 1)
file_event_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples  = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017
        samples += Samples.data_samples_2017
        #samples += Samples.leptonic_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    #samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'ntuple')

    if settings.run_n_tk_seeds:
        samples = [s for s in samples if not s.is_signal]

    def signals_no_event_filter_modifier(sample):
        if sample.is_signal:
            magic = 'event_filter = True'
            to_replace = [(magic, 'event_filter = False', 'tuple template does not contain the magic string "%s"' % magic)]
        else:
            to_replace = []
        return [], to_replace

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.ex = year
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, signals_no_event_filter_modifier)
    ms.common.publish_name = settings.batch_name() + '_' + str(year)
    ms.crab.job_control_from_sample = True
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

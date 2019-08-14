#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = True
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
#settings.event_filter = 'jets only'
settings.event_filter = False

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'ttbar_2017', dataset, 1)
#sample_files(process, 'mfv_neu_tau000100um_M0400_2017', dataset, 1)
#sample_files(process, 'mfv_neu_tau000100um_M1200_2017', dataset, 1)
max_events(process, 1000)
cmssw_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    #samples = pick_samples(dataset, all_signal=not settings.run_n_tk_seeds)
    #samples = pick_samples(dataset, both_years=False, qcd=True, ttbar=True, all_signal=not settings.run_n_tk_seeds, data=False, leptonic=False)
    samples = pick_samples(dataset, both_years=False, qcd=True, ttbar=False, all_signal=False, data=False, leptonic=False)
            
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

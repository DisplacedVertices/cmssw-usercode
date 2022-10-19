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
#if use_btag_triggers :
#    settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
#else :
#    settings.event_filter = 'jets only'
settings.event_filter = False

# see readme for randpars
settings.randpars_filter = False
# if want to test local : 
#settings.randpars_filter = 'randpar HToSSTodddd M07_ct0p05-'


process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'ggHToSSTobbbb_tau1mm_M55_2017', dataset, 1)
input_files(process, 'C47DA2BF-B0FF-EA11-A2BC-001E67586629.root')
max_events(process, 400)
cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=not settings.run_n_tk_seeds, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)
        samples = [getattr(Samples, 'ggHToSSTobbbb_tau1mm_M55_2017')]  
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier, signal_uses_random_pars_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

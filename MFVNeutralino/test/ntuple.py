#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.keep_tk = False
if use_btag_triggers :
    #settings.event_filter = 'dilepton only' # for new trigger studies
    #settings.event_filter = 'leptons only' # for new trigger studies
    settings.event_filter = 'low HT online track test' # for new trigger studies
    #settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
elif use_MET_triggers :
    settings.event_filter = 'met only'
else :
    settings.event_filter = 'jets only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
max_events(process, 100000)
cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=False, data=False) # no data currently; no sliced ttbar since inclusive is used
        samples = Samples.DisplacedJet_data_samples_2017 + Samples.qcd_samples_2017
        #samples = Samples.mfv_signal_samples_2018 + Samples.mfv_stopdbardbar_samples_2018 + Samples.mfv_stopbbarbbar_samples_2018 + Samples.HToSSTodddd_samples_2018
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2016.json' if year in [20161, 20162] else 'ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, bjet_trigger_veto_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

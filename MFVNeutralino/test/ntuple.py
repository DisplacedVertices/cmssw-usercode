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
settings.keep_tk = False
if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
elif use_MET_triggers :
    settings.event_filter = 'met only'
elif use_Lepton_triggers :
    settings.event_filter = 'leptons only'
else :
    settings.event_filter = 'jets only'

settings.randpars_filter = False
# if want to test local : 
#settings.randpars_filter = 'randpar HToSSTodddd M15_ct10-'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'qcdht2000_2017', dataset, 1)
sample_files(process, 'mfv_stopld_tau000100um_M0200_2018', dataset, 1)
#sample_files(process, 'qcdmupt15_2017', dataset, 1)
max_events(process, 1000)
cmssw_from_argv(process)



if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    # if use_btag_triggers :
    #     samples = pick_samples(dataset, qcd=True, ttbar=False, data=False) # no data currently; no sliced ttbar since inclusive is used
    # if use_MET_triggers :
    #     samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)

    if use_Lepton_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=True, diboson=False, Lepton_data=False)
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_SingleLept_2017_10pc.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
   # ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier, signal_uses_random_pars_modifier)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, signal_uses_random_pars_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

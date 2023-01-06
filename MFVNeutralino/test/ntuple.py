#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = True
settings.keep_gen = False
settings.keep_tk = False
if use_btag_triggers :
    #settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
    settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
elif use_MET_triggers :
    settings.event_filter = 'met only'
else :
    settings.event_filter = 'jets only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#input_files(process, '/eos/uscms/store/user/shogan/stop_bbarbbar_miniaod/mfv_stopbbarbbar_tau001000um_M1200_2017/miniaod_0.root') 
#sample_files(process, 'mfv_stopbbarbbar_tau001000um_M0800_2018', dataset, 1)
max_events(process, 1000)
cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=False, data=False) # no data currently; no sliced ttbar since inclusive is used
        #samples = Samples.mfv_signal_samples_2018 + Samples.mfv_stopdbardbar_samples_2018 + Samples.mfv_stopbbarbbar_samples_2018
        samples = [getattr(Samples, 'ggHToSSTobbbbb_tau1mm_M55_2017')]   
        #samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2018
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

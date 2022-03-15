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
settings.rp_filter = False

if use_btag_triggers :
    #settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
    settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
else :
    settings.event_filter = 'leptons only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'ttbar_2017', dataset, 5)
#input_files(process, '/uscms_data/d3/shogan/scratch/filter_studies/ggH_HtoSS_SStodddd_miniaod_M40_ct1mm.root')
input_files(process, '/uscms_data/d3/shogan/scratch/emerging_jets/EmergingJets_mX-1000-m_dpi-1-ctau_dpi-1_2017_num0.root')
max_events(process, 10000)
cmssw_from_argv(process)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=not settings.run_n_tk_seeds, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        samples = Samples.goofin_2017
    else :
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)
        samples = Samples.bjet_samples_2017

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

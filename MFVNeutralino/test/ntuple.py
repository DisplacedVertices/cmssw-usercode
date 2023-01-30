#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = True #event_filter bkg: False but signal: True
settings.keep_gen = False
settings.rp_filter = False

if use_btag_triggers :
    #settings.event_filter = 'bjets OR displaced dijet veto HT' # for new trigger studies
    settings.event_filter = 'bjets OR displaced dijet' # for new trigger studies
else :
    settings.event_filter = 'leptons only'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#sample_files(process, 'JetHT2017C', dataset, 5)
sample_files(process, 'ttbar_2017', dataset, 1)
#input_files(process, '/uscms_data/d3/shogan/scratch/filter_studies/ggH_HtoSS_SStodddd_miniaod_M40_ct1mm.root')
#input_files(process, '/uscms_data/d3/shogan/scratch/emerging_jets/EmergingJets_mX-1000-m_dpi-1-ctau_dpi-1_2017_num0.root')
#input_files(process, 'C47DA2BF-B0FF-EA11-A2BC-001E67586629.root') #H4b 1mm 55GeV
max_events(process, 50)
cmssw_from_argv(process)
silence_messages(process, ['TwoTrackMinimumDistanceHelixLine']) 
silence_messages(process, ['TwoTrackMinimumDistance']) 

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        #samples = Samples.mfv_signal_samples_2017 + Samples.mfv_stopdbardbar_samples_2017
        samples = [getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_2017')] 
        #samples = Samples.HToSSTodddd_samples_2017  
    else :
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)
        samples = Samples.bjet_samples_2017

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

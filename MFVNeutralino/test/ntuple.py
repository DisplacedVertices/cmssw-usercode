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
#input_files(process, '/store/mc/RunIISummer20UL17MiniAOD/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/280000/BB6E40E3-1F43-6C41-AEF8-5A7B96D0C5E5.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2550000/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/0BD790C6-883F-0147-A66E-8EC9DC53750F.root')
#sample_files(process, 'qcdht2000_2017', dataset, 1)
#sample_files(process, 'WHToSSTodddd_tau1mm_M55_2017', dataset, 1)
#sample_files(process, 'qcdmupt15_2017', dataset, 1)
#max_events(process, 10)
#set_events(process, [(1, 12002, 31167330)])
cmssw_from_argv(process)



if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    # if use_btag_triggers :
    #     samples = pick_samples(dataset, qcd=True, ttbar=False, data=False) # no data currently; no sliced ttbar since inclusive is used
    # if use_MET_triggers :
    #     samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)

    if use_Lepton_triggers :
        #samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=False)
        samples = [getattr(Samples, 'qcdbctoept080_2017')]
        #samples = [getattr(Samples, 'WplusHToSSTodddd_tau1mm_M55_2017')] 
        #samples = [getattr(Samples, 'mfv_stoplb_tau001000um_M0400_2017')] 
    else :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)

    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_SingleLept_2017_10pc.json'), limit_ttbar=True)

    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
   # ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier, signal_uses_random_pars_modifier)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, signal_uses_random_pars_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

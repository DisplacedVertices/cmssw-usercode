#!/usr/bin/env python

from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

settings = NtupleSettings()
settings.is_mc = True
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False #FIXME 
settings.keep_gen = False
settings.keep_tk = False
if use_btag_triggers :
    #settings.mode = 'dilepton only' # for new trigger studies
    #settings.mode = 'leptons only' # for new trigger studies
    #settings.mode = 'low HT online track test' # for new trigger studies
    settings.mode = 'bjets OR displaced dijet' # for new trigger studies
elif use_MET_triggers :
    #settings.mode = 'met only'
    settings.mode = 'met only'
    #settings.mode = 'met AND iso muons'
elif use_Muon_triggers :
    settings.mode = 'muons only' #FIXME
elif use_Electron_triggers :
    settings.mode = 'electrons only' #FIXME
else :
    settings.mode = 'jets only'

settings.randpars_filter = False
# if want to test local : 
#settings.randpars_filter = 'randpar HToSSTodddd M15_ct10-'

process = ntuple_process(settings)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2550000/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/0BD790C6-883F-0147-A66E-8EC9DC53750F.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/DC0DDB54-E968-A948-B805-FCCDA9CDB11A.root')
input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/A8C3978F-4BE4-A844-BEE8-8DEE129A02B7.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/8ABE7321-B876-E248-951A-02BA0140B498.root')
max_events(process, 100)
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#input_files(process, '~/nobackup/crabdirs/WplsuH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_UL2017_MINIAOD.root')
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#set_events(process, [(1, 12002, 31167330)])
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/100000/177D06A8-D7E8-E14A-8FB8-E638820EDFF3.root')
cmssw_from_argv(process)



if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
       #samples = pick_samples(dataset, qcd=True, ttbar=False, data=False) # no data currently; no sliced ttbar since inclusive is used
       samples = Samples.DisplacedJet_data_samples_2017 + Samples.qcd_samples_2017
    elif use_MET_triggers :
       samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
    elif use_Muon_triggers :
        #samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=False, leptonic=False, met=False, diboson=False, Lepton_data=False)
        samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
        #samples = [getattr(Samples, 'WplusHToSSTodddd_tau300um_M55_2017')] 
        #samples = [getattr(Samples, 'mfv_stoplb_tau001000um_M0400_2017')] 
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=False)
    else :
        #samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, all_signal=not settings.run_n_tk_seeds)
        samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
    
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2016.json' if year in [20161, 20162] else 'ana_2017p8.json'), limit_ttbar=True)
    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, bjet_trigger_veto_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

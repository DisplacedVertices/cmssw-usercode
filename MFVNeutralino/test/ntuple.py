#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

settings = NtupleSettings()
settings.is_mc = True # NOTE: you must set this differently when processing data vs. MC!
#settings.is_mc = False
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.keep_tk = False


if use_btag_vetoLepHT_triggers :
    settings.event_filter = 'bjets OR displaced dijet veto leptons and HT' # default for displacement trigger analysis!
elif use_MET_triggers :
    settings.event_filter = 'met only'
elif use_Lepton_triggers :
    settings.event_filter = 'leptons only' # default for lepton-triggered analysis! Use muons/electrons only when processing data, to not double count things in both Egamma and Muon Primary Datasets
elif use_Muon_triggers :
    settings.event_filter = 'muons only' 
elif use_Electron_triggers :
    settings.event_filter = 'electrons only veto muons' 
else :
    settings.event_filter = 'jets only'

settings.randpars_filter = False

process = ntuple_process(settings)
#max_events(process, 10)
dataset = 'miniaod' if settings.is_miniaod else 'main'
#input_files(process, 'root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL17MiniAODv2/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2550000/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
#input_files(process, 'root://cmsxrootd.fnal.gov//store/data/Run2017B/SingleElectron/MINIAOD/UL2017_MiniAODv2-v1/270000/5E96AE29-4D22-8543-80C6-D8DEA2A38DF3.root')

#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/0BD790C6-883F-0147-A66E-8EC9DC53750F.root')
#input_files(process, '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/30000/F80DB8BA-EB71-E04B-A334-5B701A3FDF3E.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/DC0DDB54-E968-A948-B805-FCCDA9CDB11A.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/A8C3978F-4BE4-A844-BEE8-8DEE129A02B7.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/8ABE7321-B876-E248-951A-02BA0140B498.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2810000/056FAB59-F395-374B-BB32-E4A70D6C65BA.root')
#set_events(process, [(1, 12002, 31167330)])
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/100000/177D06A8-D7E8-E14A-8FB8-E638820EDFF3.root')
#input_files(process, '/store/data/Run2017B/MET/MINIAOD/UL2017_MiniAODv2-v1/100000/9B53ACB7-C063-1D44-A564-42435C24DE7B.root')
input_files(process, '/store/mc/RunIISummer20UL18MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_upgrade2018_realistic_v16_L1v1-v2/110000/307A2B60-76A2-3F43-8A2D-FD3E62A0F7EA.root')

cmssw_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_vetoLepHT_triggers :
        if settings.is_mc :
            #samples = [getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_2017')]
            samples = pick_samples(dataset, all_bjet_signal=True, qcd=True, ttbar=True)
        else :
            samples = pick_samples(dataset, BTagCSV_data=True, DisplacedJet_data=True)

    elif use_Lepton_triggers :
        if not settings.is_mc :
            sys.exit('In ntuple.py, use_Lepton_triggers should not be set with is_mc False! Instead, we must do use_Muon_triggers and use_Electron_triggers to properly handle overlaps between PDs')

        samples = pick_samples(dataset, all_lep_signal=True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True)

    elif use_Muon_triggers :
        if settings.is_mc :
            sys.exit('In ntuple.py, use_Muon_triggers should not be set with is_mc True!')

        samples = pick_samples(dataset, Muon_data=True)

    elif use_Electron_triggers :
        if settings.is_mc :
            sys.exit('In ntuple.py, use_Electron_triggers should not be set with is_mc True!')

        samples = pick_samples(dataset, Electron_data=True)

    else :
        print 'trigger scenario not set properly in ntuple.py, please double check! Submitting some jobs nonetheless...'
        samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
    
    json_filename = 'ana_run2_displacement_trigger.json' if use_btag_vetoLepHT_triggers else 'ana_run2.json'
    set_splitting(samples, dataset, 'ntuple', data_json=json_path(json_filename), limit_ttbar=True)
    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier, ttH_duplicate_check_modifier)
    ms.condor.stageout_files = 'all'
    ms.condor.local_stage = False # By default do not copy remote files to local. Switch to True for primarily high mass signals, or any sample timing out via xRootD
    ms.submit(samples)

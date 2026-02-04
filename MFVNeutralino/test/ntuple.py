#!/usr/bin/env python

import FWCore.ParameterSet.Config as cms
from JMTucker.Tools.general import named_product
from JMTucker.MFVNeutralino.NtupleCommon import *
from JMTucker.Tools.Year import year

settings = NtupleSettings()
settings.is_mc = True #FIXME
settings.is_miniaod = True

settings.run_n_tk_seeds = False
settings.minitree_only = False
settings.prepare_vis = False
settings.keep_all = False
settings.keep_gen = False
settings.keep_tk = False


if use_btag_triggers :
    settings.event_filter = 'bjets OR displaced dijet'
elif use_btag_vetoLepHT_triggers :
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
# if want to test local : 
#settings.randpars_filter = 'randpar HToSSTodddd M15_ct10-'

process = ntuple_process(settings)
#max_events(process, 10)
dataset = 'miniaod' if settings.is_miniaod else 'main'
input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ZH_HToSSTodddd_ZToLL_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2550000/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/0BD790C6-883F-0147-A66E-8EC9DC53750F.root')
#input_files(process, '/store/mc/RunIISummer20UL16MiniAODAPVv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/30000/F80DB8BA-EB71-E04B-A334-5B701A3FDF3E.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WplusH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/40000/DC0DDB54-E968-A948-B805-FCCDA9CDB11A.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120001/A8C3978F-4BE4-A844-BEE8-8DEE129A02B7.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_1J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/120000/8ABE7321-B876-E248-951A-02BA0140B498.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ggH_HToSSTodddd_MH-125_MS-55_ctauS-1_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2810000/056FAB59-F395-374B-BB32-E4A70D6C65BA.root')
#max_events(process, 200)
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#input_files(process, '~/nobackup/crabdirs/WplsuH_HToSSTodddd_WToLNu_MH-125_MS-55_ctauS-1_UL2017_MINIAOD.root')
#input_files(process, '~/nobackup/crabdirs/TTJets_UL2017_MINIAOD.root')
#set_events(process, [(1, 12002, 31167330)])
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/100000/177D06A8-D7E8-E14A-8FB8-E638820EDFF3.root')
#input_files(process, '/store/data/Run2017B/MET/MINIAOD/UL2017_MiniAODv2-v1/100000/9B53ACB7-C063-1D44-A564-42435C24DE7B.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/240000/5B73F7F4-DF5B-7E4D-8F50-71A5E8024689.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/240000/5B73F7F4-DF5B-7E4D-8F50-71A5E8024689.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAOD/WJetsToLNu_0J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/260000/00F00BE5-0C38-D047-88F7-D8EC2FCDDDFA.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTHTo2C_TTTo2L2Nu_M-125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/2540000/036644E2-9F05-8D41-8CD4-885679962D80.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/100000/3B05C6F7-7877-BD43-8F5F-E29283865170.root')
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/TTJets_SingleLeptFromT_genMET-150_TuneCP5_13TeV-madgraphMLM-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v2/2430000/00351BB6-B311-8F40-B684-A1C7A375AF71.root')
#input_files(process, '/uscms/home/joeyr/nobackup/13DF01B3-1BC9-0246-8C88-DF26E2F16793.root')
cmssw_from_argv(process)



if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
       samples = pick_samples(dataset, qcd=True, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
       #samples = pick_samples(dataset, qcd=False, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True) #set settings.is_mc to False
    elif use_btag_vetoLepHT_triggers :
        #samples = [getattr(Samples, 'mfv_neu_tau001000um_M0400_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau000300um_M0400_2017')]
        #samples = [getattr(Samples, 'mfv_stopdbardbar_tau001000um_M0200_2017')]
        #samples = [getattr(Samples, 'ggHToSSTodddd_tau1mm_M55_2017')]

        if settings.is_mc :
            #samples = [getattr(Samples, 'mfv_stopdbardbar_tau010000um_M0400_2017')]
            samples = pick_samples(dataset, qcd=False, data=False, all_signal=True, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
            #samples = pick_samples(dataset, qcd=True, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False, BTagCSV_data=False, DisplacedJet_data=False)
        else :
            samples = pick_samples(dataset, qcd=False, data=False, all_signal=False, qcd_lep=False, leptonic=False, ttbar=False, diboson=False, Lepton_data=False, BTagCSV_data=True, DisplacedJet_data=True) #set settings.is_mc to False

    elif use_MET_triggers :
       samples = pick_samples(dataset, qcd=True, ttbar=False, data=False, leptonic=True, splitSUSY=True, Zvv=True, met=True, span_signal=False)
    elif use_Lepton_triggers :
        #samples = pick_samples(dataset, qcd=True, data = False, all_signal=True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True, Lepton_data=False) #bkg template
        samples = pick_samples(dataset, qcd=False, data = False, all_signal=True, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False) #trk ineff apply
        #samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=False, leptonic=False, met=True, diboson=False, Lepton_data=True) #set settings.is_mc to False
    elif use_Muon_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=True)
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = False, qcd_lep=True, leptonic=True, met=True, diboson=True, Lepton_data=False)
    else :
        samples = [getattr(Samples, 'wjetstolnu_2j_2017')]
    
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2016.json' if year in [20161, 20162] else 'ana_2017p8.json'), limit_ttbar=True)
    ms = MetaSubmitter(settings.batch_name(), dataset=dataset)
    ms.common.pset_modifier = chain_modifiers(is_mc_modifier, era_modifier, npu_filter_modifier(settings.is_miniaod), signals_no_event_filter_modifier)#, bjet_trigger_veto_modifier)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

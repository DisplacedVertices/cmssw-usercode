from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_btag_vetoLepHT_triggers, use_MET_triggers, use_Lepton_triggers, use_Muon_triggers, use_Electron_triggers
#sample_files(process, 'WplusHToSSTodddd_tau1mm_M55_2017' if is_mc else 'JetHT2017B', dataset, 1)
#sample_files(process, 'mfv_stopld_tau000100um_M0200_2018' if is_mc else 'JetHT2017B', dataset, 1)
#input_files(process, '/store/mc/RunIISummer20UL17MiniAODv2/WJetsToLNu_2J_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v9-v1/100000/177D06A8-D7E8-E14A-8FB8-E638820EDFF3.root')
#max_events(process, 100)
input_files(process, '/store/group/lpclonglived/joeyr/TTJets_TuneCP5_13TeV-amcatnloFXFX-pythia8/NtupleOnnormdzULV30BvetoLHTm_20161/250222_142639/0000/ntuple_1.root')
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

# blind btag triggered events
#if not is_mc and use_btag_triggers :
#    del process.pMiniTreeNtk3
#    del process.pMiniTreeNtk4
#    del process.pMiniTreeNtk3or4
#    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=True, data=False, bjet=False) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif  use_btag_vetoLepHT_triggers:
        samples = pick_samples(dataset, qcd=True, data = False, all_signal = False, qcd_lep=False, leptonic=False, ttbar=True, diboson=False, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, met=False, span_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_Lepton_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep=False, leptonic=True, ttbar=False, diboson=False, Lepton_data=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_Muon_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep = False, leptonic=False, met=False, diboson=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    elif use_Electron_triggers :
        samples = pick_samples(dataset, qcd=False, data = False, all_signal = True, qcd_lep = True, leptonic=True, met=True, diboson=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    else :
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, splitSUSY=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())


    json_filename = 'ana_run2_displacement_trigger.json' if (use_btag_triggers or use_btag_vetoLepHT_triggers) else 'ana_run2.json'
    set_splitting(samples, dataset, 'minitree', data_json=json_path(json_filename))

    cs = CondorSubmitter('MiniTree_LepIPCut_' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)

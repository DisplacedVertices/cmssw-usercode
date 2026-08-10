from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
study_20pc = True

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_BTagDispJet_vetoLepHT_triggers, use_BTag_triggers, use_DispJet_triggers, use_MET_triggers, use_Lepton_triggers, use_Muon_triggers, use_Electron_triggers
#sample_files(process, 'WplusHToSSTodddd_tau1mm_M55_2017' if is_mc else 'JetHT2017B', dataset, 1)
#max_events(process, 100)
input_files(process, 'root://cmseos.fnal.gov//store/group/lpcdisplacedvertices/joeyr/SingleMuon/Ntuple_tag004Lepm_2018/260731_105613/0000/ntuple_221.root')
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

# Workaround for weird vertexing bug that appears very rarely in signal MC
if is_mc : 
    process.options = cms.untracked.PSet(
        wantSummary = cms.untracked.bool(True),
        SkipEvent = cms.untracked.vstring("ProductNotFound"),
    )

# blind data events with >= 4 tracks per vertex until we're ready
if not is_mc :
    del process.pMiniTreeNtk4
    del process.pMiniTreeNtk3or4
    del process.pMiniTreeNtk3or5
    del process.pMiniTreeNtk4or5
    del process.pMiniTreeNtk3or4exact
    del process.pMiniTreeNtk3or5exact
    del process.pMiniTreeNtk4or5exact
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_BTag_triggers or use_DispJet_triggers:
        sys.exit('In minitree.py, use_BTag_triggers and use_DispJet_triggers should not be used (they are only needed for the MiniAOD -> ntuple step). After merging the orthogonal data streams, use use_BTagDispJet_vetoLepHT_triggers.')

    if use_Muon_triggers or use_Electron_triggers :
        sys.exit('In minitree.py, use_Muon_triggers and use_Electron_triggers should not be used (they are only needed for the MiniAOD -> ntuple step). Instead, do use_Lepton_triggers.')

    if  use_BTagDispJet_vetoLepHT_triggers:
        if is_mc :
            samples = pick_samples(dataset, all_bjet_signal=True, qcd=True, ttbar=True)
            pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)
        else :
            samples = pick_samples(dataset, BTagCSV_data=True, DisplacedJet_data=True)
            pset_modifier = None

    elif use_Lepton_triggers :
        if is_mc :
            samples = pick_samples(dataset, all_lep_signal=True, qcd_lep=True, leptonic=True, ttbar=True, diboson=True)
            pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)
        else :
            samples = pick_samples(dataset, Muon_data=True, Electron_data=True)
            pset_modifier = None

    else :
        print 'trigger scenario not set properly in minitree.py, please double check! Submitting some jobs nonetheless...'
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, splitSUSY=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), ttH_duplicate_check_modifier)


    json_filename = 'ana_run2_displacement_trigger.json' if use_BTagDispJet_vetoLepHT_triggers else 'ana_run2.json'
    if study_20pc : 
        json_filename = json_filename.replace(".json", "_20pc.json")
    print "json file is:", json_filename

    set_splitting(samples, dataset, 'minitree', data_json=json_path(json_filename))

    cs = CondorSubmitter('MiniTree' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)

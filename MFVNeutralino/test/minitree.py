from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers
sample_files(process, 'qcdht0500_2017' if is_mc else 'JetHT2017B', dataset, 1)
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

# blind btag triggered events
if not is_mc and use_btag_triggers :
    del process.pMiniTreeNtk3
    del process.pMiniTreeNtk4
    del process.pMiniTreeNtk3or4
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=True, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        samples=Samples.qcd_samples_2017
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), half_mc_modifier())
    elif use_MET_triggers :
        samples = pick_samples(dataset, qcd=False, ttbar=False, data=False, leptonic=False, splitSUSY=True, Zvv=False, met=False, span_signal=False)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), half_mc_modifier())
    else :
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, splitSUSY=True)
        #samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('MiniTreeTest' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)

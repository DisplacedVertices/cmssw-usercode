from DVCode.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from DVCode.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers
sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('DVCode.MFVNeutralino.MiniTree_cff')

# blind btag triggered events
if not is_mc and use_btag_triggers :
    del process.pMiniTreeNtk3
    del process.pMiniTreeNtk4
    del process.pMiniTreeNtk3or4
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from DVCode.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=True, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    else :
        samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('MiniTree' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)

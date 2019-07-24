from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

if not is_mc:
    # blind >=5-track events
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset)
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8_10pc.json'))

    cs = CondorSubmitter('MiniTree' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier(), per_sample_pileup_weights_modifier()),
                         )
    cs.submit_all(samples)

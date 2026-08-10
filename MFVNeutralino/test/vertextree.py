from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers, use_MET_triggers
#sample_files(process, 'qcdht2000_2017' if is_mc else 'JetHT2017B', dataset, 1)
#sample_files(process, 'mfv_neu_tau010000um_M0800_2017' if is_mc else 'JetHT2017B', dataset, 10)
sample_files(process, 'mfv_splitSUSY_tau000001000um_M2000_1800_2017' if is_mc else 'JetHT2017B', dataset, 10)
tfileservice(process, 'vertextree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.VertexTreer_cfi')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=True, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), half_mc_modifier())
    elif use_MET_triggers :
        #samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=True, data=False, leptonic=True, bjet=True, splitSUSY=True, Zvv=True)
        #samples = pick_samples(dataset, qcd=False, ttbar=False, all_signal=False, data=False, leptonic=False, bjet=False, splitSUSY=False, Zvv=False, span_signal=True)
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=False, data=False, leptonic=False, bjet=False, splitSUSY=True, Zvv=True, met=True)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier(), half_mc_modifier())
    else :
        samples = pick_samples(dataset, qcd=True, ttbar=True, all_signal=False, data=False, splitSUSY=True)
        #samples = pick_samples(dataset)
        pset_modifier = chain_modifiers(is_mc_modifier, per_sample_pileup_weights_modifier())
    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('VertexTree' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)

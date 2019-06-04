from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
sample_files(process, 'qcdht2000_2017', dataset, 1)
tfileservice(process, 'minitree.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

if not is_mc:
    # blind everything except presel and 3-track 1,2-vertex events
    for x in process.mfvAnalysisCutsGE1Vtx, process.mfvAnalysisCutsGE1VtxNtk4, process.mfvAnalysisCutsGE1VtxNtk3or4:
        x.max_nvertex = 1
    del process.pMiniTreeNtk3or4
    del process.pMiniTreeNtk4
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset)
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8_1pc.json'))

    cs = CondorSubmitter('MiniTree' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier(), per_sample_pileup_weights_modifier()),
                         )
    cs.submit_all(samples)

from JMTucker.Tools.BasicAnalyzer_cfg import *

is_mc = True # for blinding
cross = '' # 2017to2018' # 2017to2017p8'

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
sample_files(process, 'qcdht2000_2017', dataset, 1)
tfileservice(process, 'minitree.root')
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.MiniTree_cff')

if not is_mc:
    # blind everything except presel and 3-track 1-vertex events
    for x in process.mfvAnalysisCutsGE1Vtx, process.mfvAnalysisCutsGE1VtxNtk3, process.mfvAnalysisCutsGE1VtxNtk4, process.mfvAnalysisCutsGE1VtxNtk3or4:
        x.max_nvertex = 1
    del process.pMiniTreeNtk3or4
    del process.pMiniTreeNtk4
    del process.pMiniTree


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.all_signal_samples_2017 + Samples.data_samples_2017
        #samples = Samples.data_samples_2017
        #samples = Samples.ttbar_samples_2017 + Samples.leptonic_samples_2017 + Samples.mfv_signal_samples_2017
    elif year == 2018:
        samples = Samples.qcd_samples_2018 + Samples.data_samples_2018

    samples = [s for s in samples if s.has_dataset(dataset) and (s.is_mc or not cross)]
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8_1pc.json'))

    cs = CondorSubmitter('MiniTree%s%s' % (version, '_' + cross if cross else ''),
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(is_mc_modifier, half_mc_modifier(), per_sample_pileup_weights_modifier(cross=cross)),
                         )
    cs.submit_all(samples)

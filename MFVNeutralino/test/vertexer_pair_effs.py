from JMTucker.Tools.BasicAnalyzer_cfg import *

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset, use_btag_triggers
dataset += '_ntkseeds'
sample_files(process, 'ttbar_2017', dataset, 1)
process.TFileService.fileName = 'vertexer_pair_effs.root'
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.mfvAnalysisCuts.apply_vertex_cuts = False

process.mfvVertexerPairEffs = e = cms.EDAnalyzer('MFVVertexerPairEffs',
                                                 vpeff_src = cms.InputTag('mfvVertices'),
                                                 weight_src = cms.InputTag('mfvWeight'),
                                                 allow_duplicate_pairs = cms.bool(True),
                                                 verbose = cms.untracked.bool(False),
                                                 )

process.mfvVertexerPairEffs3TkSeed = e.clone(vpeff_src = 'mfvVertices3TkSeed')
process.mfvVertexerPairEffs4TkSeed = e.clone(vpeff_src = 'mfvVertices4TkSeed')
process.mfvVertexerPairEffs5TkSeed = e.clone(vpeff_src = 'mfvVertices5TkSeed')

process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCuts * process.mfvVertexerPairEffs * process.mfvVertexerPairEffs3TkSeed * process.mfvVertexerPairEffs4TkSeed * process.mfvVertexerPairEffs5TkSeed)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    if use_btag_triggers :
        samples = pick_samples(dataset, qcd=True, ttbar=False, all_signal=False, data=False, bjet=True) # no data currently; no sliced ttbar since inclusive is used
        pset_modifier = chain_modifiers(per_sample_pileup_weights_modifier())
    else :
        samples = pick_samples(dataset, all_signal=False)
        pset_modifier = chain_modifiers(per_sample_pileup_weights_modifier())

    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8.json'))

    cs = CondorSubmitter('VertexerPairEffs' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = pset_modifier,
                         )
    cs.submit_all(samples)

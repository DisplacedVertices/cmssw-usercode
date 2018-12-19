import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

cross = '' # 2017to2018 2017to2017p8

dataset = 'ntuplev22m_ntkseeds'
sample_files(process, 'qcdht2000_2017', dataset, 1)
process.TFileService.fileName = 'vertexer_pair_effs.root'
file_event_from_argv(process)

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
    from JMTucker.Tools.Year import year
    from JMTucker.Tools import Samples 

    if year == 2017:
        samples = Samples.ttbar_samples_2017 + Samples.qcd_samples_2017 + Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    samples = [s for s in samples if s.has_dataset(dataset) and (s.is_mc or not cross)]
    set_splitting(samples, dataset, 'histos', data_json=json_path('ana_2017p8_1pc.json'))

    cs = CondorSubmitter('VertexerPairEffsV22m%s' % ('_' + cross if cross else ''),
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(half_mc_modifier(), per_sample_pileup_weights_modifier(cross=cross)),
                         )
    cs.submit_all(samples)

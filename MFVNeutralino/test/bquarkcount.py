from JMTucker.Tools.BasicAnalyzer_cfg import *

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
sample_files(process, 'qcdht2000_2017', dataset, 1)
tfileservice(process, 'bquarkcount.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvAnalysisCuts.apply_vertex_cuts = False
process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCuts)

for i in 3,4,5:
    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = i)
    if i != 5:
        vtx.max_ntracks = i
    vtx_name = 'v%i' % i
    setattr(process, vtx_name, vtx)

    ana = cms.EDAnalyzer('MFVBQuarkCount',
                         weight_src = cms.InputTag('mfvWeight'),
                         event_src = cms.InputTag('mfvEvent'),
                         vertex_src = cms.InputTag(vtx_name),
                         )
    setattr(process, 'bqcount%i' % i, ana)

    process.p *= vtx * ana


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, ttbar=False, data=True)
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8_10pc.json'))

    cs = CondorSubmitter('BQuarkCount' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(per_sample_pileup_weights_modifier()),
                         )
    cs.submit_all(samples)

from JMTucker.Tools.BasicAnalyzer_cfg import *

from JMTucker.MFVNeutralino.NtupleCommon import ntuple_version_use as version, dataset
dataset += '_nm1refits'
sample_files(process, 'qcdht2000_2017', dataset, 1)
tfileservice(process, 'refitdist.root')
cmssw_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvAnalysisCuts.apply_vertex_cuts = False
process.p = cms.Path(process.mfvWeight * process.mfvAnalysisCuts)

for mindbv_s, mindbv in ('', None), ('mindbv0p035', 0.035), ('mindbv0p07', 0.07), ('mindbv0p1', 0.1), ('mindbv0p5', 0.5), ('mindbv1', 1.):
    for i in 3,4,5:
        vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = i)
        if mindbv:
            vtx.min_bsbs2ddist = mindbv
        if i != 5:
            vtx.max_ntracks = i
        vtx_name = 'v%i%s' % (i, mindbv_s)
        setattr(process, vtx_name, vtx)
        process.p *= vtx

        for rqgm in 0,1:
            ana = cms.EDAnalyzer('MFVRefitDistance',
                                 weight_src = cms.InputTag('mfvWeight'),
                                 event_src = cms.InputTag('mfvEvent'),
                                 vertex_src = cms.InputTag(vtx_name),
                                 require_genmatch = cms.bool(bool(rqgm)),
                                 )
            setattr(process, 'refitNtk%i%srqgm%i' % (i, mindbv_s, rqgm), ana)
            process.p *= ana


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *

    samples = pick_samples(dataset, ttbar=False, data=True)
    set_splitting(samples, dataset, 'minitree', data_json=json_path('ana_2017p8_10pc.json'))

    cs = CondorSubmitter('RefitDistance' + version,
                         ex = year,
                         dataset = dataset,
                         pset_modifier = chain_modifiers(per_sample_pileup_weights_modifier()),
                         )
    cs.submit_all(samples)

from JMTucker.MFVNeutralino.NtupleCommon import *

# JMTBAD unify with presel.py

settings = NtupleSettings()
settings.is_mc = False
settings.is_miniaod = True

process = ntuple_process(settings)
tfileservice(process, 'seed_tracks.root')
del process.out
del process.outp
del process.p

max_events(process, 10000)
report_every(process, 1000000)
#want_summary(process)
dataset = 'miniaod' if settings.is_miniaod else 'main'
sample_files(process, 'JetHT2017B', dataset, 1)
file_event_from_argv(process)

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.ByX_cfi')

process.mfvEvent.vertex_seed_tracks_src = cms.InputTag('mfvVertexTracks', 'seed')
process.mfvWeight.throw_if_no_mcstat = False
process.mfvAnalysisCuts.apply_vertex_cuts = False

process.pre = cms.Sequence(process.mfvTriggerFilterJetsOnly *
                           process.goodOfflinePrimaryVertices *
                           process.selectedPatJets *
                           process.selectedPatMuons *
                           process.selectedPatElectrons *
                           process.mfvTriggerFloats *
                           process.mfvGenParticles *
                           process.mfvUnpackedCandidateTracks *
                           process.mfvVertexTracks *
                           process.mfvEvent *
                           process.mfvWeight)

process.byrunInclusive      = process.mfvByRun.clone()
process.byrunInclusiveNoAna = process.mfvByRun.clone()

process.p = cms.Path(process.pre * process.byrunInclusiveNoAna * process.mfvAnalysisCuts * process.byrunInclusive)

#for mn,mx in (3,3), (3,4), (4,4):
#    vtx_name = 'vtx%i%i' % (mn,mx)
#    obj_name = 'byrun%i%i' % (mn,mx)
#    pth_name = 'pth%i%i' % (mn,mx)
#
#    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = mn, max_ntracks = mx)
#    obj = process.byrunInclusive.clone(vertex_src = vtx_name)
#    pth = cms.Path(process.mfvAnalysisCuts * vtx * obj)
#    setattr(process, vtx_name, vtx)
#    setattr(process, obj_name, obj)
#    setattr(process, pth_name, pth)
#
#    obj_noana = obj.clone()
#    pth_noana = cms.Path(vtx * obj_noana)
#    setattr(process, obj_name + 'noana', obj_noana)
#    setattr(process, pth_name + 'noana', pth_noana)


if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.MetaSubmitter import *
    from JMTucker.Tools import Samples

    if year == 2017:
        samples = Samples.data_samples_2017
    elif year == 2018:
        samples = Samples.data_samples_2018

    samples = [s for s in samples if s.has_dataset(dataset)]
    set_splitting(samples, dataset, 'ntuple', data_json=json_path('ana_2017p8_1pc.json'))

    ms = MetaSubmitter('ByRunStuffV21m', dataset=dataset)
    ms.condor.stageout_files = 'all'
    ms.submit(samples)

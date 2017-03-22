import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['file:ntuple.root']
process.TFileService.fileName = 'minitree.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.mfvAnalysisCuts.min_nvertex = 1

process.mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                                     event_src = cms.InputTag('mfvEvent'),
                                     vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                     weight_src = cms.InputTag('mfvWeight'),
                                     save_tracks = cms.bool(True)
                                     )

process.p = cms.Path(process.mfvWeight * process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvMiniTree)

for mn,mx in (3,3), (3,4), (4,4):
    vtx_name = 'vtx%i%i' % (mn,mx)
    ana_name = 'ana%i%i' % (mn,mx)
    tre_name = 'tre%i%i' % (mn,mx)
    pth_name = 'pth%i%i' % (mn,mx)
    vtx = process.mfvSelectedVerticesTight.clone(min_ntracks = mn, max_ntracks = mx)
    ana = process.mfvAnalysisCuts.clone(vertex_src = vtx_name)
    tre = process.mfvMiniTree.clone(vertex_src = vtx_name)
    pth = cms.Path(process.mfvWeight * vtx * ana * tre)
    setattr(process, vtx_name, vtx)
    setattr(process, ana_name, ana)
    setattr(process, tre_name, tre)
    setattr(process, pth_name, pth)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.MFVNeutralino.Year import year
    import JMTucker.Tools.Samples as Samples 
    if year == 2015:
        samples = Samples.data_samples_2015 + \
            Samples.ttbar_samples_2015 + Samples.qcd_samples_2015 + Samples.qcd_samples_ext_2015 + \
            [Samples.mfv_neu_tau00100um_M0800_2015, Samples.mfv_neu_tau00300um_M0800_2015, Samples.mfv_neu_tau01000um_M0800_2015, Samples.mfv_neu_tau10000um_M0800_2015] + \
            [Samples.xx4j_tau00001mm_M0300_2015, Samples.xx4j_tau00010mm_M0300_2015, Samples.xx4j_tau00001mm_M0700_2015, Samples.xx4j_tau00010mm_M0700_2015]
    elif year == 2016:
        samples = Samples.data_samples + \
            Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
            [Samples.official_mfv_neu_tau00100um_M0800, Samples.official_mfv_neu_tau00300um_M0800, Samples.official_mfv_neu_tau10000um_M0800]

    for sample in samples:
        sample.files_per = 20
        if not sample.is_mc:
            sample.json = 'ana_2015p6.json'

    def modify(sample):
        to_add, to_replace = [], []
        if not sample.is_mc:
            to_add.append('del process.p')
        return to_add, to_replace

    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    cs = CondorSubmitter('MinitreeV12',
                         ex = year,
                         dataset = 'ntuplev12',
                         pset_modifier = modify
                         )
    cs.submit_all(samples)

import sys

ntracks = None
for arg in sys.argv:
    if arg.startswith('ntracks='):
        ntracks = arg.split('ntracks=')[1]
        break

####

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

if ntracks == '3':
    process.mfvSelectedVerticesTight.min_ntracks = 3
    process.mfvSelectedVerticesTight.max_ntracks = 3
    process.TFileService.fileName = 'minitree.ntk3.root'
elif ntracks == '4':
    process.mfvSelectedVerticesTight.min_ntracks = 4
    process.mfvSelectedVerticesTight.max_ntracks = 4
    process.TFileService.fileName = 'minitree.ntk4.root'
elif ntracks == '3or4':
    process.mfvSelectedVerticesTight.min_ntracks = 3
    process.mfvSelectedVerticesTight.max_ntracks = 4
    process.TFileService.fileName = 'minitree.ntk3or4.root'
elif ntracks is not None:
    raise ValueError("don't understand ntracks=%r" % ntracks)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CondorSubmitter import CondorSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.registry.from_argv(
        #Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        Samples.mfv_signal_samples + \
        Samples.mfv_signal_samples_lq2 + \
        Samples.xx4j_samples
        )

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        [Samples.xx4j_tau00001mm_M0300, Samples.xx4j_tau00010mm_M0300, Samples.xx4j_tau00001mm_M0700, Samples.xx4j_tau00010mm_M0700]

    for sample in samples:
        sample.files_per = 50
        if not sample.is_mc:
            sample.json = 'ana_10pc.json'
            raise NotImplementedError('need to implement json use in CondorSubmitter')

    cs = CondorSubmitter('MinitreeV10', dataset = 'ntuplev10')
    cs.submit_all(samples)

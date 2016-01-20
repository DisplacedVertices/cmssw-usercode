import sys
from JMTucker.Tools.BasicAnalyzer_cfg import *

process.source.fileNames = ['/store/user/tucker/QCD_HT1000to1500_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/ntuplev6p1/160118_211014/0000/ntuple_1.root']
process.TFileService.fileName = 'minitree.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.mfvAnalysisCuts.min_nvertex = 1

process.mfvMiniTree = cms.EDAnalyzer('MFVMiniTreer',
                                     event_src = cms.InputTag('mfvEvent'),
                                     vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                     weight_src = cms.InputTag('mfvWeight'),
                                     )

process.p = cms.Path(process.mfvWeight * process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.mfvMiniTree)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples

    samples = Samples.registry.from_argv(
        #Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + \
        #[Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        Samples.xx4j_samples
        )

    cs = CRABSubmitter('MinitreeV6',
                       dataset = 'ntuplev6p1',
                       splitting = 'FileBased',
                       units_per_job = 25,
                       total_units = -1,
                       aaa = True,
                       )

    cs.submit_all(samples)

import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

process.source.fileNames = ['/store/user/tucker/mfv_neutralino_tau1000um_M0400/mfvntuple_v20/aaaa7d7d2dcfa08aa71c1469df6ebf05/ntuple_1_1_NQ9.root']
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.load('JMTucker.MFVNeutralino.ABCDHistos_cfi')

process.p = cms.Path(process.mfvWeight * process.mfvSelectedVerticesSeq * process.mfvAnalysisCuts * process.mfvAbcdHistosSeq)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('ABCDHistosV20',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all(samples)

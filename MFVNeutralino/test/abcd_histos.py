import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV18', 'mfv_neutralino_tau1000um_M0400', 500)
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.WeightProducer_cfi')
process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.abcdHistos = cms.EDAnalyzer('ABCDHistos',
                                    mfv_event_src = cms.InputTag('mfvEvent'),
                                    weight_src = cms.InputTag('mfvWeight'),
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                    which_mom = cms.int32(0),
                                    )

process.abcdHistosTrks = process.abcdHistos.clone()
process.abcdHistosJets = process.abcdHistos.clone(which_mom = 1)
process.abcdHistosTrksJets = process.abcdHistos.clone(which_mom = 2)
process.p = cms.Path(process.mfvWeight * process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.abcdHistosTrks * process.abcdHistosJets * process.abcdHistosTrksJets)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.from_argv([Samples.mfv_neutralino_tau0100um_M0400,
                                 Samples.mfv_neutralino_tau1000um_M0400,
                                 Samples.mfv_neutralino_tau0300um_M0400,
                                 Samples.mfv_neutralino_tau9900um_M0400] + Samples.ttbar_samples + Samples.qcd_samples)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('ABCDHistosV18',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       run_half_mc = True,
                       )
    cs.submit_all(samples)


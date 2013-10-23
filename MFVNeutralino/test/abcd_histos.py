from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
import JMTucker.MFVNeutralino.TestFiles as TestFiles

process.source.fileNames = TestFiles.qcdht1000_nt
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvSelectedVerticesTight.min_ntracks = 5
process.mfvSelectedVerticesTight.min_maxtrackpt = 0
process.abcdHistos = cms.EDAnalyzer('ABCDHistos',
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight')
                                    )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.abcdHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = [Samples.qcdht1000]
    Samples.qcdht1000.total_events /= 2

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('ABCDHistos',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    cs.submit_all(samples)


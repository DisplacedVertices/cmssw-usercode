import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
import JMTucker.MFVNeutralino.TestFiles as TestFiles

process.source.fileNames = TestFiles.qcdht1000_nt
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvSelectedVerticesTight.min_njetssharetks = 2

process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.min_ntracks01 = 0
process.mfvAnalysisCuts.min_maxtrackpt01 = 0

process.abcdHistos = cms.EDAnalyzer('ABCDHistos',
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight')
                                    )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.abcdHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples, ttbar_samples, qcd_samples
    for sample in ttbar_samples + qcd_samples:
        sample.total_events = {'ttbarhadronic': 5268722,
                               'ttbarsemilep':  12674909,
                               'ttbardilep':    6059506,
                               'qcdht0100':     25064759,
                               'qcdht0250':     13531039,
                               'qcdht0500':     15274646,
                               'qcdht1000':     6034431}[sample.name]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('ABCDHistos',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       )
    samples = mfv_signal_samples + ttbar_samples + qcd_samples
    cs.submit_all(samples)


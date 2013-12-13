import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.set(process, 'MFVNtupleV11', 'mfv_neutralino_tau0100um_M0400', 500)
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.mfvSelectedVerticesTight.min_ntracks = 5
process.mfvSelectedVerticesTight.min_maxtrackpt = 4
process.mfvSelectedVerticesTight.max_drmin = 0.5
process.mfvSelectedVerticesTight.max_drmax = 4.5
process.mfvSelectedVerticesTight.min_bs2dsig = 4.5
process.mfvSelectedVerticesTight.min_njetsntks = 1
process.mfvSelectedVerticesTight.min_sumpt2 = 40

process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')
process.mfvAnalysisCuts.min_ntracks01 = 0
process.mfvAnalysisCuts.min_maxtrackpt01 = 0
process.mfvAnalysisCuts.min_jetsntkmass01 = 60
process.mfvAnalysisCuts.min_njetsntks01 = 3
process.mfvAnalysisCuts.min_sumht = 600

process.abcdHistos = cms.EDAnalyzer('ABCDHistos',
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight')
                                    )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.abcdHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import mfv_signal_samples, ttbar_samples, qcd_samples
    for sample in ttbar_samples + qcd_samples:
        sample.total_events = sample.nevents_orig/2

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('ABCDHistos',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV11'],
                       )
    samples = mfv_signal_samples + ttbar_samples + qcd_samples
    cs.submit_all(samples)


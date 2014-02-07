import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'mfv_neutralino_tau1000um_M0400', 500)
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.abcdHistos = cms.EDAnalyzer('ABCDHistos',
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight')
                                    )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.abcdHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import *
    bkg_samples = ttbar_samples + qcd_samples
    samples = [mfv_neutralino_tau0100um_M0200, mfv_neutralino_tau0100um_M0400, mfv_neutralino_tau1000um_M0400, mfv_neutralino_tau9900um_M0400] + bkg_samples
    for sample in bkg_samples:
        sample.total_events = sample.nevents_orig/2

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('ABCDHistosV15_30',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )
    cs.submit_all(samples)


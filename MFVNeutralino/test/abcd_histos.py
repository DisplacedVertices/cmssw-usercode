import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'mfv_neutralino_tau1000um_M0400', 500)
#SampleFiles.setup(process, 'MFVNtupleV15', 'ttbarhadronic', 2503433)
#SampleFiles.setup(process, 'MFVNtupleV15', 'ttbarsemilep', 3489937)
#SampleFiles.setup(process, 'MFVNtupleV15', 'ttbardilep', 797006)
#SampleFiles.setup(process, 'MFVNtupleV15', 'qcdht0100', 18744)
#SampleFiles.setup(process, 'MFVNtupleV15', 'qcdht0250', 822457)
#SampleFiles.setup(process, 'MFVNtupleV15', 'qcdht0500', 4759413)
#SampleFiles.setup(process, 'MFVNtupleV15', 'qcdht1000', 3088150)
process.TFileService.fileName = 'abcd_histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.AnalysisCuts_cfi')

process.abcdHistos = cms.EDAnalyzer('ABCDHistos',
                                    mfv_event_src = cms.InputTag('mfvEvent'),
                                    vertex_src = cms.InputTag('mfvSelectedVerticesTight')
                                    )

process.p = cms.Path(process.mfvSelectedVerticesTight * process.mfvAnalysisCuts * process.abcdHistos)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.Samples import *
    bkg_samples = ttbar_samples + qcd_samples
    samples = mfv_signal_samples + bkg_samples
    for sample in bkg_samples:
        sample.total_events = int(sample.nevents_orig/2 * sample.ana_filter_eff)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('ABCDHistosV15',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )
    cs.submit_all(samples)


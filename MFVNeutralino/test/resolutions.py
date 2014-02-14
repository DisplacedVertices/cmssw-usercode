import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools import SampleFiles

SampleFiles.setup(process, 'MFVNtupleV15', 'mfv_neutralino_tau1000um_M0400', 1000)
process.TFileService.fileName = 'resolutions.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')

process.mfvResolutions = cms.EDAnalyzer('MFVResolutions',
                                        vertex_src = cms.InputTag('mfvSelectedVerticesTight'),
                                        mevent_src = cms.InputTag('mfvEvent'),
                                        )
process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvResolutions)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('MFVResolutionsV15',
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       manual_datasets = SampleFiles['MFVNtupleV15'],
                       )

    cs.submit_all(Samples.mfv_signal_samples)

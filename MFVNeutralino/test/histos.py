import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
from JMTucker.Tools.SampleFiles import SampleFiles

process.options.wantSummary = True
process.source.fileNames = SampleFiles['MFVHistosV10_testVtxSeedSum']['mfv_neutralino_tau1000um_M0400'][:5]
process.TFileService.fileName = 'histos.root'

process.load('JMTucker.MFVNeutralino.VertexSelector_cfi')
process.load('JMTucker.MFVNeutralino.Histos_cff')

process.p = cms.Path(process.mfvSelectedVerticesSeq * process.mfvHistos)

process.eid = cms.EDAnalyzer('EventIdRecorder')
process.peid = cms.Path(process.eid)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.ttbar_samples + Samples.qcd_samples
    samples += [Samples.mfv_neutralino_tau0100um_M0400, Samples.mfv_neutralino_tau1000um_M0400, Samples.mfv_neutralino_tau9900um_M0400]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('MFVHistos_testVtxSeedSum',
                       total_number_of_events = -1,
                       events_per_job = 25000,
                       manual_datasets = SampleFiles['MFVNtupleV10_testVtxSeedSum'],
                       )
    cs.submit_all(samples)

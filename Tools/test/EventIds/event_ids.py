import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

from JMTucker.Tools import SampleFiles
SampleFiles.setup(process, 'MFVNtupleV18', 'mfv_neutralino_tau1000um_M0400', 500)

process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.mfv_signal_samples #+ Samples.leptonic_background_samples + Samples.data_samples[:1]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('EventIdsV18',
                       total_number_of_events = -1,
                       events_per_job = 234567,
                       manual_datasets = SampleFiles['MFVNtupleV18'],
                       )
    cs.submit_all(samples)

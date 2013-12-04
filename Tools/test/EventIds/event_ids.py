import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process

process.options.wantSummary = True
process.TFileService.fileName = cms.string('eid.root')

process.evids = cms.EDAnalyzer('EventIdRecorder', check_gen_particles = cms.bool(True))
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.ttbar_samples + Samples.qcd_samples + Samples.mfv_signal_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('EventIdsV11',
                       total_number_of_events = -1,
                       events_per_job = 200000,
                       manual_datasets = SampleFiles['MFVNtupleV11'],
                       )
    cs.submit_all(samples)

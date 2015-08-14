raise NotImplementedError('run2 sample arch')
import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    bkg_samples = Samples.ttbar_samples + Samples.qcd_samples
    for sample in bkg_samples:
        sample.total_events = int(sample.nevents_orig/2 * sample.ana_filter_eff)

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    cs = CRABSubmitter('HalfMCLists',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       manual_datasets = SampleFiles['MFVNtupleV17'],
                       )
    cs.submit_all(bkg_samples)

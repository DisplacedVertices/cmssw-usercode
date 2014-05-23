import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.TFileService.fileName = cms.string('evids.root')

process.source.fileNames = ['/store/user/tucker/TTJets_HadronicMGDecays_8TeV-madgraph/mfvntuple_v17/f1615d49c4ae9d19e350601d059c4237/ntuple_600_1_BPu.root']
process.evids = cms.EDAnalyzer('EventIdRecorder')
process.veto = cms.EDFilter('EventIdVeto', list_fn = cms.string('ttbarhadronic.txt.gz'), use_run = cms.bool(False))
process.p = cms.Path(~process.veto * process.evids)

process.options.wantSummary = True

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    bkg_samples = Samples.ttbar_samples + Samples.qcd_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    def pset_modifier(sample):
        to_add = []
        to_modify = []
        to_add.append("process.veto.list_fn = '%s.txt.gz'" % sample.name)
        return to_add, to_modify

    def crab_cfg_modifier(sample):
        return [('USER', 'additional_input_files', '/uscms/home/tucker/mfvrecipe/HalfMCLists/%s.txt.gz' % sample.name)]

    cs = CRABSubmitter('HalfMCLists_TestLists',
                       job_control_from_sample = True,
                       use_ana_dataset = True,
                       pset_modifier = pset_modifier,
                       crab_cfg_modifier = crab_cfg_modifier,
                       )
    cs.submit_all(bkg_samples)

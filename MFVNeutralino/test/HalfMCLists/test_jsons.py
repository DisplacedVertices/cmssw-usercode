import sys
from JMTucker.Tools.BasicAnalyzer_cfg import cms, process
process.TFileService.fileName = cms.string('evids.root')

process.evids = cms.EDAnalyzer('EventIdRecorder')
process.p = cms.Path(process.evids)

process.source.duplicateCheckMode = cms.untracked.string('noDuplicateCheck')

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples

    bkg_samples = Samples.ttbar_samples + Samples.qcd_samples

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    from JMTucker.Tools.SampleFiles import SampleFiles

    def crab_cfg_modifier(sample):
        return [('CMSSW', 'lumi_mask', '/uscms/home/tucker/mfvrecipe/HalfMCLists/jsons/%s.json' % sample.name)]

    cs = CRABSubmitter('HalfMCLists_TestJsons',
                       use_ana_dataset = True,
                       total_number_of_lumis = -1,
                       lumis_per_job = 3500,
                       crab_cfg_modifier = crab_cfg_modifier,
                       )
    cs.submit_all(bkg_samples)

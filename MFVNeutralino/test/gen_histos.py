import os, sys, glob
from JMTucker.Tools.BasicAnalyzer_cfg import *
debug = 'debug' in sys.argv

file_event_from_argv(process)
process.TFileService.fileName = 'gen_histos.root'

process.load('JMTucker.MFVNeutralino.GenParticleFilter_cfi')
process.load('JMTucker.MFVNeutralino.GenHistos_cff')

process.p = cms.Path(process.mfvGenParticleFilter * process.mfvGenHistos)

process.histos1v = process.mfvGenHistos.clone()
process.histos2v = process.mfvGenHistos.clone()
process.histos0v = process.mfvGenHistos.clone()

process.events1v = cms.EDFilter('EventIdVeto', list_fn = cms.string('events1v.txt.gz'), use_run = cms.bool(True))
process.events2v = cms.EDFilter('EventIdVeto', list_fn = cms.string('events2v.txt.gz'), use_run = cms.bool(True))
process.p1v = cms.Path(~process.events1v * process.histos1v)
process.p2v = cms.Path(~process.events2v * process.histos2v)
process.p0v = cms.Path(process.events1v * process.events2v * process.histos0v)

if debug:
    process.printList = cms.EDAnalyzer('JMTParticleListDrawer',
                                       src = cms.InputTag('genParticles'),
                                       printVertex = cms.untracked.bool(True),
                                       )
    process.p.insert(0, process.printList)
    file_event_from_argv(process)

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    import JMTucker.Tools.Samples as Samples
    samples = Samples.ttbar_samples + Samples.qcd_samples

    def pset_modifier(sample):
        to_add = []
        to_modify = []

        to_add.append("process.events1v.list_fn = '%s_1v.txt.gz'" % sample.name)
        to_add.append("process.events2v.list_fn = '%s_2v.txt.gz'" % sample.name)
        return to_add, to_modify

    def crab_cfg_modifier(sample):
        return [('USER', 'additional_input_files', '%s_1v.txt.gz,%s_2v.txt.gz' % (sample.name, sample.name))]

    from JMTucker.Tools.CRABSubmitter import CRABSubmitter
    cs = CRABSubmitter('GenHistos',
                       total_number_of_events = -1,
                       events_per_job = 20000,
                       skip_common = True,
                       pset_modifier = pset_modifier,
                       crab_cfg_modifier = crab_cfg_modifier,
                       )
    cs.submit_all(samples)

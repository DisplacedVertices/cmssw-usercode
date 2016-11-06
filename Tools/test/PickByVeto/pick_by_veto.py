#!/usr/bin/env python

from JMTucker.Tools.BasicAnalyzer_cfg import *
del process.TFileService

process.veto = cms.EDFilter('EventIdVeto',
                         use_run = cms.bool(False),
                         list_fn = cms.string('veto.gz'),
                         debug = cms.untracked.bool(False),
                         )

process.p = cms.Path(~process.veto)

process.out = cms.OutputModule('PoolOutputModule',
                               fileName = cms.untracked.string('pick.root'),
                               SelectEvents = cms.untracked.PSet(SelectEvents = cms.vstring('p')),
                               )

process.outp = cms.EndPath(process.out)

file_event_from_argv(process)

if 'debug' in sys.argv:
    process.options.wantSummary = True
    process.veto.debug = True

if __name__ == '__main__' and hasattr(sys, 'argv') and 'submit' in sys.argv:
    from JMTucker.Tools.CRAB3Submitter import CRABSubmitter
    import JMTucker.Tools.Samples as Samples 

    samples = Samples.registry.from_argv(
        Samples.data_samples + \
        Samples.ttbar_samples + Samples.qcd_samples + Samples.qcd_samples_ext + \
        Samples.auxiliary_background_samples[:1] + \
        Samples.qcdpt_samples + \
        [Samples.mfv_neu_tau00100um_M0800, Samples.mfv_neu_tau00300um_M0800, Samples.mfv_neu_tau01000um_M0800, Samples.mfv_neu_tau10000um_M0800] + \
        Samples.xx4j_samples
        )

    samples = [Samples.qcdht1000, Samples.qcdht1500, Samples.qcdht2000] + Samples.ttbar_samples

    def vetolist_fn(sample):
        fn = 'vetolist.%s.gz' % sample.name
        assert os.path.isfile(fn)
        return fn

    def pset_modifier(sample):
        return ['process.veto.list_fn = "%s"' % vetolist_fn(sample)], []

    def cfg_modifier(cfg, sample):
        cfg.JobType.inputFiles = [vetolist_fn(sample)]

    cs = CRABSubmitter('Pick1Vtx',
                       pset_modifier = pset_modifier,
                       cfg_modifier = cfg_modifier,
                       splitting = 'FileBased',
                       units_per_job = 30,
                       total_units = -1,
                       publish_name = 'pick1vtx',
                       )

    cs.submit_all(samples)
